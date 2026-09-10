from __future__ import annotations

import json
import random
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from brewmud.game import Game
from brewmud.quests import QUESTS
from brewmud.quizzes import QUIZZES
from brewmud.regional_maps import REGIONAL_MAPS, ROOM_REGION
from brewmud.server import MUDServer
from brewmud.world import NPC_DESCRIPTIONS, NPCS, ROOMS


def npc_room(npc: str) -> str:
    return next(room.key for room in ROOMS.values() if npc in room.npcs)


class WorldTests(unittest.TestCase):
    def test_content_counts(self):
        self.assertEqual(len(ROOMS), 70)
        self.assertGreaterEqual(len(NPCS), 80)
        self.assertEqual(len(QUESTS), 14)
        self.assertGreaterEqual(sum(len(q.steps) for q in QUESTS.values()), 70)
        self.assertGreaterEqual(len(QUIZZES), 18)

    def test_world_connected_and_exits_reciprocal(self):
        opposite = {"north":"south","south":"north","east":"west","west":"east",
                    "up":"down","down":"up","in":"out","out":"in"}
        seen, todo = {"brewery_gate"}, ["brewery_gate"]
        while todo:
            key = todo.pop()
            for direction, destination in ROOMS[key].exits.items():
                self.assertEqual(ROOMS[destination].exits.get(opposite[direction]), key)
                if destination not in seen:
                    seen.add(destination); todo.append(destination)
        self.assertEqual(seen, set(ROOMS))

    def test_all_rooms_have_residents_facts_and_maps(self):
        for key, room in ROOMS.items():
            self.assertTrue(room.npcs, key)
            self.assertTrue(room.features, key)
            self.assertIn(key, ROOM_REGION)
        self.assertEqual(set(ROOM_REGION), set(ROOMS))

    def test_quest_targets_exist_and_are_placed(self):
        placed = {npc for room in ROOMS.values() for npc in room.npcs}
        for quest in QUESTS.values():
            targets = [quest.giver, *[s.target for s in quest.steps],
                       *[s.destination for s in quest.steps if s.destination]]
            for target in targets:
                self.assertIn(target, NPCS)
                self.assertIn(target, placed)

    def test_every_npc_has_a_specific_educational_description(self):
        self.assertEqual(set(NPCS), set(NPC_DESCRIPTIONS))
        for key, npc in NPCS.items():
            self.assertNotIn("occupied with", npc.description, key)
            self.assertGreater(len(npc.description), 60, key)

    def test_each_quest_can_be_played_to_completion(self):
        for key, quest in QUESTS.items():
            with self.subTest(quest=key):
                game = Game(pop_quizzes_enabled=False)
                game.state.room = npc_room(quest.giver)
                start = game.talk(quest.giver)
                self.assertIn("QUEST STARTED", start)
                while key in game.state.quest_stages:
                    step = quest.steps[game.state.quest_stages[key]]
                    game.state.room = npc_room(step.target)
                    result = game.talk(step.target)
                    if step.action == "escort":
                        self.assertEqual(game.state.companion, step.target)
                        game.state.room = npc_room(step.destination)
                        result = game.talk(step.destination)
                    self.assertTrue(result)
                self.assertIn(key, game.state.completed_quests)


class CommandTests(unittest.TestCase):
    def setUp(self):
        self.game = Game(rng=random.Random(7), pop_quizzes_enabled=False)
        self.game.introduction()

    def test_case_insensitive_commands_and_names(self):
        self.assertIn("QUEST STARTED", self.game.execute("TaLk COORDINATOR"))

    def test_coordinator_sets_an_initial_assignment_not_a_tour(self):
        intro = Game(pop_quizzes_enabled=False).introduction()
        self.assertNotIn("full brewery tour", intro.casefold())
        self.assertIn("ready to get started", intro.casefold())

    def test_fuzzy_npc_look(self):
        self.game.state.room = "germination_floor"
        self.assertIn("Gibberellic Acid", self.game.execute("look gibberlic acid"))

    def test_journal_holds_multiple_active_quests(self):
        self.game.talk("training coordinator")
        self.game.state.room = "cure_floor"
        self.game.talk("head maltster")  # orientation objective
        self.game.talk("head maltster")  # starts malt quest
        journal = self.game.journal()
        self.assertIn("2 active", journal)
        self.assertIn("First Day", journal)
        self.assertIn("Wake the Sleeping Grain", journal)

    def test_room_description_tracks_active_objectives(self):
        self.game.talk("training coordinator")
        room = self.game.describe_room()
        self.assertIn("QUEST TRACKER", room)
        self.assertIn("First Day in the Brewery: Meet the Head Maltster.", room)

    def test_room_tracker_is_compact_when_many_quests_are_active(self):
        keys = list(QUESTS)[:5]
        self.game.state.quest_stages = {key: 0 for key in keys}
        room = self.game.describe_room()
        self.assertEqual(room.count("  •"), 4)
        self.assertIn("+2 more — type JOURNAL", room)

    def test_hint_routes_to_each_active_objective(self):
        self.game.talk("coordinator")
        self.assertIn("Shortest route", self.game.hint())

    def test_map_current_location(self):
        output = self.game.map()
        self.assertIn("REGIONAL MAP — MALTINGS", output)
        self.assertIn("<GAT>", output)
        self.assertIn("Regional Transitions", output)

    def test_map_index(self):
        self.assertIn("MAP QUALITY", self.game.map("all"))

    def test_save_and_load_multiple_quests(self):
        self.game.talk("coordinator")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "save.json"
            self.assertIn("saved", self.game.save(str(path)))
            restored = Game()
            self.assertIn("loaded", restored.load(str(path)))
            self.assertEqual(restored.state.quest_stages, {"orientation": 0})


