import sys
import random
import pygame
import pygame_menu
from pygame.locals import *
import pygame.gfxdraw
from checkerboard import Checkerboard, WHITE_CHESSMAN, offset, Point, Black_color
from collections import namedtuple
from rc5 import RC5
import os


Chessman = namedtuple('Chessman', 'Name Value Color')
SIZE = 30 # Временной интервал каждой точки на доске
Line_Points = 19 # Количество точек на строку / столбец доски
Outer_Width = 20 # Наружная ширина доски
Border_Width = 4 # Ширина границы
Inside_Width = 4 # Интервал между границей и фактической шахматной доской
Border_Length = SIZE * (Line_Points-1) + Inside_Width * 2 + Border_Width # Длина линии границы
Start_X = Start_Y = Outer_Width + int (Border_Width / 2) + Inside_Width # Координаты начальной точки линии сетки (верхний левый угол)
SCREEN_HEIGHT = SIZE * (Line_Points-1) + Outer_Width * 2 + Border_Width + Inside_Width * 2 # Высота игрового экрана
SCREEN_WIDTH = SCREEN_HEIGHT + 200 # Ширина игрового экрана
color = Black_color
temp_player = 'Anoun'
win = 0
lose = 0
BLACK_CHESSMAN = ''

Stone_Radius = SIZE // 2-3 # радиус куска
Stone_Radius2 = SIZE // 2 + 3
Checkerboard_Color = (0xE3, 0x92, 0x65) # Цвет шахматной доски
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
RED_COLOR = (200, 30, 30)
BLUE_COLOR = (30, 30, 200)


RIGHT_INFO_POS_X = SCREEN_HEIGHT + Stone_Radius2 * 2 + 10



def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))


def set_color(value, temp_color):
    global color
    Red_color = (255, 0, 0)
    Black_color = (45, 45, 45)
    Blue_color = (0, 0, 255)
    Green_color = (0, 214, 120)
    print(temp_color)

    if temp_color == 1:
        color = Red_color
    elif temp_color == 2:
        color = Black_color
    elif temp_color == 3:
        color = Blue_color
    elif temp_color == 4:
        color = Green_color

def get_color_id():
    global color
    Red_color = (255, 0, 0)
    Black_color = (45, 45, 45)
    Blue_color = (0, 0, 255)
    Green_color = (0, 214, 120)
    color_id = 0
    if color == Red_color:
        color_id = 0
    elif color == Black_color:
        color_id = 1
    elif color == Blue_color:
        color_id = 2
    elif color == Green_color:
        color_id = 3
    else: 
        color_id = 0
    return color_id


def set_name(value):
    global temp_player
    temp_player = value

def settings_open(screen):
    settings_menu = pygame_menu.Menu('Настройки', 400, 300,
                    theme=pygame_menu.themes.THEME_GREEN)

    default_color = get_color_id()
    settings_menu.add.button('Играть', lambda screen=screen: start_game(screen))
    settings_menu.add.selector('Цвет шашек:', [("Красный", 1), ("Черный", 2), ("Синий", 3), ("Зелёный", 4)],
    onchange=set_color, default=default_color)
    settings_menu.add.button("Сохранить", save_settings)
    settings_menu.add.button('Назад', lambda screen=screen: start_window(screen))
    settings_menu.mainloop(screen)


def save_settings():
    global temp_player
    global color
    global win
    global lose
    encrypter = RC5(32, 12, b'\0' * 16)
    encrypter.decryptFile("temp_saves.json", "temp_saves_encr.json")
    settings = ''
    with open("temp_saves_encr.json", 'r') as f:
        temp_str = f.read()
        cut = temp_str.index(']')
        settings = eval(temp_str[:cut + 1])
        print(color)
        for player in settings:
            if player['name'] == temp_player:
                player['color'] = color
                player['win'] = win
                player['lose'] = lose
                break
        else:
            settings.append(
                {
                    "name": temp_player,
                    "color": color,
                    "win": win,
                    'lose': lose
                }
            )
    with open("temp_saves_encr.json", 'w') as f:
        print(settings, file=f)
    encrypter.encryptFile("temp_saves_encr.json", "temp_saves.json")
    os.remove("temp_saves_encr.json")


