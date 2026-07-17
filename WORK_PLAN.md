# Work Plan — "Random World – No Factions" (Hearts of Iron IV 1.19 mod)

This is the plan we follow to build the mod. Each milestone is small, has a
clear "done when…" check, and builds on the previous one. If you only read one
file in this repository, read `GUIDE.md` — it walks through every step below
as if you had never modded before. This file is the map; the guide is the road.

---

## 1. What we are building (goal recap)

One mod for **vanilla Hearts of Iron IV 1.19** that does all of this at the
start of every new game:

1. **No factions, ever.** No country — player or AI — can create or join a
   faction. Existing 1936 factions (the Comintern) are dismantled on day 1.
2. **Three custom countries** exist alongside every vanilla country and use the
   **generic focus tree** (that happens automatically when a country has no
   custom tree):
   | Tag | Country | Historic home |
   |-----|---------|---------------|
   | `NES` | Nesterivtsi | Podillia, Ukraine |
   | `KAM` | Kamianets | southern Khmelnytskyi region, Ukraine |
   | `KHA` | Kharkiv | Kharkiv region, Ukraine |
   Each has 4 ideology-dependent names (e.g. *Nesterivtsi Reich*,
   *Communist Nesterivtsi*, …) exactly as specified.
3. **Global world randomization**, run once from `on_startup`:
   - Every **existing** country (vanilla + custom) gets a **seed state**.
     Vanilla countries seed at a completely random state; the custom countries
     seed at their **historic home states** (per request).
   - From the seed, territory **grows into adjacent land states**, all
     countries taking turns (round-robin), until **every state on the map is
     owned** — no gaps.
   - Countries come out **roughly the same size** (state count within about
     ±1–2 of the average; islands and dead-ends cause small deviations).
   - Islands are the exception to the land-adjacency rule: whatever cannot be
     reached by land at the end is handed to the currently **smallest**
     countries.
   - Every country gets a **random ideology** (25% each: fascism, communism,
     democratic, neutrality) with matching popularity numbers.
   - Every state gets **re-rolled built industry**: civilian factories,
     military factories, and (coastal only) naval dockyards.
   - **Forbidden and respected:** we never touch building-slot limits
     (state categories) and never touch state population. Both stay vanilla.

Out of scope (possible later extensions): custom leaders/portraits, custom
focus trees, a lobby game-rule to toggle the randomizer, resource
randomization, randomizing air bases/infrastructure.

---

## 2. Deliverables in this repository

```
WORK_PLAN.md                  ← this plan
GUIDE.md                      ← step-by-step beginner guide (start here)
README.md                     ← short overview + quick install
random_world/                 ← THE MOD — copy this folder into the game's mod dir
tools/generate_flags.py       ← script that generated the placeholder flags
```

---

## 3. Milestones

### M0 — Tooling and empty mod skeleton
**Tasks:** install/verify game 1.19 + Paradox launcher; pick a text editor
(VS Code or Notepad++); create a local mod named `random_world` with the
launcher; understand `descriptor.mod`.
**Done when:** the empty mod shows up in the launcher's playset and the game
still starts.

### M1 — Disable factions
**Tasks:** scripted effect that (a) dismantles every existing faction at start,
(b) sets the country rules `can_create_factions = no` and
`can_join_factions = no` for **every** country; re-apply the rules weekly via
`on_weekly` so countries born later (civil wars, released nations) are covered
too.
**Done when:** in 1936 the Comintern is gone, the "Create Faction" /
"Join Faction" diplomacy buttons are disabled for everyone, and the AI never
forms a faction in a multi-year observer test.

### M2 — Custom countries NES / KAM / KHA
**Tasks:** tag definitions (`common/country_tags`), country files
(`common/countries`), color entries (append to a copy of vanilla
`colors.txt` — manual step, documented), placeholder flags in all 3 sizes
(generated TGA files), country history files (capital, techs, starting
politics), OOB files with a basic infantry division template, localisation
with the 4 ideology names each (UTF-8-BOM `.yml`).
**Done when:** in-game console `tag NES` works, names change with ideology,
no missing-flag checkerboards, no `error.log` entries for the three tags.

