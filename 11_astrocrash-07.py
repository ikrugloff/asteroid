# Прерванный полёт-07
# Анимированные взрывы + оптимизация кода (удаление дублирования кода)

import random
import games
import os
import math

STATIC = 'static'

# Вызываем метод, инициализирующий окно
games.init(screen_width=640, screen_height=480, fps=50)


class Wrapper(games.Sprite):
    """ Огибатель. Спрайт, который, двигаясь, огибает графический экран. """

    def update(self):
        """ Перенносит спрайт на противоположную сторону окна. """
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

    def __init__(self, x, y, size):
        """ Инициализирует спрайт с изображением астеройда. """
        super(Asteroid, self).__init__(
            image=Asteroid.images[size],
            x=x, y=y,
            dx=random.choice([1, -1]) * Asteroid.SPEED * random.random() / size,
            dy=random.choice([1, -1]) * Asteroid.SPEED * random.random() / size)

        self.size = size

    def die(self):
        """ Разрушает астеройд. """
        # если размеры астеройда крупные или средние, заменить его 2-мя более мелкими астеройдами
        if self.size != Asteroid.SMALL:
            for i in range(Asteroid.SPAWN):
                new_asteroid = Asteroid(x=self.x,
                                        y=self.y,
                                        size=self.size - 1)
                games.screen.add(new_asteroid)

        super(Asteroid, self).die()


class Ship(Collider):
    """ Корабль игрока. """
    image = games.load_image(os.path.join(STATIC, 'ship.bmp'))
    # thrust.wav - звук ускоряющегося рывка
    sound = games.load_sound(os.path.join(STATIC, 'thrust.wav'))
    ROTATION_STEP = 3
    # VELOCITY_STEP - константа для описания изменения скорости корабля
    VELOCITY_STEP = .03
    # MISSILE_DELAY - количество обновлений экрана, в течение которых игрок не может выпустить ракету после очередного
    # запуска
    MISSILE_DELAY = 25

    def __init__(self, x, y):
        """ Инициализирует спрайт с изображением космического корабля. """
        super(Ship, self).__init__(image=Ship.image, x=x, y=y)
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

        # если запуск следующей ракеты пока ещё не разрешён, вычесть 1 из длины оставшегося интервала ожидания
        if self.missile_wait > 0:
            self.missile_wait -= 1

        # если нажат Space и интервал ожидания истёк, выпустить ракету
        if games.keyboard.is_pressed(games.K_SPACE) and self.missile_wait == 0:
            new_missile = Missile(self.x, self.y, self.angle)
            games.screen.add(new_missile)
            self.missile_wait = Ship.MISSILE_DELAY


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


def main():
    # назначаем фоновую картинку
    nebula_image = games.load_image(os.path.join(STATIC, 'nebula.jpg'))
    games.screen.background = nebula_image

    # создаём 8 астеройдов
    for i in range(8):
        x = random.randrange(games.screen.width)
        y = random.randrange(games.screen.height)
        size = random.choice([Asteroid.SMALL, Asteroid.MEDIUM, Asteroid.LARGE])
        new_asteroid = Asteroid(x=x, y=y, size=size)
        games.screen.add(new_asteroid)

    # создаём корабль
    the_ship = Ship(x=games.screen.width / 2, y=games.screen.height / 2)
    games.screen.add(the_ship)

    games.screen.mainloop()


# Поехали!
main()
