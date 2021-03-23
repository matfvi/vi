# X-O

# minmax
# alpha-beta
import copy
class XOState:
    empty = ' '
    def __init__(self):
        self.board = [  [XOState.empty, XOState.empty, XOState.empty],
                        [XOState.empty, XOState.empty, XOState.empty],
                        [XOState.empty, XOState.empty, XOState.empty]
                    ]
        self.curr_player = 'X'
        self.prev_player = 'O'

        self.last_move = None
        self.move_count = 0

    def play_move(self, next_move):
        i, j = next_move[0], next_move[1]
        self.board[i][j] = self.curr_player
        self.move_count += 1
        self.curr_player, self.prev_player = self.prev_player, self.curr_player
        self.last_move = next_move

    def draw_board(self):
        print("{}".format(' | '.join(self.board[0])))
        print("{}".format(' | '.join(self.board[1])))
        print("{}".format(' | '.join(self.board[2])))


def end(current_state):
    winner = get_winner(current_state)
    return winner is not None or current_state.move_count == 9

def get_winner(current_state):
    board = current_state.board
    
    # vertikala
    for i in range(0, 3):
        if board[0][i] != XOState.empty and board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]

    # horizontala
    for i in range(0, 3):
        if board[i][0] != XOState.empty and board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
    # glavna dijagonala
    if board[0][0] != XOState.empty and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]

    # sporedna dijagonala
    if board[2][0] != XOState.empty and board[2][0] == board[1][1] == board[0][2]:
        return board[2][0]

    return None

def get_next_move():
    next_move = input()
    next_move = [int(x) for x in next_move.split(',')] # ['0', '0']
    return next_move

# Domaci: uracunati broj poteza u funkciju evaluacije
def evaluate(current_state:XOState):
    winner = get_winner(current_state)
    result = 0
    if winner == 'X':
        result = 1
    elif winner == 'O':
        result = -1
    return result

# Domaci: generisati stanja po potrebi.
# Hint: range, yield
def get_next_states(current_state: XOState):
    result = []
    for i in range(0,3):
        for j in range(0,3):
            if current_state.board[i][j] == XOState.empty:
                next_state = copy.deepcopy(current_state)
                next_state.play_move((i, j))
                result.append(next_state)
    result.reverse()
    return result

# Samo zbog poredjenja sa Alpha/beta inace beskorisno
number_of_calls = 0

def Min(current_state):
    global number_of_calls
    number_of_calls += 1
    if end(current_state):
        return evaluate(current_state), current_state
    
    minv = float('inf')
    best_move = None
    for next_state in get_next_states(current_state):
        maxv, _ = Max(next_state)
        if maxv < minv:
            minv = maxv
            best_move = next_state
    return minv, best_move


def Max(current_state):
    global number_of_calls
    number_of_calls += 1
    if end(current_state):
        return evaluate(current_state), current_state
    
    maxv = float('-inf')
    best_move = None
    for next_state in get_next_states(current_state):
        minv, _ = Min(next_state)
        if maxv < minv:
            maxv = minv
            best_move = next_state
    return maxv, best_move


if __name__ == '__main__':
    game = XOState()
    game.draw_board()
    while True:
        next_move = get_next_move() # 0,0 1,1
        game.play_move(next_move)
        game.draw_board()
        if get_winner(game) == 'X':
            print("Player X won")
            break

        if end(game):
            print('Tie')
            break
        
        number_of_calls = 0
        minv, next_state = Min(game)
        print("Number of Min/Max calls {}".format(number_of_calls))
        next_move = next_state.last_move
        game.play_move(next_move)
        game.draw_board()
        if get_winner(game) == 'O':
            print('Player O won')
            break

