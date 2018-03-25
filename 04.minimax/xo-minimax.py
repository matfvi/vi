class XO:

    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.board = [['-', '-', '-'],
                      ['-', '-', '-'],
                      ['-', '-', '-']]

        self.player_turn = 1
        self.num_leaves = 0

    def calculate_victory(self):

        n = len(self.board)

        # Redovi
        for i in range(n):
            if self.board[i][0] != '-' and self.board[i][0] == self.board[i][1] and self.board[i][1] == self.board[i][2]:
                if self.board[i][0] == 'X':
                    return -1
                else:
                    return 1

        # Kolone
        for j in range(n):
            if self.board[0][j] != '-' and self.board[0][j] == self.board[1][j] and self.board[1][j] == self.board[2][j]:
                if self.board[0][j] == 'X':
                    return -1
                else:
                    return 1

        # Glavna dijagonala
        if self.board[0][0] != '-' and self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2]:
            if self.board[0][0] == 'X':
                return -1
            else:
                return 1

        # Sporedna dijagonala
        if self.board[0][2] != '-' and self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0]:
            if self.board[0][2] == 'X':
                return -1
            else:
                return 1

        for i in range(n):
            for j in range(n):
                if self.board[i][j] == '-':
                    return 2

        return 0

    def player_1_move(self, i, j):

        if self.player_turn != 1:
            return

        if self.board[i][j] != '-':
            return

        self.board[i][j] = 'X'

        self.player_turn = 2

    def player_2_move(self):

        if self.player_turn != 2:
            return

        self.maximum(float('-inf'), float('inf'))
        print('Ukupno listova: %d' % self.num_leaves)
        self.num_leaves = 0

        self.board[self.p2_i][self.p2_j] = 'O'

        self.player_turn = 1

    def minimum(self, alpha, beta):
        f = self.calculate_victory()

        if f < 2:
            self.num_leaves += 1
            return f

        v = float('inf')
        n = len(self.board)

        for i in range(n):
            for j in range(n):
                if self.board[i][j] == '-':
                    self.board[i][j] = 'X'

                    M = self.maximum(alpha, beta)
                    if M < v:
                        v = M

                    self.board[i][j] = '-'

        return v

    def maximum(self, alpha, beta):
        f = self.calculate_victory()

        if f < 2:
            self.num_leaves += 1
            return f

        v = float('-inf')
        n = len(self.board)

        best_i = 0
        best_j = 0

        for i in range(n):
            for j in range(n):
                if self.board[i][j] == '-':
                    self.board[i][j] = 'O'

                    m = self.minimum(alpha, beta)
                    if m > v:
                        v = m
                        best_i = i
                        best_j = j

                    self.board[i][j] = '-'

        self.p2_i = best_i
        self.p2_j = best_j

        return v

    def draw_board(self):

        for red in self.board:
            print(red)

        print('-----------')


if __name__ == "__main__":
    game = XO()
    game.draw_board()

    f = 2

    while f == 2:
        if game.player_turn == 1:
            pos = int(input('Potez: '))
            pos -= 1
            i = pos // 3
            j = pos % 3

            game.player_1_move(i, j)
        else:
            game.player_2_move()

        game.draw_board()
        f = game.calculate_victory()

    if f == 1:
        print('Izgubili ste!')
    elif f == 0:
        print('Nereseno!')
    else:
        print('Pobedili ste!')
