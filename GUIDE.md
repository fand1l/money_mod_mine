# Random World – No Factions: complete beginner's guide

This guide assumes you have **never modded a game and never seen code**.
Follow it top to bottom. Nothing here requires programming — only copying
files, and (once) pasting a small text block and checking three numbers.

**What the mod does:**

- Factions are gone forever. Nobody can create or join one — not you, not the AI.
- Three new countries — **Nesterivtsi**, **Kamianets** and **Kharkiv** — sit
  on the pre-randomization 1936 map with their own borders on/next to their
  real Ukrainian homes (that map exists only for a moment before the
  reshuffle, see below).
- **New Game is streamlined:** only the **1936** scenario exists (1939 is
  removed), and the Select Country screen shows **no featured majors** —
  just the "Other countries" card that takes you to picking a country on
  the map.
- **The world is reshuffled when you press the decision "Randomize the
  World!"** (Decisions panel → *Random World* category — free, available
  from day 1, once per campaign; the AI never presses it): every existing
  country — the three custom ones included — gets one completely **random
  seed state** and grows outward into neighboring land until the entire
  world is divided, with everyone roughly the same size and no state left
  unowned. Because the decision fires in-session, **every campaign gets a
  fresh world** — no seed numbers, no game restarts.
- Every state is guaranteed **at least 2 civilian and 2 military
  factories** after the reshuffle, so no country starts without an economy.
- (Optional, disabled: a lobby-time trigger in `common/bookmarks/` that
  generates the world before country selection — deterministic per the
  seed number in `rw_world_seed.txt`; see Part 6, item 6.)
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
│   ├── bookmarks\
│   │   ├── the_gathering_storm.txt         ← 1936 scenario: no majors + auto-randomize on load
│   │   └── blitzkrieg.txt                  ← empty on purpose: removes the 1939 scenario
│   ├── country_tags\
│   │   └── 01_random_world_tags.txt        ← declares the tags NES, KAM, KHA
│   ├── countries\
│   │   ├── Nesterivtsi.txt                 ← art style + fallback color per country
│   │   ├── Kamianets.txt
│   │   └── Kharkiv.txt                     ← (you will add colors.txt here in Step 3)
│   ├── decisions\
│   │   ├── categories\
│   │   │   └── random_world_decision_categories.txt  ← the "Random World" decisions folder
│   │   └── random_world_decisions.txt      ← the "Randomize the World!" button
│   ├── on_actions\
│   │   └── ZZ_random_world_on_actions.txt  ← hooks: ban factions at start + weekly
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
to their historic homes through three numbers. The defaults are correct for
the vanilla map as we know it, but Paradox occasionally re-splits states
between patches — so verify once. The good news: since the custom countries
now have visible borders on the starting map, a wrong ID is impossible to
miss — the country simply sits in the wrong place.

**The 2-minute check, inside the game:**

