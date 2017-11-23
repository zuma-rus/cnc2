from template import Template


class Paz(Template):
    """спец класс для Пазов, наследуется от Template"""

    def __init__(self, name_template2, name_template3, path_to_template, path_to_progs,
                 prfx2, prfx3):
        super().__init__(name_template2, path_to_template, path_to_progs, 42, 42)
        self.mask_name_prog = '[prfx][nul][Y][X].[ext]'
        self.prfx2 = prfx2
        self.prfx3 = prfx3
        self.name_template2 = name_template2
        self.name_template3 = name_template3

    # программа, выбора
    def createProgram(self, x, y):
        if y > 500:
            if x <= 62:
                body, x, y = self.create_2p_syn(x, y)
            else:
                body, x, y = self.create_3p_syn(x, y)
        else:
            if y <= 62:
                body, x, y = self.create_2p(x, y)
            else:
                body, x, y = self.create_3p(x, y)

        return body, x, y

    # функция рассчёта и создания программы 2 пазов
    def create_2p_syn(self, x, y):
        self.subfolder = 'пазы 2п\\'
        self.file_extension_prog = 'nc'
        self.mask_name_prog = '[prfx][nul][X]x[Y].[ext]'
        self.name = "paz2p_syn.shb"
        self.prfx = "2p_syn_"

        kolevka = 8
        diametrFrezi = 9
        meja = round((x - kolevka * 2 - diametrFrezi * 2) / 3, 1)  # с округлением до 1 десятой

        k = {}

        x2 = kolevka + meja + diametrFrezi / 2
        x1 = x - x2

        y1 = x + 15
        y1e = y - y1

        k['[x1]'] = "{0:.3f}".format(x1)
        k['[x2]'] = "{0:.3f}".format(x2)
        k['[y1]'] = "{0:.3f}".format(y1)
        k['[y1e]'] = "{0:.3f}".format(y1e)

        k['[mess]'] = "2 paza pod rozetku " + str(x) + "x" + str(y)

        body = self.readTemplate(self.name)
        body = self.fillingTemplate(body, k)

        return body, x, y

    # функция рассчёта и создания программы 3 пазов для Синтека
    def create_3p_syn(self, x, y):
        self.subfolder = 'пазы 3п\\'
        self.file_extension_prog = 'nc'
        self.mask_name_prog = '[prfx][nul][X]x[Y].[ext]'
        self.name = "paz3p_syn.shb"
        self.prfx = "3p_syn_"

        seredX = x / 2

        kolevka = 8
        diametrFrezi = 9
        meja = round((x - kolevka * 2 - diametrFrezi * 3) / 4, 1) - 1
        # с округлением до 1 десятой : пример # (75 - 16 - 9*3) / 4 - 1 = 7

        mejdu = diametrFrezi + meja

        k = {}

        # считаем значения. Необходимо для правильного рассчёта, т.к. словарь нужен с нужной разрядностью
        x1 = seredX - mejdu
        x2 = seredX + mejdu
        y1 = x + 25  # подобрано опытным путём (изначально было просто фиксировано 98)
        y1e = y - y1
        y2 = x + 37  # подобрано опытным путём (изначально было просто фиксировано 110)
        y2e = y - y2

        # заполнение словаря с разрядностью 3 (это нужно для синтека)
        k['[x1]'] = "{0:.3f}".format(x1)
        k['[x2]'] = "{0:.3f}".format(x2)
        k['[y1]'] = "{0:.3f}".format(y1)
        k['[y1e]'] = "{0:.3f}".format(y1e)
        k['[y2]'] = "{0:.3f}".format(y2)
        k['[y2e]'] = "{0:.3f}".format(y2e)
        k['[srX]'] = "{0:.3f}".format(seredX)

        k['[mess]'] = "3 paza pod rozetku " + str(x) + "x" + str(y)

        body = self.readTemplate(self.name)
        body = self.fillingTemplate(body, k)

        return body, x, y

    # функция рассчёта и создания программы 2 пазов
    def create_2p(self, x, y):
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
    def create_3p(self, x, y):
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
