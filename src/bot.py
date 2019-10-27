from board import board, notPlayer
import copy
import sys

class bot:
    def __init__(self, board, player):
        self.board = board
        self.player = player

    def updateBoard(self, board):
        self.board = board

    # depth is the remaining depth to search
    # currentPlayer is the move of the current player to check heuristic against
    # returns tuple (best_move, best_score) where best move is a tuple (x,y)
    def bestMove(self, board, depth, currentPlayer, alpha=None, beta=None):
        if (depth == 0 or board.isFull() or board.isWinner()):
            return (-1, -1), board.heuristic(currentPlayer)
        possible = []
        for y in range(0, 9):
            for x in range(0, 9):
                if (board.board[x][y] == " "):
                    new_board = copy.deepcopy(board)
                    new_board.add(y, x, currentPlayer)
                    possible.append(((x, y), new_board))
        if (currentPlayer == "X"):
            best_score = -sys.maxint
        else:
            best_score = sys.maxint
        best_move = (-1, -1)
        for move in possible:
            best_move_score = self.bestMove(move[1], depth - 1,
                                            notPlayer(currentPlayer))
            if (currentPlayer == "X"):
                if (best_move_score[1] > best_score):
                    best_score = best_move_score[1]
                    best_move = move[1]
            else:
                if (best_move_score[1] < best_score):
                    best_score = best_move_score[1]
                    best_move = move[0]
        return best_move, best_score
