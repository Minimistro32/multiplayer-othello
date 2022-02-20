from functools import reduce

class Board():

    def __init__(self, size):
        self._color_playing = 1

        if size % 2 != 0:
            size = size + 1

        board = [[" " for _ in range(size)] for _ in range(size)]

        half = size // 2
        board[half][half] = board[half - 1][half - 1] = 1
        board[half][half - 1] = board[half - 1][half] = 0

        self._grid = board

    def getDisplay(self):
        output = "\n"
        for n in range(len(self._grid)):
            output += "  " + str(n + 1) + " "

        for (i, row) in enumerate(self._grid):
            output += "\n" + "+---" * 8 + "+\n| "

            for col in row:
                output += str(col) + " | "

            output += " " + str(i + 1)

        output += "\n" + "+---" * 8 + "+\n"
        output += f"It is {self._color_playing}'s turn.\n"
        return output

    def play(self, row, col):
        vectors = self._getPlayableVectors(row, col)
        print("vectors: ", vectors,"\n")
        if len(vectors) > 0: #isPlayable
            self._setTile(row, col)
            for vec in vectors:
                self._setTiles(row, col, vec)
            self._endTurn()

    def isFull(self):
        return reduce(lambda isFull, row: isFull and reduce(lambda isFull, tile: isFull and tile != " ", row, True), self._grid, True)

    def getCurrentPlayer(self):
        return self._color_playing

    ##PRIVATE FUNCTIONS
    # GETTERS AND SETTERS
    def _size(self):
        return len(self._grid) + 1

    def _getTile(self, row, col):
        return self._grid[row - 1][col - 1]
    
    def _setTiles(self, row, col, vec):
        if self._getTile(row + vec[0], col + vec[1]) == self._getOppColor():
            self._setTile(row + vec[0], col + vec[1])
            self._setTiles(row + vec[0], col + vec[1], vec)

    def _setTile(self, row, col):
        self._grid[row - 1][col - 1] = self._color_playing

    def _isPosOnGrid(self, row, col):
        return row > 0 and row < self._size() and col > 0 and col < self._size()

    def _endTurn(self):
        self._color_playing = self._getOppColor()

    def _getOppColor(self):
        return 0 if self._color_playing == 1 else 1

    #HELPERS
    def _getPlayableVectors(self, row, col):
        validVectors = []
        if self._isPosOnGrid(row, col) and self._getTile(row, col) == " ":
            adjOppTiles = self._getAdjOppTiles(row, col)
            print("\nadjOppTiles: ", adjOppTiles)
            for tile in adjOppTiles:
                vec = (tile[0] - row, tile[1] - col)
                if self._searchPathForEnd(tile[0], tile[1], vec):
                    validVectors.append(vec)

        return validVectors

    def _getAdjOppTiles(self, row, col):
        tiles = []
        for xOff in range(-1,2):
            for yOff in range(-1,2):
                if self._isPosOnGrid(row + yOff, col + xOff) and self._getTile(row + yOff, col + xOff) == self._getOppColor():
                    tiles.append((row + yOff, col + xOff))
        return tiles

    def _searchPathForEnd(self, row, col, vec):
        if self._isPosOnGrid(row + vec[0], col + vec[1]):
            if self._getTile(row + vec[0], col + vec[1]) == self._color_playing:
                return True
            else:
                self._searchPathForEnd(row + vec[0], col + vec[1], vec)
        else:
            return False
