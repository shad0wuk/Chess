import chess
import ChessEngine

class Main:

    def __init__(self, board = chess.Board):
        self.board = board

    #play human move
    def playHumanMove(self):
        try:
            print(self.board.legal_moves)
            print("To undo your last move, type \"undo\".")
            print(self.board)
            #get human move
            play = input("Your move: ")
            if (play == "undo"):
                self.board.pop()
                self.board.pop()
                print("Last move undone.")
                print(self.board)
                
                self.playHumanMove()
                return
            self.board.push_san(play)
            print(self.board)
        except:
            print("Invalid move.")
            self.playHumanMove()

    #play engine move
    def playEngineMove(self, maxDepth, colour):
        engine = ChessEngine.Engine(self.board, maxDepth, colour)
        self.board.push(engine.getBestMove())
        print(self.board)
        lastMove = self.board.peek()
        print("Opponent played: " + str(lastMove))

    #start a game
    def startGame(self):
        #get human player's colour
        colour = None
        while(colour != "white" and colour != "black"):
            colour = input("Play as (type \"white\" or \"black\"): ")
            
        maxDepth = None
        while(isinstance(maxDepth, int) == False):
            maxDepth = int(input("Choose depth: "))

        if colour == "white":
            while not self.board.is_game_over():
                if self.board.is_check():
                    print("Check!")
                self.playHumanMove()
                if not self.board.is_checkmate():
                    print("The engine is thinking...")
                    self.playEngineMove(maxDepth, chess.BLACK)
        elif colour == "black":
            while not self.board.is_game_over():
                print("The engine is thinking...")
                self.playEngineMove(maxDepth, chess.WHITE)
                if not self.board.is_checkmate():
                    if self.board.is_check():
                        print("Check!")
                    self.playHumanMove()
        print(self.board.outcome())

        #reset the board
        self.board.reset
        #start another game
        self.startGame()

#create an instance and start a game
newBoard = chess.Board()
game = Main(newBoard)
start = game.startGame()