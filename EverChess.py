"""
Clare Minnerath
05/20/20
"""

# 8 x 8 chess board
SIZE = 8

# Class istantiation of Everchess set up with original positioning
class board():
    
    def __init__(self):
        self.board = [[None]*SIZE for _ in range(SIZE)]
        # pawns located in second and second to last rows of board
        self.board[1] = ['W']*SIZE
        self.board[SIZE-2] = ['B']*SIZE
        self.print_board()
        
    def print_board(self):
        # prints board to screen using text & underline
        # includes row & column labels
        print('  ', end = '')
        print(' __'*SIZE)
        for i in range(SIZE-1,-1,-1):
            print(i+1,'|', end = '')
            for j in range(SIZE):
                if self.board[i][j] == 'W':
                    print("\u0332".join('W |'), end = '')
                elif self.board[i][j] == 'B':
                    print("\u0332".join('B |'), end = '')
                else:
                    print("\u0332".join('  |'), end = '')
            print()
        print(' ', end = '')
        [print(' ',i, end = '') for i in range(1,SIZE+1)]
        print()
        
    # checks if a peice can be played when there are no possible captures
    def legal_peice(self, cur_x, cur_y, t):
        if t == 'W':
            return 0 <= cur_x <= SIZE-1 and 0 <= cur_x <= SIZE-1 and self.board[cur_y][cur_x] == t and self.board[cur_y+1][cur_x] == None
        else:
            return 0 <= cur_x <= SIZE-1 and 0 <= cur_x <= SIZE-1 and self.board[cur_y][cur_x] == t and self.board[cur_y-1][cur_x] == None
            
    # checks if the correct piece is chosen when it must capture
    def legal_peice_capture(self, cur_x, cur_y, opp_x, opp_y, t):
        if t == 'W':
            return self.legal_peice(cur_x, cur_y, t) and cur_y + 1 == opp_y and abs(opp_x-cur_x) == 1 
        else:
            return self.legal_peice(cur_x, cur_y, t) and cur_y - 1 == opp_y and abs(opp_x-cur_x) == 1 
    
    # checks if a move is legal when there is no possible captures
    # ie checks if the pawn is moving forward 1
    def legal_move(self, cur_x, cur_y, next_x, next_y, t):
       if t == 'W':
           return cur_x == next_x and cur_y == next_y-1 and self.board[next_y][next_x] == None
       else:
           return cur_x == next_x and cur_y == next_y+1 and self.board[next_y][next_x] == None
    
    # checks to make sure the move is to capture the opponent as it must do this
    def legal_move_capture(self, next_x, next_y, opp_x, opp_y):
        return next_x == opp_x and next_y == opp_y
    
    # moves the pawn on the board
    # returns if the pawn has put itself at risk 
    # (Probably check_capture function call should occur in game class)
    def move(self, cur_x, cur_y, next_x, next_y, t):
        self.board[next_y][next_x] = self.board[cur_y][cur_x]
        self.board[cur_y][cur_x] = None
        self.print_board()
        return self.check_capture(next_x, next_y, t)
    
    # check to see if the movement of the pawn makes capture possible
    def check_capture(self, x, y, t):
        if t == 'W':
            o = 'B'
            # make sure not going off board to check
            if y < SIZE-1 and 0 < x and self.board[y+1][x-1] == o:
                return True
            elif y < SIZE-1 and x < SIZE - 1 and self.board[y+1][x+1] == o:
                return True
            else:
                return False
        else:
            o = 'W'
            # make sure not going off board to check
            if y > 0 and 0 < x and self.board[y-1][x-1] == o:
                return True
            elif y > 0 and x < SIZE - 1 and self.board[y-1][x+1] == o:
                return True
            else:
                return False
                                             
        
