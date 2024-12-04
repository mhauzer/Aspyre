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
    def __init__(self):
        self.locations = {}
        self.player = Creature("human", "", 100, 10, 0, True)

    def get_player_location(self):
        return self.locations[self.player.location_id]

    def move_player(self, direction):        
        if (not direction in self.locations[self.player.location_id].exits):
            return False
        
        self.player.location_id = self.locations[self.player.location_id].exits[direction]
        self.player.location_changed = True

        return True        
            
