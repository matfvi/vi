import copy
class Game:
    def __init__(self):
        self.initialize_game()

    def initialize_game(self):
        self.current_state = [['.', '.', '.'],
                                ['.', '.', '.'],
                                ['.', '.', '.']]
        self.player_turn = 1
    def symbol_to_player(self, symbol):
        mapping ={
                'X' : 1,
                'O' : 2
                }
        return mapping[symbol]
    def player_to_symbol(self, player):
        mapping = {
                1: 'X',
                2: 'O'
                }
        return mapping[player]
    def get_field_coordinates(self, field_number):
        if field_number < 1 or field_number > 9:
            return None
        mapping = {
                7 : (0,0), 8: (0, 1), 9: (0, 2),
                4: (1, 0), 5: (1, 1), 6: (1, 2),
                1: (2, 0), 2: (2, 1), 3: (2, 2)
                }
        return mapping[field_number]
    def evaluation(self, current_state):
        winner = None

        if current_state[0][0] != '.':
            if (current_state[0][0] == current_state[0][1]  and current_state[0][1] == current_state[0][2]) \
            or (current_state[0][0] == current_state[1][0] and current_state[1][0] == current_state[2][0]):
                winner = self.symbol_to_player(current_state[0][0])
        if current_state[1][1] != '.':
            if (current_state[0][1] == current_state[1][1] and current_state[1][1] == current_state[2][1]) \
                or (current_state[0][0] == current_state[1][1] and current_state[1][1] == current_state[2][2]) \
                or (current_state[1][0] == current_state[1][1] and current_state[1][1] == current_state[1][2]) \
                or (current_state[0][2] == current_state[1][1] and current_state[1][1] == current_state[2][0]):
                    winner = self.symbol_to_player(current_state[1][1])
        if current_state[2][2] != '.':
            if (current_state[0][2] == current_state[1][2] and current_state[1][2] == current_state[2][2]) \
                    or (current_state[2][2] == current_state[2][1] and current_state[2][1] == current_state[2][0]):
                        winner = self.symbol_to_player(current_state[2][2])

        if winner != None:
            if winner == 1:
                return -1
            else:
                return 1
        for i in range(3):
            for j in range(3):
                if current_state[i][j] == '.':
                    return None
        return 0
    def get_next_states(self, current_state, player):
        symbol = self.player_to_symbol(player)

        next_states = []
        for i in range(3):
            for j in range(3):
                if current_state[i][j] == '.':
                    next_state = copy.deepcopy(current_state)
                    next_state[i][j] = symbol
                    next_states.append((i, j, next_state))
        return next_states

    def Max(self, current_state, alpha, beta):
        state_value = self.evaluation(current_state)
        if state_value != None:
            return (state_value, None, None)
        v = float('-inf')
        (max_i, max_j) = (None, None)
        for (i, j, next_state) in self.get_next_states(current_state, 2):
            (value, min_i, min_j) = self.Min(next_state, alpha, beta)
            if v < value:
                v = value
                max_i = i
                max_j = j
            if v >= beta:
                return (v, i, j)
            if v > alpha:
                alpha = v
        return (v, max_i, max_j)

    def Min(self, current_state, alpha, beta):
        state_value = self.evaluation(current_state)
        if state_value != None:
            return (state_value, None, None)
        v = float('inf')
        (min_i, min_j) = (None, None)
        for (i, j, next_state) in self.get_next_states(current_state, 1):
            (value, max_i, max_j) = self.Max(next_state, alpha, beta)
            if v > value:
                v = value
                min_i = i
                min_j = j

            if v <= alpha:
                return (v, i ,j)
            if v < beta:
                beta = v
        return (v, min_i, min_j)


    def play(self):
        self.draw_board()

        state_value = self.evaluation(self.current_state)
        if state_value != None:
            if state_value == -1:
                print("Player 1 is the winner")
            elif state_value == 0:
                print("The game is draw")
            elif state_value == 1:
                print("Player 2 is the winner")


            self.initialize_game()
            return
        if self.player_turn == 1:
            field_number = int(input("Input field number:"))
            field_i, field_j = self.get_field_coordinates(field_number)
            self.current_state[field_i][field_j] = self.player_to_symbol(self.player_turn)
            self.player_turn = 2
            self.play()
        else:
            (v, field_i, field_j) = self.Max(self.current_state, float('-inf'), float('inf'))
            self.current_state[field_i][field_j] = self.player_to_symbol(self.player_turn)
            self.player_turn = 1
            self.play()

    def draw_board(self):
        print("{} | {} | {}".format(self.current_state[0][0], self.current_state[0][1], self.current_state[0][2]))
        print("{} | {} | {}".format(self.current_state[1][0], self.current_state[1][1], self.current_state[1][2]))
        print("{} | {} | {}".format(self.current_state[2][0], self.current_state[2][1], self.current_state[2][2]))
        print()
# 7 8 9
# 4 5 6
# 1 2 3
def main():
    print("XO krece!")
    game = Game()
    game.play()
if __name__ == "__main__":
    main()