# ever chess game class, which is the driver for game play
class game:
    
    def __init__(self):
        self.turn = 'W'  # white starts up first
        self.titles()
        self.game_board = board()
        self.must_capture = [False,0,0] # whether turn must be capture a pawn & pawn location
    
    def titles(self):
        print()
        print("Welcome to Everchess!")
        print()
    
    # basic flow of game play
    # game is played by switching turns until one of the ending conditions is met
    # if a player takes over a pawn, take_turn returns true and they go again
    def play_game(self):
        while not self.game_over():
            print("It's your turn", self.turn)
            while self.take_turn():
                print("Take another turn", self.turn)
            # switch turns
            if self.turn == 'W':
                self.turn = 'B'
            else:
                self.turn = 'W'

    # slightly messy code for taking a turn
    def take_turn(self):
        # case where a capture must be made
        if self.must_capture[0] == True:
            # loop until the coordinates given are a piece that can be played
            bad_coord = True
            while bad_coord:
                x1, y1 = self.input_coord()
                if self.game_board.legal_peice_capture(x1, y1, self.must_capture[1], self.must_capture[2], self.turn):
                    bad_coord = False
            bad_coord = True
            # pick location to move and & check if it's valid
            while bad_coord:
                x2, y2 = self.input_play(x1, y1)
                if self.game_board.legal_move_capture(x2, y2, self.must_capture[1], self.must_capture[2]):
                    bad_coord = False
            self.must_capture[0] = self.game_board.move(x1,y1,x2,y2,self.turn)
            # ugly code for case when you have another turn 
            # and the current pawn can capture an opponent
            if self.must_capture[0] == True and self.turn == 'W':
                if x2 < SIZE - 1 and self.game_board.board[y2+1][x2+1] == 'B':
                    self.must_capture[1], self.must_capture[2] = x2+1, y2+1
                elif x2 > 0:
                    self.must_capture[1], self.must_capture[2] = x2-1, y2+1
            elif self.must_capture[0] == True and self.turn == 'B':
                 if x2 < SIZE - 1 and self.game_board.board[y2-1][x2+1] == 'W':
                    self.must_capture[1], self.must_capture[2] = x2+1, y2-1
                 elif x2 > 0:
                    self.must_capture[1], self.must_capture[2] = x2-1, y2-1
            # return true because this turn did result in capture
            return True
        # case where there are no possible captures            
        else:
            # loop until the coordinates given are a piece that can be played
            bad_coord = True
            while bad_coord:
                x1, y1 = self.input_coord()
                if self.game_board.legal_peice(x1, y1, self.turn):
                    bad_coord = False
            # pick location to move and & check if it's valid
            bad_coord = True
            while bad_coord:
                x2, y2 = self.input_play(x1, y1)
                if self.game_board.legal_move(x1, y1, x2, y2, self.turn):
                    bad_coord = False
            # set must_capture for future case of possible capture
            self.must_capture[0] = self.game_board.move(x1,y1,x2,y2,self.turn)
            self.must_capture[1], self.must_capture[2] = x2, y2
            # return false because this turn didn't result in capture
            return False

    # have user input valid pawn to move coordinates
    def input_coord(self):
        bad_input = True
        while bad_input:
            try:
                print("Give the x and y coordinate of the a", self.turn, " pawn")
                x1 = int(input())
                y1 = int(input())
                break
            except ValueError:
                print("Coordinates must be integers")
                print()
        return x1-1, y1-1
    
    # have user input coordinates of spot to move to
    def input_play(self, x1, y1):
        bad_input = True
        while bad_input:
            try:
                print("Give the x and y coordinates to move pawn @(",x1+1,",",y1+1,")")
                x2 = int(input())
                y2 = int(input())
                break
            except ValueError:
                print("Coordinates must be integers")
                print()
        return x2-1, y2-1
    
    # check game ending conditions 
    def game_over(self):
        # check if either player has had a pawn reach the end of the board
        for i in range(SIZE):
            if self.game_board.board[0][i] == 'B':
                print("Black wins!")
                return True
            if self.game_board.board[SIZE-1][i] == 'W':
                print("White wins!")
                return True
        # Check for no moves
        for i in range(SIZE):
            for j in range(SIZE):
                if self.game_board.board[i][j] == self.turn and self.game_board.legal_peice(j, i, self.turn):
                    return False
        if self.turn == 'W':
            print("Black wins!")
        else:
            print("White wins!")
        return True
    
# main to run program
if __name__ == "__main__":
    newgame = game()
    newgame.play_game()
    
    
