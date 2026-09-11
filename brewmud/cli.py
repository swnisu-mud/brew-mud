from __future__ import annotations

from .game import Game


def main() -> None:
    game = Game()
    print(game.introduction())
    while game.running:
        try:
            command = input("\ncommand> ")
        except (EOFError, KeyboardInterrupt):
            print("\nYour brewery shift ends—for now.")
            break
        response = game.execute(command)
        if response:
            print(response)