### M3 — Randomizer skeleton
**Tasks:** `on_startup` entry in `common/on_actions` guarded by a global flag
(so it runs exactly once per campaign and never again on save-load); master
scripted effect `rw_randomize_world` that calls empty phase stubs; `log`
lines for every phase so progress is visible in `game.log`.
**Done when:** starting a new game writes the `[RW]` log lines once, and
loading that save does not re-run anything.

### M4 — Seeding phase
**Tasks:** free all subjects and white-peace all 1936 wars (so territory moves
cleanly); count all states into `global.rw_total_states`; seed the three
custom countries at their home states **first** (with fallback to an adjacent
free state if two homes collide, e.g. NES and KAM sit in the same vanilla
state); build the country pool (array of every existing country); **protect
one owned state per pool country** so no country can be wiped out by other
countries' seeds before receiving its own (this is the subtle bug the naive
version has); give every remaining pool country one random free seed state;
compute `global.rw_target_size = total states ÷ pool size`.
**Done when:** log shows pool size ≥ number of 1936 countries + 3, and every
pool country owns exactly 1 state (its seed) plus leftovers of its original
territory awaiting capture.

### M5 — Growth, full coverage, islands
**Tasks:** three loops.
1. **Capped round-robin growth:** repeat rounds; in each round every country
   below `rw_target_size` claims **one** free state adjacent to its claimed
   territory. Stop when nothing changed in a full round (everyone capped or
   walled in).
2. **Overflow growth:** same loop without the size cap — mops up free states
   that are only reachable by countries already at the cap (enclaves).
3. **Island assignment:** while free states remain (unreachable by land),
   give one to the currently **smallest** country as a beachhead, then rerun
   overflow growth so the rest of that island chain fills up; repeat.
**Done when:** after start, **zero** unowned states exist anywhere (checked
with the map modes / console), and state counts per country are within a
couple of states of the target in a log check.

### M6 — Politics randomization
**Tasks:** per pool country, `random_list` 25/25/25/25 →
`set_politics` + `set_popularities` (ruling party ~60%, rest split;
democracies get elections on).
**Done when:** ideology map mode shows a roughly even 4-color mix across
many restarts.

### M7 — Industry randomization
**Tasks:** per state, weighted `random_list` → `set_building_level` for
`industrial_complex` (0–8), `arms_factory` (0–6), and `dockyard` (0–5, coastal
states only). **No** changes to state category, building slots, manpower.
**Done when:** factory counts differ run-to-run; opening any state shows
vanilla slot count and vanilla population.

### M8 — Finalization, polish, full test pass
**Tasks:** set each country's capital to its seed state; give every country
cores on everything it owns and remove its cores on states it does not own
(clean, resistance-free start); final test checklist (below); write
`GUIDE.md` troubleshooting from anything we hit.
**Done when:** the full checklist passes.

---

## 4. Test checklist (run after M8, and after any change)

1. New game, 1936, pick any major — game reaches the map without crash.
2. `game.log` contains `[RW] world randomization: START` … `DONE` exactly once.
3. `error.log` has no lines mentioning `rw_`, `NES`, `KAM`, `KHA`.
4. Political map: world is a patchwork; **no grey unowned states**.
5. NES/KAM/KHA exist, sit on/next to their Ukrainian homes, correct names.
6. Ideology map mode: mix of all 4 colors.
7. Open several states: factories differ from vanilla; slots + population vanilla.
8. Diplomacy of any country: faction actions unavailable; no faction exists.
9. Save, quit, reload: world unchanged (randomizer did NOT run again).
10. Observer run (`observe`) for 2+ game years: AI never creates a faction.

---

## 5. Known risks and how the plan handles them

