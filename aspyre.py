import json
from aspyreengine import *
from narrator import Narrator

# https://reqbin.com/code/python/pbokf3iz/python-json-dumps-example

debug = False
dev = True

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

class Game:
    __LOCATIONS_FILE_NAME = 'locations.json'
    __CREATURES_FILE_NAME = 'creatures.json'

    engine = WorldEngine()
    narrator = Narrator()
    resources_changed = False
    messages = []

    def intro(self):
        self.messages.append("Aspyre - Winter Adventure by Michał Hauzer, 2024")
        self.messages.append('. * , . * . \' , ` . * . \' * .  ` . *  \' * , ` *.')
        self.messages.append("")

    def print_messages(self):
        for m in self.messages:
            print(m)
        self.messages = []

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
            for i in range(len(locations)):
                self.engine.locations[i] = locations[f"{i}"]
        f.close()        

    def save_resources(self, filename):
        print("Saving resources...")
        f = open(filename, "w")
        f.write(json.dumps(game.engine.locations, cls=LocationEncoder, indent=3))
        f.close()

    def main_loop(self):
        end = False

        while not end:
            if (self.engine.player.location_changed):                
                location = self.engine.get_player_location()
                self.messages.append(self.narrator.get_location_msg(location, detailed = True))
                self.messages.append("")
                self.messages.append(self.narrator.get_location_exits_msg(location, self.engine.locations))
                self.engine.player.location_changed = False

            self.messages.append("")
            self.print_messages()
            
            command = input(">")            
            self.messages.append("")
            self.print_messages()
    
            match(command.split()):
                case ["s"] | ["w"] | ["e"] | ["n"]: self.messages.append(self.narrator.move_player(command, self.engine.move_player(command)))
                case "go", y: self.messages.append(self.narrator.move_player(y, self.engine.move_player(y)))
                case "go", "to", y: self.messages.append(self.narrator.move_player(y, self.engine.move_player(y)))
                case "kill", x: self.messages.append(self.narrator.kill(self.kill(x)))
                case "kill", "a" | "the", x: self.messages.append(self.narrator.kill(self.kill(x)))
                case "where", "am", "i": self.engine.player.location_changed = True
                case ["wait"]: self.messages.append(self.narrator.wait())
                case ["quit"] | ["q"]: end = True
                case _: self.messages.append(self.narrator.unknown_command(command))

    def run(self):
        self.load_resources(self.__LOCATIONS_FILE_NAME)
        self.intro()

        if not dev:
            self.set_name()
        else:
            self.engine.player.name = 'Michał'

        self.messages.append(self.narrator.get_hello_msg(self.engine.player.name))
        self.messages.append("")

        self.main_loop()

        if self.resources_changed:
            game.save_resources(self.__LOCATIONS_FILE_NAME)

        self.messages.append(self.narrator.get_goodbye_msg(self.engine.player.name))
        self.print_messages()        
                
game = Game()
game.run()
