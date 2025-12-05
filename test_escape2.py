#!/usr/bin/env python3

import random
import json
from aspyreengine import WorldEngine

# Seed for reproducibility
random.seed(42)

engine = WorldEngine()
engine.load_resources('locations.json')
engine.load_creatures('creatures.json')

# Create a player and get creatures
player = type('Player', (), {'health': 100, 'max_health': 100, 'strength': 10})()
location_id = 0

# Get the wolf and manually set its health to a low value to trigger escape
creatures = engine._WorldEngine__creatures
wolf = None
for creature_key, c in creatures.items():
    if 'Gray Wolf' in c.name:
        wolf = c
        break

if wolf:
    print(f"Testing escape mechanics with heavily wounded creature:")
    print(f"Initial: {wolf.name} (HP:{wolf.health}/{wolf.max_health}, STR:{wolf.strength})")
    print(f"======================================================================\n")
    
    # Set wolf to very low health (below 10%)
    wolf.health = 2
    wolf.max_health = 30
    wolf.location = location_id
    
    for attack_num in range(1, 25):
        print(f"Attack {attack_num}:")
        result = engine.attack_creature(player, wolf)
        print(result)
        
        if not wolf.is_alive:
            print(f"\nVictor! Wolf defeated. Player HP remaining: {player.health}")
            break
        elif 'flees in panic' in result:
            print(f"Wolf successfully escaped to location {wolf.location}")
            print(f"Escape triggered after {attack_num} attacks!")
            break
        
        print()
else:
    print("Wolf not found!")
