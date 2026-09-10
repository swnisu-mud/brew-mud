# BrewMUD

BrewMUD is a quest-driven multiplayer text world about the biochemistry of beer. Students move through a working maltings, brewhouse, fermentation cellar, hop yard, packaging floor, and quality wing while diagnosing process failures for brewers, yeast, enzymes, metabolites, and other characters.

This first playable build is based on the instructor's BBMB 1200 lecture material (with the history lecture intentionally omitted). It includes:

- 70 connected rooms and seven compact regional maps
- 85 NPCs, including brewery staff, enzymes, yeast, ions, proteins, and flavor molecules
- 14 non-combat quests containing 72 objectives
- several simultaneous active quests in each player's journal
- 19 delayed, randomized pop quizzes about previously visited material
- randomized answer positions, bare `A`/`B`/`C`/`D` answers, quiz pausing, review routes, and an incorrect-answer penalty
- six progression ranks based on exploration, quests, and knowledge checks
- browser-based multiplayer chat, presence, and player following
- synchronized group quiz topics with separately shuffled answers for discussion
- first-arrival NPC chatter, colored semantic output, and quiz sound/screen flash

## Run it on this laptop

Python 3.10 or newer is recommended. From the `brew-mud` directory:

```bash
python3 -m brewmud.web
```

Open <http://127.0.0.1:8000>. Use a second browser or private window with another player name to test multiplayer.

To let trusted devices on the same local network connect:

```bash
python3 -m brewmud.web --host 0.0.0.0
```

Allow TCP port 8000 through the computer's firewall if prompted, then share `http://YOUR-LAPTOP-IP:8000`. This development server does not provide accounts, TLS, durable server-side saves, or moderation and should not be exposed directly to the public internet.

The solo terminal interface is also available:

```bash
python3 -m brewmud
```

At the `brew>` prompt, begin with:

```text
talk coordinator
journal
hint
map
```

## Commands

`LOOK`, `TALK`, compass directions or `GO`, `JOURNAL`, `HINT`, `MAP`, `NOTES`, `STATUS`, `QUIZ`, `PAUSE`, `A`–`D`, `SAVE`, `LOAD`, and `QUIT` work in solo and browser play. Browser sessions also add `SAY`, `WHO`, `FOLLOW`, and `UNFOLLOW`.

Quest NPCs announce problems in first-arrival dialogue. Talking to a quest giver starts the quest, and a player can keep several active objectives at once. `JOURNAL` records active and discovered work; `HINT` calculates a shortest route to every active objective.

## Run the tests

```bash
python3 -m unittest discover -s tests -v
```

The test suite checks all room connections, NPC/quest references, a full playthrough of all quests, map coverage, quiz behavior, save/load, and core multiplayer behavior.

## Install as editable commands (optional)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
brew-mud-web
```

On Windows PowerShell, activate the environment with `.venv\Scripts\Activate.ps1`.

## Project layout

- `brewmud/world.py` — rooms, residents, facts, speech, and connections
- `brewmud/quests.py` — data-driven quest definitions
- `brewmud/quizzes.py` — knowledge checks and explanations
- `brewmud/game.py` — commands and per-player state
- `brewmud/server.py` — shared multiplayer presence, chat, and following
- `brewmud/static/` — browser interface
- `tests/test_game.py` — content, engine, and multiplayer checks

The quest format is deliberately declarative: new quest lines can be added without changing the command engine.

## Publishing

The local repository is configured with:

```text
https://github.com/swnisu-mud/brew-mud.git
```

GitHub stores the code; hosting the running multiplayer application is a separate deployment step. The included `render.yaml` configures a Render web service from this repository.

### Deploy on Render

1. Sign in at <https://dashboard.render.com> using GitHub.
2. Choose **New > Blueprint** and connect `swnisu-mud/brew-mud`.
3. Accept the detected `render.yaml` configuration and deploy.
4. Open the generated `https://...onrender.com` address.

The Render start command is `python -m brewmud.web --host 0.0.0.0`. The public bind address is required by Render; local runs remain bound to `127.0.0.1` by default.

The Blueprint initially selects Render's free compute plan. Free services sleep after inactivity, so the first visitor may wait while the service wakes. Before classroom use, the service can be upgraded from its **Compute** page to the smallest paid plan without changing BrewMUD's code.

At this prototype stage, player sessions and progression live in server memory. A restart or redeploy disconnects current players and resets their server-side sessions. Durable accounts, a database, instructor controls, and moderation should be added before using the game for graded work.
