from template import Template

class Vik(Template):
    """спец класс для филёнок Виктории, наследуется от Template"""

    def __init__(self, name_template, path_to_template, path_to_progs, ot_x, ot_y):
        super().__init__(name_template, path_to_template, path_to_progs, ot_x, ot_y)
        self.pref_name_folder = 'вик'
        self.postfix()

    # основная программа, где вычисляются значения
    def createProgram(self, x, y):
        k = {}

        k['[x1]'] = self.ot_x
        k['[x2]'] = x - self.ot_x
        k['[y1]'] = self.ot_y
        k['[y2]'] = y - self.ot_y

        body = self.readTemplate(self.name)
        body = self.fillingTemplate(body, k)

        return body, x, y
