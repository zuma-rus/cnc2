from template import Template

class Afin(Template):
    """спец класс для филёнок Виктории, наследуется от Template"""

    def __init__(self, name_template, path_to_template, path_to_progs, ot_x, ot_y, pr):
        super().__init__(name_template, path_to_template, path_to_progs, ot_x, ot_y)
        self.pref_name_folder = 'афин'
        self.pr = pr
        self.postfix()
        self.prfx = 'a'

    # основная программа, где вычисляются значения
    def createProgram(self, x, y):
        self.prfx = 'a'
        self.name = 'afina.shb'

        k = {}

        k['[x1]'] = self.ot_x
        k['[x2]'] = x - self.ot_x
        k['[y1]'] = self.ot_y
        k['[y2]'] = y - self.ot_y

        # в процессе проб подобрано, что полукруг у нас 35мм по х и 80мм по y
        k['[yk1]'] = (y - 80) / 2       # начало полукруга
        k['[yk2]'] = y - k['[yk1]']     # конец полукруга
        k['[yk3]'] = k['[yk1]'] + 40    # центр полукруга
        k['[xk1]'] = k['[x1]'] + 35     # середина по х первого полукруга
        k['[xk2]'] = k['[x2]'] - 35     # середина по х второго полукруга

        # -------------- принудительное переключение на прямой шаблон --------------
        if self.pr:
            self.name = "afina-pr.shb"  # для любых филёнок, но без овала (как для обычных)
            self.prfx = "p"
        else:
            # -------------- переключение на прямой шаблон по условию ---------------
            if y < 184 or x < 191:
                self.prfx = "p"
                self.name = "afina-pr.shb"  # для любых филёнок, но без овала (как для обычных)

            # -------------- переключение на половинный шаблон ----------------
            if y > 900:
                self.prfx = "h"
                self.name = "afina-polov.shb"

            # -------------- переключение на перевёрнутый шаблон ----------------
            if y > 550 and y <= 900:
                self.prfx = "y"
                self.name = "afina-per.shb"

                # разворот
                x, y = y, x
                k['[x1]'] = self.ot_y
                k['[x2]'] = x - self.ot_y  # надо понимать, что х уже развёрнут и стал бывшым y-ком
                k['[y1]'] = self.ot_x
                k['[y2]'] = y - self.ot_x

                k['[xk1]'] = (x - 80) / 2       # начало полукруга
                k['[xk2]'] = x - k['[xk1]']     # конец полукруга
                k['[xk3]'] = k['[xk1]'] + 40    # центр полукруга
                k['[yk1]'] = k['[y1]'] + 35     # середина по y нижнего полукруга
                k['[yk2]'] = k['[y2]'] - 35     # середина по y верхнего полукруга

            # -------------- переключение на нижний шаблон -------------------------
            if x > 900:
                self.prfx = "y"
                self.name = "afina-niz.shb"

                # разворот
                x = y
                y = 999  # чтобы сразу было видно развёрнутые программы в пульте

                k['[x1]'] = self.ot_y
                k['[x2]'] = x - self.ot_y  # надо понимать, что х уже развёрнут и стал бывшым y-ком
                k['[y1]'] = self.ot_x

                k['[xk1]'] = (x - 80) / 2       # начало полукруга внизу
                k['[xk2]'] = x - k['[xk1]']     # конец полукруга внизу
                k['[xk3]'] = k['[xk1]'] + 40    # центр полукруга внизу
                k['[yk1]'] = k['[y1]'] + 35     # середина по y нижнего полукруга

        body = self.readTemplate(self.name)
        body = self.fillingTemplate(body, k)

        return body, x, y
