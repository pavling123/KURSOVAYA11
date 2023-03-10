from collections import namedtuple

Chessman = namedtuple('Chessman', 'Name Value Color')
Point = namedtuple('Point', 'X Y')

Red_color = (255, 0, 0)
Black_color = (45, 45, 45)
Blue_color = (0, 0, 255)
Green_color = (0, 214, 120)


WHITE_CHESSMAN = Chessman('AI', 2, (219, 219, 219))

offset = [(1, 0), (0, 1), (1, 1), (1, -1)]

class Checkerboard:
    def __init__(self, line_points):
        self._line_points = line_points
        self._checkerboard = [[0] * line_points for _ in range(line_points)]
    
    def _get_checkerboard(self):
        return self._checkerboard
    
    checkerboard = property(_get_checkerboard)

    def can_drop(self, point):
        return self._checkerboard[point.Y][point.X] == 0

    
    def drop(self, chessman, point):
        print(f'{chessman.Name} ({point.X}, {point.Y})')
        self._checkerboard[point.Y][point.X] = chessman.Value
        if self._win(point):
            print (f'{chessman.Name} выиграл')
            return chessman
    
    def _win(self, point):
        cur_value = self._checkerboard[point.Y][point.X]
        for os in offset:
            if self._get_count_on_direction(point, cur_value, os[0], os[1]):
                return True
    

    def _get_count_on_direction(self, point, value, x_offset, y_offset):
        count = 1
        for step in range(1, 5):
            x = point.X + step * x_offset
            y = point.Y + step * y_offset
            if 0 <= x < self._line_points and 0 <= y < self._line_points and self._checkerboard[y][x] == value:
                count += 1
            else:
                break
        for step in range(1, 5):
            x = point.X - step * x_offset
            y = point.Y - step * y_offset
            if 0 <= x < self._line_points and 0 <= y < self._line_points and self._checkerboard[y][x] == value:
                count += 1
            else:
                break
        return count >= 5