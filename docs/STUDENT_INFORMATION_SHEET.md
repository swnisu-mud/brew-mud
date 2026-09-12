# BrewMUD Student Information Sheet

## A study guide you can explore

BrewMUD is a substitute for a typical study guide for our material on malting, carbohydrate and protein chemistry, enzymes, mashing, and lautering. It is intended to be helpful and, hopefully, somewhat fun—or at least not boring. Instead of reading a list of review questions, you will explore a brewery, speak with its residents, and solve biochemical and brewing problems.

**Questions on the test will come directly from room and object descriptions, conversations with NPCs, and pop quizzes in BrewMUD.** Read the text carefully. Finishing a quest quickly is not as useful as understanding what the rooms, objects, and characters are telling you.

Course link: **https://brew-mud.onrender.com**

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

<!-- PAGE BREAK -->

## Regional map reference

In each diagram, rooms joined by `---` connect east and west, while vertically aligned rooms joined by `|` connect north and south. The diagrams show connections, while the room's **Exits** line remains the authority for the directions you can use. Type `MAP` in the game to display your current region, or `MAP name`—for example, `MAP ENZYME`—to display another region.

These maps are optional orientation aids. If a diagram is difficult to see or interpret, use `HINT` for a written route to your current objective. The code legends and regional transitions below also state every location and cross-region connection in text.

### Maltings (`MAP MALT`)

```text
[GRN]---[BAR]---[STP]---[AIR]---[GER]
  |       |       |       |       |
[GAT]---[CUR]---[KLN]---[END]---[ALE]
```

Codes: GRN—Grain Receiving; BAR—Two-Row Barley Laboratory; STP—Steep House; AIR—Steep Air Rest; GER—Germination Floor; GAT—Brewery Gate; CUR—Malt Curing Floor; KLN—Malt Kiln; END—Starchy Endosperm; ALE—Aleurone Workshop.

Regional transitions: Germination Floor leads **DOWN** to the Brewing Water Laboratory. Brewery Gate leads **IN** to the Packaging and Shipping Dock.

### Water and mash chemistry (`MAP MASH`)

```text
[WAT]---[PHB]---[ION]---[CTY]
  |       |       |       |
[TRT]---[MIL]---[MSH]---[PRO]
  |       |       |       |
[BET]---[ALP]---[CNV]---[OUT]
```

Codes: WAT—Brewing Water Laboratory; PHB—pH Bench; ION—Ion Gallery; CTY—Historic Water Profiles; TRT—Water Treatment Bay; MIL—Malt Mill; MSH—Mash Tun; PRO—Protein Rest; BET—Beta-Amylase Rest; ALP—Alpha-Amylase Rest; CNV—Starch Conversion Bench; OUT—Mash-Out Platform.

Regional transitions: Water Laboratory leads **UP** to Germination Floor. Mash Tun leads **IN** to the Carbohydrate and Starch Lab. Protein Rest, Beta-Amylase Rest, and Alpha-Amylase Rest each lead **IN** to the Protein and Enzyme Lab. Starch Conversion Bench leads **IN** to the Gelatinization Chamber. Mash-Out leads **DOWN** to the Lauter Tun.

### Carbohydrate and starch lab (`MAP STARCH`)

```text
[CAR]---[GLU]---[DIS]---[POL]
  |       |       |       |
[GEL]---[CRY]---[AMY]---[AMP]
```

Codes: CAR—Carbohydrate and Starch Laboratory; GLU—Glucose Bench; DIS—Disaccharide Gallery; POL—Glucose-Polymer Comparison Hall; GEL—Gelatinization Chamber; CRY—Starch Crystallinity Laboratory; AMY—Amylose Helix Walk; AMP—Amylopectin Branching Arbor.

Regional transitions: Carbohydrate Laboratory leads **OUT** to the Mash Tun. Gelatinization Chamber leads **OUT** to the Starch Conversion Bench.

<!-- PAGE BREAK -->

### Protein and enzyme lab (`MAP ENZYME`)

```text
[AAG]---[PEP]---[STR]---[FOL]---[DEN]---[CAT]
  |       |       |       |       |       |
[ACT]---[OPT]---[AMZ]---[THK]---[AUX]---[IOD]
```

Codes: AAG—Amino Acid Gallery; PEP—Peptide Bond Bench; STR—Protein Structure Gallery; FOL—Protein Folding Chamber; DEN—Denaturation and Aggregation Bay; CAT—Enzyme Catalysis Laboratory; ACT—Active-Site Workshop; OPT—Enzyme Conditions Laboratory; AMZ—Amylase Mechanism Laboratory; THK—Mash-Thickness Control Station; AUX—Accessory Enzyme Laboratory; IOD—Starch–Iodine Test Alcove.

