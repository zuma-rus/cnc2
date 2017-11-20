from template import Template


class Vik(Template):
    """спец класс для филёнок Виктории, наследуется от Template"""

    def __init__(self, name_template, path_to_template, path_to_progs, ot_x, ot_y):
        super().__init__(name_template, path_to_template, path_to_progs, ot_x, ot_y)
        self.pref_name_folder = 'вик'
        self.postfix()

    # основная программа, где вычисляются значения
    def createProgram(self, x, y):
        if y > 600:
            body, x, y = self.create_vik_syn(x, y)
        else:
            body, x, y = self.create_vik(x, y)

        return body, x, y

    # программа вычисления филёнок виктории для RZNC
    def create_vik(self, x, y):
        k = {}

        k['[x1]'] = self.ot_x
        k['[x2]'] = x - self.ot_x
        k['[y1]'] = self.ot_y
        k['[y2]'] = y - self.ot_y

        body = self.readTemplate(self.name)
        body = self.fillingTemplate(body, k)

        return body, x, y

    # Программа вычисления филёнок виктории для синтека
    def create_vik_syn(self, x, y):

        self.file_extension_prog = 'nc'
        self.mask_name_prog = '[prfx][nul][X]x[Y].[ext]'
        self.name = "vik_syn.shb"
        self.prfx = "vik_syn_" + str(self.ot_x) + "-" + str(self.ot_y) + "_"

        k = {}

        k['[x1]'] = "{0:.3f}".format(self.ot_x)
        k['[x2]'] = "{0:.3f}".format(x - self.ot_x)
        k['[y1]'] = "{0:.3f}".format(self.ot_y)
        k['[y2]'] = "{0:.3f}".format(y - self.ot_y)

        body = self.readTemplate(self.name)
        body = self.fillingTemplate(body, k)

        return body, x, y
