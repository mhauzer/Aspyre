from aspyreengine import *
from narrator import Narrator
from console import Console

# https://reqbin.com/code/python/pbokf3iz/python-json-dumps-example

debug = False
dev = True

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
        player = self.engine.get_player()
        while len(player.name) == 0:            
            player.name = self.console.get_message("What is your name? ").strip()
            self.console.add_message("")
            self.console.flush()

    def main_loop(self):
        end = False
        player = self.engine.get_player()

        while not end:
            if player.location_changed:
                location = self.engine.get_object_location(player)
                self.console.add_message(self.narrator.get_location_msg(location, detailed = True))
                self.console.add_message("")
                self.console.add_message(self.narrator.get_location_exits_msg(location, self.engine.get_locations()))
                player.location_changed = False

            self.console.add_message("")
            self.console.flush()
            
            command = self.console.get_message(">")            
            self.console.add_message("")
            self.console.flush()
    
            match(command.split()):
                case ["s"] | ["w"] | ["e"] | ["n"]: self.console.add_message(self.narrator.move_player(command, self.engine.move_object(player, command)))
                case "go", y: self.console.add_message(self.narrator.move_player(y, self.engine.move_player(y)))
                case "go", "to", y: self.console.add_message(self.narrator.move_player(y, self.engine.move_player(y)))
                case "kill", x: self.console.add_message(self.narrator.kill(player.kill(x)))
                case "kill", "a" | "the", x: self.console.add_message(self.narrator.kill(player.kill(x)))
                case "where", "am", "i": player.location_changed = True
                case "who", "am", "i": self.console.add_message(self.narrator.introduce(player.name))
                case ["wait"]: self.console.add_message(self.narrator.wait())
                case ["quit"] | ["q"]: end = True
                case _: self.console.add_message(self.narrator.unknown_command(command))

    def run(self):
        self.engine.load_resources(self.__LOCATIONS_FILE_NAME)
        self.intro()
        player = self.engine.get_player()

        if not dev:
            self.set_name(player)
        else:
            player.name = 'Michał'

        self.console.add_message(self.narrator.get_hello_msg(player.name))
        self.console.add_message("")

        self.main_loop()

        if self.engine.resources_changed:
            self.engine.save_resources(self.__LOCATIONS_FILE_NAME)

        self.console.add_message(self.narrator.get_goodbye_msg(player.name))
        self.console.flush()        

def main():                
    game = Game()
    game.run()

main()
