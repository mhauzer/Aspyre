import json

# https://reqbin.com/code/python/pbokf3iz/python-json-dumps-example

debug = False

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

class AspyreEngine:
    def __init__(self):
        self.locations = {}
        self.player = Creature("human", "", 100, 10, 0, True)

    def get_player_location(self):
        return self.locations[self.player.location_id]

class Narrator:
    def get_hello_msg(self, name):
        return f"Hello, {name}!"

    def get_goodbye_msg(self, name):
        return f"Good bye, {name}!"

    def get_location_msg(self, location, detailed = False):
        msg = f"You are {location.preposition} the {location.name}."
        if (detailed and location.description):
            msg = msg + f"\n\n{location.description}"
        return msg

    def get_location_exits_msg(self, location, locations, world_directions):
        msg = ""
        if (len(location.exits)):
            msg = msg + f"You can see:"
            for loc in location.exits:
                msg = msg + f"\n   - {locations[location.exits[loc]].name} to the {world_directions[loc]}"
        else:
            msg = msg + f"There are no exits from {location.name}"
        return msg

class Game:
    world_directions = {
        "n": "North",
        "s": "South",
        "e": "East",
        "w": "West"
    }

    engine = AspyreEngine()
    narrator = Narrator()
    messages = []

    def intro(self):
        self.messages.append("Aspyre - Winter Adventure by Michał Hauzer, 2024")
        self.messages.append('. * , . * . \' , ` . * . \' * .  ` . *  \' * , ` *.')
        self.messages.append("")

    def print_messages(self):
        for m in self.messages:
            print(m)
        self.messages = []

    def is_world_direction(self, direction):
        return direction in self.world_directions

    def go(self, direction):
        if (self.is_world_direction(direction)):            
            if (direction in self.engine.locations[self.engine.player.location_id].exits):                
                self.messages.append(f"You go {self.world_directions[direction]}")
                self.messages.append("")
                self.engine.player.location_id = self.engine.locations[self.engine.player.location_id].exits[direction]                     
                self.engine.player.location_changed = True
            else:
                self.messages.append(f"You cannot go {self.world_directions[direction]}")
        else:
            self.messages.append(f"Unknown direction: {direction}")

    def wait(self):
        self.messages.append("You wait")

    def unknown_command(self, command):
        self.messages.append(f"I don't know how to {command}")

    def kill(self, something):
        if (something == "yourself"):
            self.messages.append("Don't do that! :-0")
        else:
            self.messages.append(f"You are trying to kill a {something} but there's no {something} to kill")

    def set_name(self):
        while len(self.engine.player.name) == 0:            
            self.engine.player.name = input("What is your name? ").strip()
            print("")

    def load_resources(self, filename):
        if debug:
            print(f"Loading resources from {filename}...")
        with open(filename, 'r') as f:
            # res = json.load(f, object_hook=complex_decoder)
            # self.engine.locations = res['locations']
            # if debug:
            #     print(res['locations'])
            #     print(self.locations[0].name)
            locations = json.load(f, object_hook=complex_decoder)
            for i in range(0, len(locations)):
                self.engine.locations[i] = locations[f"{i}"]
        f.close()        

    def save_resources(self, filename):
        print("Saving resources...")
        f = open(filename, "w")
        f.write(json.dumps(game.engine.locations, cls=LocationEncoder, indent=3))
        f.close()

    def play(self):
        self.set_name()
        self.messages.append(self.narrator.get_hello_msg(self.engine.player.name))
        self.messages.append("")

        end = False

        while not end:
            if (self.engine.player.location_changed):                
                location = self.engine.get_player_location()
                self.messages.append(self.narrator.get_location_msg(location, detailed = True))
                self.messages.append("")
                self.messages.append(self.narrator.get_location_exits_msg(location, self.engine.locations, self.world_directions))
                self.engine.player.location_changed = False

            self.messages.append("")
            self.print_messages()
            
            command = input(">")            
            self.messages.append("")
            self.print_messages()
    
            match(command.split()):
                case ["s"] | ["w"] | ["e"] | ["n"]: self.go(command)
                case "go", y: self.go(y)
                case "go", "to", y: self.go(y)
                case "kill", x: self.kill(x)
                case "kill", "a" | "the", x: self.kill(x)
                case "where", "am", "i": self.engine.player.location_changed = True
                case ["wait"]: self.wait()
                case ["quit"] | ["q"]: end = True
                case _: self.unknown_command(command)
            
        self.messages.append(self.narrator.get_goodbye_msg(self.engine.player.name))
                
LOCATIONS_FILE_NAME = 'locations.json'
CREATURES_FILE_NAME = 'creatures.json'

game = Game()

game.load_resources(LOCATIONS_FILE_NAME)
game.intro()
game.play()
game.print_messages()
# game.save_resources(LOCATIONS_FILE_NAME)