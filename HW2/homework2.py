############################################################
# CIS 521: Uninformed Search Homework
############################################################

student_name = "Philip Situmorang"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import itertools
from math import factorial
import random
import numpy as np
import copy

############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
    return factorial(n ** 2) / (factorial(n) * factorial(n ** 2 - n))

def num_placements_one_per_row(n):
    return n**n

def n_queens_valid(board):
    valid = True

    count_i = 1
    for i in range(len(board)):
    
        count_j = i + 1
        for j in range(len(board) - count_i):
            diff = abs(board[count_j] - board[i])
            if diff == 0 or diff == count_j - i:
                valid = False
            count_j += 1
        count_i += 1
    return valid

def n_queens_solutions(n):
    # set initial depth = 1
    depth = 1
    initial_list = [x for x in range(n)]
    sol = []
    for branch in initial_list:
        sol = search(n, depth, [branch], sol)
    return sol

def search(n, depth, current_list, solution):
    if depth ==n:
        solution.append(current_list)
    else:
        possible_next_steps = n_queens_helper(n, current_list)
        for step in possible_next_steps:
            search(n, depth+1, step, solution)
    return solution

def n_queens_helper(n, board):
    next_steps=[]
    for i in range(n):
        temp_board = board + [i]
        if n_queens_valid(temp_board):
            next_steps.append(board + [i])
    return next_steps

############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        b = self.board
        
        coords = [[row, col], 
             [row - 1 , col],
             [row + 1 , col],
             [row, col - 1],
             [row, col + 1]]
        
        for coord in coords:
            if -1 in coord:
                coords.remove(coord)
        
        for coord in coords:
            if coord[0] > len(b)-1:
                coords.remove(coord)
        
        for coord in coords:
            if coord[1] > len(b[0])-1:
                coords.remove(coord)
        
        for coord in coords:
            b[coord[0]][coord[1]] = np.invert(b[coord[0]][coord[1]])
        
        self.board = b

    def scramble(self):
        b = self.board
        dim = [len(b), len(b[0])]
        coords = []

        for i in range(dim[0]):
            for j in range(dim[1]):
                coords.append([i,j])
        
        for coord in coords:
            if random.random() < 0.5:
                self.perform_move(coord[0], coord[1])

    def is_solved(self):
        solved = True
        for row in self.board:
            if True in row:
                solved = False
                break
        return solved

    def copy(self):
        return LightsOutPuzzle(copy.deepcopy(self.board))

    def successors(self):
        b = self.board
        dim = [len(b), len(b[0])]
        
        moves = []
        for i in range(dim[0]):
            for j in range(dim[1]):
                moves.append((i,j))
        
        for move in moves:
            new_p = self.copy()
            new_p.perform_move(move[0], move[1])
            yield (move, new_p)

  

    def find_solution(self):
        node = {'state': self.board, 'path': []}
        b = LightsOutPuzzle(node.get('state')).copy()
    
        if b.is_solved():
            return node.get('path')
    
        frontier = [node]
        reached = [copy.deepcopy(node.get('state'))]
    
        while frontier:
            node1 = frontier.pop(0)
            for child in expand(node1):
                b1 = child.get('state')
                if LightsOutPuzzle(b1).is_solved():
                    return child.get('path')
                if b1 not in reached:
                    reached.append(b1)
                    frontier.append(child)
        return None
        
    

def create_puzzle(rows, cols):
    b = [[False for i in range(cols)] for j in range(rows)]
    return LightsOutPuzzle(b)

def expand(node):
    b = node.get('state')
    actions = []
    dim = [len(b), len(b[0])]
    
    for i in range(dim[0]):
        for j in range(dim[1]):
            actions.append((i,j))
        
    for action in actions:
        b_prime = LightsOutPuzzle(b).copy()
        b_prime.perform_move(action[0],action[1])
        path_prime = copy.deepcopy(node.get('path'))
        path_prime.append(action)
        node_prime = {'state': b_prime.get_board(), 
                        'path': path_prime}
        yield node_prime

