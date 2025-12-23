"""
Этот модуль предоставляет реализацию графического интерфейса для симуляции игры «Жизнь».
"""

import random
from pathlib import Path

import pygame
from pygame.locals import (KEYDOWN, MOUSEBUTTONDOWN, QUIT, K_l, K_p, K_q, K_r,
                           K_s)

from life import GameOfLife
from ui import UI


class GUI(UI):
    """Графический интерфейс для симуляции игры "Жизнь"."""

    def __init__(
        self, life_game: GameOfLife, cell_size: int = 10, speed: int = 10
    ) -> None:
        """Инициализация графического интерфейса."""
        super().__init__(life_game)
        self.cell_size = cell_size

        self.width = self.cell_size * life_game.cols
        self.height = self.cell_size * life_game.rows
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)

        self.grid_rows = life_game.rows
        self.grid_cols = life_game.cols

        self.speed = speed
        self.paused = False
        self.random_color = False

    def draw_lines(self) -> None:
        """Отрисовка линий сетки между ячейками."""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (x, 0), (x, self.height)
            )
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (0, y), (self.width, y)
            )

    def draw_grid(self, color="purple") -> None:
        """Отрисовка сетки с закрашенными живыми ячейками."""
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                x = col * self.cell_size
                y = row * self.cell_size
                if self.life.curr_generation[row][col] == 1:
                    if isinstance(color, tuple):
                        pygame.draw.rect(
                            self.screen,
                            pygame.Color(color),
                            (x, y, self.cell_size, self.cell_size),
                        )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        (x, y, self.cell_size, self.cell_size),
                    )

    def handle_key_events(self, event: pygame.event.Event) -> bool:
        """
        Обработка событий клавиатуры.

        Args:
            event: Событие клавиатуры для обработки

        Returns:
            False если программа должна завершиться, True в противном случае
        """
        if event.key == K_q:
            return False
        elif event.key == K_p:
            self.paused = not self.paused
            print(f"Пауза: {self.paused}")
        elif event.key == K_s:
            try:
                self.life.save(Path("save.txt"))
                print("Сохранено в save.txt")
            except (IOError, OSError) as e:
                print(f"Ошибка сохранения: {e}")
        elif event.key == K_l:
            try:
                self.life = GameOfLife.from_file(Path("save.txt"))
                print("Загружено из save.txt")
                self.width = self.cell_size * self.life.cols
                self.height = self.cell_size * self.life.rows
                self.screen = pygame.display.set_mode((self.width, self.height))
            except (IOError, OSError, ValueError) as e:
                print(f"Ошибка загрузки: {e}")
        elif event.key == K_r:
            self.random_color = not self.random_color
            print(f"Случайный цвет: {self.random_color}")
        return True

    def handle_mouse_events(self, event: pygame.event.Event) -> None:
        """Обработка событий мыши для переключения ячеек."""
        if event.button == 1 and self.paused:
            x, y = event.pos
            row = y // self.cell_size
            col = x // self.cell_size
            if 0 <= row < self.life.rows and 0 <= col < self.life.cols:
                self.life.curr_generation[row][col] = (
                    1 - self.life.curr_generation[row][col]
                )
                print(f"Клетка [{row},{col}] изменена")

    def run(self) -> None:
        """Запуск главного цикла графического интерфейса"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    running = self.handle_key_events(event)
                elif event.type == MOUSEBUTTONDOWN:
                    self.handle_mouse_events(event)

            self.screen.fill(pygame.Color("white"))

            self.draw_lines()
            if self.random_color:
                self.draw_grid(
                    color=(
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255),
                    )
                )
            else:
                self.draw_grid(color="purple")

            if not self.paused:
                self.life.step()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()


if __name__ == "__main__":
    life = GameOfLife(size=(50, 50))
    gui = GUI(life, cell_size=10, speed=10)
    gui.run()
