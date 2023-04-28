import chess
import random as rnd

class Engine:

    def __init__(self, board, maxDepth, colour):
        self.board = board
        self.colour = colour
        self.maxDepth = maxDepth
    
    def getBestMove(self):
        return self.minmax(None, 1)

    def evaluate(self):
        compt = 0
        #Sums up the material values
        for i in range(64):
            square = chess.SQUARES[i]
                
            #Takes a square as input and 
            #returns the corresponding Hans Berliner's
            #system value of it's resident
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
            
            #if checkmate - ensure engine plays the move, if oppenents move - ensure engine avoids the move
            if self.board.is_checkmate():
                if (self.board.turn == self.colour):
                    compt += -9999
                else:
                    compt += 9999

            #to make the engine develop in the first moves
            #evaluate the strength of the opening moves
            if (self.board.fullmove_number < 10):
                if (self.board.turn == self.colour):
                    compt += 1 / 30 * self.board.legal_moves.count()
                else:
                    #negative score prevents engine from playing too defensively
                    #will ensure developing moves in the first 10 moves
                    compt += -1 / 30 * self.board.legal_moves.count()

            compt += 0.001 * rnd.random()
            return compt
   
    def minmax(self, candidate, depth):
        
        #reached max depth of search or no possible moves
        if ( depth == self.maxDepth or self.board.legal_moves.count() == 0):
            return self.evaluate()
        
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

                #Play move
                self.board.push(move)

                #Get value of move (by exploring the repercussions) - recursive call
                eval = self.minmax(newCandidate, depth + 1) 

                #Basic minmax algorithm:
                #if maximizing (engine's turn)
                if(eval > newCandidate and depth % 2 != 0):
                    #need to save move played by the engine
                    if (depth == 1):
                        bestMove = move
                    newCandidate = eval
                #if minimizing (human player's turn)
                elif(eval < newCandidate and depth % 2 == 0):
                    newCandidate = eval

                #Alpha-beta prunning cuts: 
                #(if previous move was made by the engine)
                if (candidate != None and eval < candidate and depth % 2 == 0):
                    self.board.pop()
                    break
                #(if previous move was made by the human player)
                elif (candidate != None and eval > candidate and depth % 2 != 0):
                    self.board.pop()
                    break
                
                #Undo last move
                self.board.pop()

            #Return result
            if (depth > 1):
                #return value of a move in the tree
                return newCandidate
            else:
                #return the move (only on first move)
                return bestMove
            