############################################################
# Section 3: Linear Disk Movement
############################################################
class LinearDisksIdentical(object):

    def __init__(self, board):
        self.board = board

    def get_board(self):
        return self.board

    def is_solved(self):
        solved = True
        b = self.board
        for i in range(len(b) - 1):
            if b[i] == 1:
                if b[i+1] == 0:
                    solved = False
        return solved

    def copy(self):
        return LinearDisksIdentical(copy.deepcopy(self.board))

    def find_solution(self):
        node = {'state': copy.deepcopy(self.board), 'path': []}
        b = LinearDisksIdentical(node.get('state')).copy()
    
        if b.is_solved():
            return node.get('path')
    
        frontier = [node]
        reached = [copy.deepcopy(node.get('state'))]
    
        while frontier:
            node1 = frontier.pop(0)
            for child in expandDisksIdentical(node1):
                b1 = child.get('state')
                if LinearDisksIdentical(b1).is_solved():
                    return child.get('path')
                if b1 not in reached:
                    reached.append(b1)
                    frontier.append(child)
        return None

def expandDisksIdentical(node):
    b = node.get('state')
    actions = []

    for i in range(len(b) - 1):
        if b[i] == 1:
            if b[i + 1] == 0:
                actions.append((i, i+1))
            if i < len(b) -2:
                if b[i + 1] == 1 and b[i + 2] == 0:
                    actions.append((i, i+2))

    for action in actions:
        b_prime = copy.deepcopy(LinearDisksIdentical(b).get_board())
        b_prime[action[0]] = 0
        b_prime[action[1]] = 1
        path_prime = copy.deepcopy(node.get('path'))
        path_prime.append(action)
        node_prime = {'state': b_prime, 
                        'path': path_prime}
        yield node_prime   

def solve_identical_disks(length, n):
    board = [1 if i < n else 0 for i in range(length)]
    ld = LinearDisksIdentical(board)
    return ld.find_solution()


class LinearDisksDistinct(object):

    def __init__(self, board):
        self.board = board

    def get_board(self):
        return self.board

    def is_solved(self):
        b = self.board
        
        zeros = [i for i in b if i == 0]
        nonzeros = [i for i in b if i != 0]
        
        solved_b = zeros + sorted(nonzeros, reverse=True)
                
        if b == solved_b:
            return True
        else:
            return False

    def copy(self):
        return LinearDisksDistinct(copy.deepcopy(self.board))

    def find_solution(self):
        node = {'state': copy.deepcopy(self.board), 'path': []}
        b = LinearDisksDistinct(node.get('state')).copy()
    
        if b.is_solved():
            return node.get('path')
    
        frontier = [node]
        reached = [copy.deepcopy(node.get('state'))]
    
        while frontier:
            node1 = frontier.pop(0)
            for child in expandDisksDistinct(node1):
                b1 = child.get('state')
                if LinearDisksDistinct(b1).is_solved():
                    return child.get('path')
                if b1 not in reached:
                    reached.append(b1)
                    frontier.append(child)
        return None
        
def expandDisksDistinct(node):
    b = node.get('state')
    actions = []

    for i in range(len(b) - 1):
        if b[i] != 0:
            if b[i + 1] == 0:
                actions.append((i, i+1))
            if i < len(b) -2:
                if b[i + 1] != 0 and b[i + 2] == 0:
                    actions.append((i, i+2))
    
    for j in [x+1 for x in range(len(b) -1)]:
        if b[j] != 0:
            if b[j - 1] == 0:
                actions.append((j, j-1))
            if j > 1:
                if b[j - 1] != 0 and b[j - 2] == 0:
                    actions.append((j, j-2))

    for action in actions:
        b_prime = copy.deepcopy(LinearDisksDistinct(b).get_board())
        disk = copy.deepcopy(b_prime[action[0]])
        b_prime[action[0]] = 0
        b_prime[action[1]] = disk
        path_prime = copy.deepcopy(node.get('path'))
        path_prime.append(action)
        node_prime = {'state': b_prime, 
                      'path': path_prime}
        yield node_prime  

def solve_distinct_disks(length, n):
    board = [i+1 if i < n else 0 for i in range(length)]
    ld = LinearDisksDistinct(board)
    return ld.find_solution()

############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
10 hrs+.
"""

feedback_question_2 = """
Understanding pseudocode was difficult. Took awhile to understand BFS and DFS just by looking at the pseudocode.
"""

feedback_question_3 = """
Learning the BFS and DFS.
"""
