import json
import random

class Creature:
    def __init__(self, species, name, health, strength, location_id, location_changed=False, description="", creature_id=None):
        self.id = creature_id
        self.species = species
        self.name = name
        self.description = description
        self.health = health
        self.max_health = health
        self.strength = strength
        self.location_id = location_id
        self.location_changed = location_changed
        self.inventory = []
        self.is_alive = True

    def take_damage(self, damage):
        """Apply damage to creature and return actual damage taken."""
        actual_damage = min(damage, self.health)
        self.health -= actual_damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
        return actual_damage

    def add_item(self, item_instance):
        self.inventory.append(item_instance)

    def remove_item(self, item_instance_id):
        for i, it in enumerate(self.inventory):
            if it.get('instance_id') == item_instance_id:
                return self.inventory.pop(i)
        return None

    def kill(self, target):
        return target

class Location:    
    def __init__(self, name, description, exits, preposition):
        self.name = name
        self.description = description
        self.exits = exits
        self.preposition = preposition

class WorldEngine:
    resources_changed = False

    def __init__(self):
        self.__locations = {}
        self.__creatures = {}
        self.__items_catalog = {}
        self.__items_on_ground = {}
        self.player = Creature("human", "", 100, 10, 0, True)

    def load_resources(self, filename):
        with open(filename, 'r') as f:
            locations = json.load(f, object_hook=complex_decoder)

        self.__locations = {}

        for i in range(len(locations)):
            self.__locations[i] = locations[f"{i}"]

    def save_resources(self, filename):
        with open(filename, "w") as f:
            f.write(json.dumps(self.__locations, cls=LocationEncoder, indent=3))

    def get_object_location(self, o):
        return self.__locations.get(o.location_id)

    def move_object(self, o, direction):        
        if not direction in self.__locations[o.location_id].exits:
            return False
        
        o.location_id = self.__locations[o.location_id].exits[direction]
        o.location_changed = True

        return True
    
    def get_locations(self):
        return self.__locations

    def load_creatures(self, filename):
        with open(filename, 'r') as f:
            creatures = json.load(f)

        self.__creatures = {}
        for k, v in creatures.items():
            # Parse JSON creature entries into in-memory Creature objects.
            self.__creatures[k] = self._parse_creature(k, v)

    def _parse_creature(self, creature_id, raw):
        species = str(raw.get('species', 'creature')).strip() if isinstance(raw, dict) else 'creature'
        if not species:
            species = 'creature'

        name = str(raw.get('name', species.title())).strip() if isinstance(raw, dict) else species.title()
        if not name:
            name = species.title()

        description = ''
        if isinstance(raw, dict):
            description = str(raw.get('description', '')).strip()

        health = self._to_int(raw.get('health') if isinstance(raw, dict) else None, 10)
        strength = self._to_int(raw.get('strength') if isinstance(raw, dict) else None, 1)
        location_id = self._to_int(raw.get('location_id') if isinstance(raw, dict) else None, 0)

        location_changed_raw = raw.get('location_changed', False) if isinstance(raw, dict) else False
        if isinstance(location_changed_raw, bool):
            location_changed = location_changed_raw
        else:
            location_changed = str(location_changed_raw).strip().lower() in {'1', 'true', 'yes'}

        return Creature(
            species=species,
            name=name,
            health=max(1, health),
            strength=max(1, strength),
            location_id=location_id,
            location_changed=location_changed,
            description=description,
            creature_id=creature_id
        )

    def _to_int(self, value, default):
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def get_creature(self, creature_id):
        return self.__creatures.get(str(creature_id))

    def load_items(self, filename):
        with open(filename, 'r') as f:
            items = json.load(f)
        self.__items_catalog = items

    def load_items_on_ground(self, filename):
        try:
            with open(filename, 'r') as f:
                items = json.load(f)
            # items expected as dict of instance objects with fields: item_id, location_id
            self.__items_on_ground = {}
            for k, v in items.items():
                inst = dict(v)
                inst['instance_id'] = int(k)
                self.__items_on_ground[int(k)] = inst
        except Exception:
            # no world items available
            self.__items_on_ground = {}

    def get_items_at(self, location_id):
        # return list of item instances present at location, with catalog merged
        results = []
        for inst in self.__items_on_ground.values():
            if inst.get('location_id') == location_id:
                catalog = self.__items_catalog.get(str(inst.get('item_id')) , {})
                combined = dict(inst)
                combined.update({'catalog': catalog})
                results.append(combined)
        return results

    def pick_up_item(self, player, instance_id):
        inst = self.__items_on_ground.pop(instance_id, None)
        if not inst:
            return False
        # attach catalog data before adding to inventory
        item_id = inst.get('item_id')
        catalog = self.__items_catalog.get(str(item_id), {})
        inst['instance_id'] = instance_id
        inst['picked_by'] = player.name
        inst['catalog'] = catalog
        player.add_item(inst)
        return True

    def drop_item(self, player, instance_id, location_id):
        dropped = player.remove_item(instance_id)
        if not dropped:
            return False
        dropped['location_id'] = location_id
        # use the instance_id from dropped item
        self.__items_on_ground[dropped['instance_id']] = dropped
        return True

    def get_creatures_at(self, location_id, include_dead=False):
        """Return creatures at a location.

        By default this excludes defeated creatures (`is_alive == False`).
        Pass `include_dead=True` to retrieve all creatures regardless of life state.
        """
        return [
            c for c in self.__creatures.values()
            if c.location_id == location_id and (include_dead or c.is_alive)
        ]

    def find_items_at_by_name(self, location_id, name_query):
        # Find items at location whose catalog name (partial match, case-insensitive) matches name_query
        # Returns list of matching item instances
        results = []
        query_lower = name_query.lower()
        for inst in self.__items_on_ground.values():
            if inst.get('location_id') == location_id:
                catalog = self.__items_catalog.get(str(inst.get('item_id')), {})
                item_name = catalog.get('name', '').lower()
                if query_lower in item_name:
                    combined = dict(inst)
                    combined.update({'catalog': catalog})
                    results.append(combined)
        return results

    def find_items_in_inventory_by_name(self, player, name_query):
        # Find items in player inventory whose catalog name (partial match, case-insensitive) matches name_query
        # Returns list of matching item instances
        results = []
        query_lower = name_query.lower()
        for inst in player.inventory:
            catalog = inst.get('catalog', {})
            item_name = catalog.get('name', '').lower()
            if query_lower in item_name:
                results.append(inst)
        return results
    
    def find_creatures_by_name(self, location_id, name_query):
        # Find creatures at location by name (partial match, case-insensitive)
        # Returns list of matching creatures
        results = []
        query_lower = name_query.lower()
        creatures_here = self.get_creatures_at(location_id)
        for creature in creatures_here:
            if creature.is_alive:
                creature_name = creature.name.lower()
                species_name = creature.species.lower()
                if query_lower in creature_name or query_lower in species_name:
                    results.append(creature)
        return results

    def attack_creature(self, attacker, defender):
        # Attacker attacks defender; return result dict with damage and outcome
        if not defender.is_alive:
            return {'hit': False, 'reason': 'already dead'}
        
        # Calculate damage: base strength + random variance
        base_damage = attacker.strength
        variance = random.randint(-2, 4)
        total_damage = max(1, base_damage + variance)
        
        # Defender has chance to dodge based on their health percentage (healthier = better dodges)
        health_percent = (defender.health / defender.max_health) * 100
        dodge_chance = max(0, min(0.5, health_percent * 0.005))  # Up to 50% dodge at full health
        if random.random() < dodge_chance:
            return {'hit': False, 'damage': 0, 'reason': 'dodge'}
        
        # Apply damage
        actual_damage = defender.take_damage(total_damage)
        result = {
            'hit': True,
            'damage': actual_damage,
            'defender_health': defender.health,
            'defender_alive': defender.is_alive,
            'attacker_name': attacker.name,
            'defender_name': defender.name,
            'escaped': False
        }
        
        # Check if creature wants to escape (creatures only)
        if defender.is_alive and hasattr(defender, 'species') and defender.species != 'human':
            escape_chance = self.calculate_escape_chance(defender)
            if random.random() < escape_chance:
                result['escaped'] = True
                result['escape_location'] = self.get_random_adjacent_location(defender.location_id)
                # Move creature to new location
                if result['escape_location'] is not None:
                    defender.location_id = result['escape_location']
                return result
        
        # If defender is alive and is a creature (not player), they counter-attack
        if defender.is_alive and hasattr(defender, 'species') and defender.species != 'human':
            counter_result = self.attack_creature(defender, attacker)
            result['counter_attack'] = counter_result
        
        return result

    def calculate_escape_chance(self, creature):
        """Calculate probability that creature escapes (based on health %)."""
        health_percent = (creature.health / creature.max_health) * 100
        # At 50% health: 10% escape chance, at 25% health: 35%, at 10% health: 60%
        if health_percent > 50:
            return 0.05  # 5% chance when healthy
        elif health_percent > 25:
            return 0.25  # 25% chance when moderately wounded
        elif health_percent > 10:
            return 0.40  # 40% chance when heavily wounded
        else:
            return 0.70  # 70% chance when critically wounded

    def get_random_adjacent_location(self, location_id):
        """Get a random adjacent location the creature can flee to."""
        location = self.__locations.get(location_id)
        if location and location.exits:
            exits = list(location.exits.values())
            if exits:
                return random.choice(exits)
        return None
    
    def get_player(self):
        return self.player
            
class LocationEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Location):
            return {
                '__type__': 'Location', 
                'name': obj.name, 
                'description': obj.description, 
                'exits': obj.exits,
                'preposition': obj.preposition
            }
        return json.JSONEncoder.default(self, obj)
    
def complex_decoder(dct):
    if '__type__' in dct:
        if dct['__type__'] == 'Location':
            return Location(dct['name'], dct['description'], dct['exits'], dct['preposition'])
    return dct
