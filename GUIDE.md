# Random World – No Factions: complete beginner's guide

This guide assumes you have **never modded a game and never seen code**.
Follow it top to bottom. Nothing here requires programming — only copying
files, and (once) pasting a small text block and checking three numbers.

**What the mod does** when you start a new game:

- Factions are gone forever. Nobody can create or join one — not you, not the AI.
- Three new countries exist next to all the normal ones: **Nesterivtsi**,
  **Kamianets** and **Kharkiv** (all from Ukraine, sitting on their real homes).
- The **whole world map is reshuffled**: every country starts from one random
  state and grows outward into neighboring land until the entire world is
  divided, with everyone roughly the same size. No state is left unowned.
  The three custom countries start growing from their historic homes.
- Every country gets a **random ideology** (fascist / communist / democratic /
  non-aligned) — names like "Nesterivtsi Reich" or "Communist Nesterivtsi"
  appear automatically.
- The **factories already built** in each state are re-rolled randomly.
  Building **slots** and **population** stay exactly vanilla — the mod never
  touches them.

---

## Part 0 — What you need

1. **Hearts of Iron IV**, version 1.19, with the normal Paradox launcher.
2. **A text editor.** Windows Notepad works, but install one of these free
   editors instead — they show line numbers and never mangle files:
   - [Visual Studio Code](https://code.visualstudio.com/) (recommended), or
   - [Notepad++](https://notepad-plus-plus.org/)
3. **This repository's files** (the folder `random_world` and its contents).
4. Ten minutes.

**Two folders you must be able to find.** Modding uses exactly two places:

| What | Typical location on Windows |
|---|---|
| The **game folder** (where the game is installed; we only READ from it) | `C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV` |
| The **mod folder** (where mods live; we WRITE here) | `C:\Users\YOURNAME\Documents\Paradox Interactive\Hearts of Iron IV\mod` |

On Mac the second one is `~/Documents/Paradox Interactive/Hearts of Iron IV/mod`.
If you can't find the game folder: Steam → right-click the game → *Manage* →
*Browse local files*.

> **Windows tip:** turn on file extensions (Explorer → *View* → tick
> *File name extensions*), otherwise a file you name `test.txt` may secretly
> be `test.txt.txt` and the game won't read it.

---

## Part 1 — Two minutes of theory: how a HOI4 mod works

A HOI4 mod is **just a folder of text files** whose layout copies the game's
own folder. When the game loads, any file in your mod sits "on top of" the
game's files: new files are added, and (for most folders) files with content
the game already has extend it. There is no compiling and no programming
environment — you edit text, start the game, and see the result.

The special file `descriptor.mod` inside the mod folder tells the launcher
the mod's name and supported game version. A second tiny file (created by the
launcher, one level up) tells the launcher where the folder is.

That's the whole theory. Everything else is details of *which* text goes in
*which* file — and this repository already contains all of it.

---

## Part 2 — Step 1: Create an empty mod with the launcher

1. Start Hearts of Iron IV so the **Paradox launcher** opens. Do not press Play.
2. In the launcher, open **All installed mods** (left menu).
3. Click **Mod tools** (top right), then **Create a mod**.
4. Fill in:
   - **Name:** `Random World - No Factions`
   - **Version:** `1.0.0`
   - **Directory name:** `random_world`  ← must be exactly this
   - **Tags:** tick anything, e.g. *Gameplay* and *Map*.
5. Click **Create**. The launcher has now made:
   - the folder `Documents\Paradox Interactive\Hearts of Iron IV\mod\random_world\`
   - the file `...\mod\random_world.mod` (launcher bookkeeping — never touch it)

*(If the launcher offers no mod-creation button in your setup: create the
folder yourself and copy `random_world/docs/random_world.mod.example` to
`mod/random_world.mod` as described inside that file.)*

## Part 3 — Step 2: Copy the mod files

Copy **the contents of** this repository's `random_world` folder into the
folder the launcher just created, replacing anything already there
(it's fine to overwrite the generated `descriptor.mod`).

When you're done, the mod folder must look exactly like this:

```
Documents\Paradox Interactive\Hearts of Iron IV\mod\random_world\
├── descriptor.mod
├── common\
│   ├── country_tags\
│   │   └── 01_random_world_tags.txt        ← declares the tags NES, KAM, KHA
│   ├── countries\
│   │   ├── Nesterivtsi.txt                 ← art style + fallback color per country
│   │   ├── Kamianets.txt
│   │   └── Kharkiv.txt                     ← (you will add colors.txt here in Step 3)
│   ├── on_actions\
│   │   └── ZZ_random_world_on_actions.txt  ← hooks: run randomizer at start, re-ban factions weekly
│   └── scripted_effects\
│       └── random_world_scripted_effects.txt  ← THE BRAIN: all randomizer logic
├── history\
│   ├── countries\
│   │   ├── NES - Nesterivtsi.txt           ← starting setup of each custom country
│   │   ├── KAM - Kamianets.txt
│   │   └── KHA - Kharkiv.txt
│   └── units\
│       ├── NES_1936.txt                    ← division blueprint of each custom country
│       ├── KAM_1936.txt
│       └── KHA_1936.txt
├── localisation\
│   └── english\
│       └── random_world_l_english.yml      ← the 4 ideology names of each country
├── gfx\
│   └── flags\                              ← 45 placeholder flags (3 sizes × 5 variants × 3 tags)
│       ├── NES.tga, NES_fascism.tga, ...
│       ├── medium\ ...
│       └── small\ ...
└── docs\
    ├── colors_txt_snippet.txt              ← used in Step 3
    └── random_world.mod.example
```

## Part 4 — Step 3: The one manual step — `colors.txt`

The game keeps every country's **map color** in one file:
`common/countries/colors.txt`. This particular file is **replaced, not
merged**, when a mod ships its own copy — so if the mod contained only our
three countries, all vanilla countries would lose their colors. Therefore the
mod does not ship it, and you build your own copy once:

1. Open the **game folder** → `common` → `countries`.
2. Copy the file `colors.txt`.
3. Paste it into the **mod** at `random_world\common\countries\` (next to
   `Nesterivtsi.txt`).
4. Open the pasted copy in your editor, scroll to the very **bottom**, and
   paste the whole block from `random_world\docs\colors_txt_snippet.txt`
   (the `NES = {...} KAM = {...} KHA = {...}` part).
5. Save. Done — this never needs touching again.

If you skip this step the mod still works; the three countries just get an
ugly auto-color on the map.

## Part 5 — Step 4: Check three numbers (the historic home states)

Every state on the map has an **ID number**. The custom countries are pinned
to their historic homes through three numbers in one file. The defaults are
correct for the vanilla map as we know it, but Paradox occasionally re-splits
states between patches — so verify once:

**The 2-minute check, inside the game:**

1. Enable the mod (Step 5 below), start any new game, and once on the map
   press **`** / **~** (the key under Esc) to open the console.
2. Type `tdebug` and press Enter.
3. Hover the mouse over **Vinnytsia / Khmelnytskyi area (western Ukraine)** —
   a tooltip appears; read **STATE ID**. Expected: **196**.
4. Hover over **Kharkiv (eastern Ukraine)**. Expected: **198**.
5. Type `tdebug` again to turn the tooltip off.

If the numbers differ, open
`random_world\common\scripted_effects\random_world_scripted_effects.txt`,
find the block marked `THE ONLY NUMBERS YOU MAY NEED TO EDIT` (section 5),
and put the IDs you saw on the `NES` / `KAM` / `KHA` lines. Change the same
numbers after `capital =` in the three files under `history\countries\`.

> Why do NES and KAM share the number 196? Both real places lie in one
> vanilla state. The script is built for this: the first country takes the
> state, the second automatically starts in a free state next door. If your
> game version has a separate "Kamenets-Podolsk" state, give KAM that ID.

## Part 6 — Step 5: Turn it on and test

1. Launcher → **Playsets**: add *Random World - No Factions* to your playset
   and tick it. (Achievements will be disabled — normal for any mod.)
2. Play → new game, **1936**, pick any country. **Note:** the selection
   screen still shows the *vanilla* world — the reshuffle happens the moment
   the session starts. Expect the start to take a few extra seconds: the
   script is dividing the whole planet.
3. On the map you should see: a patchwork world; no grey/unowned land
   anywhere; Nesterivtsi, Kamianets and Kharkiv in/near Ukraine; every
   country with a random ideology; no factions in the diplomacy screen.
4. Quick sanity check of the rules we must not break: open any state — its
   building **slots** and **population** are vanilla; only the built
   factories differ.

**Where the logs are** (your best friends when something is off):
`Documents\Paradox Interactive\Hearts of Iron IV\logs\` —
`game.log` (the script prints `[RW] ...` progress lines there) and
`error.log` (loading problems, typos, wrong effect names).

---

## Part 7 — How the world generator actually works (plain words)

Everything happens in `random_world_scripted_effects.txt`, once, at start.
The file is heavily commented; this is the same story without code:

1. **Ban factions.** Whoever leads a faction dismantles it; then every
   country gets two permanent "country rules" that grey out *Create Faction*
   and *Join Faction*. A weekly hook re-applies the rules so countries born
   later (civil wars, released nations) are covered forever.
2. **Clean the table.** All puppets are freed, the 1936 Italy–Ethiopia war is
   ended in a white peace. Now land can move without dragging wars around.
3. **Count the map.** The script counts every land state (that number ÷
   number of countries = the **target size** everyone should reach).
4. **Seed the custom countries** on their home states. If a home is taken
   (NES and KAM share one), the latecomer starts next door.
5. **Build "the pool"**: the list of every country alive in 1936 plus the
   three customs. Each pool country also secretly *protects* one of its
   current states — random seeds may not land there. This guarantees no
   country is accidentally wiped off the map before it received its own seed
   (the classic bug of naive randomizers: someone's seed lands on
   Luxembourg's only state and Luxembourg silently stops existing).
6. **Random seeds for everyone else.** Every pool country gets one random
   free, non-protected, non-wasteland state — its new "starting point".
7. **Growth, round by round** *(the balance mechanism)*: all countries take
   turns; on its turn a country below the target size claims **one** free
   state **touching** its territory. Repeat rounds until a whole round
   changes nothing. Because everyone adds at most one state per round, sizes
   stay nearly equal for as long as geography allows.
8. **Overflow pass:** the same loop with the size cap removed, to swallow
   pockets only reachable by already-full countries. Nothing may stay empty.
9. **Islands** (exempt from the land rule by design): while anything is
   still free, the currently **smallest** country gets one island state as a
   beachhead, then the overflow pass fills that island chain; repeat. When
   this ends, the free-state counter is zero — the whole world is owned.
10. **Finishing touches:** each country's capital moves to its seed; each
    country gets **cores** on what it owns and loses old cores elsewhere
    (clean start, full manpower — population itself untouched); each country
    rolls one of the 4 ideologies at 25% each.
11. **Industry re-roll:** every state's built civilian factories (0–8),
    military factories (0–6) and — on coastal states — dockyards (0–5) are
    set to weighted random values. Slot limits and population: untouched.

## Part 8 — Which file does what (one line each)

| File | Purpose |
|---|---|
| `descriptor.mod` | Mod's ID card for the launcher (name, game version). |
| `common/country_tags/01_random_world_tags.txt` | "NES, KAM, KHA exist." |
| `common/countries/*.txt` | Per country: unit-art style + fallback color. |
| `common/countries/colors.txt` | Map colors — **you** build it in Step 3. |
| `common/on_actions/ZZ_random_world_on_actions.txt` | "At game start run the randomizer once; every week re-ban factions." |
| `common/scripted_effects/random_world_scripted_effects.txt` | The entire algorithm (sections 0–12, commented). |
| `history/countries/TAG - Name.txt` | Custom country's 1936 setup: capital, techs, politics, equipment. |
| `history/units/TAG_1936.txt` | Its division blueprint (so it can train troops immediately). |
| `localisation/english/random_world_l_english.yml` | The names: 4 ideology names per custom country. **Must stay UTF-8 with BOM** (it already is; editors keep it if you just edit and save). |
| `gfx/flags/…` | Placeholder flags, 3 sizes × 5 variants per tag. |
| `tools/generate_flags.py` (repo only) | The script that generated those flags — rerun after editing colors in it, or just replace the TGAs with real art. |

## Part 9 — Troubleshooting

| Symptom | Cause & fix |
|---|---|
| Mod not in the launcher | The folder isn't at `...\Hearts of Iron IV\mod\random_world`, or `random_world.mod` (launcher side) is missing — redo Part 2, or use `docs/random_world.mod.example`. |
| Game starts but world is vanilla | The mod isn't ticked in the **active playset**; or you loaded an old save (the randomizer runs once per *new* campaign only); or `game.log` has no `[RW]` lines → check `error.log` for a typo you may have introduced. |
| Countries turned grey on the map | Your `colors.txt` copy is broken — redo Part 4 (copy vanilla file again, paste snippet at the very bottom, nothing else changed). |
| Checkerboard instead of a flag | A `.tga` is missing/renamed in `gfx/flags` (all three sizes must exist). |
| `NES`/`KAM`/`KHA` show as raw text instead of names | Localisation file lost its BOM or the `english` folder name is wrong. Re-copy `random_world_l_english.yml` from this repo. |
| Custom countries not in Ukraine | Home-state IDs differ on your game version — do Part 5 and fix the three numbers. |
| Small pause at game start | Normal: the script divides ~all states of the world once. A few seconds on slow PCs. |
| A few unowned states remain / a phase seems skipped | Open `error.log`. If it names a line in `random_world_scripted_effects.txt`, one effect spelling changed in your patch — see the substitution table below. |

**Substitution table** — HOI4 script keywords occasionally shift between
patches. Each risky construct is isolated so a one-line swap fixes it. Find
the line `error.log` complains about and try the replacement:

| If this errors | Replace with |
|---|---|
| `transfer_state = PREV` (in `rw_claim_this_state`) | `transfer_state = PREV.id` |
| `set_capital = { state = var:rw_capital_state }` | delete the whole `if` block around it — the game auto-picks capitals |
| `set_building_level = { type = X level = N instant_build = yes }` | remove ` instant_build = yes`; if still erroring, replace the line with `add_building_construction = { type = X level = N instant_build = yes }` (adds on top of vanilla instead of replacing — an acceptable fallback) |
| `while_loop_effect` unknown | replace each `while_loop_effect = { limit = {...}` with `for_loop_effect = { start = 0 end = 200` and move the old `limit` triggers into an `if` wrapped around the loop body |
| `impassable = yes` unknown trigger | delete that single line (wasteland then just becomes seedable — cosmetic) |
| `white_peace = PREV` | `white_peace = { tag = PREV }` |

## Part 10 — FAQ and honest limitations

- **Achievements** are disabled with any mod. Nothing to do about it.
- **The country-selection screen shows the old world.** The reshuffle
  happens after you press Play — the engine gives mods no earlier hook.
- **Armies on day 1** may teleport: units standing on land that changed hands
  get auto-relocated by the engine. Harmless, settles immediately.
- **Vanilla focus trees** still reference historical geography ("Danzig or
  War" when Germany is in Peru). That's inherent to every randomizer mod;
  national focuses stay usable, some just become nonsense-flavored. The
  custom countries use the **generic** tree and are immune.
- **Custom countries have no unique leader portraits** — the game shows a
  generic "unknown" politician. Adding characters is a nice later extension.
- **Saves are safe:** the randomizer marks the campaign with a flag stored in
  the save, so loading never re-randomizes.

## Part 11 — Recipe: add a fourth custom country yourself

Say you want `LVI` — "Lviv". Copy the NES pattern:

1. `common/country_tags/01_random_world_tags.txt`: add
   `LVI = "countries/Lviv.txt"` (check the tag isn't taken in vanilla's
   `00_countries.txt`).
2. `common/countries/Lviv.txt`: copy `Nesterivtsi.txt`, adjust the color.
3. Your `colors.txt`: append an `LVI = { ... }` block.
4. `history/countries/LVI - Lviv.txt`: copy the NES file; set `capital =`
   to Lviv's state ID (find it with `tdebug`); replace `NES` with `LVI`.
5. `history/units/LVI_1936.txt`: copy, done.
6. Localisation: add `LVI_neutrality`, `LVI_fascism`, `LVI_communism`,
   `LVI_democratic` (+ `_DEF`) lines.
7. Flags: copy any tag's 15 TGA files and rename to `LVI…` (or edit
   `tools/generate_flags.py` and rerun it).
8. Scripted effects, section 5: add the two `LVI` lines
   (`set_variable = { rw_home_state = <id> }` and
   `LVI = { rw_seed_at_home_state = yes }`).

That's all — the pool, growth, politics and industry phases pick the new
country up automatically, because they operate on "every existing country".
