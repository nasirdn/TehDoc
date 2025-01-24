class Settings():
    """
    Класс для хранения всех настроек игры Alien Invasion.

    Args:
        screen_width (int): Ширина экрана игры.
        screen_height (int): Высота экрана игры.
        bg_color (tuple): Цвет фона игры в формате RGB.
        ship_speed (float): Скорость перемещения корабля.
        ship_limit (int): Максимальное количество кораблей, доступных игроку.
        bullet_speed (float): Скорость снарядов.
        bullet_width (int): Ширина снаряда.
        bullet_height (int): Высота снаряда.
        bullet_color (tuple): Цвет снаряда в формате RGB.
        bullet_allowed (int): Максимальное количество снарядов, которые могут быть на экране одновременно.
        alien_speed (float): Скорость перемещения пришельцев.
        fleet_drop_speed (int): Скорость, с которой пришельцы опускаются вниз.
        fleet_direction (int): Направление движения флота пришельцев (1 для вправо, -1 для влево).
        speedup_scale (float): Темп увеличения скорости игры.
        score_scale (float): Темп увеличения стоимости пришельцев.
        ship_speed_factor (float): Фактор изменения скорости корабля во время игры.
        bullet_speed_factor (float): Фактор изменения скорости снарядов во время игры.
        alien_speed_factor (float): Фактор изменения скорости пришельцев во время игры.
        alien_points (int): Количество очков, получаемых за уничтожение пришельца.
    """

    def __init__(self):
        """
        Инициализирует статические настройки игры.
        """
        # Параметры экрана
        self.screen_width = 1200
        self.screen_height = 750
        self.bg_color = (70, 130, 180)

        # Настройки корабля
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Параметры снаряда
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3

        # Настройка пришельцев
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_diraction = 1

        # Темп ускорения игры
        self.speedup_scale = 1.1

        # Темп роста стоимости пришельцев
        self.score_scale = 1.5

        self.initialize_dinamic_settings()

    def initialize_dinamic_settings(self):
        """
        Инициализирует настройки, изменяющиеся в ходе игры.

        Эти настройки включают скорость корабля, скорость снарядов и скорость пришельцев.
        Также устанавливается начальное количество очков за уничтожение пришельца.
        """
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3.0
        self.alien_speed_factor = 1.0

        self.fleet_diraction = 1

        # Подсчет очков
        self.alien_points = 50

    def increase_speed(self):
        """
        Увеличение настройки скорости и стоимость пришельцев.

        Вызывается для увеличения сложности игры по мере прогресса игрока.
        Увеличивает скорость корабля, снарядов и пришельцев, а также
        увеличивает количество очков, получаемых за уничтожение пришельцев.
        """
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)