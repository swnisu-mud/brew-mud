# BrewMUD Student Information Sheet

## A study guide you can explore

BrewMUD is a substitute for a typical study guide for our material on malting, mashing, and lautering. It is intended to be helpful and, hopefully, somewhat fun—or at least not boring. Instead of reading a list of review questions, you will explore a brewery, speak with its residents, and solve biochemical and brewing problems.

**Questions on the test will come directly from room and object descriptions, conversations with NPCs, and pop quizzes in BrewMUD.** Read the text carefully. Finishing a quest quickly is not as useful as understanding what the rooms, objects, and characters are telling you.

Course link: ________________________________________________

## A very short history of MUDs

*Dungeons & Dragons*, first published in 1974, made it possible for players to take roles in a shared imaginary world and develop their characters through adventures. Early computer-game designers combined ideas from tabletop role-playing with text adventures. In 1978, Roy Trubshaw began **MUD1**—the first Multi-User Dungeon—on a mainframe at the University of Essex; Richard Bartle later continued its development. Players connected to the same persistent, text-described world and typed commands to explore and interact.

MUDs flourished during the 1980s and 1990s, producing families such as DikuMUD, CircleMUD, and Merc. Their shared worlds, online characters, chat, quests, and progression helped establish the basic design of later graphical **massively multiplayer online role-playing games (MMORPGs)**. *World of Warcraft*, released in 2004, presents its world graphically, but many of its underlying ideas would be familiar to a MUD player. BrewMUD returns to that text-based tradition and replaces fantasy combat with biochemical investigation.

*Historical sources: [D&D at 50](https://corp.hasbro.com/news-releases/news-release-details/dungeons-dragons-celebrates-50th-anniversary-2024-more-50), [Richard Bartle's early MUD history](https://mud.co.uk/richard/mudhist.htm), [University of Essex profile of Richard Bartle](https://www.essex.ac.uk/people/BARTL01006/Richard-Bartle), and [Blizzard's World of Warcraft timeline](https://worldofwarcraft.blizzard.com/en-gb/story/timeline/chapter-6).*

## Getting started

1. Open the course link and choose **Create new account**.
2. Choose an account name that you can report to your instructor. Your progress is recorded under that name.
3. Use a password of at least eight characters. Do not reuse your university password or another important password. Password recovery is not currently available.
4. Read the brief instructions shown when you first enter.
5. At the command prompt, type `TALK TRAIN` to speak with the Training Coordinator and begin your first assignment.

Your progress saves automatically after every command. You may log out and return later using the same account.

## How to learn from the game

Each location contains several kinds of information:

- **Room descriptions** explain the brewing operation or biochemical principle associated with that location.
- **Objects and equipment** can be examined with `LOOK object` or the shorter `L object`.
- **Nearby residents (NPCs)** include brewery staff, enzymes, sugars, ions, proteins, and other molecules. Use `LOOK name` to examine one and `TALK name` to hear what it has to say.
- **Quests** place the information in the context of a problem that needs to be solved.
- **Pop quizzes** ask you to recall material from locations you have already visited.

Do not simply run from one objective to the next. Read every new room description, examine interesting objects and residents, and talk to the NPCs you encounter. NPC means **non-player character**—one of the game's residents rather than another student.

## Navigating the brewery

Every room lists its available exits. Commands are not case-sensitive, and most names can be shortened as long as the abbreviation is unambiguous.

| Command | What it does |
|---|---|
| `N`, `S`, `E`, `W` | Move north, south, east, or west |
| `U`, `D` | Move up or down |
| `I`, `O` | Move in or out of a specialized area |
| `GO direction` | Another way to move, such as `GO NORTH` |
| `LOOK` or `L` | Read the current room again |
| `LOOK name` or `L name` | Examine a resident, object, or piece of equipment |
| `MAP` | Display a map of your current region |
| `MAP ALL` | List all regional maps |
| `HINT` | Show the shortest route to your current objective |

Examples of shortened commands:

```text
TALK TRAIN
TALK CUR
L GLUC
```

These work for the Training Coordinator, Carbohydrate Curator, and Glucose. If an abbreviation could mean more than one thing, type a few more letters.

## How quests work

The quests form a sequence through malting, water chemistry, carbohydrate and starch structure, mashing, and lautering. You may explore anywhere, but you can have only one active quest at a time, and later quests unlock after earlier ones are completed.

- `TALK name` starts or advances a quest when that resident is involved.
- The short **Objectives** line in each room reminds you what to do next.
- `JOURNAL` shows your current assignment or explains the next problem that needs attention.
- `HINT` gives directions to the resident needed for the current objective.
- `LEVEL` or `STATUS` shows your Insight, rank, locations explored, completed quests, and completed knowledge checks.

When a quest ends, read the **NEXT LEAD** message. It explains the next brewery problem, identifies the person who needs help, and tells you where to find that person.

## Pop quizzes

Pop quizzes appear while you explore, but they test a location you visited previously—not the room you have just entered. Answer by entering only `A`, `B`, `C`, or `D`. The answer positions are randomized.

- If you answer correctly, read the complete explanation before pressing a key to continue. Like the descriptions and NPC conversations, these explanations are test material.
- If you are unsure, enter `PAUSE`. The room will appear so you can investigate, use your map, or discuss the question with a classmate. Enter `QUIZ` or `RESUME` when you are ready to try again.
- An incorrect answer costs 2 Insight and pauses the quiz. Use the route provided to revisit the relevant location before answering again.

The sound and screen flash are only alerts; the important part is the question and its explanation.

## Other useful commands

| Command | What it does |
|---|---|
| `NOTES` | Review biochemical facts recorded during exploration |
| `WHO` | See nearby and currently connected players |
| `SAY message` | Speak to other students in your current room |
| `HELP` | Display the complete command list |
| `QUIT` | End the current session; progress remains saved |

## A good study strategy

1. Follow the quests in order so that each topic builds on the last.
2. Read each new room description instead of moving immediately.
3. Use `LOOK` on residents and objects, then `TALK` to the residents.
4. Treat room and object descriptions, NPC conversations, and every pop-quiz explanation as material you may see on the test.
5. Use `NOTES`, `JOURNAL`, `MAP`, and `HINT` whenever you need to review or reorient yourself.
6. Discuss difficult questions with classmates, but make sure you can explain the answer yourself.

The goal is not merely to accumulate Insight or finish every quest. The goal is to understand how the chemistry and biochemistry connect grain to wort.
