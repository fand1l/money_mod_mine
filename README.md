# Random World – No Factions (Hearts of Iron IV 1.19 mod)

A vanilla-game mod that, at the start of every new campaign:

- **permanently disables factions** for every country (player and AI);
- adds **three custom countries** on their historic Ukrainian homes —
  Nesterivtsi (NES), Kamianets (KAM), Kharkiv (KHA) — with four
  ideology-dependent names each and generic focus trees;
- **randomizes the entire world**: every existing country (vanilla + custom)
  gets a random seed state and grows into adjacent land until the whole map
  is divided with **no unowned states** and **roughly equal country sizes**
  (islands are assigned separately to the smallest countries);
- gives every country a **random ideology** (25% each);
- **re-rolls built factories** (civilian, military, dockyards) per state —
  while **never touching building-slot limits or state population**.

## Repository layout

| Path | What it is |
|---|---|
| [`WORK_PLAN.md`](WORK_PLAN.md) | The milestone plan the mod was built against. |
| [`GUIDE.md`](GUIDE.md) | **Start here.** Full step-by-step install & explanation guide for absolute beginners. |
| [`random_world/`](random_world/) | The mod itself — copy its contents into `Documents/Paradox Interactive/Hearts of Iron IV/mod/random_world/`. |
| [`tools/generate_flags.py`](tools/generate_flags.py) | Generator for the placeholder flag TGAs (already run; outputs are committed). |

## Quick install (details in GUIDE.md)

1. Launcher → *Mod tools* → *Create a mod* → directory name `random_world`.
2. Copy the contents of this repo's `random_world/` into that folder.
3. One manual step: copy the game's `common/countries/colors.txt` into the
   mod and append `random_world/docs/colors_txt_snippet.txt` to its end.
4. Optional 2-minute check of the three home-state IDs (`GUIDE.md`, Part 5).
5. Enable the mod in your playset and start a **new** 1936 game.

All randomizer logic lives in one commented file:
`random_world/common/scripted_effects/random_world_scripted_effects.txt`.
