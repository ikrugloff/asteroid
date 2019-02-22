# Взрыв
# Демонстрирует создание анимации

import games
import os

STATIC = 'static'

# Вызываем метод, инициализирующий окно
games.init(screen_width=640, screen_height=480, fps=50)

nebula_image = games.load_image(os.path.join(STATIC, 'nebula.jpg'), transparent=False)
games.screen.background = nebula_image

# Создадим список файлов-картинок, которые будут последовательно отображаться.
explosion_files = [os.path.join(STATIC, 'explosion1.bmp'),
                   os.path.join(STATIC, 'explosion2.bmp'),
                   os.path.join(STATIC, 'explosion3.bmp'),
                   os.path.join(STATIC, 'explosion4.bmp'),
                   os.path.join(STATIC, 'explosion5.bmp'),
                   os.path.join(STATIC, 'explosion6.bmp'),
                   os.path.join(STATIC, 'explosion7.bmp'),
                   os.path.join(STATIC, 'explosion8.bmp'),
                   os.path.join(STATIC, 'explosion9.bmp')]

# Класс Animation произведён от Sprite и наследует все его атрибуты, свойства и методы.
explosion = games.Animation(images=explosion_files,
                            x=games.screen.width / 2,
                            y=games.screen.height / 2,
                            n_repeats=0,
                            repeat_interval=5)
games.screen.add(explosion)

games.screen.mainloop()
