import os
import sys
import random
from time import sleep
import pygame
import pickle

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from bonus import Bonus


class AlienInvasion:
    """
    Класс для управления ресурсами и поведением игры.

    Args:
        settings (Settings): Настройки игры.
        screen (Surface): Отображение игрового окна.
        stats (GameStats): Статистика игры.
        sb (Scoreboard): Панель результатов.
        ship (Ship): Игрокский корабль.
        bullets (Group): Группа снарядов.
        aliens (Group): Группа пришельцев.
        bonuses (Group): Группа бонусов.
        shot_sound (Sound): Звук выстрела.
        gameover_sound (Sound): Звук окончания игры.
        kill_sound (Sound): Звук уничтожения пришельца.
        lostlife_sound (Sound): Звук потери жизни.
        play_button (Button): Кнопка для начала игры.
        bg_color (tuple): Цвет фона.
    """
    def __init__(self):
        """
        Инициализирует игру и создает игровые ресурсы.
        """
        pygame.init()
        self.settings = Settings()

        # Отдельное окно
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Alien Invasion")

        # Создание экземпляров для хранения статистики и панели результатов.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.bonuses = pygame.sprite.Group()

        #Инициализация звуков
        self.shot_sound = pygame.mixer.Sound(os.path.join('resources/shot.wav'))
        self.gameover_sound = pygame.mixer.Sound(os.path.join('resources/game_over.wav'))
        self.kill_sound = pygame.mixer.Sound(os.path.join('resources/kill.wav'))
        self.lostlife_sound = pygame.mixer.Sound(os.path.join('resources/lost_a_life.wav'))

        self._create_fleet()

        # Создание кнопки Play.
        self.play_button = Button(self, "Play")

        # Назначение цвета фона.
        self.bg_color = (70, 130, 180)

    def run_game(self):
        """
        Запуск основного цикла игры.
        Этот метод запускает основной цикл игры, который обрабатывает события,
        обновляет состояние игры и перерисовывает экран.
        """
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_bonuses()

            self._update_screen()

    def _save_game(self):
        """
        Сохранение текущего состояния игры в файл.
        Сохраняет уровень, счет и количество жизней в файл `savefile.pkl
        """
        game_data = {
            "level": self.stats.level,
            "score": self.stats.score,
            "lives": self.stats.ships_left
        }
        with open("savefile.pkl", "wb") as f:
            pickle.dump(game_data, f)

    def _load_game(self):
        """
        Загружение состояния игры из файла.
        Загружает уровень, счет и количество жизней из файла `savefile.pkl`.
        Если файл не найден, выводит сообщение об ошибке.
        """
        try:
            with open("savefile.pkl", "rb") as f:
                game_data = pickle.load(f)
                self.stats.level = game_data["level"]
                self.stats.score = game_data["score"]
                self.stats.ships_left = game_data["lives"]
                self.sb.prep_score()
                self.sb.prep_level()
                self.sb.prep_ships()
        except FileNotFoundError:
            print("Файл сохранения не найден.")

    def _check_events(self):
        """
        Обрабатывает нажатие клавиш и события мыши.
        Проверяет события, такие как нажатие клавиш и клик мыши,
        и вызывает соответствующие методы для обработки этих событий.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """
        Запускает новую игру при нажатии кнопки Play.

        Проверяет, была ли нажата кнопка Play, и если игра не активна,
        сбрасывает настройки и запускает новую игру.

        :param:
            mouse_pos (tuple): Позиция курсора мыши при нажатии.
        """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Сброс игровых настроек
            self.settings.initialize_dinamic_settings()

            # Сброс игровой статистики.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Очистка списков пришельцев и снарядов.
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение корабля в центре.
            self._create_fleet()
            self.ship.center_ship()

            # Указатель мыши скрывается.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """
        Реагирует на нажатие клавиш

        :param:
            event (Event): Событие нажатия клавиши.
        """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_s:
            self._save_game()
        elif event.key == pygame.K_l:
            self._load_game()

    def _check_keyup_events(self, event):
        """
        Реагирует на отпускание клавиш

        :param:
            event (Event): Событие нажатия клавиши.
        """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """
        Создание нового снаряда и добавление его в группу снарядов.

        Проверяет, не превышает ли количество снарядов максимальное значение,
        установленное в настройках. Если нет, создается новый снаряд и
        воспроизводится звук выстрела.
        """
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.shot_sound.play()

    def _update_bullets(self):
        """
        Обновляет позиции снарядов и уничтожает старые снаряды.

        Удаляет снаряды, вышедшие за верхнюю границу экрана, и проверяет
        коллизии между снарядами и пришельцами.
        """
        # Обновление позиций снарядов.
        self.bullets.update()

        # Удаление снарядов, вышедших за край экрана.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """
        Обработка коллизий снарядов с пришельцами.

        Удаляет снаряды и пришельцев, участвующих в коллизиях.
        Увеличивает счет игрока и может создавать бонусы.
        """
        # Удаление снарядов и пришельцев, участвующих в коллизиях.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.kill_sound.play()

                if random.random() < 0.3:  # 30% вероятность появления бонуса
                    bonus_type = random.choice(['life', 'shield', 'power'])
                    new_bonus = Bonus(self, bonus_type)
                    self.bonuses.add(new_bonus)

            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Уничтожение существующих снарядов и создание нового флота.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _update_bonuses(self):
        """
        Обновляет позиции бонусов и проверяет столкновения с кораблем.

        Проверяет, столкнулись ли бонусы с кораблем игрока, и применяет
        соответствующие эффекты, такие как добавление жизни, активация щита
        или увеличение количества снарядов.
        """
        self.bonuses.update()

        # Проверка на столкновение бонусов с кораблем
        collisions = pygame.sprite.spritecollide(self.ship, self.bonuses, True)
        for bonus in collisions:
            if bonus.bonus_type == 'life':
                self.stats.ships_left += 1
                self.sb.prep_ships()

            elif bonus.bonus_type == 'shield':
                self.ship.shield_active = True  # Включаем щит
                self.ship.shield_start_time = pygame.time.get_ticks()

            elif bonus.bonus_type == 'power':
                self.settings.bullet_allowed += 1  # Увеличиваем количество снарядов

    def _create_fleet(self):
        """
        Создание флота вторжения.

        Определяет количество пришельцев, которые могут поместиться на экране,
        и создает их.
        """
        # Создание пришельца.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        """Определяет количество рядов, помещающихся на экране."""
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Создание флота вторжения.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """
        Создание пришельца и размещение его в ряду.

        :param:
            alien_number (int): Индекс пришельца в ряду.
            row_number (int): Индекс ряда, в котором размещается пришелец.
        """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """
        Реагирует на достижение пришельцем края экрана.

        Проверяет, достиг ли какой-либо пришелец края экрана и меняет
        направление флота, если это необходимо.
        """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """
        Опускает весь флот и меняет направление флота.

        Меняет направление движения флота и опускает его вниз.
        """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_diraction *= -1

    def _update_aliens(self):
        """
        Проверяет, достиг ли флот края экрана, с последующим обновлением
        позиций всех пришельцев во флоте.

        Если флот достиг края экрана, изменяет его направление. Также
        проверяет на столкновение с кораблем игрока и на достижение
        нижней границы экрана пришельцами. Если все пришельцы уничтожены,
        создается новый флот и увеличивается скорость игры.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Проверка на столкновение корабля с пришельцами
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            if not self.ship.shield_active:  # Проверяем, активен ли щит
                self._ship_hit()

        # Проверить, добрались ли пришельцы до нижнего края экрана.
        self._check_aliens_bottom()

        # Проверка на переход на следующий уровень
        if not self.aliens:  # Если пришельцы уничтожены
            self.bullets.empty()  # Уничтожаем все снаряды
            self._create_fleet()  # Создаем новый флот
            self.settings.increase_speed()  # Увеличиваем скорость
            self.stats.level += 1
            self.sb.prep_level()

    def _check_aliens_bottom(self):
        """
        Проверяет, добрались ли пришельцы до нижнего края экрана.

        Если хотя бы один пришелец достигает нижней границы экрана,
        воспроизводится звук потери жизни и вызывается метод обработки
        удара по кораблю.
        """
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self.lostlife_sound.play()
                self._ship_hit()
                break

    def _ship_hit(self):
        """
        Обрабатывает столкновение корабля с пришельцами.

        Уменьшает количество оставшихся жизней игрока, обновляет
        панель счета, очищает списки пришельцев и снарядов, создает
        новый флот и размещает корабль в центре. Если жизни закончились,
        игра завершается.
        """
        if self.stats.ships_left > 0:
            # Уменьшение ships_left и обновление панели счета
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.lostlife_sound.play()

            # Очистка списков пришельцев и снарядов.
            self.aliens.empty()
            self.ship.center_ship()

            # Создание нового флота и размещение корабля в центре.
            self._create_fleet()
            self.ship.center_ship()

            # Пауза
            sleep(0.5)
        else:
            self.stats.game_active = False
            self.gameover_sound.play()
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """
        Обновляет изображения на экране и отображает новый экран.

        Заполняет экран фоновым цветом, отображает корабль, снаряды,
        пришельцев и бонусы. Также отображает текущий счет. Если игра
        не активна, отображает кнопку "Play".
        """
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.bonuses.draw(self.screen)
        self.sb.show_score()


        # Кнопка Play отображается в том случае, если игра не активна.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Отображение последнего прорисованного экрана.
        pygame.display.flip()