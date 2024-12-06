from aspyreengine import *
from narrator import Narrator

# https://reqbin.com/code/python/pbokf3iz/python-json-dumps-example

debug = False
dev = True

class Console:
    __messages = []

    def add_message(self, message):
        self.__messages.append(message)

    def get_message(self, prompt):
        return input(prompt)

    def print_messages(self):
        for m in self.__messages:
            print(m)
        self.__messages = []

    def print(self, message):
        self.add_message(message)
        self.print_messages()

class Game:
    __LOCATIONS_FILE_NAME = 'locations.json'
    __CREATURES_FILE_NAME = 'creatures.json'
    __ITEMS_FILE_NAME = 'items.json'
    __SAVEGAME_FILE_NAME = 'savegame.json'

    engine = WorldEngine()
    narrator = Narrator()
    console = Console()

    def intro(self):
        self.console.add_message("Aspyre - Winter Adventure by Michał Hauzer, 2024")
        self.console.add_message('. * , . * . \' , ` . * . \' * .  ` . *  \' * , ` *.')
        self.console.add_message("")

    def set_name(self):
        while len(self.engine.player.name) == 0:            
            self.engine.player.name = self.console.get_message("What is your name? ").strip()
            self.console.print("")

    def main_loop(self):
        end = False

        while not end:
            if self.engine.player.location_changed:
                location = self.engine.get_object_location(self.engine.player)
                self.console.add_message(self.narrator.get_location_msg(location, detailed = True))
                self.console.add_message("")
                self.console.add_message(self.narrator.get_location_exits_msg(location, self.engine.get_locations()))
                self.engine.player.location_changed = False

            self.console.add_message("")
            self.console.print_messages()
            
            command = input(">")            
            self.console.add_message("")
            self.console.print_messages()
    
            match(command.split()):
                case ["s"] | ["w"] | ["e"] | ["n"]: self.console.add_message(self.narrator.move_player(command, self.engine.move_object(self.engine.player, command)))
                case "go", y: self.console.add_message(self.narrator.move_player(y, self.engine.move_player(y)))
                case "go", "to", y: self.console.add_message(self.narrator.move_player(y, self.engine.move_player(y)))
                case "kill", x: self.console.add_message(self.narrator.kill(self.kill(x)))
                case "kill", "a" | "the", x: self.console.add_message(self.narrator.kill(self.kill(x)))
                case "where", "am", "i": self.engine.player.location_changed = True
                case ["wait"]: self.console.add_message(self.narrator.wait())
                case ["quit"] | ["q"]: end = True
                case _: self.console.add_message(self.narrator.unknown_command(command))

    def run(self):
        self.engine.load_resources(self.__LOCATIONS_FILE_NAME)
        self.intro()

        if not dev:
            self.set_name()
        else:
            self.engine.player.name = 'Michał'

        self.console.add_message(self.narrator.get_hello_msg(self.engine.player.name))
        self.console.add_message("")

        self.main_loop()

        if self.engine.resources_changed:
            self.engine.save_resources(self.__LOCATIONS_FILE_NAME)

        self.console.add_message(self.narrator.get_goodbye_msg(self.engine.player.name))
        self.console.print_messages()        

def main():                
    game = Game()
    game.run()

main()
