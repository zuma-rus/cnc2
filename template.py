import os
import re


class Template(object):

    def __init__(self, name_template, path_to_template,
                 path_to_progs, ot_x, ot_y):
        self.name = name_template
        self.path_to_template = self.correctPath(path_to_template)
        self.path_to_progs = self.correctPath(path_to_progs)
        self.mask_name_prog = '[X][prfx][nul][Y][pstfx].[ext]'
        self.file_extension_prog = 'tap'

        self.ot_x = int(ot_x)
        self.ot_y = int(ot_y)

        self.prfx = 'f'
        self.pstfx = ''
        self.subfolder = ''
        self.pref_name_folder = 'в'

    # постфикс и имя внутренней папки
    def postfix(self):
        x = self.ot_x
        y = self.ot_y
        pstfx = {48: 'v', 47: 's', 46: 's', 45: 'p', 44: 'c', 43: 't', 42: '', 41: 'e'}
        if x == y:
            self.pstfx = 'm' if x < 41 else pstfx[x]
            self.subfolder = self.pref_name_folder + '(' + str(x) + ')\\'
        else:
            self.pstfx = 'r'
            self.subfolder = self.pref_name_folder + '(' + str(x) + '-' + str(y) + ')\\'

    # чтобы при чтении-записи всё было в порядке
    def correctPath(self, name):
        return name.replace('/', '\\')

    # заполнение шаблона значениями
    def fillingTemplate(self, body, kdict):
        for key in kdict:
            body = body.replace(key, str(kdict[key]))
        return body

    # название файла готовой программы
    def createNameProg(self, x, y):
        prfx = self.prfx
        pstfx = self.pstfx

        # условная корректировка для нуля (в связи с добавленим шаблонов под синтек)
        if (y > 600):
            nul = '0' if x < 100 else ''
        else:
            nul = '0' if y < 100 else ''

        name_prog = self.mask_name_prog
        name_prog = name_prog.replace('[X]', str(x))
        name_prog = name_prog.replace('[Y]', str(y))
        name_prog = name_prog.replace('[prfx]', str(prfx))
        name_prog = name_prog.replace('[pstfx]', str(pstfx))
        name_prog = name_prog.replace('[nul]', str(nul))
        name_prog = name_prog.replace('[ext]', self.file_extension_prog)
        return name_prog

    def readTemplate(self, name):
        myfile = open(self.path_to_template + name)
        body = ''
        lines = myfile.readlines()
        for line in lines:
            body = body + line
        myfile.close()
        return body

    # чтобы в шаблоне не было запятых
    def onlyPoint(self, txt):
        return txt.replace(',', '.')

    # удаление скобок (и всё что в них) из текста
    def removeBrackets(self, txt):
        n = 1  # запустить хотя бы один раз
        while n:
            txt, n = re.subn(r'\([^()]*\)', '', txt)  # удаление скобок, включая вложенные
        return txt

    # удаление двойных пробелов
    def removeDoubleSpace(self, txt):
        n = 1  # запустить хотя бы один раз
        while n:
            txt, n = re.subn(r'  ', ' ', txt)
        return txt

    # удаление пустых строк (пока не работает)
    def remove_empty_string(self, txt):
        return txt.replace('\n\n','\n').replace('\n\n','\n')

    # создание всех программ по переданному списку
    def createProgs(self, list_table, clean_messages):
        for xy in list_table:
            x = xy[0]
            y = xy[1]
            body, x, y = self.createProgram(x, y)
            body = self.onlyPoint(body)
            if (clean_messages):
                body = self.removeBrackets(body)
            body = self.removeDoubleSpace(body)
            body = self.remove_empty_string(body) # пока не работает, нужно копать
            name_prog = self.createNameProg(x, y)
            self.saveProgram(name_prog, body)

    # основная программа, где вычисляются значения
    def createProgram(self, x, y):
        pass

    def saveProgram(self, name_prog, body):
        self.findFolder()
        full_path = self.path_to_progs + self.subfolder + name_prog
        f = open(full_path, 'w')
        f.write(body)
        f.close()

    # проверяет, есть ли папка для записи и если её нет, то создаёт
    def findFolder(self):
        full_path = self.path_to_progs + self.subfolder
        result = os.path.isdir(full_path)
        if (result):
            return
        else:
            os.makedirs(full_path)
