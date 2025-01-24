class GameStats():
    """Отслеживание статистики для игры Alien Invasion."""

    def __init__(self, ai_game):
        """
        Инициализирует статистику.

        Args:
            ai_game: Экземпляр класса игры, содержащий настройки игры.
        """
        self.settings = ai_game.settings
        self.reset_stats()

        # Игра запускается в неактивном состоянии.
        self.game_active = False

        # Рекорд не должен сбрасываться.
        self.high_score = 0
        self.level = 1

    def reset_stats(self):
        """
        Инициализирует статистику, изменяющуюся в ходе игры.

        Сбрасывает количество оставшихся кораблей и счет до начальных значений.
        """
        self.ships_left = self.settings.ship_limit
        self.score = 0