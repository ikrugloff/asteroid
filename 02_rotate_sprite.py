# Крутящийся спрайт
# Демонстрирует вращение спрайта

import games
import os

STATIC = 'static'

# Вызываем метод, инициализирующий окно
games.init(screen_width=640, screen_height=480, fps=50)


class Ship(games.Sprite):
    """ Вращающийся космический корабль. """

    def update(self):
        """ Вращает корабль определённым образом, исходя из нажатых клавиш. """
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.angle += 1
        if games.keyboard.is_pressed(games.K_LEFT):
            self.angle -= 1

        if games.keyboard.is_pressed(games.K_1):
            self.angle = 0
        if games.keyboard.is_pressed(games.K_2):
            self.angle = 90
        if games.keyboard.is_pressed(games.K_3):
            self.angle = 180
        if games.keyboard.is_pressed(games.K_4):
            self.angle = 270


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
