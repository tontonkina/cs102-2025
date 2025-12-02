import tkinter as tk
from typing import List, Union
from tkinter import ttk, messagebox
from maze import bin_tree_maze, solve_maze, add_path_to_grid


def draw_cell(x, y, color, size: int = 10):
    x *= size
    y *= size
    x1 = x + size
    y1 = y + size
    canvas.create_rectangle(x, y, x1, y1, fill=color)


def draw_maze(grid: List[List[Union[str, int]]], size: int = 10):
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == " ":
                colour = "White"
            elif cell == "■":
                colour = "black"
            elif cell == "X":
                colour = "blue"
            draw_cell(y, x, colour, size)


def show_solution():
    maze, path = solve_maze(GRID)
    maze = add_path_to_grid(GRID, path)
    if path:
        draw_maze(maze, CELL_SIZE)
    else:
        tk.messagebox.showinfo("Message", "No solutions")


if __name__ == "__main__":
    global GRID, CELL_SIZE
    N, M = 51, 77

    CELL_SIZE = 10
    GRID = bin_tree_maze(N, M)

    _, PATH = solve_maze(GRID)
    while not PATH:
        print("No solutions. Regenerating maze...")
        GRID = bin_tree_maze(N, M)
        _, PATH = solve_maze(GRID)

    window = tk.Tk()
    window.title("Maze")
    window.geometry("%dx%d" % (M * CELL_SIZE + 100, N * CELL_SIZE + 100))

    canvas = tk.Canvas(window, width=M * CELL_SIZE, height=N * CELL_SIZE)
    canvas.pack()

    draw_maze(GRID, CELL_SIZE)
    ttk.Button(window, text="Solve", command=show_solution).pack(pady=20)

    window.mainloop()
