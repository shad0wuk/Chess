#import libraries
import chess
import random as rnd
import time
class Engine:

    def __init__(self, board, maxDepth, colour):
        #initialise variables for the engine
        self.board = board
        self.colour = colour
        self.maxDepth = maxDepth
        self.difficulty = None
    
    def getBestMove(self, difficulty):
        #start timer
        start = time.time()
        self.difficulty = difficulty
        #call minmax algorithm to find best move
        bestMove = self.minmax(None, 1)
        #time taken to calculate the best move
        end = time.time()
        timeTaken = end - start
        print("Time taken: " + str(timeTaken) + " seconds.")
        #if bestMove is a float, generate a random legal move - this is if depth = 1
        if (isinstance(bestMove, float)):
            moveList = list(self.board.legal_moves)
            bestMove = moveList[rnd.randint(0, len(moveList) - 1)]
        
        return bestMove
        

    def evaluate(self):
        compt = 0
        #iterate through all squares on the board
        for i in range(64):
            square = chess.SQUARES[i]
                
            #input a square to return the Hans Berliner's value of the piece
            pieceValue = 0
            if(self.board.piece_type_at(square) == chess.PAWN):
                pieceValue = 1
            elif (self.board.piece_type_at(square) == chess.ROOK):
                pieceValue = 5.1
            elif (self.board.piece_type_at(square) == chess.BISHOP):
                pieceValue = 3.33
            elif (self.board.piece_type_at(square) == chess.KNIGHT):
                pieceValue = 3.2
            elif (self.board.piece_type_at(square) == chess.QUEEN):
                pieceValue = 8.8
            
            if (self.board.color_at(square) != self.colour):
                compt += -pieceValue
            else:
                compt += pieceValue
        
        #if checkmate - ensure engine plays the move, if opponents move - ensure engine avoids the move
        if self.board.is_checkmate():
            if (self.board.turn == self.colour):
                compt += -9999
            else:
                compt += 9999

        #to make the engine develop in the first moves
        #evaluate the strength of the opening moves
        if (self.board.fullmove_number < 10):
            if (self.board.turn == self.colour):
                #positive score prevents engine from playing too aggressively
                compt += 1 / 50 * self.board.legal_moves.count()
            else:
                #negative score prevents engine from playing too defensively
                compt += -1 / 50 * self.board.legal_moves.count()
        #random weight to prevent engine from playing the same moves
        compt += 0.001 * rnd.random()
        return compt
   
    def minmax(self, candidate, depth):
        #start timer for difficulty setting
        start = time.time()
        timeLimit = self.difficulty
        #reached max depth of search or no possible moves
        if ( depth == self.maxDepth or self.board.legal_moves.count() == 0):
            return self.evaluate()
        
        else:
            #list of legal moves
            moveList = list(self.board.legal_moves)
            
            #initialise newCandidate
            newCandidate = None
            #uneven depth = engine's turn
            if(depth % 2 != 0):
                newCandidate = float("-inf")
            else:
                newCandidate = float("inf")
            
            #analyse board after deeper moves
            for move in moveList:
                #if time limit reached, stop searching
                if (time.time() - start > timeLimit):
                    break
                #play move
                self.board.push(move)

                #recursive call to minmax algorithm to find evaluation value of the move
                evaluation = self.minmax(newCandidate, depth + 1) 

                #Minmax algorithm:
                #if maximizing (engine's turn)
                if(evaluation > newCandidate and depth % 2 != 0):
                    #if first move, set bestMove to the first move
                    if (depth == 1):
                        firstMove = move
                    newCandidate = evaluation
                #if minimizing (player's turn)
                elif(evaluation < newCandidate and depth % 2 == 0):
                    newCandidate = evaluation

                #Alpha-Beta prunning: 
                #if previous move was made by the engine
                if (candidate != None and evaluation < candidate and depth % 2 == 0):
                    self.board.pop()
                    break
                #if previous move was made by the human player
                elif (candidate != None and evaluation > candidate and depth % 2 != 0):
                    self.board.pop()
                    break
                
                #undo last move
                self.board.pop()

            #return result
            if (depth > 1):
                #return evaluation value of a move in the tree
                return newCandidate
            else:
                #for first move, return the best move
                return firstMove
            
            