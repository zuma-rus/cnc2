from template import Template

class Shield(Template):
    """спец класс для филёнок Виктории, наследуется от Template"""

    def __init__(self, name_template, path_to_template, path_to_progs, ot_x, ot_y, prfx):
        super().__init__(name_template, path_to_template, path_to_progs, ot_x, ot_y)
        self.subfolder = 'щиты\\'
        self.maskNameProg = '[prfx][X][nul][Y].tap'
        self.prfx = prfx

    # основная программа, где вычисляются значения
    def createProgram(self, x, y):

        if self.ot_x > 42:
            self.prfx = "sb"

        # Расшфровка условия otstup_y
        # 0.5   это чтобы округлялось в большую сторону
        # -16   это два отступа от края фигурной фрезы, каждый из которых занимает 8мм
        # -44   это толщина двух борозд от фрезы 22мм
        # /3    это чтобы три полосы были одинаковой ширины
        # +8    это добавляем (возвращаем) один отступ от края занятый фигурной фрезой
        # +11   это добавляем (возвращаем) половинный размер от толщины фрезы
        self.ot_y = (int(0.5 + (y - 16 - 44) / 3) + 8 + 11) if y < 140 else self.ot_y

        k = {}

        k['[x1]'] = self.ot_x
        k['[x2]'] = x - self.ot_x
        k['[y1]'] = self.ot_y
        k['[y2]'] = y - self.ot_y
        k['[y3]'] = y + 150  # кажется раньше было, оставлено для совместимости

        body = self.readTemplate(self.name)
        body = self.fillingTemplate(body, k)

        return body, x, y
