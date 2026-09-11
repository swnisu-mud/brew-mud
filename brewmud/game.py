from __future__ import annotations

import json
import random
import shlex
from collections import deque
from difflib import SequenceMatcher
from pathlib import Path

from .models import GameState
from .quests import GIVER_QUESTS, QUESTS
from .quizzes import QUIZZES
from .regional_maps import render_map
from .world import AMBIENT_SPEECH, DIRECTION_ALIASES, FACTS, ITEMS, NPCS, ROOMS


RANKS = ((0,"Brewery Visitor"), (20,"Malt House Hand"), (60,"Brewhouse Apprentice"),
         (120,"Fermentation Technician"), (220,"Brewery Biochemist"), (360,"Master Brewer"))
POP_QUIZ_INITIAL_DELAY = 6
POP_QUIZ_COOLDOWN = 6
POP_QUIZ_GUARANTEE = 10
POP_QUIZ_CHANCE = 0.45
WRONG_ANSWER_PENALTY = 2


class Game:
    """Command processor and private state for one BrewMUD player."""

    def __init__(self, state: GameState | None = None, rng: random.Random | None = None,
                 pop_quizzes_enabled: bool = True) -> None:
        self.state = state or GameState()
        self.rng = rng or random.Random()
        self.pop_quizzes_enabled = pop_quizzes_enabled
        self.running = True
        self.reset_quest_titles = self._normalize_active_quests()

    def _normalize_active_quests(self) -> list[str]:
        """Convert pre-sequence saves to one valid active assignment."""
        active = [key for key in QUESTS if key in self.state.quest_stages]
        valid = [key for key in active if all(
            required in self.state.completed_quests for required in QUESTS[key].requires
        )]
        keep = valid[0] if valid else None
        removed = [key for key in active if key != keep]
        if removed:
            self.state.quest_stages = (
                {keep: self.state.quest_stages[keep]} if keep is not None else {}
            )
            self.state.companion = None
        return [QUESTS[key].title for key in removed]

    @property
    def room(self):
        return ROOMS[self.state.room]

    @property
    def awaiting_quiz_continue(self) -> bool:
        return self.state.pending_room_description is not None and not self.state.active_quiz and not self.state.paused_quiz

    def introduction(self) -> str:
        if not self.state.quest_stages and not self.state.completed_quests:
            guidance = "Type TALK COORDINATOR to begin"
        else:
            guidance = "Type JOURNAL to review your saved objective"
        return ("BREWMUD: The Biochemistry of Beer\n"
                "You are a brewery biochemistry trainee. Seventy connected locations span maltings, "
                "brewhouse, fermentation cellar, hop yard, quality labs, and packaging. Residents throughout "
                "the brewery have substantial non-combat quests.\n"
                f"{guidance}, HELP for commands, or MAP for a regional map.\n\n"
                + self.describe_room())

    def describe_room(self) -> str:
        room = self.room
        first = room.key not in self.state.discovered_rooms
        old_rank = self.rank
        self.state.discovered_rooms.add(room.key)
        if first:
            self.state.insight += 1
            self.state.learned_facts.add(room.key)
        visible = [NPCS[k].name for k in room.npcs if k != self.state.companion]
        lines = [room.name, room.description]
        if self.state.quest_stages:
            active = list(self.state.quest_stages.items())
            objectives = [QUESTS[key].steps[stage].objective for key, stage in active[:2]]
            if len(active) > 2:
                objectives.append(f"+{len(active) - 2} more (JOURNAL)")
            lines.append("Objectives: " + " | ".join(objectives))
        if visible:
            lines.append("Nearby: " + ", ".join(visible) + ".")
        lines.append("Exits: " + ", ".join(room.exits) + ".")
        if self.state.companion:
            lines.append(f"{NPCS[self.state.companion].name} is following you.")
        if first and room.key in AMBIENT_SPEECH:
            lines.append("\n" + AMBIENT_SPEECH[room.key])
        if first:
            lines.append("Discovery: +1 Insight.")
            if self.rank != old_rank:
                lines.append(f"RANK UP: {self.rank}!")
        return "\n".join(lines)

    def execute(self, raw: str) -> str:
        raw = raw.strip()
        if not raw:
            return ""
        try:
            parts = shlex.split(raw.casefold())
        except ValueError:
            return "I could not parse that command. Check the quotation marks."
        verb, args = parts[0], parts[1:]
        if self.awaiting_quiz_continue:
            self.state.turns += 1
            if len(parts) == 1 and verb in {"c","continue"}:
                return self._reveal_pending_room()
            if verb == "help":
                return self.help() + "\n\nCONTINUE — Press C to reveal the room."
            return "The quiz explanation is still on screen. Press C to continue into the room."
        if self.state.active_quiz and len(parts) == 1 and verb in {"a","b","c","d"}:
            self.state.turns += 1
            return self.answer(verb)
        if self.state.active_quiz and verb not in {"answer","ans","quiz","pause","resume","help","status","level","rank"}:
            self.state.turns += 1
            return "A pop quiz is active. Answer A–D, or type PAUSE to investigate before answering."
        verb = DIRECTION_ALIASES.get(verb, verb)
        self.state.turns += 1
        if verb in {"north","south","east","west","up","down","in","out"}: return self.go(verb)
        if verb in {"go","move","walk"}: return self.go(" ".join(args))
        if verb in {"look","l","examine","inspect","x"}: return self.look(" ".join(args))
        if verb in {"talk","speak"}:
            target = " ".join(args)
            return self.talk(target[3:] if target.startswith("to ") else target)
        if verb in {"take","get","pickup"}: return self.take(" ".join(args))
        if verb in {"inventory","inv"}: return self.inventory()
        if verb in {"journal","quest","quests"}: return self.journal()
        if verb in {"notes","facts","notebook"}: return self.notes()
        if verb in {"explored","progress"}: return self.explored()
        if verb in {"status","level","rank"}: return self.progression()
        if verb in {"quiz","resume"}: return self.quiz()
        if verb == "pause": return self.pause_quiz()
        if verb in {"answer","ans"}: return self.answer(" ".join(args))
        if verb == "map": return self.map(" ".join(args))
        if verb == "hint": return self.hint()
        if verb == "help": return self.help()
        if verb == "save": return self.save(args[0] if args else "brewmud-save.json")
        if verb == "load": return self.load(args[0] if args else "brewmud-save.json")
        if verb in {"quit","exit"}:
            self.running = False
            return "Your brewery shift ends—for now."
        return f"Unknown command: {verb}. Type HELP for a command list."

    def go(self, direction: str) -> str:
        direction = DIRECTION_ALIASES.get(direction.strip(), direction.strip())
        destination = self.room.exits.get(direction)
        if not destination:
            return f"You cannot go {direction or 'that way'} from here. Exits: {', '.join(self.room.exits)}."
        self.state.room = destination
        pop = self._maybe_pop_quiz()
        description = self.describe_room()
        if pop:
            self.state.pending_room_description = description
            return pop
        return description

    def look(self, target: str = "") -> str:
        target = target.strip()
        if not target or target in {"around","room"}:
            return self.describe_room()
        for key in (*self.room.npcs, *((self.state.companion,) if self.state.companion else ())):
            if key in NPCS and self._matches(target, NPCS[key].aliases):
                return NPCS[key].description
        for feature in self.room.features:
            if self._matches(target, (feature.name, *feature.aliases)):
                if feature.fact: self.state.learned_facts.add(feature.fact)
                return feature.description
        suggestion = self._closest_npc(target)
        if suggestion:
            return f"Interpreting “{target}” as {NPCS[suggestion].name}.\n{NPCS[suggestion].description}"
        return f"You do not see {target} here."

    def talk(self, target: str) -> str:
        if not target:
            return "Talk to whom?"
        key = self._find_npc(target)
        if not key:
            suggestion = self._closest_npc(target)
            return f"Did you mean TALK {NPCS[suggestion].name}?" if suggestion else f"You cannot find {target} here."

        # Active objectives take priority. If one NPC is involved in two quests,
        # a second TALK advances the next one.
        for quest_key, stage in list(self.state.quest_stages.items()):
            quest = QUESTS[quest_key]
            step = quest.steps[stage]
            if step.action == "talk" and key == step.target:
                return self._advance_quest(quest_key, step.result)
            if step.action == "escort":
                if key == step.target:
                    if self.state.companion and self.state.companion != key:
                        return f"You are already escorting {NPCS[self.state.companion].name}. Finish that delivery first."
                    self.state.companion = key
                    return (f'“Lead the way,” says {NPCS[key].name}.\n\n'
                            f"OBJECTIVE UPDATED — Escort {NPCS[key].name} to {NPCS[step.destination].name}.")
                if key == step.destination and self.state.companion == step.target:
                    self.state.companion = None
                    return self._advance_quest(quest_key, step.result)

        quest_key = GIVER_QUESTS.get(key)
        if quest_key in self.state.completed_quests:
            return f'“Thanks again for your work on {QUESTS[quest_key].title},” says {NPCS[key].name}.'
        if quest_key and quest_key in self.state.quest_stages:
            stage = self.state.quest_stages[quest_key]
            return (f'“Keep following the evidence,” says {NPCS[key].name}.\n\n'
                    f"CURRENT OBJECTIVE — {QUESTS[quest_key].steps[stage].objective}")
        if quest_key:
            quest = QUESTS[quest_key]
            if self.state.quest_stages:
                active_key, active_stage = next(iter(self.state.quest_stages.items()))
                return (f"{NPCS[key].dialogue}\n\nONE QUEST AT A TIME — Finish {QUESTS[active_key].title} first.\n"
                        f"CURRENT OBJECTIVE — {QUESTS[active_key].steps[active_stage].objective}")
            missing = [required for required in quest.requires
                       if required not in self.state.completed_quests]
            if missing:
                prerequisite = QUESTS[missing[0]]
                return (f"{NPCS[key].dialogue}\n\nQUEST NOT YET AVAILABLE — "
                        f"Complete {prerequisite.title} first.")
            self.state.quest_stages[quest_key] = 0
            return (f"{quest.offer}\n\nQUEST STARTED — {quest.title}\n"
                    f"OBJECTIVE — {quest.steps[0].objective}")
        return NPCS[key].dialogue

    def _advance_quest(self, key: str, result: str) -> str:
        quest = QUESTS[key]
        stage = self.state.quest_stages[key] + 1
        if stage >= len(quest.steps):
            del self.state.quest_stages[key]
            self.state.completed_quests.add(key)
            response = f"{result}\n\nQUEST COMPLETE — {quest.title}" + self._award_insight(quest.reward)
            next_quest = self._next_available_quest()
            if next_quest:
                giver_room = next(r.key for r in ROOMS.values() if next_quest.giver in r.npcs)
                response += (f"\n\nNEXT LEAD — Find {NPCS[next_quest.giver].name} at "
                             f"{ROOMS[giver_room].name}.")
            return response
        self.state.quest_stages[key] = stage
        return f"{result}\n\nOBJECTIVE UPDATED — {quest.steps[stage].objective}"

    def take(self, target: str) -> str:
        return f"You do not need to carry {target or 'that'}; brewery quests use investigation and guided escorts."

    def inventory(self) -> str:
        companion = f" Escorting: {NPCS[self.state.companion].name}." if self.state.companion else ""
        return "You are carrying a visitor badge and field notebook." + companion

    def journal(self) -> str:
        lines = [f"QUEST JOURNAL — {len(self.state.quest_stages)} active, {len(self.state.completed_quests)}/{len(QUESTS)} completed"]
        for key, stage in self.state.quest_stages.items():
            quest = QUESTS[key]
            lines.append(f"- ACTIVE — {quest.title}: {quest.steps[stage].objective}")
        available = []
        if not self.state.quest_stages:
            quest = self._next_available_quest()
            if quest:
                giver_room = next(r.key for r in ROOMS.values() if quest.giver in r.npcs)
                available.append(f"- AVAILABLE — {quest.title}: talk to {NPCS[quest.giver].name} at {ROOMS[giver_room].name}.")
        if not self.state.quest_stages:
            lines.append("No active quest. Your next sequential assignment appears below.")
        lines.extend(available)
        return "\n".join(lines)

    def hint(self) -> str:
        if not self.state.quest_stages:
            quest = self._next_available_quest()
            if not quest:
                return "No active quest. You have completed every current brewery assignment."
            giver_room = next(r.key for r in ROOMS.values() if quest.giver in r.npcs)
            return (f"NEXT QUEST — {quest.title}: find {NPCS[quest.giver].name} at "
                    f"{ROOMS[giver_room].name}. {self._route_to(giver_room)}")
        lines = ["QUEST HINTS"]
        for key, stage in self.state.quest_stages.items():
            step = QUESTS[key].steps[stage]
            target = step.target if step.action == "talk" or self.state.companion != step.target else step.destination
            room_key = next((r.key for r in ROOMS.values() if target in r.npcs), None)
            if target == self.state.companion and step.destination:
                room_key = next((r.key for r in ROOMS.values() if step.destination in r.npcs), room_key)
            route = self._route_to(room_key) if room_key else "Use MAP to explore."
            lines.append(f"- {QUESTS[key].title}: {step.objective} {route}")
        return "\n".join(lines)

    def _next_available_quest(self):
        return next(
            (quest for key, quest in QUESTS.items()
             if key not in self.state.quest_stages
             and key not in self.state.completed_quests
             and all(required in self.state.completed_quests for required in quest.requires)),
            None,
        )

    def notes(self) -> str:
        if not self.state.learned_facts:
            return "Your notebook is empty. Explore stations and examine their equipment."
        return "FIELD NOTES\n" + "\n".join(f"- {FACTS[k]}" for k in FACTS if k in self.state.learned_facts)

    def explored(self) -> str:
        return f"You have explored {len(self.state.discovered_rooms)} of {len(ROOMS)} brewery locations and recorded {len(self.state.learned_facts)} topics."

    @property
    def rank(self) -> str:
        return next(title for threshold, title in reversed(RANKS) if self.state.insight >= threshold)

    def progression(self) -> str:
        nxt = next(((n,t) for n,t in RANKS if n > self.state.insight), None)
        next_text = f"Next rank: {nxt[1]} at {nxt[0]} Insight ({nxt[0]-self.state.insight} needed)." if nxt else "Highest current rank achieved."
        return (f"PROGRESSION\nRank: {self.rank}\nInsight: {self.state.insight}\n"
                f"Locations: {len(self.state.discovered_rooms)}/{len(ROOMS)}\n"
                f"Quests: {len(self.state.completed_quests)}/{len(QUESTS)}\n"
                f"Knowledge checks: {len(self.state.completed_quizzes)}/{len(QUIZZES)}\n{next_text}")

    def quiz(self) -> str:
        key = self.state.active_quiz
        if key is None:
            key = self.state.paused_quiz
            if key is None: return "No pop quiz is waiting. Keep exploring; questions revisit places you have already encountered."
            self.state.active_quiz, self.state.paused_quiz = key, None
        question = QUIZZES[key]
        order = self._quiz_order(question)
        options = "\n".join(f"  {chr(65+i)}. {question.options[o]}" for i,o in enumerate(order))
        return (f"KNOWLEDGE CHECK — review topic: {ROOMS[key].name}\n{question.prompt}\n{options}\n"
                "Type A, B, C, or D. Type PAUSE to revisit the relevant area.")

    def pause_quiz(self) -> str:
        key = self.state.active_quiz
        if key is None:
            return f"The {ROOMS[self.state.paused_quiz].name} check is already paused. Type QUIZ to resume." if self.state.paused_quiz else "No pop quiz is active."
        self.state.active_quiz, self.state.paused_quiz = None, key
        return (f"Knowledge check paused. Review topic: {ROOMS[key].name}. Explore, discuss, then type QUIZ or RESUME."
                + self._reveal_pending_room())

    def pop_quiz_candidates(self) -> set[str]:
        return {k for k,q in QUIZZES.items() if k in self.state.discovered_rooms and k != self.state.room
                and self.state.room not in q.arrival_exclusions and k not in self.state.completed_quizzes}

    def _maybe_pop_quiz(self, allowed: set[str] | None = None) -> str | None:
        if not self.pop_quizzes_enabled or self.state.active_quiz or self.state.paused_quiz or self.state.turns < POP_QUIZ_INITIAL_DELAY: return None
        since = self.state.turns - self.state.last_pop_quiz_turn
        if self.state.last_pop_quiz_turn and since < POP_QUIZ_COOLDOWN: return None
        eligible = sorted(self.pop_quiz_candidates() & allowed if allowed is not None else self.pop_quiz_candidates())
        if not eligible or (since < POP_QUIZ_GUARANTEE and self.rng.random() >= POP_QUIZ_CHANCE): return None
        self.state.active_quiz = self.rng.choice(eligible)
        self.state.quiz_option_order = []
        self.state.last_pop_quiz_turn = self.state.turns
        return "POP QUIZ!\n" + self.quiz()

    def begin_group_quiz(self, key: str, room_description: str) -> str:
        self.state.active_quiz, self.state.paused_quiz = key, None
        self.state.quiz_option_order = []
        self.state.pending_room_description = room_description
        self.state.last_pop_quiz_turn = self.state.turns
        return "POP QUIZ!\n" + self.quiz()

    def answer(self, response: str) -> str:
        key = self.state.active_quiz
        if key is None: return "No active knowledge check."
        question, order = QUIZZES[key], self._quiz_order(QUIZZES[key])
        answer = response.strip().casefold()
        selected = ord(answer)-97 if len(answer)==1 and answer in "abcd" else None
        if selected is None or selected >= len(order): return "I could not match that choice. Use A, B, C, or D."
        original = order[selected]
        if original != question.correct:
            self.state.active_quiz, self.state.paused_quiz = None, key
            lost = min(WRONG_ANSWER_PENALTY, self.state.insight)
            self.state.insight -= lost
            return (f"Not quite. {question.feedback[original]}\n\nINSIGHT -{lost} — total {self.state.insight}.\n"
                    "The check is paused so you can investigate before guessing again.\n"
                    f"{self._route_to(key)} Ask nearby players with SAY, then type QUIZ when ready."
                    + self._reveal_pending_room())
        self.state.completed_quizzes.add(key)
        self.state.active_quiz = self.state.paused_quiz = None
        self.state.quiz_option_order = []
        response = f"Correct. {question.explanation}" + self._award_insight(10)
        if self.state.pending_room_description is not None: response += "\n\nCONTINUE — Press C to reveal the room."
        return response

    def _quiz_order(self, question) -> list[int]:
        expected = list(range(len(question.options)))
        if sorted(self.state.quiz_option_order) != expected:
            self.state.quiz_option_order = expected
            self.rng.shuffle(self.state.quiz_option_order)
        return self.state.quiz_option_order

    def _reveal_pending_room(self) -> str:
        description, self.state.pending_room_description = self.state.pending_room_description, None
        return f"\n\n{description}" if description else ""

    def _route_to(self, target: str | None) -> str:
        if not target: return "Use MAP to locate the destination."
        if self.state.room == target: return f"You are already at {ROOMS[target].name}."
        queue, visited = deque([(self.state.room, [])]), {self.state.room}
        while queue:
            room, path = queue.popleft()
            for direction, destination in ROOMS[room].exits.items():
                if destination in visited: continue
                new = [*path, direction]
                if destination == target: return f"Shortest route to {ROOMS[target].name}: {' → '.join(new)}."
                visited.add(destination); queue.append((destination,new))
        return f"Use MAP to seek {ROOMS[target].name}."

    def _award_insight(self, amount: int) -> str:
        old = self.rank
        self.state.insight += amount
        message = f"\n\nINSIGHT +{amount} — total {self.state.insight}."
        if self.rank != old: message += f"\nRANK UP: {self.rank}!"
        return message

    def map(self, region: str = "") -> str:
        return render_map(self.state.room, region)

    @staticmethod
    def help() -> str:
        return ("COMMANDS\n  LOOK [thing]       Describe a room, resident, or equipment\n"
                "  GO <direction>     Move; N/S/E/W/U/D/I/O work\n  TALK [TO] <name>   Speak with a resident and discover quests\n"
                "  JOURNAL            Show all active and discovered quests\n  HINT               Show routes to active objectives\n"
                "  NOTES              Review discovered biochemical facts\n  STATUS             Show Insight, rank, quests, and quizzes\n"
                "  QUIZ / RESUME      Resume a paused pop quiz\n  PAUSE              Pause a quiz to investigate\n"
                "  A / B / C / D      Answer a knowledge check\n  MAP [region]        Show a compact regional map; MAP ALL lists regions\n"
                "  SAVE / LOAD [file] Solo-terminal files; browser accounts save automatically\n  QUIT                End the session")

    def save(self, filename: str) -> str:
        path = Path(filename).expanduser()
        try: path.write_text(json.dumps(self.state.to_dict(), indent=2)+"\n", encoding="utf-8")
        except OSError as exc: return f"Could not save the game: {exc}"
        return f"Game saved to {path}."

    def load(self, filename: str) -> str:
        path = Path(filename).expanduser()
        try:
            candidate = GameState.from_dict(json.loads(path.read_text(encoding="utf-8")))
            if candidate.room not in ROOMS: raise ValueError("unknown room")
            if not set(candidate.quest_stages).issubset(QUESTS): raise ValueError("unknown quest")
            if not candidate.completed_quests.issubset(QUESTS): raise ValueError("unknown completed quest")
            if any(stage < 0 or stage >= len(QUESTS[key].steps) for key,stage in candidate.quest_stages.items()): raise ValueError("invalid quest stage")
            if (candidate.active_quiz and candidate.active_quiz not in QUIZZES) or (candidate.paused_quiz and candidate.paused_quiz not in QUIZZES): raise ValueError("unknown quiz")
            self.state = candidate
        except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc: return f"Could not load the game: {exc}"
        return f"Game loaded from {path}.\n" + self.describe_room()

    def _find_npc(self, target: str) -> str | None:
        candidates = list(self.room.npcs) + ([self.state.companion] if self.state.companion else [])
        return next((k for k in candidates if self._matches(target, NPCS[k].aliases)), None)

    def _closest_npc(self, target: str) -> str | None:
        candidates = list(self.room.npcs) + ([self.state.companion] if self.state.companion else [])
        scored = [(max(SequenceMatcher(None,target.casefold(),a.casefold()).ratio() for a in NPCS[k].aliases), k) for k in candidates]
        if not scored: return None
        score, key = max(scored)
        return key if score >= 0.60 else None

    @staticmethod
    def _matches(target: str, aliases) -> bool:
        target = target.casefold().strip()
        return bool(target) and any(a.casefold() == target or a.casefold().startswith(target) for a in aliases)
