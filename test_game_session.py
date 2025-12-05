#!/usr/bin/env python3

from aspyreengine import WorldEngine
from narrator import Narrator
import random

print("QUICK GAME SESSION TEST\n")

# Quick test
random.seed(42)
we = WorldEngine()
we.load_resources('locations.json')
we.load_creatures('creatures.json')
we.load_items('items.json')
we.load_items_on_ground('items_on_ground.json')

narrator = Narrator()
player = we.get_player()

# Check player state
print(f"Player: {player.name}")
print(f"Starting Location: {we._WorldEngine__locations[player.location_id].name}")
print(f"Health: {player.health}/{player.max_health}")
print(f"Inventory: {len(player.inventory)} items")

# Try to find and attack a creature at starting location
print(f"\nSearching for creatures at starting location...")
creatures_here = we.get_creatures_at(player.location_id)
print(f"Creatures found: {len(creatures_here)}")

# Move to a location with creatures
player.location_id = 4
creatures_here = we.get_creatures_at(4)
print(f"\nMoved to deep forest - creatures found: {len(creatures_here)}")
for c in creatures_here:
    print(f"  - {c.name} (HP: {c.health})")

# Try an attack
if creatures_here:
    wolf = creatures_here[0]
    print(f"\nAttacking {wolf.name}...")
    result = we.attack_creature(player, wolf)
    msg = narrator.get_attack_msg(result, player.name, wolf.name)
    print(msg)
    print(f"\nWolf status after attack:")
    print(f"  Health: {wolf.health}/{wolf.max_health}")
    print(f"  Location: {we._WorldEngine__locations[wolf.location_id].name}")
    print(f"  Alive: {wolf.is_alive}")
    print(f"  Escaped: {result.get('escaped', False)}")

print("\n✓ Game session test completed successfully!")
