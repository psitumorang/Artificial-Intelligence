############################################################
# Informed Search
############################################################

############################################################
# Imports
############################################################

import copy
import queue
import numpy as np
import math

############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    n_cells = rows * cols
    nums = [i+1 for i in range(n_cells-1)] + [0]

    board = []
    while nums != []:
      board.append(nums[:cols])
      nums = nums[cols:]
    return TilePuzzle(board)

def to_tuple(board):
    return tuple([tuple(row) for row in board])

def to_list(board):
    return list([list(row) for row in board])

def iddfs_helper(board, limit, moves):
    if limit <= 0:
        return
    limit -=1
    for move, new_p in TilePuzzle(board).successors():
        n_moves = moves + [move]
        new_b = new_p.get_board()
        
        if TilePuzzle(new_b).is_solved():
            yield n_moves

        else:
            for x in iddfs_helper(new_b, limit, n_moves):
                yield x

class TilePuzzle(object):
    
    # Required
    def __init__(self, board):
        self.board = board
        self.nrows = len(board)
        self.ncols = len(board[0])
        self.ncells = self.nrows * self.ncols
        self.solved_board = []

        nums = [i+1 for i in range(self.ncells-1)] + [0]
        while nums != []:
            self.solved_board.append(nums[:self.ncols])
            nums = nums[self.ncols:]
            
    def get_board(self):
        return self.board
    
    def get_solved_board(self):
        return self.solved_board

    def perform_move(self, direction):
        board = copy.deepcopy(self.board)
        col_coord = None
        row_coord = None

        for row in board:
            for i in row:
                if i==0:
                    col_coord = row.index(i)
                    row_coord = board.index(row)
                    break

        coords = {"up": [row_coord - 1 , col_coord],
                  "down": [row_coord + 1 , col_coord],
                  "left":[row_coord, col_coord - 1],
                  "right": [row_coord, col_coord + 1]}

        if direction not in coords:
            return False
        
        row_max = len(board) - 1
        col_max = len(board[0]) - 1

        move_coord = coords.get(direction)
        valid = True

        if move_coord[0] > row_max or move_coord[1] > col_max:
            valid = False
            
        if move_coord[0] < 0 or move_coord[1] < 0:
            valid = False
            
        if valid:
            target_num = copy.deepcopy(board[move_coord[0]][move_coord[1]])
            board[move_coord[0]][move_coord[1]] = 0
            board[row_coord][col_coord] = target_num
            self.board = board
        
        return valid

    def scramble(self, num_moves):
        pass

    def is_solved(self):
        if self.board == self.solved_board:
            return True
        else:
            return False

    def copy(self):
        return TilePuzzle(copy.deepcopy(self.board))

    def successors(self):
        directions = ("up","down","left","right")
        
        for direction in directions:
            board = copy.deepcopy(self.board)
            new_puzzle = TilePuzzle(board)
            if new_puzzle.perform_move(direction):
                yield((direction, new_puzzle))

    # Required
    def find_solutions_iddfs(self):
        board = self.board
        moves = []
        if TilePuzzle(board).is_solved():
            return [] 
        step = 0
        
        while True:
            results = 0
            for x in iddfs_helper(board, step, moves):
                results += 1
                yield x
                
            if results > 0: 
                break
            
            else:
                step += 1

    # Required
    def find_solution_a_star(self):
        board = self.board
        p = TilePuzzle(board)
        if p.is_solved():
            return[]
 
        target_zero_loc = [len(board)-1, len(board[0])-1]
        orig_loc = [None, None]
        
        for row in board:
            for i in row:
                if i==0:
                    orig_loc[0] = row.index(i)
                    orig_loc[1] = board.index(row)
        
        f_n = abs(orig_loc[0] - target_zero_loc[0]) + abs(orig_loc[1] - target_zero_loc[1])
        moves =[]
        
        board = tuple([tuple(row) for row in board])
        frontier = queue.PriorityQueue()
        frontier.put((f_n, board, moves))

        visited = set()
        while not frontier.empty():
            f = frontier.get()
            b_tuple = f[1] 
            b = to_list(b_tuple)
            
            if b_tuple not in visited:
                visited.add(b_tuple)
                
                for move, new_p in TilePuzzle(b).successors():
                    new_b = new_p.get_board()
                    moves = f[2] + [move]
                    
                    if new_p.is_solved():
                        return moves
                    
                    # or cost < cost
                    if to_tuple(new_b) not in visited:
                        current_loc = [None,None]
                        for row in new_b:
                            for i in row:
                                if i==0:
                                    current_loc[0] = row.index(i)
                                    current_loc[1] = new_b.index(row)

                        g_n = len(moves)
                        f_n = abs(current_loc[0] - target_zero_loc[0]) + abs(current_loc[1] - target_zero_loc[1])
                        cost = g_n + f_n
                        
                        frontier.put((cost,to_tuple(new_b),moves))

