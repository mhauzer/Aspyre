# Aspyre

Aspyre is a terminal-based fantasy adventure game written in Python.
You explore a connected world, encounter creatures, fight in turn-based combat,
and pick up or drop items as you travel.

## Highlights

- Text adventure loop with directional movement (`n`, `s`, `e`, `w`)
- World loaded from JSON data files
- Creature encounters with combat and counter-attacks
- Creature escape behavior when enemies are low on health
- Ground item pickup and inventory drop by name or id
- Narrated scene descriptions, exits, and location entities

## Requirements

- Python 3.10 or newer (pattern matching syntax is used)
- No external dependencies (standard library only)

## Quick Start

From the project root:

```bash
python aspyre.py
```

If your system uses `python3`:

```bash
python3 aspyre.py
```

## Core Commands

### Movement

- `n`, `s`, `e`, `w`
- `go <direction>`
- `go to <direction>`

### Exploration

- `look` or `l`
- `where am i`
- `who am i`
- `wait`

### Inventory

- `inventory` or `i`
- `take <name_or_id>`
- `pick up <name_or_id>`
- `get <name_or_id>`
- `drop <name_or_id>`

### Combat

- `attack <creature_name>`
- `kill a <creature_name>`
- `kill the <creature_name>`

### Meta

- `help`
- `quit` or `q`

## Data Files

The game world and entities are data-driven:

- `locations.json`: location graph, descriptions, and exits
- `creatures.json`: creatures with stats and spawn locations
- `items.json`: item catalog metadata
- `items_on_ground.json`: item instances currently placed in the world
- `map.txt`: human-readable world map overview

## Project File Overview

- `aspyre.py`: main game entry point and command loop
- `aspyreengine.py`: world engine, movement, creatures, combat, and item logic
- `narrator.py`: player-facing text formatting and command responses
- `console.py`: buffered console input/output abstraction

Utility and demo scripts:

- `demo_escape.py`: demonstrates escape mechanics in combat
- `check_creatures.py`: simple creature loading/inspection helper

Ad-hoc test scripts:

- `test_combat.py`, `test_combat2.py`, `test_combat3.py`
- `test_escape.py`, `test_escape2.py`, `test_escape3.py`
- `test_game_session.py`

## Running Test Scripts

These scripts are simple executable test/demo files (not a formal test framework).
Run them directly from the project root, for example:

```bash
python test_game_session.py
python test_combat.py
python test_escape.py
```

## Notes

- The default player name is set in development mode.
- Game data is loaded at startup from JSON files in the repository root.
- Combat outcomes include randomness. For reproducible checks, test scripts set random seeds.

## License

No explicit license file is currently included in this repository.
If you plan to distribute or accept contributions, consider adding a `LICENSE` file.
