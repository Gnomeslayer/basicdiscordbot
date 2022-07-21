#pylint:disable=W0602
#creating tic tac toe game in python
#intializing board game and all other global variables
board = ["-","-","-",
"-", "-","-",
"-","-","-"
]
winner = None
GameRunning = True

#Removed SwitchPlayer variable and renamed it to PlayerTwo.
#Changed currentplayer to be PlayerOne variable.
#Added a new variable - CurrentPlayer which is the current players turn.
PlayerOne = input("Player One enter a symbol of your choice: ").upper()
PlayerTwo = input("Player Two enter a symbol of your choice: ").upper()

CurrentPlayer = PlayerOne

#print board game
def PrintBoard(board):
	print(board[0] + "|",board[1] + "|", board[2]+ "|")
	print("________")
	print(board[3] + "|",board[4] + "|", board[5]+ "|")
	print("________")
	print(board[6] + "|",board[7] + "|", board[8]+ "|")

#creating player
def PlayerInput(board):
    try:
        #Modified the text so we know which players turn it is.
        if CurrentPlayer == PlayerOne:
            inp = inp=int(input("[Player One] Enter number in range 1 - 9: "))
        else:
            inp = inp=int(input("[Player Two] Enter number in range 1 - 9: "))
        if inp >= 1 and inp <= 9 and board[inp-1] == "-":
            board[inp-1] = CurrentPlayer
            SwitchPlay()
    except ValueError:
        #Modified the text to better reflect which player made the mistake.
        if CurrentPlayer == PlayerOne:
            print("Player one please enter a valid number")
        else:
            print("Player two please enter a valid number")
    else:
        if CurrentPlayer == PlayerOne:
            print("Player one please enter number in range 1 - 9")
        else:
            print("Player two please enter number in range 1 - 9")
  
#creating WinnerRules
def Rowrules(board):
    global winner
    if board[0]==board[1]==board[2] and board[0]!="-":
        winner =board[0]
        return True
    elif board[3]==board[4]==board[5] and board[3]!="-":
        winner = board[3]
        return True
    elif board[6]==board[7]==board[8] and board[6]!="-":
        return True

def Columnrules(board):
    global winner
    if board[0]==board[3]==board[6] and board[6]!="-":
        winner = board[3]
        return True
    elif board[1]==board[4]==board[7] and board[7]!="-":
        winner = board[1]
        return True
    elif board[2]==board[5]==board[8] and board[8]!="-":
        winner = board[8]
        return True


def Diagonalrules(board):
    global winner
    if board[0] == board[4] == board[8] and board[4]!="-":
        winner = board[8]
        return True
    elif board[2] == board[4] == board[6] and board[6] != "-":
        winner = board[4]
        return True

#checking for tie
def Tierules(board):
    global GameRunning
    if "-" not in board:
        PrintBoard(board)
        print("its a tie")
        GameRunning = False
        

#check for win
def Checkforwin():
    global GameRunning
    if Rowrules(board) or Columnrules(board) or Diagonalrules(board):
        PrintBoard(board)
        #Modified the text to tell us which player one.
        if winner == PlayerOne:
            print("The winner of the game is Player One!")
        else:
            print("The winner of the game is player Two!")
        GameRunning = False


#Removed the need to call the board, since it doesn't use it there's no need.
#CurrentPlayer is compared against the two players and switches between them whenever called.
def SwitchPlay():
    global CurrentPlayer
    if CurrentPlayer == PlayerOne:
        CurrentPlayer = PlayerTwo
    else:
        CurrentPlayer = PlayerOne


while GameRunning:
    PrintBoard(board)
    PlayerInput(board)
    Checkforwin()
    Tierules(board)