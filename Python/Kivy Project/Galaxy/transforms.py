def transform(self, x, y):
    #print(self.perspective_point_y, self.perspective_point_x)
    return self.transform_perspective(x, y)
    #return self.transform_2D(x,y)


def transform_2D(self, x, y):
    return int(x), int(y)


def transform_perspective(self, x, y):
    lin_y = self.perspective_point_y * y / self.height
    if lin_y > self.perspective_point_y:
        lin_y = self.perspective_point_y
    diff_x = x - self.perspective_point_x
    diff_y = self.perspective_point_y - lin_y

    factor_y = diff_y / self.perspective_point_y  # 1 when diff_y == self.perspective_point_y  / 0 if diff_y==0
    factor_y *= factor_y
    tr_x = self.perspective_point_x + diff_x * factor_y
    tr_y = self.perspective_point_y - (factor_y * self.perspective_point_y)
    return int(tr_x), int(tr_y)