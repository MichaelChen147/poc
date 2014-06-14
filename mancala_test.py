from poc_simpletest import TestSuite
from mancala import SolitaireMancala


class SolitaireMancalaTest(TestSuite):

    def __init__(self):
        TestSuite.__init__(self)

    def run(self):
        self.test_set_board()
        self.test_is_legal_move()
        self.test_apply_move()
        self.test_choose_move()
        self.test_is_game_won()
        self.test_plan_moves()
        self.report_results()

    def test_set_board(self):
        game = SolitaireMancala()
        self.run_test(str(game.set_board([0, 1, 2, 3, 4, 5, 6])), \
                            '[6, 5, 4, 3, 2, 1, 0]')
        self.run_test(str(game.set_board([0, 1, 4, 3, 2, 5, 3])), \
                            '[3, 5, 2, 3, 4, 1, 0]')

    def test_is_legal_move(self):
        game = SolitaireMancala()
        game.set_board([0, 1, 4, 3, 2, 5, 3])
        self.run_test(game.is_legal_move(0), False, 'Moving from store should be illegal')
        self.run_test(game.is_legal_move(1), True)
        self.run_test(game.is_legal_move(2), False)
        self.run_test(game.is_legal_move(3), True)

    def test_apply_move(self):
        game = SolitaireMancala()
        game.set_board([0, 1, 4, 3, 2, 5, 3])
        self.run_test(str(game.apply_move(1)), \
                            '[3, 5, 2, 3, 4, 0, 1]')
        self.run_test(str(game.apply_move(3)), \
                            '[3, 5, 2, 0, 5, 1, 2]')
        self.run_test(str(game.apply_move(5)), \
                            '[3, 0, 3, 1, 6, 2, 3]')

    def test_choose_move(self):
        game = SolitaireMancala()
        game.set_board([0, 1, 2, 3, 4, 5, 6])
        self.run_test(game.choose_move(), 1)
        game.set_board([2, 0, 5, 0, 2, 5, 3])
        self.run_test(game.choose_move(), 5)
        game.set_board([2, 0, 5, 0, 2, 0, 3])
        self.run_test(game.choose_move(), 0)
        game.set_board([4, 1, 1, 0, 4, 5, 6])
        self.run_test(game.choose_move(), 1)

    def test_is_game_won(self):
        game = SolitaireMancala()
        game.set_board([0, 1, 2, 3, 4, 5, 6])
        self.run_test(game.is_game_won(), False)
        game.set_board([2, 0, 5, 0, 2, 0, 3])
        self.run_test(game.is_game_won(), False)
        game.set_board([6, 0, 0, 0, 0, 0, 0])
        self.run_test(game.is_game_won(), True)

    def test_plan_moves(self):
        game = SolitaireMancala()

        game.set_board([0, 1, 0, 0, 2, 4, 6])
        self.run_test(game.plan_moves(), \
                            [1, 6, 1, 5, 1, 2, 1, 4, 1, 3, 1, 2, 1])
        self.run_test(str(game), '[6, 4, 2, 0, 0, 1, 0]')

        game.set_board([0, 0, 0, 3, 0, 0, 0])
        self.run_test(game.plan_moves(), [3, 1])
        self.run_test(str(game), '[0, 0, 0, 3, 0, 0, 0]')

        game.set_board([6, 0, 0, 0, 0, 0, 0])
        self.run_test(game.plan_moves(), [])


if __name__ == '__main__':
    test = SolitaireMancalaTest()
    test.run()

