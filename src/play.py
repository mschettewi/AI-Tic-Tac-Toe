import board
import bot
import sys


def main():
    x = board.board()
    i = 0
    sys.stdout.write("\n")
    _bot = bot.bot(x, "O")
    while (not x.isWinner()):
        try:
            x.printBoard()
            if (i == 0):
                a, b = input("X's turn. in form(x,y): ")
                x.add(a, b, "X")
            elif (i == 1):
                _bot.updateBoard(x)
                move = _bot.bestMove(x, 2, "O", sys.maxint, -sys.maxint)
                x.add(move[0][1], move[0][0], "O")
            i = not i
            sys.stdout.write("\n")

        except ValueError:
            sys.stdout.write("invalid spot, please try again\n")
        except (TypeError, SyntaxError, NameError):
            sys.stdout.write("enter ints in form (x,y), please try again\n")
        except IndexError:
            sys.stdout.write("out of range, please try again\n")
    if (x.winner != None):
        x.printBoard()
        if (x.winner == "O"):
            sys.stdout.write("congrats O\n")
        elif (x.winner == "X"):
            sys.stdout.write("congrats X\n")
        else:
            sys.stdout.write(x.winner + "\n")


if (__name__ == "__main__"):
    main()