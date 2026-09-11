"""SQLite-backed BrewMUD accounts and automatic game-state persistence."""

from __future__ import annotations

import hashlib
import hmac
import json
import secrets
import sqlite3
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .models import GameState


PASSWORD_ITERATIONS = 600_000


@dataclass(frozen=True)
class Account:
    id: int
    name: str
    state: GameState


@dataclass(frozen=True)
class AccountProgress:
    id: int
    name: str
    state: GameState
    created_at: str
    updated_at: str


class AccountStore:
    def __init__(self, database_path: str | Path) -> None:
        path = str(database_path)
        if path != ":memory:":
            Path(path).expanduser().parent.mkdir(parents=True, exist_ok=True)
            path = str(Path(path).expanduser())
        self._connection = sqlite3.connect(path, check_same_thread=False)
        self._connection.row_factory = sqlite3.Row
        self._lock = threading.RLock()
        with self._lock, self._connection:
            self._connection.execute("PRAGMA journal_mode=WAL")
            self._connection.execute("PRAGMA busy_timeout=5000")
            self._connection.execute(
                """CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    name_key TEXT NOT NULL UNIQUE,
                    password_salt BLOB NOT NULL,
                    password_hash BLOB NOT NULL,
                    password_iterations INTEGER NOT NULL,
                    state_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )"""
            )

    def register(self, name: str, password: str) -> Account:
        self._validate_password(password)
        salt = secrets.token_bytes(16)
        password_hash = self._hash_password(password, salt, PASSWORD_ITERATIONS)
        state = GameState()
        now = datetime.now(timezone.utc).isoformat()
        try:
            with self._lock, self._connection:
                cursor = self._connection.execute(
                    """INSERT INTO accounts
                       (name, name_key, password_salt, password_hash, password_iterations,
                        state_json, created_at, updated_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (name, name.casefold(), salt, password_hash, PASSWORD_ITERATIONS,
                     json.dumps(state.to_dict()), now, now),
                )
        except sqlite3.IntegrityError as exc:
            raise ValueError("That account name is already registered. Try logging in.") from exc
        return Account(int(cursor.lastrowid), name, state)

    def authenticate(self, name: str, password: str) -> Account:
        self._validate_password(password)
        # Perform a real hash even for an unknown name to reduce timing leakage.
        with self._lock:
            row = self._connection.execute(
                "SELECT * FROM accounts WHERE name_key = ?", (name.casefold(),)
            ).fetchone()
        if row is None:
            salt, expected, iterations = bytes(16), bytes(32), PASSWORD_ITERATIONS
        else:
            salt = bytes(row["password_salt"])
            expected = bytes(row["password_hash"])
            iterations = int(row["password_iterations"])
        supplied = self._hash_password(password, salt, iterations)
        if row is None or not hmac.compare_digest(supplied, expected):
            raise ValueError("Incorrect account name or password.")
        try:
            state = GameState.from_dict(json.loads(str(row["state_json"])))
        except (TypeError, ValueError, json.JSONDecodeError) as exc:
            raise ValueError("This account's saved progress is damaged; contact the instructor.") from exc
        return Account(int(row["id"]), str(row["name"]), state)

    def save(self, account_id: int, state: GameState) -> None:
        now = datetime.now(timezone.utc).isoformat()
        state_json = json.dumps(state.to_dict(), separators=(",", ":"))
        with self._lock, self._connection:
            cursor = self._connection.execute(
                "UPDATE accounts SET state_json = ?, updated_at = ? WHERE id = ?",
                (state_json, now, account_id),
            )
            if cursor.rowcount != 1:
                raise KeyError("Account no longer exists.")

    def list_progress(self) -> list[AccountProgress]:
        with self._lock:
            rows = self._connection.execute(
                "SELECT id, name, state_json, created_at, updated_at "
                "FROM accounts ORDER BY name_key"
            ).fetchall()
        progress = []
        for row in rows:
            state = GameState.from_dict(json.loads(str(row["state_json"])))
            progress.append(AccountProgress(
                id=int(row["id"]),
                name=str(row["name"]),
                state=state,
                created_at=str(row["created_at"]),
                updated_at=str(row["updated_at"]),
            ))
        return progress

    def close(self) -> None:
        with self._lock:
            self._connection.close()

    @staticmethod
    def _validate_password(password: str) -> None:
        if len(password) < 8:
            raise ValueError("Passwords must contain at least 8 characters.")
        if len(password) > 128:
            raise ValueError("Passwords must contain no more than 128 characters.")

    @staticmethod
    def _hash_password(password: str, salt: bytes, iterations: int) -> bytes:
        return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
