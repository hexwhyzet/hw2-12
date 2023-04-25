from dataclasses import dataclass
from random import choice
from enum import Enum


class GameState(Enum):
    RUNNING = 0
    LOSE = 1
    WIN = 2


@dataclass
class GameMessage:
    censored_word: str = None
    is_correct_guess: bool = True
    mistakes_counter: int = None
    error: str = None
    state_has_changed: bool = False


POOL = ["black", "game", "challenge", "song", "phrase", "reinforcement"]
MAX_MISTAKES = 5


class HangmanCore:
    def __init__(self, word):
        self.word = word
        assert isinstance(self.word, str) and len(self.word)
        self.state = GameState.RUNNING
        self.guesses = [False] * len(self.word)
        self.attempts_letters = set()
        self.mistakes_counter = 0

    def censored_word(self):
        ans = ""
        for i, letter in enumerate(self.word):
            if self.guesses[i]:
                ans += letter
            else:
                ans += "*"
        return ans

    def word_length(self):
        return len(self.word)

    def make_guess(self, letter: str) -> GameMessage:
        if self.state != GameState.RUNNING:
            return GameMessage(error="Game is already finished")

        if not isinstance(letter, str) or len(letter) != 1:
            return GameMessage(error="Specify only one letter")

        if letter in self.attempts_letters:
            return GameMessage(error="This letter has already been tried")

        is_mistake = True
        for i, correct_letter in enumerate(self.word):
            if correct_letter == letter:
                is_mistake = False
                self.guesses[i] = True
        self.attempts_letters.add(letter)
        if is_mistake:
            self.mistakes_counter += 1
            if self.mistakes_counter >= MAX_MISTAKES:
                self.state = GameState.LOSE
                return GameMessage(censored_word=self.censored_word(), state_has_changed=True, is_correct_guess=False)
            return GameMessage(censored_word=self.censored_word(), is_correct_guess=False,
                               mistakes_counter=self.mistakes_counter)
        if all(self.guesses):
            self.state = GameState.WIN
            return GameMessage(censored_word=self.censored_word(), state_has_changed=True)
        return GameMessage(censored_word=self.censored_word(), is_correct_guess=True,
                           mistakes_counter=self.mistakes_counter)


class HangmanGame:
    def __init__(self):
        self.core = HangmanCore(choice(POOL))

    def start(self):
        print("Game started!")
        print(f"Word has {self.core.word_length()} letters")
        while self.core.state == GameState.RUNNING:
            print(f"The word: {self.core.censored_word()}")
            letter = input("Guess a letter: ")
            message = self.core.make_guess(letter)
            if message.error is not None:
                print(message.error)
                continue
            if message.is_correct_guess:
                print("Hit!")
            else:
                print(f"Missed, mistake {message.mistakes_counter} out of {MAX_MISTAKES}.")
            if message.state_has_changed:
                if self.core.state == GameState.WIN:
                    print("You won!")
                else:
                    print("You lost!")
        print("Game is over!")


if __name__ == '__main__':
    game = HangmanGame()
    game.start()
