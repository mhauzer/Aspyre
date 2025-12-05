from aspyreengine import WorldEngine, Creature
import random
random.seed(42)

# Setup
we = WorldEngine()
we.load_resources('locations.json')
we.load_creatures('creatures.json')
player = we.get_player()
player.location_id = 4

# Get creatures at location
creatures = we.get_creatures_at(4)
print('Creatures at location 4:', [c.name for c in creatures])

# Find creature by name
matches = we.find_creatures_by_name(4, 'wolf')
print('Found wolf:', [c.name for c in matches])

if matches:
    wolf = matches[0]
    print(f'\nCombat test: {player.name} (HP:{player.health}, STR:{player.strength}) vs {wolf.name} (HP:{wolf.health}, STR:{wolf.strength})')
    
    # First attack
    result1 = we.attack_creature(player, wolf)
    print(f'Attack 1: Hit={result1["hit"]}, Damage={result1.get("damage", 0)}, Wolf HP={wolf.health}')
    
    # Second attack
    result2 = we.attack_creature(player, wolf)
    print(f'Attack 2: Hit={result2["hit"]}, Damage={result2.get("damage", 0)}, Wolf HP={wolf.health}')
    
    # Third attack
    result3 = we.attack_creature(player, wolf)
    print(f'Attack 3: Hit={result3["hit"]}, Damage={result3.get("damage", 0)}, Wolf HP={wolf.health}, Alive={wolf.is_alive}')
