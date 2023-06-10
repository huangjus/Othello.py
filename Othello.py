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
    def __init__(self, name, color):
        """
        Initialize a Player with a name and a color.

        Args:
            name: Player's name
            color: Color of the player's pieces ("black" or "white")
        """
        self._name = name
        self._color = color


class Othello:
    _directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    def __init__(self):
        """
        Initialize an Othello game with an empty board and no players.
        """
        self._board = [['*' for _ in range(10)] for _ in range(10)]
        for i in range(1, 9):
            for j in range(1, 9):
                self._board[i][j] = '.'
        self._board[4][4], self._board[5][5] = 'X', 'X'
        self._board[4][5], self._board[5][4] = 'O', 'O'
        self.players = []

    def print_board(self):
        """
        Print the current state of the game board.
        """
        for row in self._board:
            print(' '.join(row))

    def create_player(self, player_name, color):
        """
        Create a Player and add them to the list of players.

        Args:
            player_name: Player's name
            color: Color of the player's pieces ("black" or "white")
        """
        color = 'X' if color == 'black' else 'O'
        self.players.append(Player(player_name, color))

    def return_winner(self):
        """
        Return the winner of the game based on the current state of the board.

        Returns:
            A string indicating the winner or declaring a tie
        """
        count_black = sum(row.count('X') for row in self._board)
        count_white = sum(row.count('O') for row in self._board)
        if count_black > count_white:
            winner = next(player._name for player in self.players if player._color == 'X')
            return f"Winner is black player: {winner}"
        elif count_white > count_black:
            winner = next(player._name for player in self.players if player._color == 'O')
            return f"Winner is white player: {winner}"
        else:
            return "It's a tie"

    def return_available_positions(self, color):
        """
        Return a list of available positions for a player.

        Args:
            color: Color of the player's pieces ("black" or "white")

        Returns:
            A list of tuples representing available positions on the board
        """
        positions = []
        for i in range(1, 9):
            for j in range(1, 9):
                if self._board[i][j] == '.':
                    for direction in self._directions:
                        if self._check_line_match(i, j, direction, color):
                            positions.append((i, j))
                            break
        return positions

    def _check_line_match(self, i, j, direction, color):
        """
        Check if a line matches a player's color in a specific direction.

        Args:
            i, j: Position on the board to check from
            direction: Direction to check in
            color: Color to check for

        Returns:
            True if a match is found, False otherwise
        """
        i += direction[0]
        j += direction[1]
        if self._board[i][j] == '.' or self._board[i][j] == '*' or self._board[i][j] == color:
            return False
        while self._board[i][j] != '*':
            i += direction[0]
            j += direction[1]
            if self._board[i][j] == color:
                return True
        return False

    def make_move(self, color, piece_position):
        """
        Make a move for a player at a specified position.

        Args:
            color: Color of the player's pieces ("black" or "white")
            piece_position: Position on the board to place a piece
        """
        i, j = piece_position
        self._board[i][j] = color
        for direction in self._directions:
            if self._check_line_match(i, j, direction, color):
                self._flip_pieces_in_line(i, j, direction, color)
        return self._board

    def _flip_pieces_in_line(self, i, j, direction, color):
        """
        Flip pieces in a line in a specific direction.

        Args:
            i, j: Position on the board to flip pieces from
            direction: Direction to flip pieces in
            color: Color of pieces to flip to
        """
        i += direction[0]
        j += direction[1]
        while self._board[i][j] != color:
            self._board[i][j] = color
            i += direction[0]
            j += direction[1]

    def play_game(self, player_color, piece_position):
        """
        Attempt a move for a player and update the game state accordingly.

        Args:
            player_color: Color of the player making the move ("black" or "white")
            piece_position: Position on the board to make the move
        """
        color = 'X' if player_color == 'black' else 'O'
        if piece_position not in self.return_available_positions(color):
            print("Invalid move")
            print("Here are the valid moves:", self.return_available_positions(color))
            return "Invalid move"
        else:
            self.make_move(color, piece_position)
            if not (self.return_available_positions('X') or self.return_available_positions('O')):
                print("Game is ended white piece: ", sum(row.count('O') for row in self._board),
                      "black piece: ", sum(row.count('X') for row in self._board))
                print(self.return_winner())
