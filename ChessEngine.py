import chess
import random as rnd

class Engine:

    def __init__(self, board, maxDepth, colour):
        self.board = board
        self.colour = colour
        self.maxDepth = maxDepth
    
    def getBestMove(self):
        return self.engine(None, 1)

    def evalFunct(self):
        compt = 0
        #Sums up the material values
        for i in range(64):
            compt += self.squareResPoints(chess.SQUARES[i])
        compt += self.mateOpportunity() + self.openning() + 0.001 * rnd.random()
        return compt

    def mateOpportunity(self):
        if (self.board.legal_moves.count() == 0):
            if (self.board.turn == self.colour):
                return -999
            else:
                return 999
        else:
            return 0

    #to make the engine developp in the first moves
    def openning(self):
        if (self.board.fullmove_number < 10):
            if (self.board.turn == self.colour):
                return 1 / 30 * self.board.legal_moves.count()
            else:
                return -1 / 30 * self.board.legal_moves.count()
        else:
            return 0

    #Takes a square as input and 
    #returns the corresponding Hans Berliner's
    #system value of it's resident
    def squareResPoints(self, square):
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
            return -pieceValue
        else:
            return pieceValue

        
    def engine(self, candidate, depth):
        
        #reached max depth of search or no possible moves
        if ( depth == self.maxDepth
        or self.board.legal_moves.count() == 0):
            return self.evalFunct()
        
        else:
            #get list of legal moves of the current position
            moveList = list(self.board.legal_moves)
            
            #initialise newCandidate
            newCandidate = None
            #(uneven depth means engine's turn)
            if(depth % 2 != 0):
                newCandidate = float("-inf")
            else:
                newCandidate = float("inf")
            
            #analyse board after deeper moves
            for move in moveList:

                #Play move i
                self.board.push(move)

                #Get value of move i (by exploring the repercussions)
                value = self.engine(newCandidate, depth + 1) 

                #Basic minmax algorithm:
                #if maximizing (engine's turn)
                if(value > newCandidate and depth % 2 != 0):
                    #need to save move played by the engine
                    if (depth == 1):
                        bestMove = move
                    newCandidate = value
                #if minimizing (human player's turn)
                elif(value < newCandidate and depth % 2 == 0):
                    newCandidate = value

                #Alpha-beta prunning cuts: 
                #(if previous move was made by the engine)
                if (candidate != None
                 and value < candidate
                 and depth % 2 == 0):
                    self.board.pop()
                    break
                #(if previous move was made by the human player)
                elif (candidate != None 
                and value > candidate 
                and depth % 2 != 0):
                    self.board.pop()
                    break
                
                #Undo last move
                self.board.pop()

            #Return result
            if (depth > 1):
                #eturn value of a move in the tree
                return newCandidate
            else:
                #return the move (only on first move)
                return bestMove
