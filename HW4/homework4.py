############################################################
# CIS 521: adversarial_search
############################################################

student_name = "Type your full name here."

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

import collections
import copy
import itertools
import random
import math
import numpy as np

############################################################
# Section 1: Dominoes Game
############################################################

def create_dominoes_game(rows, cols):
    return DominoesGame([[False for i in range(cols)] for j in range(rows)])

class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.board = board
        self.nrows = len(self.board)
        self.ncols = len(self.board[0])
    
    def get_board(self):
        return self.board
    
    def reset(self):
        self.board = [[False for i in range(self.ncols)] for j in range(self.nrows)]
        
    def is_legal_move(self, row, col, vertical):
        board = self.board
        if vertical:
            if row >= len(board) - 1:
                return False
            else:
                if not board[row][col] and not board[row+1][col]:
                    return True
                else:
                    return False
        else:
            if col >= len(board[0]) - 1:
                return False
            else:
                if not board[row][col] and not board[row][col+1]:
                    return True
                else:
                    return False
                
    def legal_moves(self, vertical):
        
        for row in range(self.nrows):
            for col in range(self.ncols):
                if self.is_legal_move(row, col, vertical):
                    yield (row, col)
                    
    def perform_move(self, row, col, vertical):
        
        if self.is_legal_move(row, col, vertical):
            if vertical:
                self.board[row][col] = True
                self.board[row+1][col] = True
            else:
                self.board[row][col] = True
                self.board[row][col+1] = True
    
    def game_over(self, vertical):
        if len(list(self.legal_moves(vertical))) == 0:
            return True
        else:
            return False
            
    def copy(self):
        return copy.deepcopy(self)
    
    def successors(self, vertical):
        
        for move in self.legal_moves(vertical):
            new_g = self.copy()
            new_g.perform_move(move[0],move[1],vertical)
            yield move, new_g
            
    # required
    def get_best_move(self, vertical, limit):
        return self.max_value(vertical, vertical, limit, float("-inf"), float("inf"))
    
    def get_board_value(self, vertical):
        player_moves_count = len(list(self.legal_moves(vertical)))
        opponent_moves_count = len(list(self.legal_moves(np.invert(vertical))))
        #print(player_moves_count, opponent_moves_count)
        return player_moves_count - opponent_moves_count
    
    def max_value(self, max_is_vertical, move_is_vertical, limit, alpha, beta):
        if self.game_over(move_is_vertical) or limit == 0:
            return None, self.get_board_value(max_is_vertical), 1

        #initialize return vars
        best_move, best_value, total_leaves = None, float("-inf"), 0
        

        # try to find the max of self's successors
        for move, result_game_state in self.successors(move_is_vertical):
            #print(move, result_game_state.get_board())
            #print("1.",result_game_state.min_value(max_is_vertical, np.invert(move_is_vertical), limit -1, alpha, beta))
            new_move, new_value, new_leaves = result_game_state.min_value(max_is_vertical, np.invert(move_is_vertical), limit -1, alpha, beta)
            total_leaves += new_leaves

            if new_value > best_value:
                best_value = new_value
                best_move = move

            #pruning check
            if best_value >= beta: # the Min from the level above would never choose it
                break
            
            if new_value > alpha:
                alpha = max(alpha, best_value)
        return best_move, best_value, total_leaves
    
    def min_value(self, max_is_vertical, move_is_vertical, limit, alpha, beta):
        if self.game_over(move_is_vertical) or limit == 0:
            return None, self.get_board_value(max_is_vertical), 1

        #initialize return vars
        best_move, best_value, total_leaves = None, float("inf"), 0

        # try to find the max of self's successors
        for move, result_game_state in self.successors(move_is_vertical):
            #print("1.",result_game_state.max_value(max_is_vertical, np.invert(move_is_vertical), limit -1, alpha, beta))
            new_move, new_value, new_leaves = result_game_state.max_value(max_is_vertical, np.invert(move_is_vertical), limit - 1, alpha, beta)
            total_leaves += new_leaves
            
            #print(new_value, best_value)
            if new_value < best_value:
                best_value = new_value
                best_move = move

            #pruning check
            if best_value <= alpha: # the Min from the level above would never choose it
                break
            
            if new_value < beta:
                beta = new_value
        return best_move, best_value, total_leaves    

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = 6

feedback_question_2 = """
Hard to understand initially alpha and beta and how they were used to prune unneccessary searches. Probably better in
the future to split the hw into two parts: one without pruning and one where pruning is implemented.

Trying to implement all at onceis a bit overwhelming.
"""

feedback_question_3 = """
Great to learn adversarial search.
"""
