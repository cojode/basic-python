import random


def _validate_type_and_raise_otherwise(value, _type: type):
    if not isinstance(value, _type):
        raise TypeError(
            f"wrong type introduced for {value}: {type(value)}, should be {_type}"
        )


class GamePole:
    __slots__ = ("__mine_count", "__size", "__pole")

    class Cell:
        __slots__ = ("around_mines", "mine", "fl_open")

        def __init__(self, around_mines: int, mine: bool):
            self.around_mines: int = around_mines
            self.mine: bool = mine
            self.fl_open: bool = False

        def __str__(self):
            if not self.fl_open:
                return "#"
            if self.mine:
                return "*"
            return str(self.around_mines)

    @staticmethod
    def _validate_size(size: int):
        _validate_type_and_raise_otherwise(size, int)
        if size <= 0:
            raise ValueError(f"size must be higher than a zero: {size}")

    @staticmethod
    def _validate_mine_count(mine_count: int):
        _validate_type_and_raise_otherwise(mine_count, int)
        if mine_count < 0:
            raise ValueError(f"mine count must be non-negative: {mine_count}")

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, new_size: int):
        self._validate_size(new_size)
        if (
            hasattr(self, "_GamePole__mine_count")
            and new_size**2 < self.__mine_count
        ):
            raise ValueError(
                f"Pole size {new_size}x{new_size} can not contain this amount of mines: {self.mine_count}"
            )
        self.__size = new_size

    @property
    def mine_count(self):
        return self.__mine_count

    @mine_count.setter
    def mine_count(self, new_mine_count: int):
        self._validate_mine_count(new_mine_count)
        if hasattr(self, "_GamePole__size") and self.size**2 < new_mine_count:
            raise ValueError(
                f"Pole size {self.size}x{self.size} can not contain this amount of mines: {new_mine_count}"
            )
        self.__mine_count = new_mine_count

    def __init__(self, size: int, mine_count: int):
        self.size: int = size
        self.mine_count: int = mine_count
        self.init()

    def init(self):
        """Creates a minesweeper board and fills it with mines."""
        self.__pole = [
            [GamePole.Cell(0, False) for _ in range(self.size)]
            for _ in range(self.size)
        ]
        self._scatter_mines()

    def _scatter_mines(self):
        """Randomly generates mines layout and provides correct 'around_mines' values"""
        if self.mine_count == 0:
            return

        def obtain_random_cell_placement() -> tuple[int, int]:
            """Obtain random cell placement within provided board size.

            :return: obtained random placement - row and column in a tuple
            :rtype: tuple[int, int]
            """
            rand_mine_placement = random.randint(0, self.size**2 - 1)
            target_row, target_col = (
                rand_mine_placement // self.size,
                rand_mine_placement % self.size,
            )
            return target_row, target_col

        def update_around_mines(target_row: int, target_col: int):
            """Append all cell's 'around_mines' value around provided placement.

            :param target_row: row placement
            :type target_row: int
            :param target_col: row placement
            :type target_col: int
            """
            for row_offset in range(-1, 2):
                for col_offset in range(-1, 2):
                    neighbor_row = target_row + row_offset
                    neighbor_col = target_col + col_offset

                    if (
                        0 <= neighbor_row < self.size
                        and 0 <= neighbor_col < self.size
                    ):
                        self.__pole[neighbor_row][
                            neighbor_col
                        ].around_mines += 1

        for _ in range(self.mine_count):
            # ? iterate mine_count times
            target_row, target_col = obtain_random_cell_placement()
            # ? attempts to get random cell without a mine
            while self.__pole[target_row][target_col].mine:
                target_row, target_col = obtain_random_cell_placement()

            # ? sign it with mine
            self.__pole[target_row][target_col].mine = True

            # ? update affected cells
            update_around_mines(target_row, target_col)

    def show(self):
        for row in self.__pole:
            for cell in row:
                print(cell, end=" ")
            print("\n")

    def open_cell(self, cell_row: int, cell_col: int):
        _validate_type_and_raise_otherwise(cell_row, int)
        _validate_type_and_raise_otherwise(cell_col, int)
        if not (0 <= cell_row < self.size):
            raise IndexError(
                f"there are no row with provided index: {cell_row}"
            )
        if not (0 <= cell_col < self.size):
            raise IndexError(
                f"there are no column with provided index: {cell_col}"
            )

        self.__pole[cell_row][cell_col].fl_open = True

    def open_all(self):
        for row in self.__pole:
            for cell in row:
                cell.fl_open = True


gp = GamePole(10, 12)
