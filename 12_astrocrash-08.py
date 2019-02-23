# Прерванный полёт-08
# Система уровней, игровая статистика, музыкальная тема  + оптимизация кода

import random
import os
import math

import games
import color

STATIC = 'static'

# Вызываем метод, инициализирующий окно
games.init(screen_width=640, screen_height=480, fps=50)


class Wrapper(games.Sprite):
    """ Огибатель. Спрайт, который, двигаясь, огибает графический экран. """

    def update(self):
        """ Переносит спрайт на противоположную сторону окна. """
        if self.top > games.screen.height:
            self.bottom = 0

        if self.bottom < 0:
            self.top = games.screen.height

        if self.left > games.screen.width:
            self.right = 0

        if self.right < 0:
            self.left = games.screen.width

    def die(self):
        """ Разрушает объект(self). """
        self.destroy()


class Collider(Wrapper):
    """ Погибатель. Огибатель, котторый  может сталкиваться с другими объектами и гибнуть. """

    def update(self):
        """ Проверяет, нет ли спрайтов, визуально перекрывающихся с данным. """
        super(Collider, self).update()

        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()
            self.die()

    def die(self):
        """ Разрушает объект(self) со взрывом. """
        new_explosion = Explosion(x=self.x, y=self.y)
        games.screen.add(new_explosion)
        self.destroy()


class Asteroid(Wrapper):
    """ Астеройд, прямолинейно движущийся по экрану. """
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    images = {SMALL: games.load_image(os.path.join(STATIC, 'asteroid_small.bmp')),
              MEDIUM: games.load_image(os.path.join(STATIC, 'asteroid_med.bmp')),
              LARGE: games.load_image(os.path.join(STATIC, 'asteroid_big.bmp'))}

    SPEED = 2
    # SPAWN - количество новых астеройдов, но которое распадается один взорванный
    SPAWN = 2
    POINTS = 30
    # total - общая численность астеройдов
    total = 0

    def __init__(self, game, x, y, size):
        """ Инициализирует спрайт с изображением астеройда. """
        Asteroid.total += 1

        super(Asteroid, self).__init__(
            image=Asteroid.images[size],
            x=x, y=y,
            dx=random.choice([1, -1]) * Asteroid.SPEED * random.random() / size,
            dy=random.choice([1, -1]) * Asteroid.SPEED * random.random() / size)

        self.game = game
        self.size = size

    def die(self):
        """ Разрушает астеройд. """
        Asteroid.total -= 1

        self.game.score.value += int(Asteroid.POINTS / self.size)
        self.game.score.right = games.screen.width - 10

        # если размеры астеройда крупные или средние, заменить его 2-мя более мелкими астеройдами
        if self.size != Asteroid.SMALL:
            for i in range(Asteroid.SPAWN):
                new_asteroid = Asteroid(game=self.game,
                                        x=self.x,
                                        y=self.y,
                                        size=self.size - 1)
                games.screen.add(new_asteroid)

        # если больше астеройдов не осталось, переходим на следующий уровень   
        if Asteroid.total == 0:
            self.game.advance()

        super(Asteroid, self).die()


class Ship(Collider):
    """ Корабль игрока. """
    image = games.load_image(os.path.join(STATIC, 'ship.bmp'))
    # thrust.wav - звук ускоряющегося рывка
    sound = games.load_sound(os.path.join(STATIC, 'thrust.wav'))
    ROTATION_STEP = 3
    # VELOCITY_STEP - константа для описания изменения скорости корабля
    VELOCITY_STEP = .03
    # VELOCITY_MAX - константа ограничивающая максимальную скорость корабля
    VELOCITY_MAX = 3
    # MISSILE_DELAY - количество обновлений экрана, в течение которых игрок не может выпустить ракету после очередного
    # запуска
    MISSILE_DELAY = 25

    def __init__(self, game, x, y):
        """ Инициализирует спрайт с изображением космического корабля. """
        super(Ship, self).__init__(image=Ship.image, x=x, y=y)
        self.game = game
        self.missile_wait = 0

    def update(self):
        """ Вращает, ускоряет и выпускает ракеты при нажатии клавиш. """
        super(Ship, self).update()

        # вращает корабль при нажатии <- и ->
        if games.keyboard.is_pressed(games.K_LEFT):
            self.angle -= Ship.ROTATION_STEP
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.angle += Ship.ROTATION_STEP

        # корабль совершает рывок при нажатии стрелки вверх
        if games.keyboard.is_pressed(games.K_UP):
            Ship.sound.play()
            # изменение горизонтальной и вертикальной скорости корабля с учётом угла поворота
            angle = self.angle * math.pi / 180  # преобразование в радианы
            self.dx += Ship.VELOCITY_STEP * math.sin(angle)
            self.dy += Ship.VELOCITY_STEP * -math.cos(angle)

            # ограничение горизонтальной и вертикальной скорости
            self.dx = min(max(self.dx, -Ship.VELOCITY_MAX), Ship.VELOCITY_MAX)
            self.dy = min(max(self.dy, -Ship.VELOCITY_MAX), Ship.VELOCITY_MAX)

        # если запуск следующей ракеты пока ещё не разрешён, вычесть 1 из длины оставшегося интервала ожидания
        if self.missile_wait > 0:
            self.missile_wait -= 1

        # если нажат Space и интервал ожидания истёк, выпустить ракету
        if games.keyboard.is_pressed(games.K_SPACE) and self.missile_wait == 0:
            new_missile = Missile(self.x, self.y, self.angle)
            games.screen.add(new_missile)
            self.missile_wait = Ship.MISSILE_DELAY

    def die(self):
        """ Разрушает корабль и завершает игру. """
        self.game.end()
        super(Ship, self).die()


