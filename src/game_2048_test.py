from poc_simpletest import TestSuite
from game_2048 import should_merge_tiles, merge_tiles, \
    merge, UP, DOWN, LEFT, RIGHT, OFFSETS, TwentyFortyEight

class TwentyFortyEightTest(TestSuite):

    def __init__(self):
        TestSuite.__init__(self)

    def run(self):
        self.test_should_merge_tiles()
        self.test_merge_tiles()
        self.test_merge()
        self.test_init_game()
        self.test_change_tile()
        self.test_new_tile()
        self.test_get_sides()
        self.test_get_line()
        self.test_set_line()
        self.test_move()
        self.report_results()

    def test_should_merge_tiles(self):
        self.run_test(should_merge_tiles([2], False), False,
                      'Should not merge line with single tile')
        self.run_test(should_merge_tiles([2, 2], False), True,
                      'Should merge line with equal last two tiles')
        self.run_test(should_merge_tiles([4, 4], True), False,
                      'Should not merge line with equal last two tiles after previous merge')

    def test_merge_tiles(self):
        self.run_test(merge_tiles([2], False), ([2], False),
                      'Does not merge line with single tile')
        self.run_test(merge_tiles([2, 2], False), ([4], True),
                      'Merges line with equal last two tiles')
        self.run_test(merge_tiles([4, 4], True), ([4, 4], False),
                      'Does not merge line with equal last two tiles after previous merge')

    def test_merge(self):
        self.run_test(merge([2, 0, 2, 4]), [4, 4, 0, 0],
                      'Test merge #1')
        self.run_test(merge([0, 0, 2, 2]), [4, 0, 0, 0],
                      'Test merge #2')
        self.run_test(merge([2, 2, 0, 0]), [4, 0, 0, 0],
                      'Test merge #3')
        self.run_test(merge([2, 2, 2, 2]), [4, 4, 0, 0],
                      'Test merge #4')
        self.run_test(merge([8, 16, 16, 8]), [8, 32, 8, 0],
                      'Test merge #5')

    def test_init_game(self):
        game = TwentyFortyEight(5, 4)
        self.run_test(game.get_grid_height(), 5,
                      'Initializes grid height propery')
        self.run_test(game.get_grid_width(), 4,
                      'Initializes grid width propery')
        self.run_test(game.get_tile(2, 1), 0,
                      'Initializes tile values to zero')

    def test_change_tile(self):
        game = TwentyFortyEight(5, 4)
        game.set_tile(2, 1, 8)
        self.run_test(game.get_tile(2, 1), 8,
                      'Changes tile value to non-empty')
        game.set_tile(2, 1, 0)
        self.run_test(game.get_tile(2, 1), 0,
                      'Changes tile value back to empty')

    def test_new_tile(self):
        game = TwentyFortyEight(1, 1)
        game.new_tile()
        self.run_test(game.get_tile(0, 0) != 0, True,
                      'Creates new tile when there are empty tiles in 1x1 grid')

        game = TwentyFortyEight(2, 2)
        game.new_tile()
        nonempty_count = sum([0 if game.get_tile(row, col) == 0 else 1 \
                              for col in range(game.get_grid_width()) \
                              for row in range(game.get_grid_height())])
        self.run_test(nonempty_count, 1,
                      'Creates new tile when there are empty tiles in 2x2 grid')

        game = TwentyFortyEight(1,1)
        game.set_tile(0, 0, 8)
        game.new_tile()
        self.run_test(game.get_tile(0, 0), 8,
                      'Does not create new tile when there are no empty tiles')

    def test_get_sides(self):
        game = TwentyFortyEight(3, 2)
        self.run_test(game.get_side(UP), [(0, 0), (0, 1)],
                      'UP side')
        self.run_test(game.get_side(DOWN), [(2, 0), (2, 1)],
                      'DOWN side')
        self.run_test(game.get_side(LEFT), [(0, 0), (1, 0), (2, 0)],
                      'LEFT side')
        self.run_test(game.get_side(RIGHT), [(0, 1), (1, 1), (2, 1)],
                      'RIGHT side')

    def test_get_line(self):
        game = TwentyFortyEight(2, 3)
        # 1 2 3
        # 4 5 6
        game.set_tile(0, 0, 1)
        game.set_tile(0, 1, 2)
        game.set_tile(0, 2, 3)
        game.set_tile(1, 0, 4)
        game.set_tile(1, 1, 5)
        game.set_tile(1, 2, 6)

        self.run_test(game.get_line((0, 0), OFFSETS[UP]),
                      [1, 4],
                      'Line to merge when moving UP')
        self.run_test(game.get_line((1, 2), OFFSETS[DOWN]),
                      [6, 3],
                      'Line to merge when moving DOWN')
        self.run_test(game.get_line((1, 0), OFFSETS[LEFT]),
                      [4, 5, 6],
                      'Line to merge when moving LEFT')
        self.run_test(game.get_line((0, 2), OFFSETS[RIGHT]),
                      [3, 2, 1],
                      'Line to merge when moving RIGHT')

    def test_set_line(self):
        game = TwentyFortyEight(2, 3)
        # 1 2 0
        # 4 5 6
        game.set_tile(0, 0, 1)
        game.set_tile(0, 1, 2)
        game.set_tile(0, 2, 0)
        game.set_tile(1, 0, 4)
        game.set_tile(1, 1, 5)
        game.set_tile(1, 2, 6)
        line_changed = game.set_line((0, 2), OFFSETS[RIGHT], [2, 1, 0])
        # 0 1 2
        # 4 5 6

        self.run_test(line_changed, True, 'Line has changed')
        self.run_test(game.get_tile(0, 0), 0, 'Moving line RIGHT #1')
        self.run_test(game.get_tile(0, 1), 1, 'Moving line RIGHT #2')
        self.run_test(game.get_tile(0, 2), 2, 'Moving line RIGHT #3')

        line_changed = game.set_line((1, 0), OFFSETS[DOWN], [4, 0])
        self.run_test(line_changed, False, 'Line has not changed')
        self.run_test(game.get_tile(0, 0), 0, 'Moving DOWN #1')
        self.run_test(game.get_tile(1, 0), 4, 'Moving DOWN #2')

    def test_move(self):
        game = TwentyFortyEight(3, 3)
        # 1 2 0
        # 4 0 6
        # 0 8 9
        game.set_tile(0, 0, 1)
        game.set_tile(0, 1, 2)
        game.set_tile(0, 2, 0)
        game.set_tile(1, 0, 4)
        game.set_tile(1, 1, 0)
        game.set_tile(1, 2, 6)
        game.set_tile(2, 0, 0)
        game.set_tile(2, 1, 8)
        game.set_tile(2, 2, 9)

        game.move(RIGHT)
        # 0 1 2
        # 0 4 6
        # 0 8 9
        self.run_test(game.get_tile(0, 1), 1, 'Moving RIGHT (0, 1)')
        self.run_test(game.get_tile(0, 2), 2, 'Moving RIGHT (0, 2)')
        self.run_test(game.get_tile(1, 1), 4, 'Moving RIGHT (1, 1)')
        self.run_test(game.get_tile(1, 2), 6, 'Moving RIGHT (1, 2)')
        self.run_test(game.get_tile(2, 1), 8, 'Moving RIGHT (2, 1)')
        self.run_test(game.get_tile(2, 2), 9, 'Moving RIGHT (2, 2)')


if __name__ == '__main__':
    test_suite = TwentyFortyEightTest()
    test_suite.run()
