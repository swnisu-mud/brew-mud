from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Feature:
    name: str
    aliases: tuple[str, ...]
    description: str
    fact: str | None = None


@dataclass(frozen=True)
class NPC:
    key: str
    name: str
    aliases: tuple[str, ...]
    description: str
    dialogue: str


@dataclass(frozen=True)
class Room:
    key: str
    name: str
    description: str
    exits: dict[str, str]
    features: tuple[Feature, ...] = ()
    npcs: tuple[str, ...] = ()
    items: tuple[str, ...] = ()


@dataclass
class GameState:
    room: str = "brewery_gate"
    inventory: set[str] = field(default_factory=set)
    taken_items: set[str] = field(default_factory=set)
    discovered_rooms: set[str] = field(default_factory=set)
    learned_facts: set[str] = field(default_factory=set)
    quest_stages: dict[str, int] = field(default_factory=dict)
    completed_quests: set[str] = field(default_factory=set)
    companion: str | None = None
    insight: int = 0
    completed_quizzes: set[str] = field(default_factory=set)
    active_quiz: str | None = None
    paused_quiz: str | None = None
    quiz_option_order: list[int] = field(default_factory=list)
    pending_room_description: str | None = None
    last_pop_quiz_turn: int = 0
    turns: int = 0

    def to_dict(self) -> dict[str, object]:
        return {
            "version": 4, "room": self.room,
            "inventory": sorted(self.inventory), "taken_items": sorted(self.taken_items),
            "discovered_rooms": sorted(self.discovered_rooms),
            "learned_facts": sorted(self.learned_facts),
            "quest_stages": self.quest_stages,
            "completed_quests": sorted(self.completed_quests),
            "companion": self.companion, "insight": self.insight,
            "completed_quizzes": sorted(self.completed_quizzes),
            "active_quiz": self.active_quiz, "paused_quiz": self.paused_quiz,
            "quiz_option_order": self.quiz_option_order,
            "pending_room_description": self.pending_room_description,
            "last_pop_quiz_turn": self.last_pop_quiz_turn, "turns": self.turns,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "GameState":
        version = int(data.get("version", 1))
        quest_stages = {str(k): int(v) for k, v in dict(data.get("quest_stages", {})).items()}
        # Version 3 replaced the broad department tour with a malting/mashing
        # orientation while retaining seven steps. Map old progress forward so
        # returning players do not replay every introduction.
        if version < 3 and "orientation" in quest_stages:
            quest_stages["orientation"] = {0: 0, 1: 2, 2: 5}.get(
                quest_stages["orientation"], 6
            )
        # Version 4 shortened two first-exam quests while preserving the key
        # concepts. Move active players to the nearest equivalent new step.
        if version < 4 and "starch_structure" in quest_stages:
            old_stage = quest_stages["starch_structure"]
            quest_stages["starch_structure"] = {
                0: 0, 1: 1, 2: 2, 3: 2, 4: 2, 5: 3,
                6: 4, 7: 4, 8: 4, 9: 5, 10: 6, 11: 6,
            }.get(old_stage, 6)
        if version < 4 and "protein_enzymes" in quest_stages:
            old_stage = quest_stages["protein_enzymes"]
            quest_stages["protein_enzymes"] = {
                0: 0, 1: 1, 2: 1, 3: 1, 4: 1, 5: 2,
                6: 3, 7: 3, 8: 4, 9: 5, 10: 5, 11: 5,
                12: 5, 13: 5, 14: 5, 15: 5, 16: 6,
            }.get(old_stage, 6)
        return cls(
            room=str(data.get("room", "brewery_gate")),
            inventory=set(data.get("inventory", [])),
            taken_items=set(data.get("taken_items", [])),
            discovered_rooms=set(data.get("discovered_rooms", [])),
            learned_facts=set(data.get("learned_facts", [])),
            quest_stages=quest_stages,
            completed_quests=set(data.get("completed_quests", [])),
            companion=data.get("companion") if isinstance(data.get("companion"), str) else None,
            insight=int(data.get("insight", 0)),
            completed_quizzes=set(data.get("completed_quizzes", [])),
            active_quiz=data.get("active_quiz") if isinstance(data.get("active_quiz"), str) else None,
            paused_quiz=data.get("paused_quiz") if isinstance(data.get("paused_quiz"), str) else None,
            quiz_option_order=[int(v) for v in data.get("quiz_option_order", [])],
            pending_room_description=(data.get("pending_room_description") if isinstance(data.get("pending_room_description"), str) else None),
            last_pop_quiz_turn=int(data.get("last_pop_quiz_turn", 0)), turns=int(data.get("turns", 0)),
        )