| Risk | Mitigation |
|------|------------|
| **State IDs for the Ukrainian homes vary by game version** (the Soviet map was re-split in later DLC patches) | Home IDs are 3 clearly-marked constants in one file; guide has a 2-minute recipe (console `tdebug`, or search the game's `history/states` files) to verify/fix them. Wrong-but-valid IDs cannot crash the script — worst case a country seeds elsewhere. |
| **Two custom homes in the same vanilla state** (Nesterivtsi and Kamianets are both in the Podillia area) | Seeding has an explicit collision fallback: home taken → adjacent free state → any free state. |
| **A small country could be annexed mid-seeding when someone's random seed lands on its only state** → it would silently vanish from the pool | The "protected state" step in M4 exists precisely for this; seeds may not take protected states. |
| **`colors.txt` fully replaces the vanilla file** | We do NOT ship `colors.txt`. The guide has a required manual step: copy the vanilla file into the mod, append our 3 entries (snippet provided in `random_world/docs/`). |
| **Exact syntax of a few effects differs between patches** (`transfer_state = PREV`, `set_building_level`, `while_loop_effect`) | Every risky construct is isolated in one small helper effect, and the guide's troubleshooting table lists the drop-in alternative for each. `error.log` pinpoints the line if a name is wrong. |
| **Runaway loops** | Every `while_loop_effect` has a hard safety counter in its limit. |
| **Startup lag** | All work is one-time at day 1; a few seconds on weak PCs is expected and documented. |
| **Units standing in transferred states** | Engine auto-relocates them; documented as harmless day-1 weirdness. |

---

## 6. Order of implementation in this repo

1. Commit 1 — this plan.
2. Commit 2 — full mod (`random_world/`), flag generator + generated flags,
   `GUIDE.md`, `README.md`.

---

## 7. Follow-up changes (v1.1)

Requested after the first release:

1. **Activation moved from `on_startup` to a decision.** The world reshuffle
   is now fired manually: Decisions panel → category *Random World* →
   one-shot, zero-cost decision **"Randomize the World!"** (`ai_will_do = 0`,
   so only a human can press it; the global flag keeps it once-per-campaign).
   `on_startup` now only enforces the faction ban (idempotent, unguarded).
   Side benefit: the decision doubles as a "is the mod loaded?" indicator —
   the original complaint was that the mod showed no visible effect.
2. **Custom countries have borders on the initial map.** Their
   `history/countries` files now `transfer_state` + `add_state_core` their
   home states during map setup, so NES/KAM/KHA are visible and selectable
   in the lobby before any randomization. Because Nesterivtsi and
   Kamianets-Podilskyi share one vanilla state (196) and a state has exactly
   one owner, KAM's default home moved to the adjacent state 78
   (Khotyn / northern Bessarabia, across the Dniester from the real
   Kamianets); documented in both files with a note to use a dedicated
   Kamenets-Podolsk state id if the installed version has one.
   The randomizer's dynamic collision fallback remains as a safety net, and
   `rw_build_pool` was simplified: customs now exist before pool building,
   so the special-case size bookkeeping was deleted.

---

## 8. Follow-up changes (v1.2)

Requested after play-testing the reshuffle:

1. **Historic-homes switch.** `global.rw_use_historic_homes` (top of
   `rw_seed_custom_countries`, default `1`) — set to `0` to give the custom
   countries fully random seeds like everyone else. Keeping them at home was
   the original spec; the play-tester was surprised by it, so it is now an
   explicit, documented one-number choice.
2. **Seed spacing.** Random seeds now try to land with two full rings of
   unclaimed neighbors, then one ring, then anywhere. Adjacent seeds were a
   main cause of countries squeezing into corridors.
3. **Anti-snake growth tiers.** Each growth turn now prefers: seal
   fully-enclosed holes → grow into land touching no other country's claims
   → any adjacent free state. Combined with seed spacing this produces
   compact blobs instead of the elongated "snake" countries observed on the
   first play-test map.

---

## 9. Follow-up changes (v1.3)

Clarified intent: historic homes were meant for the PRE-randomization map
only, and the reshuffle should happen before country selection.

1. **Custom countries fully random by default.**
   `global.rw_use_historic_homes` now defaults to `0`: NES/KAM/KHA enter the
   common seed lottery. Their historic homes remain as starting borders on
   the pre-reshuffle map (history files unchanged); setting the switch back
   to `1` re-anchors them during the reshuffle.
2. **Randomization moved to scenario load.** The vanilla 1936 bookmark file
   is overridden: no featured majors (only "Other countries"), and its
   `effect` block — the same place vanilla runs `randomize_weather` — fires
   the world reshuffle, so the map lobby where the player picks a country
   is already randomized. Known caveat (documented): the exact moment the
   engine runs bookmark effects is version-dependent; worst case the
   reshuffle lands right after pressing Play.
3. **1939 scenario removed** via an intentionally empty `blitzkrieg.txt`
   override, leaving 1936 as the only New Game choice.
4. **The decision is now a dormant fallback**: it only appears if the
   bookmark override failed to attach (e.g. renamed vanilla files), since
   the global flag that hides it is set by the bookmark effect.

---

## 10. Follow-up changes (v1.4)

Play-test report: world randomized neither in the lobby nor after starting,
and the screenshots also showed no custom countries on the pre-game map
(a script-free history feature) — i.e. the mod likely did not load in that
session at all. Two fixes regardless:

1. **Fixed a real v1.3 flaw.** The bookmark effect set the "already
   randomized" flag BEFORE calling the reshuffle; if the call itself was
   inert in that context, the flag still hid the fallback decision, leaving
   no path to randomize. The flag is now set inside `rw_randomize_world`
   itself — only when the reshuffle really starts.
2. **Three-layer trigger chain**, all guarded by that flag: bookmark
   `effect` (before the lobby — best case) → `on_startup` (right after
   pressing Play) → the manual decision (last resort, visible only while
   the flag is unset). The earliest layer that works on the installed
   engine build wins; later layers no-op.
3. **`on_startup` now always logs** `[RW] on_startup fired` — the
   definitive "is the mod loaded at all?" probe.
4. GUIDE: added "The 60-second log check" diagnostic ladder.

---

## 11. Follow-up changes (v1.5)

The play-tester's logs found the real blocker, and disproved the "mod not
loaded" hypothesis from v1.4 (the mod loaded fine; the custom countries were
on the map all along):

