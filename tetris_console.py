"""

Created at 24.08.23
@original_author: Mohammad Ashraf Abdin
@title: 
@description: 

"""
from time import sleep

import numpy as np

from tetris_pieces.pieces_enum import Pieces


class TetrisSolverConsole:
    def __init__(self):
        # Initialize the container
        self.container_l = 7
        self.container_w = 8
        self.container = np.zeros((self.container_l, self.container_w))

        # Initialize the pieces
        self.current_piece_index = 0
        self.pieces = [Pieces.o.value, Pieces.l_90.value, Pieces.i_90.value, Pieces.i_0.value,
                       Pieces.t_180.value, Pieces.j_270.value, Pieces.l_180.value, Pieces.j_180.value,
                       Pieces.z_0.value, Pieces.s_90.value, Pieces.o.value, Pieces.l_180.value,
                       Pieces.j_270.value, Pieces.t_0.value]

        # Initialize the score and holes
        self.score = 0
        self.holes = np.zeros((self.container_l, self.container_w), dtype=int)
        # print("Score : 0")
        # print("Holes : 0")

    def can_add_next_piece(self, piece):
        # Start filling from bottom-left corner
        row, col = self.container_l - len(piece), 0

        while row >= 0:
            fit = True
            for i in range(len(piece)):
                for j in range(len(piece[0])):
                    if (piece[i][j] == 1 and
                            (row + i > self.container_l
                             or col + j > self.container_w
                             or self.container[i + row][j + col] == 1)):
                        fit = False
                        break
            if fit:
                return True
            col += 1
            if col + len(piece[0]) > self.container_w:
                row -= 1
                col = 0
        return False

    def place_next_piece(self):
        if self.current_piece_index < len(self.pieces):
            piece = self.pieces[self.current_piece_index]
            # Check if there is enough space to add the next piece
            if self.can_add_next_piece(piece):
                row, col = self.container_l - len(piece), 0
                while row >= 0:
                    fit = True
                    for i in range(len(piece)):
                        for j in range(len(piece[0])):
                            if (piece[i][j] == 1 and
                                    (row + i > self.container_l
                                     or col + j > self.container_w
                                     or self.container[i + row][j + col] == 1)):
                                fit = False
                                break
                    if fit:
                        for i in range(len(piece)):
                            for j in range(len(piece[0])):
                                if piece[i][j] == 1:
                                    self.container[row + i][col + j] = 1
                                    self.holes[row + i][col + j] = 0  # Mark as not a hole
                        break
                    col += 1
                    if col + len(piece[0]) > self.container_w:
                        row -= 1
                        col = 0
                print(self.container)
                self.current_piece_index += 1

                # Calculate and update the score based on filled spaces
                filled_spaces = np.sum(self.container)
                self.score += filled_spaces

                # Count holes for each space individually
                self.calculate_holes()

                # Update the labels
                self.update_score()
                self.update_holes()
                sleep(1)
                self.place_next_piece()

            else:
                print("No more space for the next piece. Stopping the simulation.")
                print("Final Score:", self.score)
        else:
            print("Game Over")
            print("Final Score:", self.score)

    def calculate_holes(self):
        for col in range(self.container_w):
            hole_found = False
            for row in range(self.container_l):
                if self.container[row][col] == 1:
                    hole_found = True
                elif hole_found:
                    self.holes[row][col] = 1

    def update_score(self):
        print("Score: {}", self.score)

    def update_holes(self):
        total_holes = np.sum(self.holes)
        print("Holes: {}", total_holes)


def main():
    app = TetrisSolverConsole()
    app.place_next_piece()


if __name__ == "__main__":
    main()
