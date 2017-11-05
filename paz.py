from template import Template

class Paz(Template):
    """спец класс для Пазов, наследуется от Template"""

    def __init__(self, name_template2, name_template3, path_to_template, path_to_progs,
                 prfx2, prfx3):
        super().__init__(name_template2, path_to_template, path_to_progs, 42, 42)
        self.maskNameProg = '[prfx][nul][Y][X].tap'
        self.prfx2 = prfx2
        self.prfx3 = prfx3
        self.name_template2 = name_template2
        self.name_template3 = name_template3

    # программа, выбора
    def createProgram(self, x, y):
        if y <= 62:
            body, x, y = self.create2p(x, y)
        else:
            body, x, y = self.create3p(x, y)

        return body, x, y

    # функция рассчёта и создания программы 2 пазов
    def create2p(self, x, y):
        self.subfolder = 'пазы 2п\\'
        self.name = self.name_template2
        self.prfx = self.prfx2

        kolevka = 8
        diametrFrezi = 9
        meja = round((y - kolevka * 2 - diametrFrezi * 2) / 3, 1)  # с округлением до 1 десятой

        k = {}

        k['[y2]'] = kolevka + meja + diametrFrezi / 2
        k['[y1]'] = y - k['[y2]']

        k['[x1]'] = y + 15
        k['[x1e]'] = x - k['[x1]']

        body = self.readTemplate(self.name)
        body = self.fillingTemplate(body, k)

        return body, x, y

    # функция рассчёта и создания программы 3 пазов
    def create3p(self, x, y):
        self.subfolder = 'пазы 3п\\'
        self.name = self.name_template3
        self.prfx = self.prfx3

        seredY = y / 2

        kolevka = 8
        diametrFrezi = 9
        meja = round((y - kolevka * 2 - diametrFrezi * 3) / 4, 1) - 1
        # с округлением до 1 десятой : пример # (75 - 16 - 9*3) / 4 - 1 = 7

        mejdu = diametrFrezi + meja

        k = {}

        k['[y1]'] = seredY - mejdu
        k['[y2]'] = seredY + mejdu

        k['[x1]'] = y + 25  # подобрано опытным путём (изначально было просто фиксировано 98)
        k['[x1e]'] = x - k['[x1]']
        k['[x2]'] = y + 37  # подобрано опытным путём (изначально было просто фиксировано 110)
        k['[x2e]'] = x - k['[x2]']
        k['[srY]'] = seredY

        body = self.readTemplate(self.name)
        body = self.fillingTemplate(body, k)

        return body, x, y
