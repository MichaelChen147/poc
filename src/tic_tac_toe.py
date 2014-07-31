"""
Mini-max Tic-Tac-Toe Player
"""

#import poc_ttt_gui
import poc_ttt_provided as provided

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    winner = board.check_win()
    # regression base case
    if winner:
        #print "the winner is", winner, ":", SCORES[winner]
        #print board
        return SCORES[winner], (-1, -1)
    
    # inductive case - check minimax score for all possible player moves
    res_score = None
    res_move = (-1, -1)
    for cell in board.get_empty_squares():
        # checking cell move for player
        mm_board = board.clone()
        mm_board.move(cell[0], cell[1], player)
        mm_player = provided.switch_player(player)
        # the best (minimal) score according to all possible moves by other player
        score = mm_move(mm_board, mm_player)[0]
        # this move is better than others
        if res_score == None or score*SCORES[player] > res_score*SCORES[player]:
            res_score, res_move = score, cell
        # this move makes the player win, no need to check other possible moves
        if res_score*SCORES[player] == 1:
            return (res_score, res_move)
    return (res_score, res_move)


def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
