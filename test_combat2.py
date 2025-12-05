from aspyreengine import WorldEngine
import random
random.seed(100)

we = WorldEngine()
we.load_resources('locations.json')
we.load_creatures('creatures.json')
player = we.get_player()
player.location_id = 4

matches = we.find_creatures_by_name(4, 'wolf')
wolf = matches[0]
print(f'Starting: {wolf.name} HP={wolf.health}')

for i in range(10):
    result = we.attack_creature(player, wolf)
    if result['hit']:
        print(f'Attack {i+1}: HIT for {result["damage"]} damage, HP now {wolf.health}', end='')
        if not wolf.is_alive:
            print(' - DEFEATED!')
            break
        else:
            print()
    else:
        print(f'Attack {i+1}: DODGE')
