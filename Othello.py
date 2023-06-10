# Author: Justin Huang
# GitHub username: huangjus
# Date: 6/9/23
# Description: This Python code implements a text-based version of the Othello game. It has two classes, `Player` and
# `Othello`. `Player` creates players with a name and a color (black or white). The `Othello` class represents the game,
# maintaining the game board and players. It includes methods to print the game board, create players, determine
# the game winner, return available move positions for a player, update the game board with a player's move, and
# direct the game flow. The game concludes when no more moves are possible and the winner is determined by the most
# pieces on the board.

class Player:
    """Player class that represents a player in the game."""

    def __init__(self, name, color):
        """Initialize a player with a name and a color.

        name: Player's name.
        color: Player's piece color. Either "black" or "white".
        """
        self._name = name
        self._color = color


class Othello:
    """Othello class that represents the game as played."""

    def __init__(self):
        """Initialize a game with the default board setting."""
        self._board = [['*' if i == 0 or i == 9 or j == 0 or j == 9 else '.' for j in range(10)] for i in range(10)]
        self._board[4][4] = 'O'
        self._board[5][5] = 'O'
        self._board[4][5] = 'X'
        self._board[5][4] = 'X'
        self._players = []
        self._directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    def print_board(self):
        """Prints the current game board, including the boundaries."""
        for row in self._board:
            print(' '.join(row))
        print()

    def create_player(self, player_name, color):
        """Creates a player object and adds it to the player list.

        player_name: Player's name.
        color: Player's color. Either "black" or "white".
        """
        player = Player(player_name, color)
        self._players.append(player)

    def return_winner(self):
        """Returns the winner of the game.

        Returns: The name of the winner or a statement indicating a tie.
        """
        count_black = sum(row.count('X') for row in self._board)
        count_white = sum(row.count('O') for row in self._board)
        if count_black > count_white:
            return f"Winner is black player: " \
                   f"{self._players[0]._name if self._players[0]._color == 'black' else self._players[1]._name}"
        elif count_white > count_black:
            return f"Winner is white player: " \
                   f"{self._players[0]._name if self._players[0]._color == 'white' else self._players[1]._name}"
        else:
            return "It's a tie"

    def return_available_positions(self, color):
        """Returns a list of possible positions for a move.

        color: The color of the player's piece.

        Returns: A list of possible positions for a move.
        """
        positions = []
        opponent = 'O' if color == 'X' else 'X'
        for i in range(1, 9):
            for j in range(1, 9):
                if self._board[i][j] == '.':
                    for direction in self._directions:
                        x, y = i+direction[0], j+direction[1]
                        if self._board[x][y] == opponent:
                            while self._board[x][y] == opponent:
                                x += direction[0]
                                y += direction[1]
                            if self._board[x][y] == color:
                                positions.append((i, j))
        return positions

    def make_move(self, color, piece_position):
        """Puts a piece at the given position and updates the board.

            color: The color of the piece to place.
            piece_position: The position to place the piece.

            Returns: The current state of the game board.
            """
        i, j = piece_position
        self._board[i][j] = color
        opponent = 'O' if color == 'X' else 'X'
        for direction in self._directions:
                x, y = i + direction[0], j + direction[1]
                if self._board[x][y] == opponent:
                    while self._board[x][y] == opponent:
                        x += direction[0]
                        y += direction[1]
                    if self._board[x][y] == color:
                        while x != i or y != j:
                            x -= direction[0]
                            y -= direction[1]
                            self._board[x][y] = color
        return self._board

    def play_game(self, player_color, piece_position):
        """Attempts to make a move for the player at the specified position.

        player_color: The color of the player's piece.
        piece_position: The position to place the piece.

        Returns: A message indicating the result of the attempted move.
        """
        color = 'X' if player_color == 'black' else 'O'
        valid_positions = self.return_available_positions(color)
        if piece_position not in valid_positions:
            return "Invalid move\nHere are the valid moves:" + str(valid_positions)
        else:
            self.make_move(color, piece_position)
            if not self.return_available_positions('O') and not self.return_available_positions('X'):
                count_black = sum(row.count('X') for row in self._board)
                count_white = sum(row.count('O') for row in self._board)
                print(f"Game is ended. White pieces: {count_white}, Black pieces: {count_black}")
                print(self.return_winner())
            return "Move completed."