def take_settings(user='all'):
    global temp_player
    global color
    global win
    global lose
    encrypter = RC5(32, 12, b'\0' * 16)
    encrypter.decryptFile("temp_saves.json", "temp_saves_encr.json")
    with open('temp_saves_encr.json') as f:
        temp_str = f.read()
        cut = temp_str.index(']')
        settings = eval(temp_str[:cut + 1])
        for player in settings:
            if player['name'] == user:
                temp_player = player['name']
                color = player['color']
                win = player['win']
                lose = player['lose']
                break
        else:
            temp_player = settings[0]['name']
            color = settings[0]['color']
            win = settings[0]['win']
            lose = settings[0]['lose']

    os.remove("temp_saves_encr.json")
    return

def finish_game_window(screen, winner):
    finish_menu = pygame_menu.Menu('Конец игры', 400, 300,
                    theme=pygame_menu.themes.THEME_GREEN)
    finish_menu.add.label(f"Победил игрок {winner.Name}")
    global win
    global lose
    finish_menu.add.label(f"Побед AI {lose}")
    finish_menu.add.label(f"Побед игрока {win}")
    finish_menu.add.button('Играть заного', lambda screen=screen: start_game(screen))
    finish_menu.add.button("Выход в меню", lambda screen=screen: start_window(screen))
    finish_menu.add.button('Выход на рабочий стол',pygame_menu.events.EXIT)
    finish_menu.mainloop(screen)


def start_game(screen):
    take_settings(temp_player)
    global BLACK_CHESSMAN
    BLACK_CHESSMAN = Chessman('Player', 1, color)
    font1 = pygame.font.SysFont('SimHei', 32)
    font2 = pygame.font.SysFont('SimHei', 72)
    fwidth, fheight = font2.size ('Победа черных')
    checkerboard = Checkerboard(Line_Points)
    cur_runner = BLACK_CHESSMAN
    winner = None
    computer = AI(Line_Points, WHITE_CHESSMAN)
    black_win_count = 0
    white_win_count = 0


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                save_settings()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if winner is not None:
                        winner = None
                        cur_runner = BLACK_CHESSMAN
                        checkerboard = Checkerboard(Line_Points)
                        computer = AI(Line_Points, WHITE_CHESSMAN)
            elif event.type == MOUSEBUTTONDOWN:
                if winner is None:
                    pressed_array = pygame.mouse.get_pressed()
                    if pressed_array[0]:
                        mouse_pos = pygame.mouse.get_pos()
                        click_point = _get_clickpoint(mouse_pos)
                        if click_point is not None:
                            if checkerboard.can_drop(click_point):
                                winner = checkerboard.drop(cur_runner, click_point)
                                if winner is None:
                                    cur_runner = _get_next(cur_runner)
                                    computer.get_opponent_drop(click_point)
                                    AI_point = computer.AI_drop()
                                    winner = checkerboard.drop(cur_runner, AI_point)
                                    if winner is not None:
                                        white_win_count += 1
                                    cur_runner = _get_next(cur_runner)
                                else:
                                    black_win_count += 1
                        else:
                            print ('Превышение площади доски')
        _draw_checkerboard(screen)
        for i, row in enumerate(checkerboard.checkerboard):
            for j, cell in enumerate(row):
                if cell == BLACK_CHESSMAN.Value:
                    _draw_chessman(screen, Point(j, i), BLACK_CHESSMAN.Color)
                elif cell == WHITE_CHESSMAN.Value:
                    _draw_chessman(screen, Point(j, i), WHITE_CHESSMAN.Color)
        _draw_left_info(screen, font1, cur_runner, black_win_count, white_win_count)
        if winner:
            global lose
            global win
            if winner.Name == 'AI':
                lose += 1
            else:
                win += 1
            save_settings()
            finish_game_window(screen, winner)
        pygame.display.flip()


def start_window(screen):
    menu = pygame_menu.Menu('Гобан', 400, 300,
                       theme=pygame_menu.themes.THEME_GREEN)

    menu.add.text_input('Ваше имя:', default=temp_player, onchange=set_name)
    menu.add.button('Играть', lambda screen=screen: start_game(screen))
    menu.add.button("Настройки", lambda screen=screen: settings_open(screen))
    menu.add.button('Выход', pygame_menu.events.EXIT)
    menu.mainloop(screen)



def main():
    take_settings()
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption ('Gobang')
    start_window(screen)