```
common/bookmarks/the_gathering_storm.txt:43: rw_randomize_world:
  Invalid Scope, supported: State|Country|..., provided: None
common/on_actions/ZZ_random_world_on_actions.txt:32/35: same
```

1. **Root cause:** the engine refuses to invoke *scripted effects* from
   scope-less contexts — and both automatic triggers (bookmark `effect`,
   `on_startup`) run with scope "None". Plain effects (`log`,
   `randomize_weather`, listers) work there; custom scripted effects do not.
   This also explains why the v1.1 decision-based trigger worked: decisions
   execute in the player country's scope.
2. **Fix:** both call sites now wrap the calls in `random_country = { ... }`
   — entering an arbitrary existing country's scope. The reshuffle operates
   on the whole world via global listers, so the host country is irrelevant.
3. **Confirmed by timestamps:** on the tester's build the bookmark effect
   executes at scenario setup, several seconds *before* the map lobby opens
   — so with the scope fix, picking a country on an already-randomized map
   works as designed.
4. GUIDE: log-check ladder and substitution table updated with the
   "Invalid Scope / provided: None" case.

---

## 12. Follow-up changes (v1.6)

Play-test: the reshuffle finally ran — but every New Game produced the
IDENTICAL randomized world.

1. **Root cause:** during scenario setup the engine seeds its random
   generator with a fixed value (the same reason vanilla hardcodes
   `randomize_weather = 22345`), so any randomness consumed at bookmark-
   effect time repeats deterministically each campaign. Randomness consumed
   *inside* the session (after Play) is seeded fresh per launch — which is
   why the earlier decision-triggered runs varied.
2. **New default:** the reshuffle fires from `on_startup` (right after
   pressing Play) → a genuinely fresh world every New Game. The player
   picks a country on the pre-reshuffle lobby map.
3. **Lobby-time mode kept as an explicit opt-in:** the bookmark-effect call
   remains in `the_gathering_storm.txt`, commented out, with the trade-off
   documented inline ("world visible in the lobby" ⟷ "identical world
   every campaign"). The two properties are mutually exclusive at engine
   level.
4. GUIDE: intro, Part 6 flow, Part 7, FAQ and troubleshooting updated with
   the trade-off; new troubleshooting row for "same world every campaign".
