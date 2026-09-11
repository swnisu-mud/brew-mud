from __future__ import annotations

import json
import random
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from brewmud.accounts import AccountStore
from brewmud.game import (
    POP_QUIZ_CHANCE,
    POP_QUIZ_COOLDOWN,
    POP_QUIZ_GUARANTEE,
    POP_QUIZ_INITIAL_DELAY,
    Game,
)
from brewmud.models import GameState
from brewmud.quests import QUESTS
from brewmud.quizzes import QUIZZES
from brewmud.regional_maps import REGIONAL_MAPS, ROOM_REGION, compact_map_data
from brewmud.server import MUDServer
from brewmud.world import NPC_DESCRIPTIONS, NPC_DIALOGUE, NPCS, ROOMS


def npc_room(npc: str) -> str:
    return next(room.key for room in ROOMS.values() if npc in room.npcs)


class WorldTests(unittest.TestCase):
    def test_content_counts(self):
        self.assertEqual(len(ROOMS), 90)
        self.assertGreaterEqual(len(NPCS), 111)
        self.assertEqual(len(QUESTS), 16)
        self.assertGreaterEqual(sum(len(q.steps) for q in QUESTS.values()), 101)
        self.assertGreaterEqual(len(QUIZZES), 39)

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

    def test_quest_responses_are_substantive_conversations(self):
        for quest_key, quest in QUESTS.items():
            for step_number, step in enumerate(quest.steps, 1):
                label = f"{quest_key} step {step_number}: {step.target}"
                self.assertGreaterEqual(len(step.result), 120, label)
                self.assertIn("“", step.result, label)
                self.assertIn("”", step.result, label)
                if step.action == "escort":
                    self.assertIsNotNone(step.start_result, label)
                    self.assertGreaterEqual(len(step.start_result or ""), 120, label)
                    self.assertIn("“", step.start_result or "", label)
                    self.assertIn("”", step.start_result or "", label)

    def test_every_npc_has_a_specific_educational_description(self):
        self.assertEqual(set(NPCS), set(NPC_DESCRIPTIONS))
        for key, npc in NPCS.items():
            self.assertNotIn("occupied with", npc.description, key)
            self.assertGreater(len(npc.description), 60, key)

    def test_npc_dialogue_does_not_repeat_the_room_description(self):
        for room in ROOMS.values():
            for key in room.npcs:
                self.assertNotIn(room.description, NPCS[key].dialogue, key)
        self.assertIn("several parts of the load", NPC_DIALOGUE["barley_inspector"])

    def test_each_quest_can_be_played_to_completion(self):
        for key, quest in QUESTS.items():
            with self.subTest(quest=key):
                game = Game(pop_quizzes_enabled=False)
                game.state.completed_quests.update(quest.requires)
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

    def test_quest_prerequisites_form_one_complete_sequence(self):
        completed = set()
        order = []
        while len(completed) < len(QUESTS):
            available = [key for key, quest in QUESTS.items()
                         if key not in completed
                         and all(required in completed for required in quest.requires)]
            self.assertEqual(len(available), 1, (completed, available))
            completed.add(available[0])
            order.append(available[0])
        self.assertEqual(order[:7], ["orientation", "malt_house", "water_profile",
                                    "starch_structure", "protein_enzymes",
                                    "stalled_mash", "clear_wort"])
        self.assertTrue(all(quest.lead for quest in QUESTS.values()))

    def test_lecture_four_topics_have_dedicated_learning_spaces(self):
        expected = {
            "carbohydrate_lab", "glucose_bench", "disaccharide_gallery",
            "polymer_comparison", "gelatinization_chamber", "crystallinity_lab",
            "amylose_helix", "amylopectin_arbor",
        }
        self.assertEqual(
            expected,
            {room for room, region in ROOM_REGION.items() if region == "starch"},
        )
        self.assertTrue(expected.issubset(QUIZZES))
        self.assertEqual(ROOMS["mash_tun"].exits["in"], "carbohydrate_lab")
        self.assertEqual(ROOMS["gelatinization_chamber"].exits["out"], "conversion_bench")

    def test_first_test_protein_and_enzyme_topics_have_dedicated_spaces(self):
        expected = {
            "amino_acid_gallery", "peptide_bond_bench",
            "protein_structure_gallery", "folding_chamber", "denaturation_bay",
            "enzyme_catalysis_lab", "active_site_workshop",
            "enzyme_conditions_lab", "amylase_mechanism_lab",
            "mash_thickness_station", "accessory_enzyme_lab",
            "iodine_test_alcove",
        }
        self.assertEqual(
            expected,
            {room for room, region in ROOM_REGION.items() if region == "enzyme"},
        )
        self.assertTrue(expected.issubset(QUIZZES))
        self.assertEqual(ROOMS["protein_rest"].exits["in"], "amino_acid_gallery")
        self.assertEqual(ROOMS["beta_rest"].exits["in"], "amylase_mechanism_lab")
        self.assertEqual(ROOMS["alpha_rest"].exits["in"], "iodine_test_alcove")