class Missile(Collider):
    """ Ракета, которую может выпустить космический корабль игрока. """
    image = games.load_image(os.path.join(STATIC, 'missile.bmp'))
    sound = games.load_sound(os.path.join(STATIC, 'missile.wav'))
    BUFFER = 40
    VELOCITY_FACTOR = 7
    LIFETIME = 40

    def __init__(self, ship_x, ship_y, ship_angle):
        """ Инициализация спрайта с изображением ракеты. """
        Missile.sound.play()

        # преобразование в радианы
        angle = ship_angle * math.pi / 180

        # вычисление начальной позиции ракеты
        buffer_x = Missile.BUFFER * math.sin(angle)
        buffer_y = Missile.BUFFER * -math.cos(angle)
        x = ship_x + buffer_x
        y = ship_y + buffer_y

        # вычисление горизонатльной и вертикальной скорости ракеты
        dx = Missile.VELOCITY_FACTOR * math.sin(angle)
        dy = Missile.VELOCITY_FACTOR * -math.cos(angle)

        # создание ракеты
        super(Missile, self).__init__(image=Missile.image,
                                      x=x, y=y,
                                      dx=dx, dy=dy)
        # атрибут lifetime ограничивает время странствия ракеты по космосу
        self.lifetime = Missile.LIFETIME

    def update(self):
        """ Перемещаем ракету. """
        super(Missile, self).update()

        # если lifetime ракеты истёк, то она уничтожается
        self.lifetime -= 1
        if self.lifetime == 0:
            self.destroy()


class Explosion(games.Animation):
    """ Анимированный взрыв. """
    sound = games.load_sound(os.path.join(STATIC, 'explosion.wav'))
    images = [os.path.join(STATIC, 'explosion1.bmp'),
              os.path.join(STATIC, 'explosion2.bmp'),
              os.path.join(STATIC, 'explosion3.bmp'),
              os.path.join(STATIC, 'explosion4.bmp'),
              os.path.join(STATIC, 'explosion5.bmp'),
              os.path.join(STATIC, 'explosion6.bmp'),
              os.path.join(STATIC, 'explosion7.bmp'),
              os.path.join(STATIC, 'explosion8.bmp'),
              os.path.join(STATIC, 'explosion9.bmp')]

    def __init__(self, x, y):
        super(Explosion, self).__init__(images=Explosion.images,
                                        x=x, y=y,
                                        repeat_interval=4, n_repeats=1,
                                        is_collideable=False)
        Explosion.sound.play()


class Game(object):
    """ Собственно игра. """

    def __init__(self):
        """ Инициализирует объект Game. """
        # выбор начального игрового уровня
        self.level = 0

        # загрузка звука, сопровождающего переход на следующий уровень
        self.sound = games.load_sound(os.path.join(STATIC, 'level.wav'))

        # создание объекта, в котором будет храниться текущий счёт
        self.score = games.Text(value=0,
                                size=30,
                                color=color.white,
                                top=5,
                                right=games.screen.width - 10,
                                is_collideable=False)
        games.screen.add(self.score)

        # создание корабля, которым будет управлять игрок
        self.ship = Ship(game=self,
                         x=games.screen.width / 2,
                         y=games.screen.height / 2)
        games.screen.add(self.ship)

    def play(self):
        """ Начинает игру. """
        # запуск музыкальной темы
        games.music.load(os.path.join(STATIC, 'theme.mid'))
        games.music.play(-1)

        # загрузка и назначение фоновой картинки
        nebula_image = games.load_image(os.path.join(STATIC, 'nebula.jpg'))
        games.screen.background = nebula_image

        # переход к уровню 1
        self.advance()

        # начало игры
        games.screen.mainloop()

    def advance(self):
        """ Переводит игру на очередной уровень. """
        self.level += 1

        # зарезервированное пространство вокруг корабля
        BUFFER = 150

        # создание новых астеройдов
        for i in range(self.level):
            # вычислим x и y, чтобы от корабля они отстояли минимум на BUFFER пикселов
            # сначала выберем минимальные отступы по горизонтали(x-axis) и вертикали(y-axis)
            x_min = random.randrange(BUFFER)
            y_min = BUFFER - x_min

            # исходя из этих минимумов, сгенерируем расстояния от корабля по горизонтали и вертикали
            x_distance = random.randrange(x_min, games.screen.width - x_min)
            y_distance = random.randrange(y_min, games.screen.height - y_min)

            # исходя из этих расстояний, вычислим экранные координаты
            x = self.ship.x + x_distance
            y = self.ship.y + y_distance

            # если необходимо, вернём объект внутрь окна
            x %= games.screen.width
            y %= games.screen.height

            # создадим астеройд
            new_asteroid = Asteroid(game=self,
                                    x=x, y=y,
                                    size=Asteroid.LARGE)
            games.screen.add(new_asteroid)

        # отображение номера уровня
        level_message = games.Message(value="Level " + str(self.level),
                                      size=40,
                                      color=color.yellow,
                                      x=games.screen.width / 2,
                                      y=games.screen.width / 10,
                                      lifetime=3 * games.screen.fps,
                                      is_collideable=False)
        games.screen.add(level_message)

        # звуковой эффект перехода на новый уровень (кроме первого)
        if self.level > 1:
            self.sound.play()

    def end(self):
        """ Завершает игру. """
        # 5-секундное отображение 'Game Over'
        end_message = games.Message(value="Game Over",
                                    size=90,
                                    color=color.red,
                                    x=games.screen.width / 2,
                                    y=games.screen.height / 2,
                                    lifetime=5 * games.screen.fps,
                                    after_death=games.screen.quit,
                                    is_collideable=False)
        games.screen.add(end_message)


def main():
    astrocrash = Game()
    astrocrash.play()


# Поехали!
main()
