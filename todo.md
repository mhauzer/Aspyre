# TODO

- [ ] Integrate creature loading/parsing into the engine (if you want creatures instantiated as Creature objects).
- [ ] Add loot/items and connect to items.json.
- [ ] Place creatures at different location_id values or add more creatures.
- [ ] instantiate these creatures in the engine now,
- [ ] add loot entries to items.json and link them, or
- [ ] add more varied creatures?
- [ ] I can add detailed creature descriptions (HP/strength) to the display.
- [ ] I can add loot linking between creatures.json and items.json.
- [ ] I can make creatures persistently saved/updated when moved or killed.
- [ ] Link these items to creatures' loot drops in creatures.json.
- [ ] Add item-loading helpers to WorldEngine (like load_items() and get_item(id)).
- [ ] Add inventory support for the player and commands to pick up/drop items.
- [ ] Add item pickup messages including item names (currently shows id; we can display names).
- [ ] Allow taking items by name (e.g., take coin) with disambiguation for multiple instances.
- [ ] Save updated items_on_ground.json when items are picked/dropped so the world persists between runs.
- [ ] Add equip/use commands that apply item stats (e.g., equipping weapon changes player's strength or damage calculation).
- [ ] Show item names in pickup/drop confirmation messages,
- [ ] Allow taking items by name (with disambiguation),
- [ ] Persist items_on_ground.json so picks/drops survive game restarts.

What I recommend next

If you want defeated creatures to still appear in logs/admin UIs, call get_creatures_at(location_id, include_dead=True) where appropriate.
Optionally, add a short-lived corpse object or a dropped loot display when a creature dies (I can implement that next).
If you'd like, I can also update narrator.get_location_creatures_msg() to explicitly skip dead creatures (it should already not show them because it calls get_creatures_at()).
Would you like me to:

Add corpse/loot display when a creature is defeated? (useful for looting)
Search for and update any other places that intentionally need to see dead creatures and add include_dead=True there?