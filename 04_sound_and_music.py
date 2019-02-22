# Звук и музыка
# Демонстрирует воспроизведение звуков и музыкальных файлов

import games
import os

STATIC = 'static'

# Вызываем метод, инициализирующий окно
games.init(screen_width=640, screen_height=480, fps=50)

# загрузка звукового файла
missile_sound = games.load_sound(os.path.join(STATIC, 'missile.wav'))

# загрузка музыкального файла
games.music.load(os.path.join(STATIC, 'theme.mid'))

choice = None
while choice != '0':

    print(
        """
        Звук и музыка
    
        0 - Выйти
        1 - Воспроизвести звук ракетного залпа
        2 - Циклизовать звук ракетного залпа
        3 - Остановить звук ракетного залпа
        4 - Воспроизвести музыкальную тему игры
        5 - Циклизовать музыкальную тему игры
        6 - Остановить музыкальную тему игры
        """
    )

    choice = input('Ваш выбор: ')
    print()

    # выход
    if choice == '0':
        print('До свидания.')

    # воспроизвести звук ракетного залпа
    elif choice == '1':
        missile_sound.play()
        print('Воспроизвожу звук ракетного залпа.')

    # циклизация звука ракетного залпа
    elif choice == '2':
        loop = int(input('Сколько ещё раз воспроизвести этот звук? (-1 = воспроизводить не переставая): '))
        missile_sound.play(loop)
        print('Циклизую звук ракетного залпа.')

    # остановка звука ракетного залпа
    elif choice == '3':
        missile_sound.stop()
        print('Останавливаю звук ракетного залпа.')

    # воспроизведение музыкальной темы
    elif choice == '4':
        games.music.play()
        print('Исполняю музыкальную тему игры.')

    # циклизация музыкальной темы
    elif choice == '5':
        loop = int(input('Сколько ещё раз воспроизвести эту музыку? (-1 = воспроизводить не переставая): '))
        games.music.play(loop)
        print('Циклизую музыкальную тему игры.')

    # остановка музыкальной темы
    elif choice == '6':
        games.music.stop()
        print('Останавливаю музыкальную тему игры.')

    # непонятный пользовательский ввод
    else:
        print('Извините, в меню нет пункта ', choice)

input('\n\nНажмите Enter, чтобы выйти.')