class QuizTests(unittest.TestCase):
    def test_options_are_shuffled_and_bare_letter_works(self):
        game = Game(rng=random.Random(3), pop_quizzes_enabled=False)
        game.state.active_quiz = "mash_tun"
        game.quiz()
        displayed = game.state.quiz_option_order.index(QUIZZES["mash_tun"].correct)
        response = game.execute(chr(65 + displayed))
        self.assertIn("Correct.", response)

    def test_wrong_answer_costs_insight_and_pauses(self):
        game = Game(rng=random.Random(3), pop_quizzes_enabled=False)
        game.state.insight = 10
        game.state.active_quiz = "mash_tun"
        game.quiz()
        displayed = next(i for i,o in enumerate(game.state.quiz_option_order) if o != QUIZZES["mash_tun"].correct)
        response = game.answer(chr(65 + displayed))
        self.assertEqual(game.state.insight, 8)
        self.assertEqual(game.state.paused_quiz, "mash_tun")
        self.assertIn("Shortest route", response)

    def test_correct_explanation_requires_continue_before_room(self):
        game = Game(rng=random.Random(5), pop_quizzes_enabled=False)
        game.state.active_quiz = "kiln"
        game.state.pending_room_description = "SECRET ROOM DESCRIPTION"
        game.quiz()
        displayed = game.state.quiz_option_order.index(QUIZZES["kiln"].correct)
        response = game.answer(chr(65 + displayed))
        self.assertIn("CONTINUE", response)
        self.assertNotIn("SECRET ROOM DESCRIPTION", response)
        self.assertIn("SECRET ROOM DESCRIPTION", game.execute("c"))

    def test_candidates_require_prior_visit_not_current_room(self):
        game = Game(pop_quizzes_enabled=True)
        game.state.discovered_rooms = {"mash_tun", "kiln"}
        game.state.room = "kiln"
        self.assertEqual(game.pop_quiz_candidates(), {"mash_tun"})


class MultiplayerTests(unittest.TestCase):
    def test_chat_presence_and_following(self):
        server = MUDServer()
        alice, _ = server.login("Alice")
        bob, _ = server.login("Bob")
        self.assertIn("Alice says", server.command(alice, "say Ready?") + "\n" + "\n".join(server.poll(bob)))
        self.assertIn("begin following", server.command(bob, "follow Alice"))
        server.command(alice, "east")
        self.assertEqual(server._players[alice].game.state.room, server._players[bob].game.state.room)

    def test_players_have_independent_quest_state(self):
        server = MUDServer()
        alice, _ = server.login("Alice")
        bob, _ = server.login("Bob")
        server.command(alice, "talk coordinator")
        self.assertIn("orientation", server._players[alice].game.state.quest_stages)
        self.assertNotIn("orientation", server._players[bob].game.state.quest_stages)


class AssetTests(unittest.TestCase):
    def test_browser_assets_are_brewery_branded(self):
        static = Path(__file__).parents[1] / "brewmud" / "static"
        self.assertIn("BrewMUD", (static / "index.html").read_text())
        self.assertIn("brew>", (static / "app.js").read_text())
        self.assertNotIn("mito>", (static / "app.js").read_text())

    def test_render_blueprint_uses_web_service_and_health_check(self):
        blueprint = (Path(__file__).parents[1] / "render.yaml").read_text()
        self.assertIn("type: web", blueprint)
        self.assertIn("python -m brewmud.web --host 0.0.0.0", blueprint)
        self.assertIn("healthCheckPath: /api/status", blueprint)

    def test_render_port_environment_selects_public_bind_default(self):
        from brewmud import web
        with patch.dict("os.environ", {"PORT": "10000"}, clear=True):
            self.assertEqual(web.default_bind_host(), "0.0.0.0")
        with patch.dict("os.environ", {}, clear=True):
            self.assertEqual(web.default_bind_host(), "127.0.0.1")


if __name__ == "__main__":
    unittest.main()