class CommandTests(unittest.TestCase):
    def setUp(self):
        self.game = Game(rng=random.Random(7), pop_quizzes_enabled=False)
        self.game.introduction()

    def test_case_insensitive_commands_and_names(self):
        self.assertIn("QUEST STARTED", self.game.execute("TaLk COORDINATOR"))

    def test_trainer_is_a_direct_coordinator_alias(self):
        self.assertIn("QUEST STARTED", self.game.execute("talk trainer"))

    def test_coordinator_sets_an_initial_assignment_not_a_tour(self):
        intro = Game(pop_quizzes_enabled=False).introduction()
        self.assertNotIn("full brewery tour", intro.casefold())
        self.assertIn("ready to get started", intro.casefold())

    def test_coordinator_describes_a_linked_brewery(self):
        response = self.game.execute("talk coordinator")
        self.assertIn("not just a row of tanks", response)

    def test_fuzzy_npc_look(self):
        self.game.state.room = "germination_floor"
        self.assertIn("Gibberellic Acid", self.game.execute("look gibberlic acid"))

    def test_only_one_quest_can_be_active(self):
        self.game.talk("training coordinator")
        self.game.state.room = "cure_floor"
        self.game.talk("head maltster")  # orientation objective
        response = self.game.talk("head maltster")  # tries to start malt quest
        journal = self.game.journal()
        self.assertIn("ONE QUEST AT A TIME", response)
        self.assertIn("1 active", journal)
        self.assertIn("First Day", journal)
        self.assertNotIn("ACTIVE — Wake the Sleeping Grain", journal)

    def test_quests_unlock_in_sequence(self):
        game = Game(pop_quizzes_enabled=False)
        game.state.room = npc_room("head_maltster")
        self.assertIn("Complete First Day", game.talk("head maltster"))
        game.state.completed_quests.add("orientation")
        self.assertIn("QUEST STARTED — Wake the Sleeping Grain", game.talk("head maltster"))

    def test_old_overlapping_quests_are_returned_to_sequence(self):
        state = GameState.from_dict({
            "version": 2,
            "quest_stages": {"orientation": 3, "stalled_mash": 1},
        })
        game = Game(state=state, pop_quizzes_enabled=False)
        self.assertEqual(game.state.quest_stages, {"orientation": 6})
        self.assertEqual(game.reset_quest_titles, ["The Stalled Mash"])

    def test_stalled_mash_first_objective_names_the_miller(self):
        self.assertIn("Miller", QUESTS["stalled_mash"].steps[0].objective)

    def test_carbohydrate_and_enzyme_quests_precede_the_stalled_mash(self):
        self.assertEqual(QUESTS["starch_structure"].requires, ("water_profile",))
        self.assertEqual(QUESTS["protein_enzymes"].requires, ("starch_structure",))
        self.assertEqual(QUESTS["stalled_mash"].requires, ("protein_enzymes",))
        game = Game(pop_quizzes_enabled=False)
        game.state.room = "carbohydrate_lab"
        game.state.completed_quests.update({"orientation", "malt_house", "water_profile"})
        response = game.talk("curator")
        self.assertIn("QUEST STARTED — Rebuild the Carbohydrate Map", response)
        self.assertIn("Identify the monomer", response)

    def test_completed_carbohydrate_quest_leads_to_enzyme_investigation(self):
        game = Game(pop_quizzes_enabled=False)
        game.state.room = "amino_acid_gallery"
        game.state.completed_quests.update(
            {"orientation", "malt_house", "water_profile", "starch_structure"}
        )
        response = game.talk("protein chemist")
        self.assertIn("QUEST STARTED — The Enzyme That Lost Its Shape", response)
        self.assertIn("Identify the common building blocks", response)

    def test_existing_stalled_mash_save_returns_to_new_prerequisite(self):
        state = GameState(
            completed_quests={"orientation", "malt_house", "water_profile"},
            quest_stages={"stalled_mash": 2},
        )
        game = Game(state=state, pop_quizzes_enabled=False)
        self.assertEqual(game.state.quest_stages, {})
        self.assertEqual(game.reset_quest_titles, ["The Stalled Mash"])
        self.assertIn("Rebuild the Carbohydrate Map", game.journal())

    def test_stalled_mash_save_with_starch_complete_returns_to_enzyme_quest(self):
        state = GameState(
            completed_quests={
                "orientation", "malt_house", "water_profile", "starch_structure"
            },
            quest_stages={"stalled_mash": 2},
        )
        game = Game(state=state, pop_quizzes_enabled=False)
        self.assertEqual(game.state.quest_stages, {})
        self.assertEqual(game.reset_quest_titles, ["The Stalled Mash"])
        self.assertIn("The Enzyme That Lost Its Shape", game.journal())

    def test_room_description_leaves_active_objective_in_side_panel(self):
        self.game.talk("training coordinator")
        room = self.game.describe_room()
        self.assertNotIn("Objectives:", room)
        self.assertEqual(
            self.game.side_panel_data()["quest"]["objective"],
            "Find and meet the Head Maltster.",
        )

    def test_head_maltster_welcomes_player_and_explains_next_step(self):
        self.game.talk("coordinator")
        self.game.state.room = "cure_floor"
        response = self.game.talk("head maltster")
        self.assertIn("you found me", response)
        self.assertIn("incoming grain was uniform", response)
        self.assertIn("Find the Barley Inspector", response)

    def test_next_lead_explains_the_problem_and_destination(self):
        self.game.state.quest_stages = {"orientation": len(QUESTS["orientation"].steps) - 1}
        response = self.game.talk("coordinator")
        self.assertIn("NEXT LEAD — A barley lot is germinating unevenly", response)
        self.assertIn("Find Head Maltster at Malt Curing Floor", response)

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

    def test_side_panel_tracks_quest_and_regional_map(self):
        panel = self.game.side_panel_data()
        self.assertEqual(panel["quest"]["status"], "Next quest")
        self.assertEqual(panel["map"]["current_name"], "Brewery Gate")
        self.game.talk("coordinator")
        panel = self.game.side_panel_data()
        self.assertEqual(panel["quest"]["status"], "Active quest")
        self.assertEqual(panel["quest"]["title"], "First Day in the Brewery")
        self.assertIn("Head Maltster", panel["quest"]["objective"])

    def test_side_panel_map_waits_for_hidden_room_description(self):
        self.game.state.pending_room_description = "HIDDEN ROOM"
        self.assertIsNone(self.game.side_panel_data()["map"])

    def test_compact_map_marks_current_room(self):
        map_data = compact_map_data("brewery_gate")
        current = [node for row in map_data["rows"] for node in row if node["current"]]
        self.assertEqual([(node["code"], node["name"]) for node in current], [("GAT", "Brewery Gate")])

    def test_save_and_load_multiple_quests(self):
        self.game.talk("coordinator")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "save.json"
            self.assertIn("saved", self.game.save(str(path)))
            restored = Game()
            self.assertIn("loaded", restored.load(str(path)))
            self.assertEqual(restored.state.quest_stages, {"orientation": 0})


