import pathlib
import random
import typing as tp

from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            return [[random.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]
        else:
            return [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell
        neighbours = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr = row + dr
                nc = col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    neighbours.append(self.curr_generation[nr][nc])
        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = self.create_grid()
        for x, row in enumerate(self.curr_generation):
            for y, cell in enumerate(row):
                neighbours = self.get_neighbours((x, y))
                live_neighbours = sum(neighbours)
                if cell == 1:
                    if live_neighbours < 2 or live_neighbours > 3:
                        new_grid[x][y] = 0
                    else:
                        new_grid[x][y] = 1
                else:
                    if live_neighbours == 3:
                        new_grid[x][y] = 1
                    else:
                        new_grid[x][y] = 0
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is None or self.max_generations == float("inf"):
            return False
        else:
            return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename) as file:
            lines = file.readlines()
            grid = []
            for line in lines:
                row_str = line.rstrip()
                if row_str:
                    row = [int(c) for c in row_str]
                    grid.append(row)
            rows = len(grid)
            cols = len(grid[0]) if grid else 0
            game = GameOfLife((rows, cols), randomize=False)
            game.curr_generation = grid
            game.prev_generation = [row[:] for row in grid]
            game.generations = 1
            return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        to_write = ""
        for x, row in enumerate(self.curr_generation):
            for y, cell in enumerate(row):
                to_write += str(cell)
            to_write += "\n"

        with open(filename, "w") as file:
            file.write(to_write)
