class Narrator:
    __world_directions = {
        "n": "North",
        "s": "South",
        "e": "East",
        "w": "West"
    }

    def is_world_direction(self, direction):
        return direction in self.__world_directions

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
            for loc in location.exits:
                msg = msg + f"\n   - {locations[location.exits[loc]].name} to the {self.__world_directions[loc]}"
        else:
            msg = msg + f"There are no exits from {location.name}"
        return msg

    def wait(self):
        return "You wait"
    
    def move_player(self, direction, result):        
        if (result):
            return f"You go {self.__world_directions[direction]}"
        else:
            return f"You cannot go {self.__world_directions[direction]}"
    
    def kill(self, something):
        if (something == "yourself"):
            return "Don't do that! :-0"
        else:
            return f"You are trying to kill a {something} but there's no {something} to kill"

    def unknown_command(self, command):
        return f"I don't know how to {command}"
