import sys
import math
import copy

#    board = """
#        ____________________________
#        |__|__|__|__|__|__|__|__|__|
#        |__|__|__|__|__|__|__|__|__|
#        |__|__|__|__|__|__|__|__|__|
#        |__|__|__|__|__|__|__|__|__|
#        |__|__|__|__|__|__|__|__|__|
#        |__|__|__|__|__|__|__|__|__|
#        |__|__|__|__|__|__|__|__|__|
#        |__|__|__|__|__|__|__|__|__|
#        |__|__|__|__|__|__|__|__|__|
#    """


def notPlayer(player):
    if (player == "X"):
        return "O"
    elif (player == "O"):
        return "X"
    return " "


class board:
    def __init__(self):
        self.board = [[" " for y in range(9)] for x in range(9)]
        self.b_winner = False
        self.winner = None

    # adds to board and updates winner
    def add(self, y, x, player):
        if (type(y) is not int or type(x) is not int):
            raise TypeError("enter an int")
            return
        if (x < 0 or x > 8 or y < 0 or y > 8):
            raise IndexError("out of range")
            return
        if (self.board[x][y] != "X" and self.board[x][y] != "O"):
            self.board[x][y] = player
            self.updateWinner()
            return
        else:
            raise ValueError("this spot is already taken")
            return

    def isWinner(self):
        return self.b_winner

    def isFull(self):
        for x in range(0, 9):
            for y in range(0, 9):
                if (self.board[y][x] != " "):
                    return False
        return True

    # prints out the current board
    def printBoard(self):
        sys.stdout.write(" "),
        for i in range(0, 9):
            sys.stdout.write("\033[4m " + str(i) + "\033[0m")
        sys.stdout.write("\n")
        line = "___________________"
        for x, row in enumerate(self.board):
            sys.stdout.write(str(x))
            for y, element in enumerate(row):
                if (element == "X"):
                    sys.stdout.write("|" + "\033[4m" + element + "\033[0m")
                elif (element == "O"):
                    sys.stdout.write("|" + "\033[4m" + element + "\033[0m")
                else:
                    sys.stdout.write("|" + "\033[4m" + element + "\033[0m")
                if (y == 8):
                    sys.stdout.write("|\n")

    # returns calculated heuristic for a given board
    # player is either "X" or "O"
    # "X" is trying to increase score, "O" is trying to decrease score
    # before considering if it is open on both sides:
    # 5 in a row = 10000
    # 4 in a row = 1000
    # 3 in a row = 100
    # 2 in a row = 10
    # 1 in a row = 1
    # if there is an open spot on one side, it will add one to
    # multiplier and two if there are open spots on both sides.
    # Multiplier is to the power of count ie. if it is open on both sides
    # score += (10+2)**(number in a row - 1)
    def heuristic(self, player):
        # checked contains a tuple (x, y, direction)
        # so that it doesn't check a given direction more than once
        # direction is either "S", "E", "NE", or "SE"
        checked = []
        score = 0
        for y in range(0, 9):
            for x in range(0, 9):
                if (self.board[y][x] != " "):
                    # check right (E)
                    if ((x, y, "E") not in checked):
                        check_x = x + 1
                        count = 0
                        while (check_x < 9):
                            if (self.board[y][x] == self.board[y][check_x]):
                                count += 1
                                check_x += 1
                                checked.append((check_x, y, "E"))
                            else:
                                break
                        multiplier = 0
                        if (x - 1 >= 0):
                            if (self.board[y][x - 1] == " "):
                                multiplier += 1
                        if (check_x + 1 < 9):
                            if (self.board[y][check_x + 1] == " "):
                                multiplier += 1
                        if (self.board[y][x] == "X"):
                            score += (10 + multiplier)**(count)
                        else:
                            score -= (10 + multiplier)**(count)

                    # check down (S)
                    if ((x, y, "S") not in checked):
                        check_y = y + 1
                        count = 0
                        while (check_y < 9):
                            if (self.board[y][x] == self.board[check_y][x]):
                                count += 1
                                check_y += 1
                                checked.append((x, check_y, "S"))
                            else:
                                break

                        multiplier = 0
                        if (y - 1 >= 0):
                            if (self.board[y - 1][x] == " "):
                                multiplier += 1
                        if (check_y + 1 < 9):
                            if (self.board[check_y + 1][x] == " "):
                                multiplier += 1
                        if (self.board[y][x] == "X"):
                            score += (10 + multiplier)**(count)
                        else:
                            score -= (10 + multiplier)**(count)

                    # check diagonal (NE)
                    if ((x, y, "NE") not in checked):
                        check_x = x + 1
                        check_y = y - 1
                        count = 0
                        while (check_x < 9 and check_y >= 0):
                            if (self.board[y][x] == self.board[check_y]
                                [check_x]):
                                count += 1
                                check_x += 1
                                check_y -= 1
                                checked.append((check_x, check_y, "NE"))
                            else:
                                break
                        multiplier = 0
                        if (x - 1 >= 0 and y + 1 < 9):
                            if (self.board[y + 1][x - 1] == " "):
                                multiplier += 1
                        if (check_x + 1 < 9 and check_y - 1 >= 0):
                            if (self.board[check_y - 1][check_x + 1] == " "):
                                multiplier += 1
                        if (self.board[y][x] == "X"):
                            score += (10 + multiplier)**(count)
                        else:
                            score -= (10 + multiplier)**(count)

                    # check diagonal (SE)
                    if ((x, y, "SE") not in checked):
                        check_x = x + 1
                        check_y = y + 1
                        count = 0
                        while (check_x < 9 and check_y < 9):
                            if (self.board[y][x] == self.board[check_y]
                                [check_x]):
                                count += 1
                                check_x += 1
                                check_y += 1
                                checked.append((check_x, check_y, "SE"))
                            else:
                                break
                        multiplier = 0
                        if (x - 1 >= 0 and y - 1 >= 0):
                            if (self.board[y - 1][x - 1] == " "):
                                multiplier += 1
                        if (check_x + 1 < 9 and check_y + 1 < 9):
                            if (self.board[check_y + 1][check_x + 1] == 0):
                                multiplier += 1
                        if (self.board[y][x] == "X"):
                            score += (10 + multiplier)**(count)
                        else:
                            score -= (10 + multiplier)**(count)
        return score

    # updates self.b_winner and self.winner
    def updateWinner(self):
        count = 0
        for y in range(0, 9):
            for x in range(0, 9):
                if (self.board[x][y] != " "):
                    count += 1
                    # check down (S)
                    if (y < 5
                        ):  # if it's >= 5, not possible to get a 5 in a row
                        check_y = y + 1
                        count = 1
                        while (check_y < 9):
                            if (self.board[x][y] == self.board[x][check_y]):
                                count += 1
                                check_y += 1
                            else:
                                break
                        if (count >= 5):
                            self.b_winner = True
                            self.winner = self.board[x][y]
                            return

                    # check right (E)
                    if (x < 5):
                        check_x = x + 1
                        count = 1
                        while (check_x < 9):
                            if (self.board[x][y] == self.board[check_x][y]):
                                count += 1
                                check_x += 1
                            else:
                                break
                        if (count >= 5):
                            self.b_winner = True
                            self.winner = self.board[x][y]
                            return

                    # check diagonal (NE)
                    if (x < 5 and y > 3):
                        check_x = x + 1
                        check_y = y - 1
                        count = 1
                        while (check_x < 9 and check_y >= 0):
                            if (self.board[x][y] == self.board[check_x]
                                [check_y]):
                                count += 1
                                check_x += 1
                                check_y -= 1
                            else:
                                break
                        if (count >= 5):
                            self.b_winner = True
                            self.winner = self.board[x][y]
                            return

                    # check diagonal (SE)
                    if (x < 5 and y < 5):
                        check_x = x + 1
                        check_y = y + 1
                        count = 1
                        while (check_x < 9 and check_y < 9):
                            if (self.board[x][y] == self.board[check_x]
                                [check_y]):
                                count += 1
                                check_x += 1
                                check_y += 1
                            else:
                                break
                        if (count >= 5):
                            self.b_winner = True
                            self.winner = self.board[x][y]
                            return
        # stale mate
        if (count == 9 * 9):
            self.b_winner = True
            self.winner = "Stale Mate"