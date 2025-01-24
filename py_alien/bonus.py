import pygame
import random
import os
from pygame.sprite import Sprite


class Bonus(Sprite):
    """Класс для представления бонуса."""

    def __init__(self, ai_game, bonus_type):
        """
        Инициализирует бонус и задает его начальную позицию.

        Args:
            ai_game: Экземпляр класса игры, содержащий параметры экрана и настройки.
            bonus_type (str): Тип бонуса ('life', 'shield', 'power'), определяющий изображение и эффекты.
        """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.bonus_type = bonus_type

        # Загрузка изображения бонуса в зависимости от типа
        if self.bonus_type == 'life':
            self.image = pygame.image.load(os.path.join('resources/life.bmp'))
        elif self.bonus_type == 'shield':
            self.image = pygame.image.load(os.path.join('resources/shield.bmp'))
        elif self.bonus_type == 'power':
            self.image = pygame.image.load(os.path.join('resources/powerup.bmp'))

        self.rect = self.image.get_rect()

        # Позиция бонуса
        self.rect.x = random.randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = 0  # Начальная позиция вверху экрана

        self.speed = 1  # Скорость падения бонуса

    def update(self):
        """
        Обновляет позицию бонуса.
        Перемещает бонус вниз экрана с заданной скоростью.
        """
        self.rect.y += self.speed

    def draw_bonus(self):
        """
        Выводит бонус на экране.

        Отображает изображение бонуса в его текущей позиции на экране.
        """
        self.screen.blit(self.image, self.rect)
