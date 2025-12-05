#!/usr/bin/env python3

from aspyreengine import WorldEngine
from narrator import Narrator
import random

print("=" * 70)
print("CREATURE ESCAPE MECHANICS DEMONSTRATION")
print("=" * 70)

# Test with the seed that triggers escape
random.seed(0)

we = WorldEngine()
we.load_resources('locations.json')
we.load_creatures('creatures.json')
narrator = Narrator()

player = we.get_player()
player.location_id = 4

matches = we.find_creatures_by_name(4, 'wolf')
wolf = matches[0]

print(f"\nPlayer: {player.name} (HP: {player.health}, STR: {player.strength})")
print(f"Enemy:  {wolf.name} (HP: {wolf.health}, STR: {wolf.strength})")
print(f"Location: {we._WorldEngine__locations[4].name}")
print("\nBattle starts...\n")

for attack_num in range(1, 20):
    if not player.is_alive or not wolf.is_alive:
        break
    
    result = we.attack_creature(player, wolf)
    msg = narrator.get_attack_msg(result, player.name, wolf.name)
    
    print(f"--- Round {attack_num} ---")
    print(msg)
    
    if result.get('escaped'):
        escaped_loc_id = result['escape_location']
        escaped_loc_name = we._WorldEngine__locations[escaped_loc_id].name
        print(f"\n>>> {wolf.name} successfully escaped to {escaped_loc_name}!")
        print(f">>> Combat ended!")
        break
    elif not wolf.is_alive:
        print(f"\n>>> {wolf.name} has been defeated!")
        break
    elif not player.is_alive:
        print(f"\n>>> You were defeated by {wolf.name}!")
        break
    
    print()

print(f"\nFinal Status:")
print(f"  Player HP: {player.health}/{player.max_health}")
print(f"  {wolf.name} HP: {wolf.health}/{wolf.max_health}")
print(f"  {wolf.name} Location: {we._WorldEngine__locations[wolf.location_id].name}")