class QuizTests(unittest.TestCase):
    def test_pop_quiz_frequency_is_tuned_for_study_sessions(self):
        self.assertEqual(POP_QUIZ_INITIAL_DELAY, 4)
        self.assertEqual(POP_QUIZ_COOLDOWN, 4)
        self.assertEqual(POP_QUIZ_GUARANTEE, 7)
        self.assertEqual(POP_QUIZ_CHANCE, 0.60)

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
        self.assertIn("Press any key to continue", response)
        self.assertNotIn("SECRET ROOM DESCRIPTION", response)
        self.assertIn("SECRET ROOM DESCRIPTION", game.execute("any-key"))

    def test_candidates_require_prior_visit_not_current_room(self):
        game = Game(pop_quizzes_enabled=True)
        game.state.discovered_rooms = {"mash_tun", "kiln"}
        game.state.room = "kiln"
        self.assertEqual(game.pop_quiz_candidates(), {"mash_tun"})


class MultiplayerTests(unittest.TestCase):
    def test_chat_presence_and_following(self):
        server = MUDServer(":memory:", following_enabled=True)
        self.addCleanup(server.close)
        alice, _ = server.register("Alice", "barley-123")
        bob, _ = server.register("Bob", "maltose-123")
        self.assertIn("Alice says", server.command(alice, "say Ready?") + "\n" + "\n".join(server.poll(bob)))
        self.assertIn("begin following", server.command(bob, "follow Alice"))
        server.command(alice, "east")
        self.assertEqual(server._players[alice].game.state.room, server._players[bob].game.state.room)

    def test_group_chat_reaches_only_the_follow_group(self):
        server = MUDServer(":memory:", following_enabled=True)
        self.addCleanup(server.close)
        alice, _ = server.register("Alice", "barley-123")
        bob, _ = server.register("Bob", "maltose-123")
        carol, _ = server.register("Carol", "glucose-123")
        server.command(bob, "follow Alice")
        for player in (alice, bob, carol):
            server.poll(player)

        response = server.command(alice, "group Check beta-amylase?")

        self.assertIn("You tell your group", response)
        self.assertIn("Alice tells the group", "\n".join(server.poll(bob)))
        self.assertEqual(server.poll(carol), [])

    def test_group_chat_requires_a_follow_group(self):
        server = MUDServer(":memory:", following_enabled=True)
        self.addCleanup(server.close)
        alice, _ = server.register("Alice", "barley-123")
        self.assertIn("No one else", server.command(alice, "group Anyone here?"))

    def test_following_and_private_groups_are_disabled_by_default(self):
        server = MUDServer(":memory:")
        self.addCleanup(server.close)
        alice, _ = server.register("Alice", "barley-123")
        bob, _ = server.register("Bob", "maltose-123")
        self.assertIn("Following is disabled", server.command(bob, "follow Alice"))
        self.assertIn("Private groups are disabled", server.command(alice, "group Hello"))
        self.assertIn("You say", server.command(alice, "say Hello"))
        self.assertIn("Alice says", "\n".join(server.poll(bob)))

    def test_players_have_independent_quest_state(self):
        server = MUDServer(":memory:")
        self.addCleanup(server.close)
        alice, _ = server.register("Alice", "barley-123")
        bob, _ = server.register("Bob", "maltose-123")
        server.command(alice, "talk coordinator")
        self.assertIn("orientation", server._players[alice].game.state.quest_stages)
        self.assertNotIn("orientation", server._players[bob].game.state.quest_stages)

    def test_instructor_progress_matches_player_level(self):
        server = MUDServer(":memory:")
        self.addCleanup(server.close)
        token, _ = server.register("Alice", "barley-123")
        server.command(token, "talk coordinator")
        expected = server._players[token].game.progression_data()

        report = server.instructor_progress()

        self.assertEqual(len(report), 1)
        self.assertEqual(report[0]["name"], "Alice")
        self.assertTrue(report[0]["online"])
        for field in ("rank", "insight", "locations", "quests", "knowledge_checks", "next_rank"):
            self.assertEqual(report[0][field], expected[field])

    def test_player_progression_returns_live_level_summary(self):
        server = MUDServer(":memory:")
        self.addCleanup(server.close)
        token, _ = server.register("Alice", "barley-123")

        progress = server.player_progression(token)

        self.assertEqual(progress, server._players[token].game.progression_data())

        server.command(token, "quit")
        self.assertIsNone(server.player_progression(token))

    def test_player_side_panel_returns_live_quest_and_map_context(self):
        server = MUDServer(":memory:")
        self.addCleanup(server.close)
        token, _ = server.register("Alice", "barley-123")

        panel = server.player_side_panel(token)

        self.assertEqual(panel, server._players[token].game.side_panel_data())

    def test_account_progress_survives_logout_and_login(self):
        server = MUDServer(":memory:")
        self.addCleanup(server.close)
        token, _ = server.register("Alice", "barley-123")
        server.command(token, "talk coordinator")
        server.command(token, "north")
        saved_room = server._players[token].game.state.room
        saved_insight = server._players[token].game.state.insight
        server.logout(token)
        restored, welcome = server.login("alice", "barley-123")
        self.assertIn("saved progress has been restored", welcome)
        self.assertNotIn("TALK COORDINATOR to begin", welcome)
        self.assertIn("JOURNAL", welcome)
        self.assertEqual(server._players[restored].game.state.room, saved_room)
        self.assertEqual(server._players[restored].game.state.insight, saved_insight)
        self.assertEqual(server._players[restored].game.state.quest_stages, {"orientation": 0})

    def test_instruction_screen_is_not_mixed_into_game_output(self):
        server = MUDServer(":memory:")
        self.addCleanup(server.close)
        token, welcome = server.register("Alice", "barley-123")
        self.assertNotIn("NEW PLAYER QUICK START", welcome)
        self.assertIn("BREWMUD: The Biochemistry of Beer", welcome)
        server.logout(token)
        _restored, returning = server.login("Alice", "barley-123")
        self.assertNotIn("NEW PLAYER QUICK START", returning)

    def test_account_progress_survives_complete_server_restart(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "accounts.db"
            first = MUDServer(database)
            token, _ = first.register("Alice", "barley-123")
            first.command(token, "talk coordinator")
            first.command(token, "north")
            expected_room = first._players[token].game.state.room
            first.close()

            second = MUDServer(database)
            try:
                restored, _ = second.login("Alice", "barley-123")
                self.assertEqual(second._players[restored].game.state.room, expected_room)
                self.assertEqual(second._players[restored].game.state.quest_stages, {"orientation": 0})
            finally:
                second.close()

    def test_wrong_password_and_duplicate_account_are_rejected(self):
        server = MUDServer(":memory:")
        self.addCleanup(server.close)
        token, _ = server.register("Alice", "barley-123")
        with self.assertRaisesRegex(ValueError, "already registered"):
            server.register("alice", "different-123")
        server.logout(token)
        with self.assertRaisesRegex(ValueError, "Incorrect"):
            server.login("Alice", "wrong-pass")

    def test_browser_file_save_and_load_are_disabled(self):
        server = MUDServer(":memory:")
        self.addCleanup(server.close)
        token, _ = server.register("Alice", "barley-123")
        self.assertIn("saves automatically", server.command(token, "save ../../unsafe.json"))
        self.assertIn("saves automatically", server.command(token, "load ../../unsafe.json"))

    def test_restart_requires_confirmation_and_resets_only_progress(self):
        server = MUDServer(":memory:")
        self.addCleanup(server.close)
        token, _ = server.register("Alice", "barley-123")
        server.command(token, "talk coordinator")
        server.command(token, "north")
        old_insight = server._players[token].game.state.insight

        warning = server.command(token, "restart")
        self.assertIn("RESTART CONFIRM", warning)
        self.assertEqual(server._players[token].game.state.insight, old_insight)

        reset = server.command(token, "RESTART CONFIRM")
        self.assertIn("PROGRESS RESET", reset)
        self.assertEqual(server._players[token].game.state.quest_stages, {})
        self.assertEqual(server._players[token].game.state.completed_quizzes, set())
        self.assertEqual(server._players[token].game.state.room, "brewery_gate")
        server.logout(token)
        restored, _ = server.login("Alice", "barley-123")
        self.assertEqual(server._players[restored].game.state.quest_stages, {})
        self.assertEqual(server._players[restored].game.state.room, "brewery_gate")


class AccountStoreTests(unittest.TestCase):
    def test_passwords_are_hashed_and_state_is_serialized(self):
        store = AccountStore(":memory:")
        self.addCleanup(store.close)
        account = store.register("Cellar Student", "not-plain-text")
        row = store._connection.execute("SELECT * FROM accounts").fetchone()
        self.assertNotEqual(bytes(row["password_hash"]), b"not-plain-text")
        account.state.insight = 47
        store.save(account.id, account.state)
        self.assertEqual(store.authenticate("cellar student", "not-plain-text").state.insight, 47)
        report = store.list_progress()
        self.assertEqual(report[0].name, "Cellar Student")
        self.assertEqual(report[0].state.insight, 47)

    def test_short_password_is_rejected(self):
        store = AccountStore(":memory:")
        self.addCleanup(store.close)
        with self.assertRaisesRegex(ValueError, "at least 8"):
            store.register("Alice", "short")


class AssetTests(unittest.TestCase):
    def test_browser_assets_are_brewery_branded(self):
        static = Path(__file__).parents[1] / "brewmud" / "static"
        self.assertIn("BrewMUD", (static / "index.html").read_text())
        self.assertIn("command>", (static / "app.js").read_text())
        self.assertNotIn("brew>", (static / "app.js").read_text())
        self.assertNotIn("mito>", (static / "app.js").read_text())
        colorizer = (static / "app.js").read_text()
        self.assertIn('trimmed.startsWith("Exits:")', colorizer)
        self.assertIn('trimmed.includes("Shortest route to ")', colorizer)
        self.assertIn(': /<[A-Z0-9]{3,4}>/g;', colorizer)
        instructions = (static / "index.html").read_text()
        self.assertIn("TALK TRAIN", instructions)
        self.assertIn("Press any key to continue", instructions)
        self.assertIn("show_instructions", (static / "app.js").read_text())
        self.assertNotIn('id="group-form"', instructions)
        self.assertLess(instructions.index("Create new account"), instructions.index("Log in</button>"))

    def test_instructor_dashboard_assets(self):
        static = Path(__file__).parents[1] / "brewmud" / "static"
        page = (static / "instructor.html").read_text()
        script = (static / "instructor.js").read_text()
        self.assertIn("Instructor progress", page)
        self.assertIn("Knowledge checks", page)
        self.assertIn("/api/instructor/progress", script)
        self.assertNotIn("localStorage", script)

    def test_render_blueprint_uses_web_service_and_health_check(self):
        blueprint = (Path(__file__).parents[1] / "render.yaml").read_text()
        self.assertIn("type: web", blueprint)
        self.assertIn("python -m brewmud.web --host 0.0.0.0", blueprint)
        self.assertIn("healthCheckPath: /api/status", blueprint)
        self.assertIn("mountPath: /var/data", blueprint)
        self.assertIn("BREWMUD_DB_PATH", blueprint)
        self.assertIn("BREWMUD_ADMIN_PASSWORD", blueprint)

    def test_render_port_environment_selects_public_bind_default(self):
        from brewmud import web
        with patch.dict("os.environ", {"PORT": "10000"}, clear=True):
            self.assertEqual(web.default_bind_host(), "0.0.0.0")
        with patch.dict("os.environ", {}, clear=True):
            self.assertEqual(web.default_bind_host(), "127.0.0.1")

    def test_local_database_path_defaults_to_project_file(self):
        from brewmud import web
        with patch.dict("os.environ", {}, clear=True):
            self.assertEqual(web.account_database_path(), "brewmud.db")

    def test_render_requires_configured_mounted_persistent_storage(self):
        from brewmud import web
        with patch.dict("os.environ", {"RENDER": "true"}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "attach a disk"):
                web.account_database_path()
        with patch.dict(
            "os.environ",
            {"RENDER": "true", "BREWMUD_DB_PATH": "brewmud.db"},
            clear=True,
        ):
            with self.assertRaisesRegex(RuntimeError, "must be inside"):
                web.account_database_path()
        with patch.dict(
            "os.environ",
            {"RENDER": "true", "BREWMUD_DB_PATH": "/var/data/brewmud.db"},
            clear=True,
        ), patch.object(Path, "is_mount", return_value=False):
            with self.assertRaisesRegex(RuntimeError, "no persistent disk"):
                web.account_database_path()
        with patch.dict(
            "os.environ",
            {"RENDER": "true", "BREWMUD_DB_PATH": "/var/data/brewmud.db"},
            clear=True,
        ), patch.object(Path, "is_mount", return_value=True):
            self.assertEqual(web.account_database_path(), "/var/data/brewmud.db")

    def test_instructor_password_requires_a_configured_exact_match(self):
        from brewmud.web import instructor_password_matches
        self.assertTrue(instructor_password_matches("secret phrase", "secret phrase"))
        self.assertFalse(instructor_password_matches("wrong", "secret phrase"))
        self.assertFalse(instructor_password_matches("", ""))


if __name__ == "__main__":
    unittest.main()
