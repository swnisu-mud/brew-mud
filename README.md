# BrewMUD

BrewMUD is a quest-driven multiplayer text world about the biochemistry of beer. Students move through a working maltings, brewhouse, fermentation cellar, hop yard, packaging floor, and quality wing while diagnosing process failures for brewers, yeast, enzymes, metabolites, and other characters.

This first playable build is based on the instructor's BBMB 1200 lecture material (with the history lecture intentionally omitted). It includes:

- 90 connected rooms and nine compact regional maps
- 111 NPCs, including brewery staff, enzymes, yeast, ions, proteins, and flavor molecules
- 16 non-combat quests containing 101 objectives
- one active quest at a time in a sequential, prerequisite-based quest line
- 39 delayed, randomized pop quizzes about previously visited material
- randomized answer positions, bare `A`/`B`/`C`/`D` answers, quiz pausing, review routes, and an incorrect-answer penalty
- six progression ranks based on exploration, quests, and knowledge checks
- browser-based multiplayer presence and local room chat
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

Allow TCP port 8000 through the computer's firewall if prompted, then share `http://YOUR-LAPTOP-IP:8000`. Local accounts are stored in `brewmud.db`, but this development server does not provide TLS or moderation and should not be exposed directly to the public internet.

The solo terminal interface is also available:

```bash
python3 -m brewmud
```

At the `command>` prompt, begin with:

```text
talk coordinator
journal
hint
map
```

## Commands

`LOOK`, `TALK`, compass directions or `GO`, `JOURNAL`, `HINT`, `MAP`, `NOTES`, `STATUS`, `QUIZ`, `PAUSE`, `A`–`D`, and `QUIT` work in solo and browser play. Browser sessions also add local `SAY`, `WHO`, and a two-step `RESTART` command for resetting personal progress; account progress saves automatically. Following and private group chat are retained internally as an experimental mode but disabled in the student study-guide version. The solo terminal additionally supports file-based `SAVE` and `LOAD`.

Quest NPCs announce problems in first-arrival dialogue. The assignments unlock sequentially, and each player can have only one active quest. `JOURNAL` records the current assignment and next available lead; `HINT` calculates a shortest route to the objective.

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
- `brewmud/server.py` — shared multiplayer presence and chat, plus disabled experimental following code
- `brewmud/static/` — browser interface
- `tests/test_game.py` — content, engine, and multiplayer checks

The quest format is deliberately declarative: new quest lines can be added without changing the command engine.

## Student materials

- `docs/BrewMUD_Student_Information_Sheet.docx` introduces the game, commands, quests, quizzes, and regional maps.
- `docs/BBMB_1200_First_Test_Study_Guide.docx` is a conventional study guide covering the same first-test content, with review questions and explanatory answers.
- Editable Markdown sources for both documents are stored beside the Word files in `docs/`.

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

The Blueprint selects Render's smallest paid compute plan and attaches a 1 GB persistent disk at `/var/data`. Browser accounts are stored in `/var/data/brewmud.db` so they survive service restarts and deployments.

### Instructor progress

Set `BREWMUD_ADMIN_PASSWORD` to a strong, unique value in the Render service's **Environment** page. Then visit `/instructor` on the deployed BrewMUD site and enter that password. The read-only dashboard shows each account's rank, Insight, locations explored, quests completed, knowledge checks completed, next rank, and last activity. It refreshes every 30 seconds while open. Students should report their player-chosen account names if the dashboard will be used for extra credit.

Player presence and chat remain in server memory, so a restart or redeploy disconnects current players. Account progress survives. Password reset and moderation are not included in this first account version.
