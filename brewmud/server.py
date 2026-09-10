from __future__ import annotations

import re
import secrets
import threading
from dataclasses import dataclass, field

from .game import Game


@dataclass
class PlayerSession:
    name: str
    game: Game = field(default_factory=Game)
    messages: list[str] = field(default_factory=list)
    following: str | None = None


class MUDServer:
    """Thread-safe shared world wrapped around per-player game state.

    Room occupancy and chat are shared. Quest progress and inventories currently
    belong to individual players; later party quests can live alongside them.
    """

    def __init__(self) -> None:
        self._players: dict[str, PlayerSession] = {}
        self._lock = threading.RLock()

    def login(self, requested_name: str) -> tuple[str, str]:
        name = " ".join(requested_name.strip().split())
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9 _-]{1,23}", name):
            raise ValueError("Names must be 2–24 characters and begin with a letter.")
        with self._lock:
            if any(player.name.casefold() == name.casefold() for player in self._players.values()):
                raise ValueError("That name is already in use.")
            token = secrets.token_urlsafe(24)
            session = PlayerSession(name=name)
            self._players[token] = session
            self._broadcast(session.game.state.room, f"{name} checks in for a brewery shift.", exclude=token)
            welcome = session.game.introduction() + self._occupants_text(token)
            return token, welcome

    def logout(self, token: str) -> None:
        with self._lock:
            session = self._require(token)
            room = session.game.state.room
            name = session.name
            self._end_follow_relationships(token)
            del self._players[token]
            self._broadcast(room, f"{name} has left the brewery.")

    def command(self, token: str, raw_command: str) -> str:
        with self._lock:
            session = self._require(token)
            command = raw_command.strip()
            if not command:
                return ""

            verb, _, argument = command.partition(" ")
            if verb.lower() in {"say", "chat"}:
                return self._say(token, argument)
            if verb.lower() == "who":
                return self._who(token)
            if verb.lower() == "follow":
                return self._follow(token, argument)
            if verb.lower() in {"unfollow", "nofollow"}:
                return self._unfollow(token)
            if verb.lower() == "help":
                response = (
                    session.game.help()
                    + "\n  SAY <message>       Speak to players in your room"
                    + "\n  WHO                 List nearby and online players"
                    + "\n  FOLLOW <player>     Move with another player"
                    + "\n  UNFOLLOW            Stop following"
                )
                if session.game.awaiting_quiz_continue:
                    response += "\n\nCONTINUE — Press C to reveal the room."
                return response

            if self._is_movement_command(command) and session.game.state.active_quiz is None:
                return self._move_group(token, command)

            old_room = session.game.state.room
            pending_room_before = session.game.state.pending_room_description is not None
            response = session.game.execute(command)
            new_room = session.game.state.room
            if verb.lower() in {"quit", "exit"}:
                name = session.name
                self._end_follow_relationships(token)
                del self._players[token]
                self._broadcast(old_room, f"{name} has left the brewery.")
                return response
            if old_room != new_room:
                self._broadcast(old_room, f"{session.name} departs.", exclude=token)
                self._broadcast(new_room, f"{session.name} arrives.", exclude=token)
                response += self._occupants_text(token)
            elif verb.lower() in {"look", "l"} and not argument:
                response += self._occupants_text(token)
            elif pending_room_before and session.game.state.pending_room_description is None:
                response += self._occupants_text(token)
            return response

    def poll(self, token: str) -> list[str]:
        with self._lock:
            session = self._require(token)
            messages = session.messages[:]
            session.messages.clear()
            return messages

    def player_count(self) -> int:
        with self._lock:
            return len(self._players)

    def _say(self, token: str, message: str) -> str:
        session = self._require(token)
        message = message.strip()
        if not message:
            return "Say what?"
        if len(message) > 500:
            return "Please keep messages under 500 characters."
        room = session.game.state.room
        self._broadcast(room, f'{session.name} says, “{message}”', exclude=token)
        return f'You say, “{message}”'

    def _who(self, token: str) -> str:
        session = self._require(token)
        here = [p.name for p in self._players.values() if p.game.state.room == session.game.state.room]
        everyone = sorted(p.name for p in self._players.values())
        lines = [f"Here: {', '.join(sorted(here))}", f"Online ({len(everyone)}): {', '.join(everyone)}"]
        if session.following in self._players:
            lines.append(f"Following: {self._players[session.following].name}")
        followers = sorted(
            player.name for player in self._players.values() if player.following == token
        )
        if followers:
            lines.append(f"Followers: {', '.join(followers)}")
        return "\n".join(lines)

    def _follow(self, token: str, requested_name: str) -> str:
        session = self._require(token)
        requested_name = requested_name.strip().casefold()
        if not requested_name:
            return "Follow whom? Try FOLLOW <player>."

        candidates = [
            (other_token, player)
            for other_token, player in self._players.items()
            if player.name.casefold().startswith(requested_name)
        ]
        exact = [entry for entry in candidates if entry[1].name.casefold() == requested_name]
        if exact:
            candidates = exact
        if not candidates:
            return "That player is not online."
        if len(candidates) > 1:
            return "Be more specific: " + ", ".join(sorted(player.name for _, player in candidates)) + "."

        leader_token, leader = candidates[0]
        if leader_token == token:
            return "You cannot follow yourself."
        if leader.game.state.room != session.game.state.room:
            return f"{leader.name} is not in this room."

        ancestor = leader_token
        while ancestor in self._players:
            if ancestor == token:
                return "That would create a follow loop."
            ancestor = self._players[ancestor].following
            if ancestor is None:
                break

        if session.following == leader_token:
            return f"You are already following {leader.name}."
        self._detach(token, notify=True)
        session.following = leader_token
        leader.messages.append(f"{session.name} begins following you.")
        return (
            f"You begin following {leader.name}. When {leader.name} moves, you will move too.\n"
            "Your pop quizzes remain private; use SAY to discuss them with the group."
        )

    def _unfollow(self, token: str) -> str:
        session = self._require(token)
        if session.following is None:
            return "You are not following anyone."
        leader_name = self._players.get(session.following)
        name = leader_name.name if leader_name else "your leader"
        self._detach(token, notify=True)
        return f"You stop following {name}."

    def _detach(self, token: str, *, notify: bool) -> None:
        session = self._require(token)
        leader_token = session.following
        session.following = None
        if notify and leader_token in self._players:
            self._players[leader_token].messages.append(f"{session.name} stops following you.")

    def _end_follow_relationships(self, token: str) -> None:
        departing = self._require(token)
        if departing.following in self._players:
            self._players[departing.following].messages.append(
                f"{departing.name} stops following you."
            )
        for follower in self._players.values():
            if follower.following == token:
                follower.following = None
                follower.messages.append(f"{departing.name} is no longer here; you stop following.")

    @staticmethod
    def _is_movement_command(command: str) -> bool:
        verb = command.casefold().split(maxsplit=1)[0]
        return verb in {
            "north", "south", "east", "west", "up", "down", "in", "out",
            "n", "s", "e", "w", "u", "d", "i", "o", "go", "move", "walk",
        }

    def _move_group(self, token: str, command: str) -> str:
        """Move a leader and the connected followers who share the origin room."""
        leader = self._require(token)
        origin = leader.game.state.room
        group = self._followers_in_room(token, origin)
        blocked = [
            (
                self._players[follower_token].name,
                "answer A–D or PAUSE"
                if self._players[follower_token].game.state.active_quiz is not None
                else "press C to continue",
            )
            for follower_token in group[1:]
            if (
                self._players[follower_token].game.state.active_quiz is not None
                or self._players[follower_token].game.awaiting_quiz_continue
            )
        ]
        if blocked:
            details = ", ".join(f"{name} ({action})" for name, action in blocked)
            return (
                f"Group movement waits for {details}. "
                "The group can continue discussing the question with SAY."
            )

        previous_leader = leader.following
        synchronize_quiz = len(group) > 1 and not any(
            self._players[group_token].game.state.paused_quiz is not None
            for group_token in group
        )
        quiz_settings = {
            group_token: self._players[group_token].game.pop_quizzes_enabled
            for group_token in group
        }
        if synchronize_quiz:
            for group_token in group:
                self._players[group_token].game.pop_quizzes_enabled = False
        try:
            response = leader.game.execute(command)
        finally:
            leader.game.pop_quizzes_enabled = quiz_settings[token]
        destination = leader.game.state.room
        if destination == origin:
            for group_token in group[1:]:
                self._players[group_token].game.pop_quizzes_enabled = quiz_settings[group_token]
            return response
        breakaway = ""
        if previous_leader is not None:
            previous_name = self._players.get(previous_leader)
            display_name = previous_name.name if previous_name else "your leader"
            self._detach(token, notify=True)
            breakaway = f"You stop following {display_name} and move independently.\n"

        moved = [token]
        movement_results = {token: response}
        for follower_token in group[1:]:
            follower = self._players[follower_token]
            try:
                result = follower.game.execute(command)
            finally:
                follower.game.pop_quizzes_enabled = quiz_settings[follower_token]
            if follower.game.state.room == destination:
                moved.append(follower_token)
                movement_results[follower_token] = result

        if synchronize_quiz:
            quiz_members = [moved_token for moved_token in moved if quiz_settings[moved_token]]
            if quiz_members:
                common_questions = set.intersection(
                    *(self._players[moved_token].game.pop_quiz_candidates() for moved_token in quiz_members)
                )
                quiz_key = None
                for moved_token in quiz_members:
                    game = self._players[moved_token].game
                    if game._maybe_pop_quiz(common_questions):
                        quiz_key = game.state.active_quiz
                        break
                if quiz_key is not None:
                    for moved_token in quiz_members:
                        game = self._players[moved_token].game
                        movement_results[moved_token] = game.begin_group_quiz(
                            quiz_key, movement_results[moved_token]
                        )

        moving_tokens = set(moved)
        for moved_token in moved:
            moving_player = self._players[moved_token]
            self._broadcast(origin, f"{moving_player.name} departs.", exclude=moving_tokens)
            self._broadcast(destination, f"{moving_player.name} arrives.", exclude=moving_tokens)

        for follower_token in moved[1:]:
            follower = self._players[follower_token]
            direct_leader = self._players.get(follower.following)
            leader_name = direct_leader.name if direct_leader else leader.name
            occupants = (
                "" if follower.game.state.pending_room_description is not None
                else self._occupants_text(follower_token)
            )
            follower.messages.append(
                f"You follow {leader_name}.\n\n{movement_results[follower_token]}{occupants}"
            )
        occupants = (
            "" if leader.game.state.pending_room_description is not None
            else self._occupants_text(token)
        )
        return breakaway + movement_results[token] + occupants

    def _followers_in_room(self, leader_token: str, room: str) -> list[str]:
        group = [leader_token]
        index = 0
        while index < len(group):
            current = group[index]
            group.extend(
                token
                for token, player in self._players.items()
                if player.following == current
                and player.game.state.room == room
                and token not in group
            )
            index += 1
        return group

    def _occupants_text(self, token: str) -> str:
        session = self._require(token)
        others = sorted(
            player.name
            for other_token, player in self._players.items()
            if other_token != token and player.game.state.room == session.game.state.room
        )
        return "\nPlayers here: " + (", ".join(others) if others else "none") + "."

    def _broadcast(self, room: str, message: str, exclude: str | set[str] | None = None) -> None:
        excluded = {exclude} if isinstance(exclude, str) else (exclude or set())
        for token, session in self._players.items():
            if token not in excluded and session.game.state.room == room:
                session.messages.append(message)

    def _require(self, token: str) -> PlayerSession:
        try:
            return self._players[token]
        except KeyError as exc:
            raise KeyError("Session not found; please log in again.") from exc
