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
    __ITEMS_ON_GROUND_FILE_NAME = 'items_on_ground.json'

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
                creatures = self.engine.get_creatures_at(player.location_id)
                if creatures:
                    self.console.add_message("")
                    self.console.add_message(self.narrator.get_location_creatures_msg(creatures))
                # show items on ground
                items_here = self.engine.get_items_at(player.location_id)
                if items_here:
                    self.console.add_message("")
                    self.console.add_message(self.narrator.get_location_items_msg(items_here))
                player.location_changed = False

            self.console.add_message("")
            self.console.flush()
            
            command = self.console.get_message(">")            
            self.console.add_message("")
            self.console.flush()
    
            # command handling (supports movement, inventory, pickup and drop)
            tokens = command.split()
            match(tokens):
                case ["s"] | ["w"] | ["e"] | ["n"]: self.console.add_message(self.narrator.move_player(command, self.engine.move_object(player, command)))
                case "go", y: self.console.add_message(self.narrator.move_player(y, self.engine.move_player(y)))
                case "go", "to", y: self.console.add_message(self.narrator.move_player(y, self.engine.move_player(y)))
                case "attack" | "a", x: 
                    # Attack a creature by name
                    matches = self.engine.find_creatures_by_name(player.location_id, x)
                    if len(matches) == 0:
                        self.console.add_message(f"There is no {x} to kill here.")
                    elif len(matches) == 1:
                        creature = matches[0]
                        result = self.engine.attack_creature(player, creature)
                        self.console.add_message(self.narrator.get_attack_msg(result, "You", creature.name))
                        # Show player status after combat
                        if player.is_alive:
                            self.console.add_message(f"Your health: {player.health}/{player.max_health} HP")
                        else:
                            self.console.add_message(f"You have been defeated! Game Over.")
                            end = True
                    else:
                        msg = f"Multiple creatures match '{x}':\n"
                        for c in matches:
                            msg += f"   - {c.name} ({c.species})\n"
                        self.console.add_message(msg)
                case "kill", "a" | "the", x: 
                    # Attack a creature by name (with article)
                    matches = self.engine.find_creatures_by_name(player.location_id, x)
                    if len(matches) == 0:
                        self.console.add_message(f"There is no {x} to kill here.")
                    elif len(matches) == 1:
                        creature = matches[0]
                        result = self.engine.attack_creature(player, creature)
                        self.console.add_message(self.narrator.get_attack_msg(result, "You", creature.name))
                        # Show player status after combat
                        if player.is_alive:
                            self.console.add_message(f"Your health: {player.health}/{player.max_health} HP")
                        else:
                            self.console.add_message(f"You have been defeated! Game Over.")
                            end = True
                    else:
                        msg = f"Multiple creatures match '{x}':\n"
                        for c in matches:
                            msg += f"   - {c.name} ({c.species})\n"
                        self.console.add_message(msg)
                # pick up an item: 'take 3' or 'pick up 3' or 'take coin' (by name)
                case ["take", item_ref] | ["pick", "up", item_ref] | ["get", item_ref]:
                    # first try as numeric id
                    try:
                        iid = int(item_ref)
                        ok = self.engine.pick_up_item(player, iid)
                        if ok:
                            inst = player.inventory[-1]  # just picked up
                            name = inst.get('catalog', {}).get('name', 'item')
                            self.console.add_message(f"You pick up {name}.")
                        else:
                            self.console.add_message(f"There is no item with id {iid} here.")
                    except ValueError:
                        # not a numeric id; try name-based lookup
                        matches = self.engine.find_items_at_by_name(player.location_id, item_ref)
                        if len(matches) == 0:
                            self.console.add_message(f"No item named '{item_ref}' here.")
                        elif len(matches) == 1:
                            # unique match; pick it up
                            match_inst = matches[0]
                            iid = match_inst['instance_id']
                            ok = self.engine.pick_up_item(player, iid)
                            if ok:
                                name = match_inst['catalog'].get('name', 'item')
                                self.console.add_message(f"You pick up {name}.")
                            else:
                                self.console.add_message(f"Could not pick up the item.")
                        else:
                            # multiple matches; ask for disambiguation
                            self.console.add_message(self.narrator.get_item_matches_msg(matches))
                # drop an item from inventory: 'drop 3' or 'drop coin'
                case ["drop", item_ref]:
                    # first try as numeric id
                    try:
                        iid = int(item_ref)
                        ok = self.engine.drop_item(player, iid, player.location_id)
                        if ok:
                            self.console.add_message(f"You drop item id {iid}.")
                        else:
                            self.console.add_message(f"You are not carrying item id {iid}.")
                    except ValueError:
                        # not a numeric id; try name-based lookup in inventory
                        matches = self.engine.find_items_in_inventory_by_name(player, item_ref)
                        if len(matches) == 0:
                            self.console.add_message(f"You are not carrying an item named '{item_ref}'.")
                        elif len(matches) == 1:
                            # unique match; drop it
                            match_inst = matches[0]
                            iid = match_inst['instance_id']
                            ok = self.engine.drop_item(player, iid, player.location_id)
                            if ok:
                                name = match_inst['catalog'].get('name', 'item')
                                self.console.add_message(f"You drop {name}.")
                            else:
                                self.console.add_message(f"Could not drop the item.")
                        else:
                            # multiple matches; ask for disambiguation
                            self.console.add_message(self.narrator.get_drop_matches_msg(matches))
                # inventory listing
                case ["inventory"] | ["i"]:
                    self.console.add_message(self.narrator.get_inventory_msg(player.inventory, catalog=True))
                case "where", "am", "i": player.location_changed = True
                case ["look"] | ["l"]:
                    # show current location details immediately
                    self.console.add_message(self.narrator.get_scene_msg(self.engine.get_object_location(player),
                                                                        self.engine.get_locations(),
                                                                        self.engine.get_creatures_at(player.location_id),
                                                                        self.engine.get_items_at(player.location_id)))
                
                case "who", "am", "i": self.console.add_message(self.narrator.introduce(player.name))
                case ["help"]: self.console.add_message(self.narrator.get_help_msg())
                case ["wait"]: self.console.add_message(self.narrator.wait())
                case ["quit"] | ["q"]: end = True
                case _: self.console.add_message(self.narrator.unknown_command(command))

    def run(self):
        self.engine.load_resources(self.__LOCATIONS_FILE_NAME)
        # load creatures data so we can display creatures per location
        try:
            self.engine.load_creatures(self.__CREATURES_FILE_NAME)
        except Exception:
            # if creatures file missing or invalid, continue without creatures
            pass
        # load items catalog
        try:
            self.engine.load_items(self.__ITEMS_FILE_NAME)
        except Exception:
            # if items file missing or invalid, continue without items
            pass
        # load items on ground
        try:
            self.engine.load_items_on_ground(self.__ITEMS_ON_GROUND_FILE_NAME)
        except Exception:
            # if items on ground file missing or invalid, continue without items
            pass

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
