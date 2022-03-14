import time


class Node:

    def __init__(self, board, prev_player, value):
        self.board = board
        self.children = []
        self.prev_player = prev_player
        self.value = value

    def equal_to(self, other_board):
        same = True
        i = 0
        height = len(self.board)
        width = len(self.board[0])

        while same and i < height:
            j = 0
            while same and j < width:
                same = (self.board[i][j] == other_board[i][j])
                j += 1
            i += 1

        return same

    def copy_board(self, board):
        height = len(self.board)
        width = len(self.board[0])

        for i in range(height):
            for j in range(width):
                board[i][j] = self.board[i][j]

        return board

    def is_win(self):

        # Horizontal win conditions
        if self.board[0][0] == self.board[0][1] and self.board[0][0] == self.board[0][2] and self.board[0][0] != '-':
            return True, self.board[0][0]
        if self.board[1][0] == self.board[1][1] and self.board[1][0] == self.board[1][2] and self.board[1][0] != '-':
            return True, self.board[1][0]
        if self.board[2][0] == self.board[2][1] and self.board[2][0] == self.board[2][2] and self.board[2][0] != '-':
            return True, self.board[2][0]

        # Vertical win conditions
        if self.board[0][0] == self.board[1][0] and self.board[0][0] == self.board[2][0] and self.board[0][0] != '-':
            return True, self.board[0][0]
        if self.board[0][1] == self.board[1][1] and self.board[0][1] == self.board[2][1] and self.board[0][1] != '-':
            return True, self.board[0][1]
        if self.board[0][2] == self.board[1][2] and self.board[0][2] == self.board[2][2] and self.board[0][2] != '-':
            return True, self.board[0][2]

        # Diagonal win conditions
        if self.board[0][0] == self.board[1][1] and self.board[0][0] == self.board[2][2] and self.board[0][0] != '-':
            return True, self.board[0][0]
        if self.board[2][0] == self.board[1][1] and self.board[2][0] == self.board[0][2] and self.board[2][0] != '-':
            return True, self.board[2][0]

        for row in self.board:
            for elem in row:
                if elem == '-':
                    return False, '-'
        return True, 'Tie'

    def find_min(self):
        min_val = 1
        for node in self.children:
            if node.value < min_val:
                min_val = node.value
        return min_val

    def find_max(self):
        max_val = -1
        for node in self.children:
            if node.value > max_val:
                max_val = node.value
        return max_val

    def __str__(self):
        height = len(self.board)
        width = len(self.board[0])
        result = "  "
        for i in range(width):
            result += str(i + 1) + " "
        result += "\n"

        for i in range(height):
            result += str(i + 1) + " "
            for j in range(width):
                result += self.board[i][j] + " "
            result += "\n"
        return result


class Tree:

    def __init__(self, root):
        self.root = root

    def build_tree(self, node):
        win, who_won = node.is_win()
        if win:
            if who_won == 'Tie':
                node.value = 0
            elif who_won == 'O':
                node.value = -1
            elif who_won == 'X':
                node.value = 1
            return
        width = len(node.board)
        height = len(node.board[0])
        for i in range(width):
            for j in range(height):
                if node.board[i][j] == '-':
                    new_board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
                    node.copy_board(new_board)
                    temp = 'X'
                    if node.prev_player == 'X':
                        temp = 'O'
                    new_board[i][j] = temp
                    new_node = Node(new_board, temp, 0)
                    node.children.append(new_node)
                    self.build_tree(new_node)
        if node.prev_player == 'X':
            node.value = node.find_min()
        else:
            node.value = node.find_max()


def play_game():
    game_board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

    # process first move and build tree
    row = input("Enter the row: ")
    col = input("Enter the col: ")
    game_board[int(row) - 1][int(col) - 1] = 'X'

    root = Node(game_board, 'X', 0)
    game_tree = Tree(root)
    game_tree.build_tree(root)

    print(root)
    current = root
    done, winner = current.is_win()
    while not done:
        print("hmmmm...")
        time.sleep(1)
        print("thinking...\n")
        time.sleep(1)

        min = 1
        next_min = current.children[0]
        terminal = False
        i = 0
        length = len(current.children)
        while not terminal and i < length:
            if current.children[i].value <= min:
                min = current.children[i].value
                next_min = current.children[i]
                terminal, temp = next_min.is_win()
            i += 1
        current = next_min

        current.copy_board(game_board)
        print(current)

        done, winner = current.is_win()
        if not done:
            row = input("Enter the row: ")
            col = input("Enter the col: ")
            game_board[int(row) - 1][int(col) - 1] = "X"

            found = False
            i = 0
            length = len(current.children)
            while (not found) and i < length:
                if current.children[i].board == game_board:
                    found = True
                    current = current.children[i]
                    print(current)
                else:
                    i += 1

        done, winner = current.is_win()
    if winner == 'Tie':
        print("Tie game!")
    else:
        print(winner + " won the game!")


def main():
    next_game = 'y'
    while next_game == 'y':
        play_game()
        next_game = input("Would you like to play again?(y/n) ")


if __name__ == '__main__':
    main()