############################################################
# Grid Navigation
############################################################

def find_path(start, goal, scene):
    if start == goal:
        return[]
    
    f_n = euclidean_dist(start, goal)
    
    frontier = queue.PriorityQueue()
    frontier.put((f_n, start, [start]))
    visited = []

    while not frontier.empty():
        f = frontier.get()
        point1 = f[1]
        
        if point1 not in visited:
            visited += [point1]
            for point2 in succ_points(point1, scene):
                
                path = f[2] + [point2]
                cost = g_n(path) + euclidean_dist(point2, goal)
                #cost = euclidean_dist(start, point1) + euclidean_dist(point1, point2) + euclidean_dist(point2, goal)
                
                if point2 == goal:
                    return path
                
                if path not in visited:
                    frontier.put((cost,point2,path))
                    
    return None

def euclidean_dist(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def g_n(path):
    cost = 0
    for i in range(len(path) -1):
        cost += euclidean_dist(path[i],path[i+1])
    return cost

def succ_points(point, scene):
    row_coord = point[0]
    col_coord = point[1]
    
    coords = {"up": (row_coord - 1 , col_coord),
          "down": (row_coord + 1 , col_coord),
          "left": (row_coord, col_coord - 1),
          "right": (row_coord, col_coord + 1),
          "up-left": (row_coord - 1 , col_coord -1) ,
          "up-right": (row_coord - 1 , col_coord +1),
          "down-left": (row_coord + 1 , col_coord -1) ,
          "down-right": (row_coord + 1 , col_coord +1)}
    
    row_max = len(scene) - 1
    col_max = len(scene[0]) - 1
    
    for coord in coords.values():
        if coord[0] <= row_max and coord[1] <= col_max:
            if coord[0] >= 0 and coord[1] >= 0:
                if not scene[coord[0]][coord[1]]:
                    yield coord

############################################################
# Linear Disk Movement, Revisited
############################################################

class LinearDisksDistinct(object):

    def __init__(self, board):
        self.board = board
       
        zeros = [i for i in board if i == 0]
        nonzeros = [i for i in board if i != 0]
        
        self.solved_board = zeros + sorted(nonzeros, reverse=True)
        
    def get_board(self):
        return self.board
    
    def get_solved_board(self):
        return self.solved_board

    def is_solved(self):
        if self.board == self.solved_board:
            return True
        else:
            return False

    def copy(self):
        return LinearDisksDistinct(copy.deepcopy(self.board))

    def find_solution(self):
        board = self.board
        solved_board = self.solved_board
        path = []
        
        if LinearDisksDistinct(board).is_solved():
            return path
    
        f_n = find_fn(board, solved_board)
        
        frontier = queue.PriorityQueue()
        frontier.put((f_n, tuple(board), path))
        
        visited = set()
        visited.add(tuple(board))
    
        while not frontier.empty():
            f = frontier.get()
            b_tuple = f[1] 
            b = list(b_tuple)
            p = f[2]
        
            if b_tuple not in visited:
                visited.add(b_tuple)
            
            for new_b, new_p in expandDisksDistinct(b, p):
                if LinearDisksDistinct(new_b).is_solved():
                    return new_p
     
                if tuple(new_b) not in visited:

                    g_n = len(new_p)
                    f_n = find_fn(new_b, solved_board)
                    cost = g_n + f_n
                    
                    frontier.put((cost, tuple(new_b), new_p))
        return None
        
def expandDisksDistinct(board, path):
    b = board
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
        b_prime = copy.deepcopy(b)
        disk = copy.deepcopy(b_prime[action[0]])
        b_prime[action[0]] = 0
        b_prime[action[1]] = disk
        path_prime = path + [action]
        yield b_prime, path_prime

def solve_distinct_disks(length, n):
    board = [i+1 if i < n else 0 for i in range(length)]
    ld = LinearDisksDistinct(board)
    return ld.find_solution()

def find_fn(board, solved_board):
    f_n = 0
    for i in board:
        if i!= 0:
            f_n += math.ceil((solved_board.index(i) - board.index(i))/2)
    return f_n