Regional transitions: Amino Acid Gallery leads **OUT** to the Protein Rest. Amylase Mechanism Laboratory leads **OUT** to the Beta-Amylase Rest. Starch–Iodine Test Alcove leads **OUT** to the Alpha-Amylase Rest.

### Brewhouse (`MAP BREW`)

```text
[LAU]---[BED]---[SPA]---[GRA]---[KET]
  |       |       |       |       |
[BRK]---[HOP]---[WHL]---[HEX]---[OXY]
```

Codes: LAU—Lauter Tun; BED—Grain-Bed Gallery; SPA—Sparge Arm; GRA—Wort Grant; KET—Copper Kettle; BRK—Hot-Break Deck; HOP—Hop-Dosing Balcony; WHL—Whirlpool; HEX—Wort Heat Exchanger; OXY—Wort Oxygenation Station.

Regional transitions: Lauter Tun leads **UP** to Mash-Out. Hop-Dosing Balcony leads **IN** to the Hop Lab. Wort Oxygenation Station leads **DOWN** to the Fermentation Cellar.

### Fermentation cellar (`MAP FERMENT`)

```text
[PIT]---[ALE]---[LAG]---[YLB]---[MEM]---[MGP]---[MLT]
  |       |       |       |       |       |       |
[GLY]---[NAD]---[LIP]---[EST]---[DIA]---[SUL]---[MAT]
```

Codes: PIT—Yeast Pitching Deck; ALE—Ale Fermenter; LAG—Lager Fermenter; YLB—Yeast Culture Laboratory; MEM—Yeast Membrane Walk; MGP—Maltose Transport Gate; MLT—Maltase Bench; GLY—Glycolysis Lane; NAD—NAD+ Recycling Junction; LIP—Sterol and Lipid Workshop; EST—Ester Laboratory; DIA—Diacetyl Rest; SUL—Sulfur Vent; MAT—Maturation Cellar.

Regional transitions: Pitching Deck leads **UP** to Wort Oxygenation. Yeast Laboratory leads **IN** to Microbiology. Maturation Cellar leads **DOWN** to Packaging.

<!-- PAGE BREAK -->

### Hop yard and flavor lab (`MAP HOPS`)

```text
[YRD]---[CON]---[LUP]---[AAC]
  |       |       |       |
[OIL]---[IBU]---[DRY]---[LGT]
```

Codes: YRD—Hop Yard; CON—Female Cone Arbor; LUP—Lupulin Gland; AAC—Alpha-Acid Bench; OIL—Hop Essential-Oil Lab; IBU—IBU Spectrophotometer; DRY—Dry-Hop Gallery; LGT—Lightstrike Booth.

Regional transition: Alpha-Acid Bench leads **OUT** to the Brewhouse Hop-Dosing Balcony.

### Packaging and sensory (`MAP PACK`)

```text
[BRT]---[CO2]---[BOT]---[CAN]---[NIT]
  |       |       |       |       |
[FOM]---[SNS]---[STY]---[CLD]---[SHP]
```

Codes: BRT—Brite Beer Tank; CO2—Carbonation Station; BOT—Bottle-Conditioning Line; CAN—Canning Line; NIT—Nitrogen Service Tap; FOM—Beer Foam Laboratory; SNS—Sensory Evaluation Room; STY—Style Taproom; CLD—Cold Storage; SHP—Packaging and Shipping Dock.

Regional transitions: Brite Tank leads **UP** to Maturation. Style Taproom leads **DOWN** to Quality Assurance. Shipping Dock leads **OUT** to Brewery Gate.

### Quality and training (`MAP QUALITY`)

```text
[MIC]---[SAN]---[QAC]
  |       |       |
[BNK]---[PIL]---[CLS]
```

Codes: MIC—Brewery Microbiology Lab; SAN—Cleaning and Sanitation Bay; QAC—Analytical Chemistry Lab; BNK—Production Yeast Bank; PIL—Pilot Brewery; CLS—Brewery Training Classroom.

Regional transitions: Microbiology Laboratory leads **OUT** to the Yeast Laboratory. Quality Chemistry Laboratory leads **UP** to the Style Taproom.

## How quests work

The quests form a sequence through malting, water chemistry, carbohydrate and starch structure, protein structure, enzyme and amylase behavior, mashing, and lautering. You may explore anywhere, but you can have only one active quest at a time, and later quests unlock after earlier ones are completed.

### First-exam quest path

The seven first-exam quests contain 42 required objectives. They are designed to build one connected explanation from raw barley to separated wort.