1. Enable the mod (Step 5 below), start any new game, and once on the map
   press **`** / **~** (the key under Esc) to open the console.
2. Type `tdebug` and press Enter.
3. Hover the mouse over **Vinnytsia / Khmelnytskyi area (western Ukraine)** —
   a tooltip appears; read **STATE ID**. Expected: **196** (Nesterivtsi).
4. Hover just south of it, across the Dniester river (**Khotyn / northern
   Bessarabia**). Expected: **78** (Kamianets — see the note below).
5. Hover over **Kharkiv (eastern Ukraine)**. Expected: **198**.
6. Type `tdebug` again to turn the tooltip off.

If a number differs, change it in **two places** (both are commented):

- `random_world\common\scripted_effects\random_world_scripted_effects.txt`,
  block `THE ONLY NUMBERS YOU MAY NEED TO EDIT` (section 5) — the
  `NES` / `KAM` / `KHA` lines;
- that country's file in `history\countries\` — the three lines
  `capital = X`, `transfer_state = X`, `add_state_core = X`.

> **Why is Kamianets on 78 and not 196?** Both real places (Nesterivtsi and
> Kamianets-Podilskyi) lie inside one and the same vanilla state, 196 — and
> one state can only have one owner on the starting map. So Nesterivtsi
> keeps 196, and Kamianets starts on the nearest neighboring state: Khotyn /
> northern Bessarabia (78), directly across the Dniester from the real
> Kamianets-Podilskyi. If your game version has a separate
> "Kamenets-Podolsk" state, give KAM that ID instead — then both sit
> perfectly.

## Part 6 — Step 5: Turn it on and test

1. Launcher → **Playsets**: add *Random World - No Factions* to your playset
   and tick it. (Achievements will be disabled — normal for any mod.)
2. **New Game.** First proof the mod is loaded: there is **only one
   scenario — 1936** (no 1939 card), and the Select Country screen shows
   **no major portraits**, only **"Other countries"**.
3. Continue to the map lobby. It shows the normal 1936 world plus the
   three custom countries on their homes — pick any country and press
   **START**.
4. In-game, open the **Decisions** panel: the category **"Random World"**
   with the decision **"Randomize the World!"** must be there. *(This
   doubles as the mod-loaded check: no category = mod not active.)* Press
   it whenever you like — it is free. The game freezes for a few seconds
   while the script divides the planet, and then: a patchwork world, no
   grey/unowned land, every country a random ideology, the custom
   countries somewhere random too. Because this runs in-session, **every
   campaign gives a different world**.
5. Sanity checks: the diplomacy screen offers no faction actions; open any
   state — building **slots** and **population** are vanilla; built
   factories are re-rolled with a floor of **2 civilian + 2 military** per
   state. The decision and its category disappear after use and never
   return in this campaign, not even after save/load.
6. **Optional alternative — generate the world before country selection**
   (useful for multiplayer, where everyone picks on the finished map):
   uncomment the marked five-line block in
   `common\bookmarks\the_gathering_storm.txt`. Engine trade-off: at that
   moment the random generator is deterministic, so the world is fixed by
   the number in `common\scripted_effects\rw_world_seed.txt` — same number
   = same world (a feature for MP sync and replays), new world = new
   number **+ full HOI4 restart** (the game reads mod files only at
   launch). `randomize_seed_and_play.bat` in the mod root automates that:
   run it while the game is closed and it writes a random seed and starts
   HOI4 for you.

**Where the logs are** (your best friends when something is off):
`Documents\Paradox Interactive\Hearts of Iron IV\logs\` —
`game.log` (the script prints `[RW] ...` progress lines there) and
`error.log` (loading problems, typos, wrong effect names).

---

## Part 7 — How the world generator actually works (plain words)

Everything lives in `random_world_scripted_effects.txt` (heavily commented);
this is the same story without code. The **faction ban** (step 1) runs by
itself every time a session starts. Steps 2–11 run once per campaign when
you press the **"Randomize the World!"** decision — in-session, where the
random generator is fresh every time, hence a different world per campaign.
(The optional lobby-time trigger in `common/bookmarks/` runs the same steps
during scenario setup instead; there the generator is deterministic, and
the script first "burns" as many throwaway draws as `rw_world_seed.txt`
says, which is how the seed number selects the world.) Separately, the
three custom countries receive their home states during map setup via
their `history/countries` files — that ownership is what brings them into
existence so the reshuffle can include them in the pool.

1. **Ban factions.** Whoever leads a faction dismantles it; then every
   country gets two permanent "country rules" that grey out *Create Faction*
   and *Join Faction*. A weekly hook re-applies the rules so countries born
   later (civil wars, released nations) are covered forever.
2. **Clean the table.** All puppets are freed, all running wars are ended in
   white peace, and then **every land division of every country is
   deleted** — equipment included. Nobody drags a vanilla army (or the
   stockpile from disbanding one) into the new world; everyone rebuilds
   from their new, equalized factories on equal footing. Navies and air
   wings are relocated to owned bases by the engine automatically.
3. **Count the map.** The script counts every land state (that number ÷
   number of countries = the **target size** everyone should reach).
4. **(Optional) seed the custom countries** on their home states. **Off by
   default** — NES/KAM/KHA drop through to the common lottery in step 6 and
   can end up anywhere, like everyone else. Flip one switch (below) to
   anchor them at their historic homes instead.
5. **Build "the pool"**: the list of every country alive in 1936 plus the
   three customs. Each pool country also secretly *protects* one of its
   current states — random seeds may not land there. This guarantees no
   country is accidentally wiped off the map before it received its own seed
   (the classic bug of naive randomizers: someone's seed lands on
   Luxembourg's only state and Luxembourg silently stops existing).
6. **Random seeds for everyone else, spread apart.** Every pool country gets
   one random free, non-protected, non-wasteland state — its new "starting
   point". To avoid ugly shapes later, the seeder first looks for spots with
   **two full rings of unclaimed neighbors** around them, then one ring,
   then anywhere — countries that start far apart can grow into round blobs
   before they collide.
7. **Growth, round by round** *(the balance mechanism)*: all countries take
   turns; on its turn a country below the target size claims **one** free
   state **touching** its territory. Repeat rounds until a whole round
   changes nothing. Because everyone adds at most one state per round, sizes
   stay nearly equal for as long as geography allows. Each grab prefers, in
   order: **sealing holes** (free states already surrounded by claimed land)
   → **uncontested land** (free states touching no other country's claims)
   → anything adjacent. That anti-snake ordering is what keeps countries
   compact instead of stretched along corridors.
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

**Tuning switch — anchor the custom countries at home.** By default
NES/KAM/KHA are thrown into the same lottery as everyone and their historic
homes only exist as starting borders on the brief pre-reshuffle map. If you
want them to *stay and grow from* their historic homes during the reshuffle,
open `random_world_scripted_effects.txt`, find `rw_seed_custom_countries`
(section 5) and change `set_variable = { global.rw_use_historic_homes = 0 }`
to `= 1`. Independently, removing the `transfer_state` / `add_state_core`
lines in their `history/countries` files removes their pre-reshuffle
starting borders.

## Part 7.5 — The start-buff system (imported from `fand1l/hoi4_rcpZ_mod`)

The mod also contains the complete "choose your nation's buffs" system
ported from the author's other mod. How it plays:

1. About a day after a campaign starts, a hidden bootstrap event opens a
   chooser for the human player: **who gets to pick buffs** — everyone /
   minors only / only me / everyone but me (AI countries pick their paths
   automatically via weighted chances; a follow-up question can hand a
   special tech to AI puppet nations).
2. Each participating country then gets **"History of Our Nation"** — the
   branching event: *great history / ordinary / wronged / full random /
   a secret path* — and the follow-up choices grant **national spirits**
   (the buffs), free units, techs or bonuses depending on the path.
3. The Decisions panel gains the imported **UGN category** with: a button
   to re-open the selection event, a button to grant selection to your
   puppets, and the whole chain of later "upgrade" decisions that swap
   weaker spirits for stronger ones over time (industrialise farmers,
   equip/train the army, uproot corruption, …).
4. Everything the branches reference came along: ideas + icons, event
   pictures, custom traits, the handful of custom techs/units some silly
   branches use (flame cavalry and friends), localisation.

Interaction with the world reshuffle: buff **spirits** survive it fine, but
since v2.1 the reshuffle **deletes every division on the map** — including
free divisions a buff path may have just spawned. Recommended order
therefore: press **"Randomize the World!" first**, pick your buff paths
after. (Two equalizations were also applied to the imported events for the
random-map context: the AI-chance bias favoring vanilla majors and the
majors-exception on the *destined greatness* roll are gone — everyone has
equal chances.)

**IMPORTANT:** disable the original rcpZ/UGN mod in your playset once this
version is installed. Running both at once duplicates every event, idea and
decision (log spam, double events).

## Part 8 — Which file does what (one line each)

| File | Purpose |
|---|---|
| `descriptor.mod` | Mod's ID card for the launcher (name, game version). |
| `common/country_tags/01_random_world_tags.txt` | "NES, KAM, KHA exist." |
| `common/countries/*.txt` | Per country: unit-art style + fallback color. |
| `common/countries/colors.txt` | Map colors — **you** build it in Step 3. |
| `common/bookmarks/the_gathering_storm.txt` | Overrides the 1936 scenario: removes the featured majors; also holds the optional (disabled) lobby-time randomizer trigger. |
| `common/bookmarks/blitzkrieg.txt` | Deliberately empty: erases the 1939 scenario from New Game. |
| `common/decisions/categories/…` | The "Random World" folder in the Decisions panel. |
| `common/decisions/random_world_decisions.txt` | **The trigger:** one-shot, free "Randomize the World!" button (player-only; AI never presses it). |
| `common/on_actions/ZZ_random_world_on_actions.txt` | "At every session start ban factions; every week re-ban them." |
| `common/scripted_effects/random_world_scripted_effects.txt` | The entire algorithm (sections 0–12, commented). |
| `common/scripted_effects/rw_world_seed.txt` | The one number that selects **which** world is generated — edit for a new world, keep to replay one. |
| `randomize_seed_and_play.bat` (mod root) | One-click helper for the optional lobby mode: writes a random seed and starts HOI4. Run it while the game is closed. |
| `events/ugn_events.txt`, `common/ideas/ugn_*` + `vanilla_ideas.txt`, `common/decisions/*ugn*`, `common/technologies*/ugn_*`, `common/units/…`, `common/country_leader/ugn_traits.txt`, `interface/ugn_*.gfx`, `gfx/…` | The imported start-buff system (Part 7.5) — self-contained, prefix `ugn_`/`uniqueness`. |
| `history/countries/TAG - Name.txt` | Custom country's 1936 setup: capital, **its starting borders** (`transfer_state` + `add_state_core`), techs, politics, equipment. |
| `history/units/TAG_1936.txt` | Its division blueprint (so it can train troops immediately). |
| `localisation/english/random_world_l_english.yml` | The names: 4 ideology names per custom country. **Must stay UTF-8 with BOM** (it already is; editors keep it if you just edit and save). |
| `gfx/flags/…` | Placeholder flags, 3 sizes × 5 variants per tag. |
| `tools/generate_flags.py` (repo only) | The script that generated those flags — rerun after editing colors in it, or just replace the TGAs with real art. |

## Part 9 — Troubleshooting

| Symptom | Cause & fix |
|---|---|
| Mod not in the launcher | The folder isn't at `...\Hearts of Iron IV\mod\random_world`, or `random_world.mod` (launcher side) is missing — redo Part 2, or use `docs/random_world.mod.example`. |
| **Mod seems to have no effect in-game** (no custom countries on the map, no "Random World" decision) | The mod is not actually loading. Check, in order: (1) it is **ticked in the active playset** (top of the launcher — the playset selected there is what launches); (2) the folder is exactly `mod\random_world` with `descriptor.mod` **directly** inside it — a very common mistake is a nested `mod\random_world\random_world\…`; (3) you started a **new** game, not an old save from before the mod; (4) `error.log` after launch — a syntax typo can make the game silently drop a file. |
| Decision pressed but nothing changed | Impossible in a loaded mod — but check `game.log` for the `[RW]` lines; if they stop at some phase, `error.log` names the guilty line (see the substitution table below). |
| **Still two scenarios** on New Game, or the majors' portraits are still there | Your game version names its bookmark files differently, so the override didn't attach. Open the **game's** `common\bookmarks\` folder and rename the mod's two files to match the vanilla names exactly. |
| The "Random World" decision category is missing in-game | The mod isn't loading (see the rows above), or the world was already randomized in this campaign — the category hides itself after use. |
| **Pressed the decision, world not randomized** | Run **the 60-second log check** below; it pinpoints the broken link. |
| *(lobby mode only)* The same world appears in every campaign | Expected — setup randomness is deterministic by engine design. Change the number in `common/scripted_effects/rw_world_seed.txt` **and restart HOI4** (mod files are parsed only at application launch), or run `randomize_seed_and_play.bat`. |
| *(lobby mode only)* Changed the seed number but the world stayed the same | You didn't restart HOI4 — the game cannot see file edits made while it is running. Quit to desktop, relaunch, then New Game. |

**The 60-second log check.** Start a new game, reach the map, quit to
desktop. Open `Documents\Paradox Interactive\Hearts of Iron IV\logs\game.log`
and search for `[RW]`:

1. **No `[RW]` lines at all** (not even `on_startup fired`) — the mod is not
   loading, full stop. This is launcher/folder territory: is the mod ticked
   in the **active** playset? Is the folder exactly
   `mod\random_world\descriptor.mod` (not nested twice)? Did the launcher
   re-verify the playset after you replaced files? The custom countries
   missing from the pre-game map is the same disease — they come from plain
   history files and need no scripts at all.
2. **`on_startup fired` present, but no `world randomization: START`** —
   normal **until you press the decision**. If you DID press it and START
   is still missing, check `error.log` for
   `Invalid Scope ... provided: None` on the calling line — a
   scripted-effect call sitting in a scope-less context must be wrapped in
   `random_country = { ... }` (decisions run in country scope, so the stock
   decision never hits this; it can only appear if you moved the call).
3. **`START` present but no `DONE`** — the script died mid-way on a keyword
   your game version spells differently; `error.log` names the exact file
   and line. Fix it with the substitution table below.
4. **`START` and `DONE` present but the map looks vanilla** — the claims
   loop ran but the actual ownership transfer is failing silently; apply
   the `transfer_state = PREV` row of the substitution table.
| Countries turned grey on the map | Your `colors.txt` copy is broken — redo Part 4 (copy vanilla file again, paste snippet at the very bottom, nothing else changed). |
| Checkerboard instead of a flag | A `.tga` is missing/renamed in `gfx/flags` (all three sizes must exist). |
| `NES`/`KAM`/`KHA` show as raw text instead of names | Localisation file lost its BOM or the `english` folder name is wrong. Re-copy `random_world_l_english.yml` from this repo. |
| Custom countries visible but in the wrong place | Home-state IDs differ on your game version — do Part 5 and fix the numbers in both files. |
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
| `all_neighbor_state` unknown trigger | delete the whole "Tier 1" `random_state` block in `rw_capped_growth` (hole-sealing is a shape optimization; Tiers 2–3 still cover everything) |
| `white_peace = PREV` | `white_peace = { tag = PREV }` |
| `Invalid Scope ..., provided: None` on a `rw_...` call | The call site has no active scope (bookmark `effect`, `on_startup`). Wrap the call: `random_country = { rw_... = yes }` — already done in v1.5 for both stock call sites. |
| `delete_units` unknown effect (older patches) | In `rw_delete_all_armies`, try `delete_units = { disband = yes }`; if the effect itself is missing, delete the `rw_delete_all_armies = yes` line in the master switch — armies then survive the reshuffle (they teleport home) and only this equalization is lost. |

## Part 10 — FAQ and honest limitations

- **Achievements** are disabled with any mod. Nothing to do about it.
- **You pick your country first; the world transforms when you press the
  decision.** The classic bookmark screen with major portraits is gone
  (only "Other countries" remains), and the 1939 scenario is removed.
  Every campaign's reshuffle is fresh. If you'd rather pick countries on
  the finished map (e.g. multiplayer), enable the lobby-time trigger —
  Part 6, item 6 — and accept its fixed-seed determinism.
- **All land divisions are deleted at randomization** — deliberately, for
  equal chances: no army may keep standing in what became foreign land,
  and the old majors may not carry their huge forces into the new world.
  Everyone (including you) rebuilds from scratch. Fleets and air wings are
  not deleted; the engine relocates them to owned bases.
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
4. `history/countries/LVI - Lviv.txt`: copy the NES file; set Lviv's state
   ID (find it with `tdebug`) on all three lines — `capital`,
   `transfer_state`, `add_state_core` — so Lviv has borders on the starting
   map; replace `NES` with `LVI`.
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