def _get_next(cur_runner):
    if cur_runner == BLACK_CHESSMAN:
        return WHITE_CHESSMAN
    else:
        return BLACK_CHESSMAN



def _draw_checkerboard(screen):
    screen.fill(Checkerboard_Color)
    pygame.draw.rect(screen, BLACK_COLOR, (Outer_Width, Outer_Width, Border_Length, Border_Length), Border_Width)
    for i in range(Line_Points):
        pygame.draw.line(screen, BLACK_COLOR,
                         (Start_Y, Start_Y + SIZE * i),
                         (Start_Y + SIZE * (Line_Points - 1), Start_Y + SIZE * i),
                         1)
    for j in range(Line_Points):
        pygame.draw.line(screen, BLACK_COLOR,
                         (Start_X + SIZE * j, Start_X),
                         (Start_X + SIZE * j, Start_X + SIZE * (Line_Points - 1)),
                         1)
    for i in (3, 9, 15):
        for j in (3, 9, 15):
            if i == j == 9:
                radius = 5
            else:
                radius = 3
            pygame.gfxdraw.aacircle(screen, Start_X + SIZE * i, Start_Y + SIZE * j, radius, BLACK_COLOR)
            pygame.gfxdraw.filled_circle(screen, Start_X + SIZE * i, Start_Y + SIZE * j, radius, BLACK_COLOR)



# Нарисуйте шахматные фигуры
def _draw_chessman(screen, point, stone_color):
    # pygame.draw.circle(screen, stone_color, (Start_X + SIZE * point.X, Start_Y + SIZE * point.Y), Stone_Radius)
    pygame.gfxdraw.aacircle(screen, Start_X + SIZE * point.X, Start_Y + SIZE * point.Y, Stone_Radius, stone_color)
    pygame.gfxdraw.filled_circle(screen, Start_X + SIZE * point.X, Start_Y + SIZE * point.Y, Stone_Radius, stone_color)



# Нарисуйте информационный дисплей слева
def _draw_left_info(screen, font, cur_runner, black_win_count, white_win_count):
    _draw_chessman_pos(screen, (SCREEN_HEIGHT + Stone_Radius2, Start_X + Stone_Radius2), BLACK_CHESSMAN.Color)
    _draw_chessman_pos(screen, (SCREEN_HEIGHT + Stone_Radius2, Start_X + Stone_Radius2 * 4), WHITE_CHESSMAN.Color)
    _draw_chessman_pos(screen, (SCREEN_HEIGHT + Stone_Radius2, SCREEN_HEIGHT - int(Stone_Radius2 * 4.5)), BLACK_CHESSMAN.Color)
    _draw_chessman_pos(screen, (SCREEN_HEIGHT + Stone_Radius2, SCREEN_HEIGHT - Stone_Radius2 * 2), WHITE_CHESSMAN.Color)




def _draw_chessman_pos(screen, pos, stone_color):
    pygame.gfxdraw.aacircle(screen, pos[0], pos[1], Stone_Radius2, stone_color)
    pygame.gfxdraw.filled_circle(screen, pos[0], pos[1], Stone_Radius2, stone_color)



# В соответствии с положением щелчка мыши, вернуться к координатам игровой области
def _get_clickpoint(click_pos):
    pos_x = click_pos[0] - Start_X
    pos_y = click_pos[1] - Start_Y
    if pos_x < -Inside_Width or pos_y < -Inside_Width:
        return None
    x = pos_x // SIZE
    y = pos_y // SIZE
    if pos_x % SIZE > Stone_Radius:
        x += 1
    if pos_y % SIZE > Stone_Radius:
        y += 1
    if x >= Line_Points or y >= Line_Points:
        return None


    return Point(x, y)



