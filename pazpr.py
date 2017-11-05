from template import Template

class PazPr(Template):
    """спец класс для Пазов, наследуется от Template"""

    def __init__(self, name, path_to_template, path_to_progs,
                 prfx, ot_left, ot_right, pazov):
        super().__init__(name, path_to_template, path_to_progs, 42, 42)
        self.maskNameProg = '[prfx][nul][Y][X].tap'
        self.prfx = prfx
        self.pazov = pazov
        self.ot_left = ot_left
        self.ot_right = ot_right

    # программа, выбора
    def createProgram(self, x, y):
        if self.pazov == 5:
            body, x, y = self.create5p(x, y)
        elif self.pazov == 3:
            body, x, y = self.create3p(x, y)
        else:
            body, x, y = self.create2p(x, y)

        return body, x, y

    # функция рассчёта и создания программы 2 пазов
    def create2p(self, x, y):
        self.subfolder = 'пазы прямые 2п\\'
        k = {}

        kolevka = 8
        diametrFrezi = 9
        meja = round((y - kolevka * 2 - diametrFrezi * 2) / 3, 1)  # с округлением до 1 десятой

        k['[y2]'] = kolevka + meja + diametrFrezi / 2
        k['[y1]'] = y - k['[y2]']

        k['[x1]'] = self.ot_left
        k['[x1e]'] = x - self.ot_right

        body = self.readTemplate(self.name)
        body = self.fillingTemplate(body, k)

        return body, x, y

    # функция рассчёта и создания программы 3 пазов
    def create3p(self, x, y):
        self.subfolder = 'пазы прямые 3п\\'
        k = {}

        seredY = y / 2

        kolevka = 8
        diametrFrezi = 9
        meja = round((y - kolevka * 2 - diametrFrezi * 3) / 4, 1) - 1
        # с округлением до 1 десятой : пример ' (75 - 16 - 9*3) / 4 - 1 = 7

        mejdu = diametrFrezi + meja

        k['[y1]'] = seredY - mejdu
        k['[y2]'] = seredY + mejdu

        k['[x1]'] = self.ot_left
        k['[x1e]'] = x - self.ot_right
        k['[srY]'] = seredY

        body = self.readTemplate(self.name)
        body = self.fillingTemplate(body, k)

        return body, x, y

    # функция рассчёта и создания программы 5 пазов
    def create5p(self, x, y):
        self.subfolder = 'пазы прямые 5п\\'
        k = {}

        seredY = y / 2

        kolevka = 8
        diametrFrezi = 9
        kolvoPolos = 5  # задел на будущее, а вдруг нужно будет больше полос

        meja = round((y - kolevka * 2 - diametrFrezi * kolvoPolos) / (kolvoPolos + 1), 1) - 1
        # с округлением до 1 десятой : пример ' (75 - 16 - 9*3) / 4 - 1 = 7

        mejdu = diametrFrezi + meja

        k['[y1]'] = seredY - mejdu * 2
        k['[y2]'] = seredY - mejdu
        k['[y3]'] = seredY + mejdu
        k['[y4]'] = seredY + mejdu * 2

        k['[x1]'] = self.ot_left
        k['[x1e]'] = x - self.ot_right
        k['[srY]'] = seredY

        body = self.readTemplate(self.name)
        body = self.fillingTemplate(body, k)

        return body, x, y
