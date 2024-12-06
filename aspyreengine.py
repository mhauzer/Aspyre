import json

class Creature:
    def __init__(self, species, name, health, strength, location_id, location_changed = False):
        self.species = species
        self.name = name
        self.health = health
        self.strength = strength
        self.location_id = location_id
        self.location_changed = location_changed

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
