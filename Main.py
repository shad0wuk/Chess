#import libraries and classes
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
            #if undo, pop the last two moves from the board(stack) and play again
            if (play == "undo"):
                self.board.pop()
                self.board.pop()
                print("Last move undone.")
                print(self.board)
                
                self.playHumanMove()
                return
            #push move to the board(stack)
            self.board.push_san(play)
            print(self.board)
        except:
            #if move is invalid, try again
            print("Invalid move.")
            self.playHumanMove()

    #play engine move
    def playEngineMove(self, maxDepth, colour, difficulty):
        #create an instance of the engine
        engine = ChessEngine.Engine(self.board, maxDepth, colour)
        #push the best move to the board(stack)
        self.board.push(engine.getBestMove(difficulty))
        print(self.board)
        #print the last move played by the engine
        lastMove = self.board.peek()
        print("Opponent played: " + str(lastMove))

    #start a game
    def startGame(self):
        #get human player's colour
        colour = None
        while(colour != "white" and colour != "black"):
            colour = input("Play as (type \"white\" or \"black\"): ")
        #get difficulty
        difficulty = None
        while(difficulty != "easy" and difficulty != "medium" and difficulty != "hard"):
            difficulty = input("Choose difficulty (type \"easy\", \"medium\" or \"hard\"): ")
        #set difficulty level
        if difficulty == "easy":
            difficulty = 10         
        elif difficulty == "medium":
            difficulty = 20          
        elif difficulty == "hard":
            difficulty = 30      
        #get max depth
        maxDepth = None
        while(isinstance(maxDepth, int) == False):
            maxDepth = int(input("Choose depth: "))
        #play game
        if colour == "white":
            while not self.board.is_game_over():
                if self.board.is_check():
                    print("Check!")
                self.playHumanMove()
                if not self.board.is_checkmate():
                    print("The engine is thinking...")
                    #play engine move
                    self.playEngineMove(maxDepth, chess.BLACK, difficulty)
        elif colour == "black":
            while not self.board.is_game_over():
                print("The engine is thinking...")
                #play engine move
                self.playEngineMove(maxDepth, chess.WHITE, difficulty)
                if not self.board.is_checkmate():
                    if self.board.is_check():
                        print("Check!")
                    self.playHumanMove()
        #print checkmate or stalemate
        print(self.board.outcome())

        #reset the board
        self.board.reset
        #start another game
        #self.startGame()

#create an instance and start a game
newBoard = chess.Board()
game = Main(newBoard)
start = game.startGame()