class AI:
    def __init__(self, line_points, chessman):
        self._line_points = line_points
        self._my = chessman
        self._opponent = BLACK_CHESSMAN if chessman == WHITE_CHESSMAN else WHITE_CHESSMAN
        self._checkerboard = [[0] * line_points for _ in range(line_points)]


    def get_opponent_drop(self, point):
        self._checkerboard[point.Y][point.X] = self._opponent.Value


    def AI_drop(self):
        point = None
        score = 0
        for i in range(self._line_points):
            for j in range(self._line_points):
                if self._checkerboard[j][i] == 0:
                    _score = self._get_point_score(Point(i, j))
                    if _score > score:
                        score = _score
                        point = Point(i, j)
                    elif _score == score and _score > 0:
                        r = random.randint(0, 100)
                        if r % 2 == 0:
                            point = Point(i, j)
        self._checkerboard[point.Y][point.X] = self._my.Value
        return point


    def _get_point_score(self, point):
        score = 0
        for os in offset:
            score += self._get_direction_score(point, os[0], os[1])
        return score


    def _get_direction_score(self, point, x_offset, y_offset):
        count = 0 # Количество наших фишек выставленных последовательно
        _count = 0 # Количество фишек противника выставленных последовательно
        space = None # Есть ли пробел в нашей последовательности
        _space = None # Есть ли пробел в последовательности противника
        both = 0 # Есть ли какие-либо препятствия на обоих концах нашего продолжения
        _both = 0 # Есть ли какие-либо препятствия на обоих концах продолжения противника


        flag = self._get_stone_color(point, x_offset, y_offset, True)
        if flag != 0:
            for step in range(1, 6):
                x = point.X + step * x_offset
                y = point.Y + step * y_offset
                if 0 <= x < self._line_points and 0 <= y < self._line_points:
                    if flag == 1:
                        if self._checkerboard[y][x] == self._my.Value:
                            count += 1
                            if space is False:
                                space = True
                        elif self._checkerboard[y][x] == self._opponent.Value:
                            _both += 1
                            break
                        else:
                            if space is None:
                                space = False
                            else:
                                break
                    elif flag == 2:
                        if self._checkerboard[y][x] == self._my.Value:
                            _both += 1
                            break
                        elif self._checkerboard[y][x] == self._opponent.Value:
                            _count += 1
                            if _space is False:
                                _space = True
                        else:
                            if _space is None:
                                _space = False
                            else:
                                break
                else:
                    if flag == 1:
                        both += 1
                    elif flag == 2:
                        _both += 1


        if space is False:
            space = None
        if _space is False:
            _space = None


        _flag = self._get_stone_color(point, -x_offset, -y_offset, True)
        if _flag != 0:
            for step in range(1, 6):
                x = point.X - step * x_offset
                y = point.Y - step * y_offset
                if 0 <= x < self._line_points and 0 <= y < self._line_points:
                    if _flag == 1:
                        if self._checkerboard[y][x] == self._my.Value:
                            count += 1
                            if space is False:
                                space = True
                        elif self._checkerboard[y][x] == self._opponent.Value:
                            _both += 1
                            break
                        else:
                            if space is None:
                                space = False
                            else:
                                break # Выход при встрече со вторым пробелом
                    elif _flag == 2:
                        if self._checkerboard[y][x] == self._my.Value:
                            _both += 1
                            break
                        elif self._checkerboard[y][x] == self._opponent.Value:
                            _count += 1
                            if _space is False:
                                _space = True
                        else:
                            if _space is None:
                                _space = False
                            else:
                                break
                else:
                                        # Встреча с краем блокирует
                    if _flag == 1:
                        both += 1
                    elif _flag == 2:
                        _both += 1


        score = 0
        if count == 4:
            score = 10000
        elif _count == 4:
            score = 9000
        elif count == 3:
            if both == 0:
                score = 1000
            elif both == 1:
                score = 100
            else:
                score = 0
        elif _count == 3:
            if _both == 0:
                score = 900
            elif _both == 1:
                score = 90
            else:
                score = 0
        elif count == 2:
            if both == 0:
                score = 100
            elif both == 1:
                score = 10
            else:
                score = 0
        elif _count == 2:
            if _both == 0:
                score = 90
            elif _both == 1:
                score = 9
            else:
                score = 0
        elif count == 1:
            score = 10
        elif _count == 1:
            score = 9
        else:
            score = 0


        if space or _space:
            score /= 2
        return score


    # Возвращает цвет камушка
    def _get_stone_color(self, point, x_offset, y_offset, next):
        x = point.X + x_offset
        y = point.Y + y_offset
        if 0 <= x < self._line_points and 0 <= y < self._line_points:
            if self._checkerboard[y][x] == self._my.Value:
                return 1
            elif self._checkerboard[y][x] == self._opponent.Value:
                return 2
            else:
                if next:
                    return self._get_stone_color(Point(x, y), x_offset, y_offset, False)
                else:
                    return 0
        else:
            return 0



if __name__ == '__main__':
    main()
