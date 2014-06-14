"""
Clone of 2048 game.
"""

import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


def should_merge_tiles(line, last_tile_merged):
    """
    Check if last two tiles in a line should be merged
    """
    return len(line) > 1 and line[-1] == line[-2] \
        and not last_tile_merged


def merge_tiles(line, last_tile_merged):
    """
    Merge last two tiles in a line if necessary
    Return resulting line and flag indication if the merge occured
    """
    if should_merge_tiles(line, last_tile_merged):
        line[-2] += line[-1]
        line.pop()
        last_tile_merged = True
    else:
        last_tile_merged = False
    return line, last_tile_merged


def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    merged_line = []
    last_tile_merged = False
    for tile in line:
        if tile != 0:
            merged_line.append(tile)
            merged_line, last_tile_merged = merge_tiles(merged_line, last_tile_merged)
    while len(merged_line) < len(line):
        merged_line.append(0)
    return merged_line


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.height = grid_height
        self.width = grid_width
        self.reset()
        self.sides = {UP: [(0, col) for col in range(self.width)],
                      DOWN: [(self.height - 1, col) for col in range(self.width)],
                      LEFT: [(row, 0) for row in range(self.height)],
                      RIGHT: [(row, self.width - 1) for row in range(self.height)]}

    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        self.grid = [[0 for dummy_col in range(self.width)] for dummy_row in range(self.height)]

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return '\n'.join([str(row) for row in self.grid])

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.width

    def get_side(self, direction):
        """
        Get one of the four sides on the grid,
        as specified in direction parameter.
        """
        return self.sides[direction]

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        side = self.get_side(direction)
        grid_changed = False
        for start_tile in side:
            line = self.get_line(start_tile, OFFSETS[direction])
            merged_line = merge(line)
            grid_changed = self.set_line(start_tile, OFFSETS[direction], merged_line) or grid_changed

        if grid_changed:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        value = 2 if random.random() < 0.9 else 4
        empty_tiles = [(row, col) \
                       for col in range(self.width) \
                       for row in range(self.height) \
                       if self.get_tile(row, col) == 0]
        if empty_tiles:
            tile = random.choice(empty_tiles)
            self.set_tile(tile[0], tile[1], value)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.grid[row][col]

    def set_line(self, start_tile, offset, new_line):
        """
        Set values of a line of tiles, starting at start_tile
        and moving by one offset at a time.
        Return flag indicating if line has changed comapred to it's previous state.
        """
        row = start_tile[0]
        col = start_tile[1]
        line_changed = False
        for new_value in new_line:
            old_value = self.get_tile(row, col)
            if old_value != new_value:
                line_changed = True
            self.set_tile(row, col, new_value)
            row += offset[0]
            col += offset[1]
        return line_changed

    def get_line(self, start_tile, offset):
        """
        Return values of a line of tiles, starting at start_tile
        and moving by one offset at a time
        """
        row = start_tile[0]
        col = start_tile[1]
        line = []
        while 0 <= row < self.height and 0 <= col < self.width:
            line.append(self.get_tile(row, col))
            row += offset[0]
            col += offset[1]
        return line


# import poc_2048_gui
# poc_2048_gui.run_gui(TwentyFortyEight(4, 4))

