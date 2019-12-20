# -*- coding: utf-8 -*-


from numpy import delete, array, where


class Dnf:
    _val_to_draw = []
    _h = False

    def __init__(self, matrix, x, y):
        self._x = x
        self._y = y
        self._matrix = matrix
        self.solve()

    @staticmethod
    def search_p_n(matrix, x, y):
        p, n = [], []
        for i in range(1, y + 1):
            if matrix[i][x - 1] == 1:
                p.append(matrix[i][x])
            else:
                n.append(matrix[i][x])
        return p, n

    @staticmethod
    def choose_r(matrix):
        m, index = 0, int
        for i in range(len(matrix[0]) - 2):
            n, d = 0, 0
            for j in range(len(matrix) - 1):
                if matrix[j + 1][i] == matrix[j + 1][len(matrix[0]) - 2] == 1:
                    n += 1
                elif matrix[j + 1][i] == 1 and matrix[j + 1][len(matrix[0]) - 2] == 0:
                    d += 1
            if d == 0:
                d = 0.001
            if n / d > m:
                m = n / d
                index = int(str(matrix[0][i])[1])
        return index

    @staticmethod
    def remove_from_d(d, n, tmp):
        n_args, rem_row = [], []
        d = array(d)
        for i in n:
            n_args.append(int(str(i)[1]))
        for i in n_args:
            test = where(d == "x" + str(i))[0][0]
            if d[test][tmp - 1] == 0:
                n.remove("x" + str(i))
                rem_row.append(test)
        d = delete(d, rem_row, 0)
        test = where(d == "f" + str(tmp))
        d = delete(d, test[1][0], 1)
        return d, n

    def cover_p(self, r):
        d = array(self._matrix)
        r_args, rem_row, p = [], [], []
        for i in r.args:
            r_args.append(int(str(i)[1]))
        self._val_to_draw.append(r_args)
        for i in range(1, self._y + 1):
            if all(d[i][r_ar - 1] == 1 for r_ar in r_args):
                p.append("x" + str(i))
                tmp = where(d == "x" + str(i))
                rem_row.append(tmp[0][0])
        d = delete(d, rem_row, 0)
        return p, d

    def make_result(self):
        test = []
        values = self._val_to_draw
        matrix = self._matrix
        for i in values:
            for j in range(1, self._y + 1):
                for k in i:
                    test.append([j, k - 1])
                if all(matrix[j][r_ar - 1] == 1 for r_ar in i):
                    test.append([j, self._x - 1])
                else:
                    for x in range(len(i)):
                        test.pop()
        self._val_to_draw = test

    def get_result(self):
        return [self._h, self._val_to_draw]

    def solve(self):
        data, x, y = self._matrix, self._x, self._y
        positive = self.search_p_n(data, x, y)[0]
        h = False
        while positive:
            negative = self.search_p_n(data, len(data[0]) - 1, len(data) - 1)[1]
            r = True

            while negative:
                try:
                    test = len(r.atoms())
                except AttributeError:
                    test = 1
                if test == self._x - 1:
                    return
                else:
                    tmp = self.choose_r(data)
                    r = r & self._matrix[0][tmp - 1]
                    data, negative = self.remove_from_d(data, negative, tmp)
            h = h | r
            cover, data = self.cover_p(r)
            if cover:
                positive = [el for el in positive if el not in cover]
            else:
                return
        self._h = h
        return self.make_result()
