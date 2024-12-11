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

    def unknown_command(self, command):
        return f"I don't know how to {command}"
