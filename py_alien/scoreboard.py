import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
    """
        Класс для вывода игровой информации, включая текущий счет, рекорды,
    уровень и количество оставшихся кораблей.

        Args:
            ai_game (object): Ссылка на экземпляр основного игрового класса.
            screen (Surface): Экран, на котором будет отображаться информация.
            screen_rect (Rect): Прямоугольник, представляющий размеры экрана.
            settings (Settings): Настройки игры.
            stats (Stats): Статистика игры, включая очки и уровень.
            bg_color (tuple): Цвет фона для текста.
            text_color (tuple): Цвет текста.
            font (Font): Шрифт для отображения текста.
            score_image (Surface): Изображение текущего счета.
            score_rect (Rect): Прямоугольник для размещения текущего счета.
            high_score_image (Surface): Изображение рекорда.
            high_score_rect (Rect): Прямоугольник для размещения рекорда.
            level_image (Surface): Изображение уровня.
            level_rect (Rect): Прямоугольник для размещения уровня.
            ships (Group): Группа кораблей, представляющих оставшиеся жизни игрока.
    """

    def __init__(self, ai_game):
        """
        Инициализирует атрибуты подсчета очков и подготавливает
        графические изображения для отображения.
        """
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.bg_color = self.settings.bg_color

        # Настройка шрифта для вывода счета.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Подготовка изображений счетов.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """
        Преобразует текущий счет в графическое изображение и устанавливает
        его позицию на экране.
        """
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(f"Счет: {score_str}", True, self.text_color, self.settings.bg_color)

        # Вывод счета в правой верхней части экрана.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """
        Преобразует рекордный счет в графическое изображение
        и устанавливает его позицию на экране.
        """
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(f"Рекорд: {high_score_str}", True, self.text_color, self.settings.bg_color)

        # Рекорд выравнивается по центру верхний стороны.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top

    def show_score(self):
        """
        Отображает текущий счет, рекорд, уровень и количество оставшихся
        кораблей на экране.
        """
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """
        Проверяет, появился ли новый рекорд, и обновляет его, если это так.
        """
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """
        Преобразует уровень в графическое изображение и устанавливает его
        позицию на экране.
        """
        level_str = str(self.stats.level)
        self.level_image = self.font.render(f"Уровень: {level_str}", True, self.text_color, self.bg_color)

        # Убедитесь, что rect правильно установлен
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """
        Создает графическое представление оставшихся кораблей и
        добавляет их в группу.
        """
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            self.ship = Ship(self.ai_game)
            self.ship.rect.x = 10 + ship_number * self.ship.rect.width
            self.ship.rect.y = 10
            self.ships.add(self.ship)