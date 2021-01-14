import logging
from copy import deepcopy
from itertools import product
from typing import Iterable, List


class Cell:
    digits: List[int]
    determined: bool

    def __init__(self):
        self.digits = list(range(1, 10))
        self.determined = False

    def determine(self, n: int) -> None:
        self.digits = [n]
        self.determined = True

    def erase(self, n: int) -> None:
        if n in self.digits:
            self.digits.remove(n)


class WorkingTable:
    cells: List[List[Cell]]

    def __init__(self, table: List[List[int]]):
        self.cells = [[Cell() for _ in range(9)] for _ in range(9)]
        for x, y in product(range(9), repeat=2):
            n = table[y][x]
            if n > 0:
                self.determine(x, y, n)

    def copy(self) -> 'WorkingTable':
        return deepcopy(self)

    def determine(self, x: int, y: int, n: int) -> None:
        self.erase_n_from_row(x, n)
        self.erase_n_from_column(y, n)
        self.erase_n_from_block(x, y, n)
        self.cells[y][x].determine(n)

    def erase_n_from_row(self, x: int, n: int) -> None:
        for y in range(9):
            self.cells[y][x].erase(n)

    def erase_n_from_column(self, y: int, n: int) -> None:
        for x in range(9):
            self.cells[y][x].erase(n)

    def erase_n_from_block(self, x: int, y: int, n: int) -> None:
        # the top-left coordinates in the block
        x0, y0 = x // 3 * 3, y // 3 * 3
        for dx, dy in product(range(3), repeat=2):
            x, y = x0 + dx, y0 + dy
            self.cells[y][x].erase(n)

    def to_list(self) -> List[List[int]]:
        return [[cell.digits[0] if cell.determined else 0
                 for cell in row] for row in self.cells]

    # for debug purpose
    def __str__(self) -> str:
        def init_buffer() -> List[List[str]]:
            l0 = list('#===+===+===#===+===+===#===+===+===#')
            l1 = list('H---+---+---H---+---+---H---+---+---H')
            l2 = list('H   |   |   H   |   |   H   |   |   H')
            return [l0[:], l2[:], l2[:], l2[:],
                    l1[:], l2[:], l2[:], l2[:],
                    l1[:], l2[:], l2[:], l2[:],
                    l0[:], l2[:], l2[:], l2[:],
                    l1[:], l2[:], l2[:], l2[:],
                    l1[:], l2[:], l2[:], l2[:],
                    l0[:], l2[:], l2[:], l2[:],
                    l1[:], l2[:], l2[:], l2[:],
                    l1[:], l2[:], l2[:], l2[:], l0[:]]

        def fill_determined_cell(x: int, y: int) -> None:
            buf_x = 4 * x + 2
            buf_y = 4 * y + 2
            buffer[buf_y][buf_x] = str(self.cells[y][x].digits[0])

        def fill_undetermined_cell(x: int, y: int) -> None:
            left = 4 * x + 1
            top = 4 * y + 1
            for n in range(1, 10):
                buf_x = left + (n - 1) % 3
                buf_y = top + (n - 1) // 3
                if n in self.cells[y][x].digits:
                    buffer[buf_y][buf_x] = str(n)
                else:
                    buffer[buf_y][buf_x] = 'x'

        def buffer_to_str() -> str:
            return '\n'.join(''.join(line) for line in buffer)

        buffer = init_buffer()
        for x, y in product(range(9), repeat=2):
            if self.cells[y][x].determined:
                fill_determined_cell(x, y)
            else:
                fill_undetermined_cell(x, y)

        return buffer_to_str()


def solve(table: List[List[int]]) -> Iterable[List[List[int]]]:
    def solve_wt(wt: WorkingTable) -> Iterable[List[List[int]]]:
        undetermined = [(x, y) for x in range(9) for y in range(9)
                        if not wt.cells[y][x].determined]
        if not undetermined:
            logger.info('solved')
            yield wt.to_list()
            return

        # pick one of the most determined coordinates
        x, y = min(undetermined,
                   key=lambda xy: len(wt.cells[xy[1]][xy[0]].digits))
        next_digits = wt.cells[y][x].digits

        # try each possibility
        # (in the case of inconsistency, particularly,
        # there's no possibility and this loop is skipped)
        for n in next_digits:
            logger.debug(f'place {n} at ({x}, {y}) '
                         f'out of {len(next_digits)} possibilities')
            copy = wt.copy()
            copy.determine(x, y, n)

            yield from solve_wt(copy)

    logger.info('start to solve')
    yield from solve_wt(WorkingTable(table))


logger = logging.getLogger(__name__)
