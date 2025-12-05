#!/usr/bin/env python3

import random
from aspyreengine import WorldEngine

engine = WorldEngine()
engine.load_resources('locations.json')

creatures = engine._WorldEngine__creatures
print(f"Available creatures: {len(creatures)}")
for c in creatures:
    print(f"  - {c.name} (HP:{c.health}/{c.max_health}, STR:{c.strength})")
