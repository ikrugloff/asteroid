# Читаю с клавиатуры
# Демонстрирует чтение клавиатурного ввода

import games
import os

STATIC = 'static'

# Вызываем метод, инициализирующий окно
games.init(screen_width=640, screen_height=480, fps=50)


# Следующее на повестке дня - создать класс для представленя корабля. В методе update() проверяется, нажата ли хоть
# одна из клавиш, обрабатываемых программой.
class Ship(games.Sprite):
    """ Подвижный космический корабль. """

    def update(self):
        """ Перемещает корабль определённым образом, исходя из нажатых клавиш. """
        if games.keyboard.is_pressed(games.K_w):
            self.y -= 1
        if games.keyboard.is_pressed(games.K_s):
            self.y += 1
        if games.keyboard.is_pressed(games.K_a):
            self.x -= 1
        if games.keyboard.is_pressed(games.K_d):
            self.x += 1


# Наконец функция main(). Она загружает фоновую картинку с туманностью, создаёт посередине экрана спрайт с изображением
# космического корабля и запускает работу графического окна вызовом mainloop().
def main():
    nebula_image = games.load_image(os.path.join(STATIC, 'nebula.jpg'), transparent=False)
    games.screen.background = nebula_image

    ship_image = games.load_image(os.path.join(STATIC, 'ship.bmp'))
    the_ship = Ship(image=ship_image,
                    x=games.screen.width / 2,
                    y=games.screen.height / 2)
    games.screen.add(the_ship)

    games.screen.mainloop()


main()
