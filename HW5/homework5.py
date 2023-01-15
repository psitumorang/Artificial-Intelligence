############################################################
# CIS 521: Sudoku Homework 
############################################################

student_name = "Philip Situmorang"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import numpy as np
import collections
import copy
import queue


############################################################
# Section 1: Sudoku Solver
############################################################


def find_neighbors(cell):
    bcells = box_cells()
    #coords = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]
    neighbors = set()
    coords = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]
    for coord in coords:
        neighbor = (cell[0]+coord[0], cell[1]+coord[1])
        if 0 <= neighbor[0] <= 8 and 0 <=neighbor[1] <= 8:
            neighbors.add(neighbor)
    
    for box in bcells:
        if cell in box:
            for neighbor in box:
                if neighbor!= cell:
                    neighbors.add(neighbor)
            
    for i in range(9):
        neighbor1 = (cell[0],i)
        neighbor2 = (i, cell[1])
        
        if neighbor1 != cell:
            neighbors.add(neighbor1)
        if neighbor2 != cell:
            neighbors.add(neighbor2)
        
    return neighbors
            
def box_cells():
    corners = [(2,2),(2,5),(2,8),(5,2),(5,5),(5,8),(8,2),(8,5),(8,8)]
    lst=[]
    for corner in corners:
        temp_lst =[]
        for i in range(corner[0]-2,corner[0]+1):
            for j in range(corner[1]-2,corner[1]+1):
                temp_lst.append((i,j))
        lst.append(temp_lst)
    return lst

def sudoku_cells():
    dct = {}
    keys = [[(j,i) for i in range(9)] for j in range(9)]
    for i in keys:
        for j in i:
            dct[j] = None
    return list(dct.keys())

def sudoku_arcs():
    cells = sudoku_cells()
    lst = []
    for cell in cells:
        for pair in cells:
            if cell != pair:
                if cell[0] == pair[0] or cell[1] == pair[1]:
                    lst.append((cell, pair))
                    
    bcells = box_cells()
    for i in bcells:
        for cell in i:
            for pair in i:
                if cell!=pair:
                    if (cell,pair) not in lst:
                        lst.append((cell,pair))
    
    lst = [tuple(i) for i in lst]
    return lst

def read_board(path):
    dct = {}
    keys = [[(j,i) for i in range(9)] for j in range(9)]
    for i in keys:
        for j in i:
            dct[j] = None

    counter = [0,0]
    with open(path) as file:
        for i in file.read().strip():
            if i == '\n':
                pass
            else:
                if i == '*':
                    dct[tuple(counter)] = {1,2,3,4,5,6,7,8,9}
                else:
                    dct[tuple(counter)] = {int(i)}

                if counter[1] < 8:
                    counter[1] += 1
                else:
                    counter[0] += 1
                    counter[1] = 0
    return dct

class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()
    BCELLS = box_cells()

    def __init__(self, board):
        self.board = board
        self.arcs = sudoku_arcs()

    def get_values(self, cell):
        return self.board.get(cell)
    
    def get_board(self):
        return self.board
    
    def is_solved(self):
        solved = True
        for cell in Sudoku.CELLS:
            if len(self.board[cell]) != 1:
                solved = False
        
        return solved

    def remove_inconsistent_values(self, cell1, cell2):
        b = self.board
        revised = False
        inconsistent_values = set()
        
        for i in b[cell1]:
            if (cell1, cell2) in Sudoku.ARCS and len(b[cell2]) == 1:
                if i in b[cell2]:
                    inconsistent_values.add(i)
                    revised = True

        for j in inconsistent_values:
            b[cell1].remove(j)
        
        return revised

    def infer_ac3(self):
        queue = collections.deque(Sudoku.ARCS)
        
        while queue:
            cells = queue.pop()
            c1 = cells[0]
            c2 = cells[1]
            if self.remove_inconsistent_values(c1, c2):
                for neighbor in find_neighbors(c1):
                    if neighbor != c2:
                        queue.append((neighbor, c1))

    def infer_improved(self):
        made_additional_inference = True
        while made_additional_inference:
            self.infer_ac3()
            made_additional_inference = False
            for cell in Sudoku.CELLS:
                if len(self.board[cell]) > 1:
                    empty_cells = []
                    for box in Sudoku.BCELLS:
                        if cell in box:
                            for bcell in box:
                                if len(self.board[bcell]) > 1 and bcell!= cell:
                                    empty_cells.append(bcell)

                    nums = set()
                    for ecell in empty_cells:
                        for i in self.board[ecell]:
                            nums.add(i)
                    
                    possible_vals = set()
                    for i in self.board[cell]:
            
                        if i not in nums:
                            possible_vals.add(i)
                        if len(possible_vals) == 1:
                            
                            self.board[cell] = possible_vals
                            made_additional_inference = True

    def infer_with_guessing(self):
        self.infer_improved()
        for cell in Sudoku.CELLS:
            if len(self.board[cell]) > 1:
                for i in self.board[cell]:
                    sudoku_copy = copy.deepcopy(self)
                    self.board[cell] = {i}
                    self.infer_with_guessing()
                    if self.is_solved():
                        break
                    else:
                        self.board = sudoku_copy.get_board()
                        
                return
                    
        
############################################################
# Section 2: Feedback
############################################################

# Just an approximation is fine.
feedback_question_1 = 10

feedback_question_2 = """
Some extensive debugging required for my case in this assignment. Took awhile to get to the right solution.
"""

feedback_question_3 = """
I think I'm a bit better at sudoku now.
"""
