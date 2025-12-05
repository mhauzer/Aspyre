from aspyreengine import WorldEngine
from narrator import Narrator
import random
random.seed(300)

we = WorldEngine()
we.load_resources('locations.json')
we.load_creatures('creatures.json')
narrator = Narrator()
player = we.get_player()
player.location_id = 4

matches = we.find_creatures_by_name(4, 'wolf')
wolf = matches[0]
print(f'Starting combat: {player.name} (HP:{player.health}, STR:{player.strength}) vs {wolf.name} (HP:{wolf.health}, STR:{wolf.strength})')
print('=' * 70)

for i in range(20):
    if not player.is_alive or not wolf.is_alive:
        break
    
    result = we.attack_creature(player, wolf)
    msg = narrator.get_attack_msg(result, player.name, wolf.name)
    print(f'\nAttack {i+1}:')
    print(msg)
    
    if result.get('escaped'):
        print(f'\n{wolf.name} has fled to location {result["escape_location"]}')
        print(f'Combat ended! Player HP: {player.health}')
        break
    elif not wolf.is_alive:
        print(f'\nVictory! Player HP remaining: {player.health}')
        break
    elif not player.is_alive:
        print(f'\nDefeat! You were overcome by {wolf.name}')
        break
