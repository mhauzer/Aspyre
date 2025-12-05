#!/usr/bin/env python3

from aspyreengine import WorldEngine
from narrator import Narrator
import random

# Try different seeds to find one that triggers escape
for seed in range(0, 100):
    random.seed(seed)
    
    we = WorldEngine()
    we.load_resources('locations.json')
    we.load_creatures('creatures.json')
    narrator = Narrator()
    
    player = we.get_player()
    player.location_id = 4
    
    matches = we.find_creatures_by_name(4, 'wolf')
    if not matches:
        continue
        
    wolf = matches[0]
    
    escape_triggered = False
    for attack_num in range(1, 30):
        if not player.is_alive or not wolf.is_alive:
            break
        
        result = we.attack_creature(player, wolf)
        
        if result.get('escaped'):
            escape_triggered = True
            print(f"Seed {seed}: ESCAPE TRIGGERED!")
            print(f"Starting: {player.name} (HP:{100}) vs {wolf.name} (HP:30)")
            print(f"After {attack_num} attacks: Wolf escaped to location {result['escape_location']}")
            print()
            break
    
    if escape_triggered:
        break
else:
    print("No escape found in first 100 seeds with normal combat")

# Now test with manually wounded creature
print("\n--- Testing with manually wounded creature ---\n")
random.seed(42)
we = WorldEngine()
we.load_resources('locations.json')
we.load_creatures('creatures.json')
narrator = Narrator()

player = we.get_player()
player.location_id = 4

matches = we.find_creatures_by_name(4, 'wolf')
wolf = matches[0]

# Manually wound it
wolf.health = 2
initial_location = wolf.location_id

print(f"Starting: {player.name} (HP:{player.health}) vs {wolf.name} (HP:2/30, heavily wounded)")
print(f"Location: {initial_location}")
print('=' * 70)

for attack_num in range(1, 25):
    if not player.is_alive or not wolf.is_alive:
        break
    
    result = we.attack_creature(player, wolf)
    msg = narrator.get_attack_msg(result, player.name, wolf.name)
    print(f'\nAttack {attack_num}:')
    print(msg)
    
    if result.get('escaped'):
        print(f'\n✓ {wolf.name} escaped to location {result["escape_location"]} (was at {initial_location})')
        print(f'Combat ended! Player HP: {player.health}')
        break
    elif not wolf.is_alive:
        print(f'\n✓ Victory! Player HP remaining: {player.health}')
        break
    elif not player.is_alive:
        print(f'\n✗ Defeat! You were overcome by {wolf.name}')
        break
