import unittest
from main import HangmanCore, GameState


class Testing(unittest.TestCase):
    def setUp(self) -> None:
        self.core = HangmanCore("idiot")

    def test_wrong_input(self):
        for inp_str in ["aa", "", 1]:
            message = self.core.make_guess(inp_str)
            assert message.error == "Specify only one letter"

    def test_correct_guess(self):
        message = self.core.make_guess("d")
        assert not message.state_has_changed
        assert message.is_correct_guess
        assert message.censored_word == "".join([letter if letter == "d" else "*" for letter in self.core.word])

    def test_mistake(self):
        for inp_letter in ["g", "h", "a", "m"]:
            message = self.core.make_guess(inp_letter)
            assert not message.state_has_changed
            assert not message.is_correct_guess
            assert message.censored_word == "*" * len(self.core.word)

    def test_win(self):
        for inp_letter in ["i", "d", "o", "t"]:
            message = self.core.make_guess(inp_letter)
        assert message.state_has_changed
        assert self.core.state == GameState.WIN

    def test_lose(self):
        for inp_letter in ["a", "m", "p", "k", "f"]:
            message = self.core.make_guess(inp_letter)
        assert message.state_has_changed
        assert self.core.state == GameState.LOSE


if __name__ == '__main__':
    unittest.main()
