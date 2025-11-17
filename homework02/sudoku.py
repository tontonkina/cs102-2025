import pathlib
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    sudoku_grid = group(digits, 9)
    return sudoku_grid


def display(sudoku_grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                sudoku_grid[row][col].center(width) + ("|" if str(col) in "25" else "")
                for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    if len(values) != n * n:
        raise ValueError

    return [values[i * n : (i + 1) * n] for i in range(n)]


def get_row(sudoku_grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    row, col = pos
    return sudoku_grid[row]


def get_col(sudoku_grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    row, col = pos
    return [sudoku_grid[i][col] for i in range(len(sudoku_grid))]


def get_block(sudoku_grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    row, col = pos
    block_row = (row // 3) * 3
    block_col = (col // 3) * 3

    result = []
    for i in range(block_row, block_row + 3):
        for j in range(block_col, block_col + 3):
            result.append(sudoku_grid[i][j])

    return result


def find_empty_positions(
    sudoku_grid: tp.List[tp.List[str]],
) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for i in range(len(sudoku_grid)):
        for j in range(len(sudoku_grid[i])):
            if sudoku_grid[i][j] == '.':
                return i, j
    return None


def find_possible_values(
    sudoku_grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]
) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    all_values = set(str(i) for i in range(1, 10))

    row_values = set(get_row(sudoku_grid, pos))
    col_values = set(get_col(sudoku_grid, pos))
    block_values = set(get_block(sudoku_grid, pos))

    used_values = row_values | col_values | block_values
    used_values.discard('.')

    return all_values - used_values

def solve(sudoku_grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """Решение пазла, заданного в grid"""
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    empty_pos = find_empty_positions(sudoku_grid)

    if empty_pos is None:
        return sudoku_grid

    row, col = empty_pos

    possible_values = find_possible_values(sudoku_grid, (row, col))

    if not possible_values:
        return None

    for value in possible_values:
        sudoku_grid[row][col] = value
        solutionn = solve(sudoku_grid)

        if solutionn is not None:
            return solutionn

        sudoku_grid[row][col] = '.'

    return None


def check_solution(solutionn: tp.List[tp.List[str]]) -> bool:
    """Если решение solution верно, то вернуть True, в противном случае False"""
    for i in range(9):
        row = get_row(solutionn, (i, 0))
        if set(row) != set('123456789'):
            return False

    for j in range(9):
        col = get_col(solutionn, (0, j))
        if set(col) != set('123456789'):
            return False

    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            block = get_block(solutionn, (i, j))
            if set(block) != set('123456789'):
                return False
    return True

import random
import typing as tp
def generate_sudoku(n: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    n = max(0, min(n, 81))

    sudoku_grid = [['.' for _ in range(9)] for _ in range(9)]

    for block in range(0, 9, 3):
        fill_block(sudoku_grid, block, block)

    solve(sudoku_grid)

    all_positions = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(all_positions)

    for i in range(81 - n):
        row, col = all_positions[i]
        sudoku_grid[row][col] = '.'

    return sudoku_grid


def fill_block(sudoku_grid: tp.List[tp.List[str]], start_row: int, start_col: int) -> None:
    numbers = list(range(1, 10))
    random.shuffle(numbers)

    idx = 0
    for i in range(3):
        for j in range(3):
            sudoku_grid[start_row + i][start_col + j] = str(numbers[idx])
            idx += 1


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
