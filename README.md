# Epic Adventure (WIP)

A simple terminal-based, text adventure game. Navigate branching paths, face distinct enemies, and try to survive long enough to beat them all. This is the **original Python version** that the the web UI mirrors. The web version gets continuously ported as I make updates to this version.

---

## What’s inside

* **Pure Python**: standard library only (no external deps).
* **Data-driven game logic**: difficulty presets, enemy aggression, damage variance, victory rewards.
* **Simple, readable code** using `@dataclass`es and small functions—easy to extend and balance.

---

## How to play

1. **Run the game** in a terminal:

   ```bash
   python3 epic_adventure.py
   # or: python epic_adventure.py
   ```
2. Choose a **difficulty** (Easy / Medium / Hard).
3. Enter your **name**. *(Try “Marcus” for a fun easter egg.)*
4. From the crossroads, **pick a direction** and survive the fights using:

   * `1` = **Attack** — deals damage; enemy may attack or defend
   * `2` = **Defend** — mitigates damage and may counter

Winning grants **health + attack rewards** and levels you up. Defeat ends the run (with suitably dramatic flavor text).

---

## Architecture (Design Notes)

* **Difficulty Settings**: player baselines, enemy multipliers, and post-battle rewards via the `DIFFICULTY_SETTINGS` dict.
* **Encounters**: configured with the `EncounterConfig` dataclass (`BASE_ENCOUNTERS` maps directions → encounters).
* **Enemy AI**: weighted “attack vs defend” choice based on remaining HP and aggression.
* **Damage Model**: variable damage band, minimum chip damage, and block/counter behavior.
* **Progression**: post-battle recovery + attack increment; `level` increases after victories.
* **Easter egg**: entering the name `marcus` unlocks the Rock at the campfire.

---

## Extending the game

### Add a new encounter

Open your game script and append a new entry to `BASE_ENCOUNTERS` (keys are directions shown to the player):

```python
from dataclasses import dataclass

# Existing dataclass:
# @dataclass(frozen=True)
# class EncounterConfig: ...

BASE_ENCOUNTERS["northeast"] = EncounterConfig(
    name="Wraith",
    base_health=80,
    base_attack=20,
    base_defense=4,
    aggression=70,
    crossroad_description=(
        "To the North-East:\tCold mist coils over an old grave road."
    ),
    intro_text=(
        "\n\tA chill pools at your feet as whispers rise from the stones..."
    ),
    victory_text=(
        "The wraith dissolves like frost in sunlight. You press on.\n"
    ),
    defeat_text=(
        "Your warmth gutters out; the mist keeps what it takes.\n"
    ),
)
```

> The crossroad menu is auto-built from the keys of `BASE_ENCOUNTERS` (plus the campfire encounter when the player name is `marcus`). No extra wiring needed.

### Tweak difficulty

Adjust `DIFFICULTY_SETTINGS` to change player baselines, enemy multipliers, and post-battle rewards:

```python
DIFFICULTY_SETTINGS = {
    "medium": {
        "player": {"health": 100, "attack": 15, "defense": 5},
        "enemy":  {
            "health_multiplier": 1.0,
            "attack_multiplier": 1.0,
            "defense_multiplier": 1.0,
        },
        "rewards": {"health": 15, "attack": 2},
    },
    # "easy", "hard", etc.
}
```

---

## CLI UX & Notes

* Input is **case-insensitive** and validated; you’ll be reprompted on invalid entries.
* Health/status is printed each round; press **Enter** when prompted to continue.
* Directions are typed exactly as shown in the prompt (e.g., `north`, `west`).

---

## Roadmap

* [ ] Save/load runs (local file / JSON)
* [ ] Encounter scripting helpers (status effects, items, skills)
