import random
import re
import math

class Board:
    def __init__(self, size, no_of_bomb):
        self.size = size
        self.no_of_bomb = no_of_bomb
        self.board = self.make_new_board() 
        self.assign_value_to_board()
        self.dug = set()

    def make_new_board(self):
        board = [[None for _ in range(self.size)] for _ in range(self.size)]
        plant_bomb = 0
        while plant_bomb < self.no_of_bomb:
            location = random.randint(0, math.pow(self.size, 2) - 1)
            row = location // self.size 
            col = location % self.size  
            if board[row][col] == '*':
                continue
            board[row][col] = '*' 
            plant_bomb += 1
        return board

    def assign_value_to_board(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        num_neighboring_bombs = 0
        for r in range(max(0, row-1), min(self.size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.size-1, col+1)+1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1
        return num_neighboring_bombs

    def dig(self, row, col):
        self.dug.add((row, col)) 

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        for r in range(max(0, row-1), min(self.size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.size-1, col+1)+1):
                if (r, c) in self.dug:
                    continue 
                self.dig(r, c)
        return True

    def __str__(self):
        visible_board = [[None for _ in range(self.size)] for _ in range(self.size)]
        for row in range(self.size):
            for col in range(self.size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        string_rep = ''
        widths = []
        for idx in range(self.size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(len(max(columns, key = len)))
        indices = [i for i in range(self.size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep


def play_game(size=10, no_of_bomb=10):
    board = Board(size, no_of_bomb)
    safe = True 

    while len(board.dug) < board.size ** 2 - no_of_bomb:
        print(board)
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row,col: "))  # '0, 3'
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.size or col < 0 or col >= size:
            print("Invalid location. Try again.")
            continue

        safe = board.dig(row, col)
        if not safe:
            break 

    if safe:
        print("CONGRATULATIONS!!!! YOU ARE VICTORIOUS!")
    else:
        print("SORRY GAME OVER :(")
        board.dug = [(r,c) for r in range(board.size) for c in range(board.size)]
        print(board)

if __name__ == '__main__': 
    play_game()