| Quest | What you will investigate | Steps |
|---|---|---:|
| **First Day in the Brewery** | Follow the broad grain-to-wort route and meet the people responsible for each major stage | 7 |
| **Wake the Sleeping Grain** | Diagnose uneven germination by tracing hydration, gibberellic-acid signaling, aleurone enzymes, and endosperm modification | 5 |
| **A Tale of Two Ions** | Separate pH, alkalinity, and hardness while correcting bicarbonate and sulfate/chloride balance | 6 |
| **Rebuild the Carbohydrate Map** | Connect glucose and maltose to amylose, amylopectin, starch packing, and gelatinization | 7 |
| **The Enzyme That Lost Its Shape** | Connect amino-acid chains and protein folding to denaturation, active sites, temperature and pH optima, and alpha- versus beta-amylase | 7 |
| **The Stalled Mash** | Use milling, gelatinization, pH, and amylase evidence to diagnose an iodine-dark production mash | 6 |
| **The Stuck Runoff** | Restore wort flow by understanding husk-supported filtration, vorlauf, sparging, channeling, and bed compaction | 4 |

Completing **The Stuck Runoff** marks the end of the first-exam quest material. **The Vanishing Hop Aroma** and the quests that follow introduce later course material. The other residents and rooms in the first-exam regions remain useful for optional review and additional pop quizzes.

- `TALK name` starts or advances a quest when that resident is involved.
- The **Active quest** section beside the game window shows the current problem and objective.
- `JOURNAL` shows your current assignment or explains the next problem that needs attention.
- `HINT` gives directions to the resident needed for the current objective.
- `LEVEL` or `STATUS` shows your Insight, rank, locations explored, completed quests, and completed knowledge checks.

When a quest ends, read the **NEXT LEAD** message. It explains the next brewery problem, identifies the person who needs help, and tells you where to find that person.

## Pop quizzes

Pop quizzes appear while you explore, but they test a location you visited previously—not the room you have just entered. Answer by entering only `A`, `B`, `C`, or `D`. The answer positions are randomized.

- If you answer correctly, read the complete explanation before pressing a key to continue. Like the descriptions and NPC conversations, these explanations are test material.
- If you are unsure, enter `PAUSE`. The room will appear so you can use `NOTES`, revisit the relevant area, consult your map, or discuss the question with a classmate. Enter `QUIZ` or `RESUME` when you are ready to try again.
- An incorrect answer costs 2 Insight and pauses the quiz. Use `NOTES` or the provided route to review the relevant material before answering again.

The sound and screen flash are only alerts; the important part is the question and its explanation.

## Other useful commands

| Command | What it does |
|---|---|
| `NOTES` | Review biochemical facts recorded during exploration |
| `WHO` | See nearby and currently connected players |
| `SAY message` | Speak to other students in your current room |
| `SURVEY` or `EVALUATE` | Open the optional anonymous course evaluation |
| `HELP` | Display the complete command list |
| `QUIT` | End the current session; progress remains saved |

## Course evaluation

Enter `SURVEY` or `EVALUATE` in the game to open a short evaluation. It contains ten optional 1–10 ratings and one optional comment. A rating of 1 means **strongly disagree**, and 10 means **strongly agree**.

The game records that your account completed the evaluation, but stores your answers separately without your account name, rank, activity, or submission time. Do not put your name or other identifying details in the optional comment. Anonymous results will not appear in the instructor report until at least five students have responded.

## Optional game-testing extra credit

You may earn up to **20 extra-credit points** by using BrewMUD as a study guide and helping evaluate it. Your points are based on the highest rank shown by the `LEVEL` command at the deadline.

| Rank reached | Extra-credit points |
|---|---:|
| Brewery Visitor | 0 |
| Brewery Trainee | 3 |
| Malt House Hand | 6 |
| Maltings Specialist | 9 |
| Water Chemistry Assistant | 12 |
| Carbohydrate Analyst | 15 |
| Enzyme Technician | 18 |
| Brewhouse Operator or any higher rank | 20 |

To receive points:

1. Report your BrewMUD account name to your instructor by **[deadline]**.
2. Enter `SURVEY` or `EVALUATE` and submit the course evaluation by that deadline. You may leave individual ratings or the optional comment unanswered.

The instructor can see your account name, rank, and whether you submitted the evaluation. The instructor cannot connect your account to your ratings or comment. Submitting the evaluation is required for game-testing credit, but expressing any particular opinion is not.

## A good study strategy

1. Follow the quests in order so that each topic builds on the last.
2. Read each new room description instead of moving immediately.
3. Use `LOOK` on residents and objects, then `TALK` to the residents.
4. Treat room and object descriptions, NPC conversations, and every pop-quiz explanation as material you may see on the test.
5. Use `NOTES`, `JOURNAL`, `MAP`, and `HINT` whenever you need to review or reorient yourself.
6. Discuss difficult questions with classmates, but make sure you can explain the answer yourself.

The goal is not merely to accumulate Insight or finish every quest. The goal is to understand how the chemistry and biochemistry connect grain to wort.
