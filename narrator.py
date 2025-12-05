class WorldDirections:
    __world_directions = {
        "n": "North",
        "s": "South",
        "e": "East",
        "w": "West"
    }

    def is_world_direction(direction):
        return direction in WorldDirections.__world_directions
    
    def get_full_name(short_name):
        return WorldDirections.__world_directions[short_name]

class Narrator:
    def get_hello_msg(self, name):
        return f"Hello, {name}!"

    def get_goodbye_msg(self, name):
        return f"Good bye, {name}!"
    
    def get_scene_msg(self, location, locations, creatures, items):
        msg = self.get_location_msg(location, detailed = True)
        msg += "\n\n"
        msg += self.get_location_exits_msg(location, locations)
        if creatures:
            msg += "\n\n"
            msg + self.get_location_creatures_msg(creatures)
        if items:
            msg += "\n\n"
            msg += self.get_location_items_msg(items)
        return msg

    def get_location_msg(self, location, detailed = False):
        msg = f"You are {location.preposition} the {location.name}."
        if (detailed and location.description):
            msg = msg + f"\n\n{location.description}"
        return msg

    def get_location_exits_msg(self, location, locations):
        msg = ""
        if (len(location.exits)):
            msg = msg + f"You can see:"
            for short_name in location.exits:
                msg = msg + f"\n   - {locations[location.exits[short_name]].name} to the {WorldDirections.get_full_name(short_name)}"
        else:
            msg = msg + f"There are no exits from {location.name}"
        return msg

    def get_location_creatures_msg(self, creatures):
        if not creatures:
            return ""
        msg = "Creatures here:"
        for c in creatures:
            if isinstance(c, dict):
                name = c.get('name', 'a creature')
                species = c.get('species', '')
            else:
                name = getattr(c, 'name', 'a creature')
                species = getattr(c, 'species', '')
            if species:
                msg += f"\n   - {name} ({species})"
            else:
                msg += f"\n   - {name}"
        return msg

    def get_location_items_msg(self, items, catalog_lookup = None):
        if not items:
            return ""
        msg = "Items here:"
        for it in items:
            name = it.get('name') if isinstance(it, dict) and it.get('name') else None
            # if catalog provided in merged structure
            if not name and isinstance(it, dict):
                cat = it.get('catalog')
                if cat:
                    name = cat.get('name')
            if not name:
                name = 'an item'
            msg += f"\n   - {name} (id:{it.get('instance_id')})"
        return msg

    def get_inventory_msg(self, inventory, catalog=False):
        if not inventory:
            return "You are carrying nothing."
        msg = "You are carrying:"
        for it in inventory:
            # inventory items are item instances with optional catalog
            name = it.get('catalog', {}).get('name') if catalog else it.get('name')
            if not name:
                name = it.get('name') or 'an item'
            msg += f"\n   - {name} (id:{it.get('instance_id')})"
        return msg

    def wait(self):
        return "You wait"
    
    def move_player(self, direction, result):        
        if (result):
            return f"You go {WorldDirections.get_full_name(direction)}"
        else:
            return f"You cannot go {WorldDirections.get_full_name(direction)}"
    
    def kill(self, something):
        if (something == "yourself"):
            return "Don't do that! :-0"
        else:
            return f"You are trying to kill a {something} but there's no {something} to kill"
        
    def introduce(self, name):
        return f"Your are {name}"

    def get_item_matches_msg(self, matches):
        # Format disambiguation message for multiple items matching by name
        if not matches:
            return None
        if len(matches) == 1:
            item = matches[0]
            name = item.get('catalog', {}).get('name', 'item')
            return f"Taking {name}."
        # Multiple matches
        msg = "Multiple items match that name:\n"
        for it in matches:
            name = it.get('catalog', {}).get('name', 'item')
            iid = it.get('instance_id')
            msg += f"   - {name} (id:{iid})\n"
        msg += "Please specify by id: 'take <id>'"
        return msg

    def get_drop_matches_msg(self, matches):
        # Format disambiguation message for multiple items in inventory matching by name
        if not matches:
            return None
        if len(matches) == 1:
            item = matches[0]
            name = item.get('catalog', {}).get('name', 'item')
            return f"Dropping {name}."
        # Multiple matches
        msg = "Multiple items match that name:\n"
        for it in matches:
            name = it.get('catalog', {}).get('name', 'item')
            iid = it.get('instance_id')
            msg += f"   - {name} (id:{iid})\n"
        msg += "Please specify by id: 'drop <id>'"
        return msg

    def get_attack_msg(self, result, attacker_name, defender_name):
        """Format combat result message."""
        if not result['hit']:
            if result['reason'] == 'dodge':
                return f"{defender_name} dodges your attack!"
            else:
                return f"You cannot attack {defender_name}."
        
        damage = result['damage']
        health = result['defender_health']
        msg = f"You hit {defender_name} for {damage} damage!"
        
        # Check if creature escaped
        if result.get('escaped'):
            msg += f"\n{defender_name} flees in panic!"
            return msg
        
        if result['defender_alive']:
            msg += f" ({health} HP remaining)"
        else:
            msg += f"\n{defender_name} has been defeated!"
        
        # Handle creature counter-attack
        if 'counter_attack' in result:
            counter = result['counter_attack']
            if counter['hit']:
                counter_dmg = counter['damage']
                player_health = counter.get('defender_health', 'unknown')
                msg += f"\n{defender_name} counter-attacks and hits you for {counter_dmg} damage!"
                if player_health != 'unknown':
                    msg += f" (You have {player_health} HP left)"
                if not counter['defender_alive']:
                    msg += f"\nYou have been defeated!"
            else:
                if counter['reason'] == 'dodge':
                    msg += f"\n{defender_name} tries to counter but you dodge!"
                else:
                    msg += f"\n{defender_name} tries to counter but misses!"
        
        return msg

    def get_help_msg(self):
        msg = "Available commands:\n"
        msg += "  Movement:\n"
        msg += "    n, s, e, w          - Move north, south, east, or west\n"
        msg += "    go <direction>      - Move in a direction\n"
        msg += "    go to <direction>   - Move to a location\n"
        msg += "\n  Interaction:\n"
        msg += "    look or l           - Examine current location\n"
        msg += "    where am i          - Show current location\n"
        msg += "    who am i            - Show your name\n"
        msg += "    wait                - Wait a moment\n"
        msg += "\n  Inventory:\n"
        msg += "    inventory or i      - Show what you're carrying\n"
        msg += "    take <name/id>      - Pick up an item by name or id\n"
        msg += "    pick up <name/id>   - Pick up an item (alternate)\n"
        msg += "    get <name/id>       - Pick up an item (alternate)\n"
        msg += "    drop <id>           - Drop an item from inventory\n"
        msg += "\n  Combat:\n"
        msg += "    kill <creature>     - Attack a creature\n"
        msg += "\n  Meta:\n"
        msg += "    help                - Show this help message\n"
        msg += "    quit or q           - Exit the game\n"
        return msg

    def unknown_command(self, command):
        return f"I don't know how to {command}"
