import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.addstr(0, 0, "+" + "-" * self.life.cols + "+")
        screen.addstr(self.life.rows + 1, 0, "+" + "-" * self.life.cols + "+")
        for i in range(1, self.life.rows + 1):
            screen.addch(i, 0, ord("|"))
            screen.addch(i, self.life.cols + 1, ord("|"))

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                char = "*" if self.life.curr_generation[row][col] else " "
                screen.addch(row + 1, col + 1, ord(char))

    def run(self) -> None:
        screen = curses.initscr()
        curses.curs_set(0)
        screen.clear()
        self.draw_borders(screen)
        self.draw_grid(screen)
        screen.refresh()
        screen.nodelay(True)
        screen.timeout(200)
        while True:
            key = screen.getch()
            if key != -1 and chr(key) == "q":
                break
            if not self.life.is_changing or self.life.is_max_generations_exceeded:
                break
            self.life.step()
            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
        curses.endwin()


if __name__ == "__main__":
    game = GameOfLife(size=(15, 80), randomize=True, max_generations=10000)
    ui = Console(game)
    ui.run()
