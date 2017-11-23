# Импорт необходимых библиотек (классов)
import sys
import configparser
import os
# Импортируем наш интерфейс и подключаем интерфейсные файлы
from cnc_ui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
# интерфейсные файлы
from my_tables import My_tables
from messages import Mess
# файлы-модули для работы с шаблонами
from vik import Vik
from afin import Afin
from shield import Shield
from paz import Paz
from pazpr import PazPr
# другие подключения
from version import get_version_app as vers


# Основной класс для работы с интерфейсом
class MyWin(QtWidgets.QMainWindow):
    """Основной класс для работы с интерфейсом сделанным в PyQT5 Designer"""

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.tb = My_tables({
            'vik': [self.ui.tableWidget_vik, 12, 2],
            'afin': [self.ui.tableWidget_afin, 12, 2],
            'shit': [self.ui.tableWidget_shit, 12, 2],
            'paz': [self.ui.tableWidget_paz, 12, 2],
            'pazpr': [self.ui.tableWidget_pazpr, 12, 2]
        })

        # инициализация настроек программы и последней сессии
        initSettings(self.ui)

        self.tf = self.ui.lineEdit_setting_templatefolder.text()
        self.mf = self.ui.lineEdit_setting_mainfolder.text()

        # Кнопка запуска создания программ Виктории
        self.ui.btn_create_vik.clicked.connect(self.createVictories)

        # Кнопка запуска создания программ Афин
        self.ui.btn_create_afin.clicked.connect(self.createAfines)

        # Кнопка запуска создания программ Щитов
        self.ui.btn_create_shit.clicked.connect(self.createShields)

        # Кнопка запуска создания программ Пазов для колонн
        self.ui.btn_create_paz.clicked.connect(self.createPaz)

        # Кнопка запуска создания программ Прямых Пазов для колонн
        self.ui.btn_create_pazpr.clicked.connect(self.createPazPr)

        # Кнопка сохранения настроек
        self.ui.btn_save_setting.clicked.connect(self.savSet)

        # Кнопка Прямые Пазы отступы
        self.ui.btn_ots_papr_2030.clicked.connect(self.BtnOtsPazpr)

        # Кнопка Щитов Отступы
        self.ui.btn_ots_shit_42.clicked.connect(self.BtnOtsShit)

        # Кнопки Виктория Отступы
        self.ui.btn_ots_vik_40.clicked.connect(lambda: self.BtnOtsVik(40))
        self.ui.btn_ots_vik_41.clicked.connect(lambda: self.BtnOtsVik(41))
        self.ui.btn_ots_vik_42.clicked.connect(lambda: self.BtnOtsVik(42))
        self.ui.btn_ots_vik_43.clicked.connect(lambda: self.BtnOtsVik(43))
        self.ui.btn_ots_vik_44.clicked.connect(lambda: self.BtnOtsVik(44))
        self.ui.btn_ots_vik_45.clicked.connect(lambda: self.BtnOtsVik(45))
        self.ui.btn_ots_vik_46.clicked.connect(lambda: self.BtnOtsVik(46))

        # Кнопки Афина Отступы
        self.ui.btn_ots_afin_40.clicked.connect(lambda: self.BtnOtsAfin(40))
        self.ui.btn_ots_afin_41.clicked.connect(lambda: self.BtnOtsAfin(41))
        self.ui.btn_ots_afin_42.clicked.connect(lambda: self.BtnOtsAfin(42))
        self.ui.btn_ots_afin_43.clicked.connect(lambda: self.BtnOtsAfin(43))
        self.ui.btn_ots_afin_44.clicked.connect(lambda: self.BtnOtsAfin(44))
        self.ui.btn_ots_afin_45.clicked.connect(lambda: self.BtnOtsAfin(45))
        self.ui.btn_ots_afin_46.clicked.connect(lambda: self.BtnOtsAfin(46))

        # Переключатели Афины шаблона (с арками или прямой)
        self.ui.rBtn_afin_arc.clicked.connect(lambda: self.chekerAfin(1))
        self.ui.rBtn_afin_pr.clicked.connect(lambda: self.chekerAfin(0))

        # выбор главной папки
        self.ui.toolButton_select_mainfolder.clicked.connect(
            lambda: self.selectFileFolder('folder', self.ui.lineEdit_setting_mainfolder))
        # выбор папки с шаблонами
        self.ui.toolButton_select_templatefolder.clicked.connect(lambda: self.selectFileFolder(
            'folder', self.ui.lineEdit_setting_templatefolder))

        # выбор шаблона щитов
        self.ui.toolButton_select_shield_template.clicked.connect(lambda: self.selectFileFolder(
            'file', self.ui.lineEdit_shield_template))

        # выбор шаблона на 2 паза
        self.ui.toolButton_select_paz2_template.clicked.connect(lambda: self.selectFileFolder(
            'file', self.ui.lineEdit_paz2_template))
        # выбор шаблона на 3 паза
        self.ui.toolButton_select_paz3_template.clicked.connect(lambda: self.selectFileFolder(
            'file', self.ui.lineEdit_paz3_template))

        # выбор шаблона на 2 паза (прямые)
        self.ui.toolButton_select_pazpr2_template.clicked.connect(lambda: self.selectFileFolder(
            'file', self.ui.lineEdit_pazpr2_template))
        # выбор шаблона на 3 паза (прямые)
        self.ui.toolButton_select_pazpr3_template.clicked.connect(lambda: self.selectFileFolder(
            'file', self.ui.lineEdit_pazpr3_template))
        # выбор шаблона на 5 пазов (прямые)
        self.ui.toolButton_select_pazpr5_template.clicked.connect(lambda: self.selectFileFolder(
            'file', self.ui.lineEdit_pazpr5_template))

        # очистка всех таблиц
        self.tb.cleanAll()

        # для тестов
        # if self.ui.checkBox_setting_cleancomments.isChecked():
        #     test_message = "Включено"
        # else:
        #     test_message = "ВЫКЛючено"
        # print(test_message)

    # запуск создания программ Виктории
    def createVictories(self):
        self.tb.sorting('vik')
        name = 'vik.shb'
        ot_x = self.ui.spinBox_ots_vik_X.value()
        ot_y = self.ui.spinBox_ots_vik_Y.value()
        list = self.tb.getTable('vik')
        vik = Vik(name, self.tf, self.mf, ot_x, ot_y)
        vik.createProgs(list, self.ui.checkBox_setting_cleancomments.isChecked())
        self.statusBar().showMessage('Программы филёнок Виктории созданы!')
        mes = Mess()
        mes.MesProgComplete('Программы готовы', 'Программы филёнок Виктории созданы!')

    # запуск создания программ Афин
    def createAfines(self):
        self.tb.sorting('afin')
        name = 'afina.shb'
        ot_x = self.ui.spinBox_ots_afin_X.value()
        ot_y = self.ui.spinBox_ots_afin_Y.value()
        list = self.tb.getTable('afin')
        pr = self.ui.rBtn_afin_pr.isChecked()
        afin = Afin(name, self.tf, self.mf, ot_x, ot_y, pr)
        afin.createProgs(list, self.ui.checkBox_setting_cleancomments.isChecked())
        self.statusBar().showMessage('Программы филёнок Афин созданы!')
        mes = Mess()
        mes.MesProgComplete('Программы готовы', 'Программы филёнок Афин созданы!')

    # запуск создания программ Щитов
    def createShields(self):
        self.tb.sorting('shit')
        name = self.ui.lineEdit_shield_template.text()
        prfx = self.ui.lineEdit_shield_prefix.text()
        ot_x = self.ui.spinBox_ots_shit_X.value()
        ot_y = self.ui.spinBox_ots_shit_Y.value()
        list = self.tb.getTable('shit')
        shit = Shield(name, self.tf, self.mf, ot_x, ot_y, prfx)
        shit.createProgs(list, self.ui.checkBox_setting_cleancomments.isChecked())
        self.statusBar().showMessage('Программы Щитов созданы!')
        mes = Mess()
        mes.MesProgComplete('Программы готовы', 'Программы Щитов созданы!')

    # запуск создания программ Пазов для колонн
    def createPaz(self):
        self.tb.sorting('paz')
        name2 = self.ui.lineEdit_paz2_template.text()
        prfx2 = self.ui.lineEdit_paz2_prefix.text()
        name3 = self.ui.lineEdit_paz3_template.text()
        prfx3 = self.ui.lineEdit_paz3_prefix.text()
        list = self.tb.getTable('paz')
        paz = Paz(name2, name3, self.tf, self.mf, prfx2, prfx3)
        paz.createProgs(list, self.ui.checkBox_setting_cleancomments.isChecked())
        self.statusBar().showMessage('Программы Пазов созданы!')
        mes = Mess()
        mes.MesProgComplete('Программы готовы', 'Программы Пазов созданы!')

    # запуск создания программ Прямых Пазов для колонн
    def createPazPr(self):
        self.tb.sorting('pazpr')
        ot_left = self.ui.spinBox_ots_pazpr_X_left.value()
        ot_right = self.ui.spinBox_ots_pazpr_X_right.value()
        name2 = self.ui.lineEdit_pazpr2_template.text()
        prfx2 = self.ui.lineEdit_pazpr2_prefix.text()
        name3 = self.ui.lineEdit_pazpr3_template.text()
        prfx3 = self.ui.lineEdit_pazpr3_prefix.text()
        name5 = self.ui.lineEdit_pazpr5_template.text()
        prfx5 = self.ui.lineEdit_pazpr5_prefix.text()
        list = self.tb.getTable('pazpr')

        # узнать сколько пазов делать
        if self.ui.rBtn_pazpr_2paz.isChecked():
            pazpr = PazPr(name2, self.tf, self.mf, prfx2, ot_left, ot_right, 2)
        elif self.ui.rBtn_pazpr_3paz.isChecked():
            pazpr = PazPr(name3, self.tf, self.mf, prfx3, ot_left, ot_right, 3)
        else:
            pazpr = PazPr(name5, self.tf, self.mf, prfx5, ot_left, ot_right, 5)

        pazpr.createProgs(list, self.ui.checkBox_setting_cleancomments.isChecked())
        self.statusBar().showMessage('Программы Прямых Пазов созданы!')
        mes = Mess()
        mes.MesProgComplete('Программы готовы', 'Программы Прямых Пазов созданы!')

    # диалоговое окно, для выбора файла или папки
    def selectFileFolder(self, param, lineEdit):

        if param == 'file':
            startFolder = self.ui.lineEdit_setting_templatefolder.text()
            fname = QFileDialog.getOpenFileName(
                self, 'Выберите файл', startFolder, '*.shb')[0]
            fname = os.path.basename(fname)
        else:
            fname = QFileDialog.getExistingDirectory(self, 'Выберите папку')
            if (len(fname) > 0):
                fname += '/'

        if (len(fname) > 0):
            lineEdit.setText(fname)

    # функция запуска внешней функции сохранения настроек
    def savSet(self):
        saveSettings(self.ui)
        self.statusBar().showMessage('Настройки сохранены!')

    # Функция переключения режима для Афин
    def chekerAfin(self, value):
        if value == 1:
            self.ui.label_pix_afin.setPixmap(QtGui.QPixmap("pix/afin_arc.png"))
        else:
            self.ui.label_pix_afin.setPixmap(QtGui.QPixmap("pix/afin_pr.png"))

    # Функция кнопки установки отступов Щитов
    def BtnOtsPazpr(self):
        self.ui.spinBox_ots_pazpr_X_left.setValue(30)
        self.ui.spinBox_ots_pazpr_X_right.setValue(20)

    # Функция кнопки установки отступов Щитов
    def BtnOtsShit(self):
        self.ui.spinBox_ots_shit_X.setValue(42)
        self.ui.spinBox_ots_shit_Y.setValue(42)

    # Функция установки отступов Виктории для быстрых кнопок
    def BtnOtsVik(self, value):
        self.ui.spinBox_ots_vik_X.setValue(value)
        self.ui.spinBox_ots_vik_Y.setValue(value)

    # Функция установки отступов Афин для быстрых кнопок
    def BtnOtsAfin(self, value):
        self.ui.spinBox_ots_afin_X.setValue(value)
        self.ui.spinBox_ots_afin_Y.setValue(value)

    # Операции происходящие после нажатия на кнопку закрытия (выхода)
    def closeEvent(self, event):
        saveSession(self.ui)
        saveSettings(self.ui)
        print("Выход")
        # sys.exit(app.exec_())


# загрузка и инициализация настроек программы
def initSettings(ui):
    loadSettings(ui)
    loadSession(ui)


# загрузка и установка настроек программы из файла settings.ini
def loadSettings(ui):
    # версия (устанавливается в конце этого файла)
    ui.label_version.setText(str(versionApp))

    # main
    # очищать комментраии в готовых программах
    if str(conf.get("main", "clean_comments")) == 'True':
        ui.checkBox_setting_cleancomments.setChecked(True)
    else:
        ui.checkBox_setting_cleancomments.setChecked(False)
    # папка с шаблонами
    ui.lineEdit_setting_templatefolder.setText(
        str(conf.get("main", "templates_folder")))
    # корневая папка для готовых программ
    ui.lineEdit_setting_mainfolder.setText(
        str(conf.get("main", "main_prog_folder")))

    # shields
    # шаблон для щитов
    ui.lineEdit_shield_template.setText(
        str(conf.get("shields", "shield_template")))
    # префикс для щитов
    ui.lineEdit_shield_prefix.setText(
        str(conf.get("shields", "shield_prefix")))

    # paz
    # шаблон 2 пазов
    ui.lineEdit_paz2_template.setText(str(conf.get("paz", "paz2_template")))
    # префикс 2 пазов
    ui.lineEdit_paz2_prefix.setText(str(conf.get("paz", "paz2_prefix")))
    # шаблон 3 пазов
    ui.lineEdit_paz3_template.setText(str(conf.get("paz", "paz3_template")))
    # префикс 3 пазов
    ui.lineEdit_paz3_prefix.setText(str(conf.get("paz", "paz3_prefix")))

    # pazpr
    # шаблон 2 пазов прямых
    ui.lineEdit_pazpr2_template.setText(
        str(conf.get("pazpr", "pazpr2_template")))
    # префикс 2 пазов прямых
    ui.lineEdit_pazpr2_prefix.setText(str(conf.get("pazpr", "pazpr2_prefix")))
    # шаблон 3 пазов прямых
    ui.lineEdit_pazpr3_template.setText(
        str(conf.get("pazpr", "pazpr3_template")))
    # префикс 3 пазов прямых
    ui.lineEdit_pazpr3_prefix.setText(str(conf.get("pazpr", "pazpr3_prefix")))
    # шаблон 5 пазов прямых
    ui.lineEdit_pazpr5_template.setText(
        str(conf.get("pazpr", "pazpr5_template")))
    # префикс 5 пазов прямых
    ui.lineEdit_pazpr5_prefix.setText(str(conf.get("pazpr", "pazpr5_prefix")))


# сохранение настроек программы в файл settings.ini
def saveSettings(ui):
    # main
    # очищать комментраии в готовых программах
    conf.set("main", "clean_comments", str(
        ui.checkBox_setting_cleancomments.isChecked()))
    # корневая папка для готовых программ
    conf.set("main", "main_prog_folder", ui.lineEdit_setting_mainfolder.text())
    # папка с шаблонами
    conf.set("main", "templates_folder",
             ui.lineEdit_setting_templatefolder.text())

    # shields
    # шаблон для щитов
    conf.set("shields", "shield_template", ui.lineEdit_shield_template.text())
    # префикс для щитов
    conf.set("shields", "shield_prefix", ui.lineEdit_shield_prefix.text())

    # paz
    # шаблон 2 пазов
    conf.set("paz", "paz2_template", ui.lineEdit_paz2_template.text())
    # префикс 2 пазов
    conf.set("paz", "paz2_prefix", ui.lineEdit_paz2_prefix.text())
    # шаблон 3 пазов
    conf.set("paz", "paz3_template", ui.lineEdit_paz3_template.text())
    # префикс 3 пазов
    conf.set("paz", "paz3_prefix", ui.lineEdit_paz3_prefix.text())

    # pazpr
    # шаблон 2 пазов прямых
    conf.set("pazpr", "pazpr2_template", ui.lineEdit_pazpr2_template.text())
    # префикс 2 пазов прямых
    conf.set("pazpr", "pazpr2_prefix", ui.lineEdit_pazpr2_prefix.text())
    # шаблон 3 пазов прямых
    conf.set("pazpr", "pazpr3_template", ui.lineEdit_pazpr3_template.text())
    # префикс 3 пазов прямых
    conf.set("pazpr", "pazpr3_prefix", ui.lineEdit_pazpr3_prefix.text())
    # шаблон 5 пазов прямых
    conf.set("pazpr", "pazpr5_template", ui.lineEdit_pazpr5_template.text())
    # префикс 5 пазов прямых
    conf.set("pazpr", "pazpr5_prefix", ui.lineEdit_pazpr5_prefix.text())

    # обязательная секция для сохранения настроек
    with open("settings.ini", "w") as config:
        conf.write(config)


# загрузка и инициализация сессии из файла work.ini
def loadSession(ui):
    # вкладка
    ui.tabWidget.setCurrentIndex(int(work.get("main", "tab")))

    # viktory
    ui.spinBox_ots_vik_X.setValue(int(work.get("viktory", "otstup_x")))
    ui.spinBox_ots_vik_Y.setValue(int(work.get("viktory", "otstup_y")))

    # afina
    ui.spinBox_ots_afin_X.setValue(int(work.get("afina", "otstup_x")))
    ui.spinBox_ots_afin_Y.setValue(int(work.get("afina", "otstup_y")))
    if str(work.get("afina", "style")) == 'arc':
        ui.rBtn_afin_arc.setChecked(True)
        ui.label_pix_afin.setPixmap(QtGui.QPixmap("pix/afin_arc.png"))
    else:
        ui.rBtn_afin_pr.setChecked(True)
        ui.label_pix_afin.setPixmap(QtGui.QPixmap("pix/afin_pr.png"))

    # shields
    ui.spinBox_ots_shit_X.setValue(int(work.get("shields", "otstup_x")))
    ui.spinBox_ots_shit_Y.setValue(int(work.get("shields", "otstup_y")))

    # paz # pass

    # pazpr
    ui.spinBox_ots_pazpr_X_left.setValue(
        int(work.get("pazpr", "otstup_x_left")))
    ui.spinBox_ots_pazpr_X_right.setValue(
        int(work.get("pazpr", "otstup_x_right")))
    if int(work.get("pazpr", "kolich")) == 2:
        ui.rBtn_pazpr_2paz.setChecked(True)
    elif int(work.get("pazpr", "kolich")) == 3:
        ui.rBtn_pazpr_3paz.setChecked(True)
    else:
        ui.rBtn_pazpr_5paz.setChecked(True)

    # prop
    ui.spinBox_prop_zag_X.setValue(int(work.get("prop", "otstup_x_zag")))
    ui.spinBox_prop_zag_Y.setValue(int(work.get("prop", "otstup_y_zag")))


# сохранение сессии программы в файл work.ini
def saveSession(ui):
    work.set("main", "tab", ui.tabWidget.currentIndex())  # вкладка
    # viktory
    work.set("viktory", "otstup_x", ui.spinBox_ots_vik_X.value())
    work.set("viktory", "otstup_y", ui.spinBox_ots_vik_Y.value())
    # afina
    work.set("afina", "otstup_x", ui.spinBox_ots_afin_X.value())
    work.set("afina", "otstup_y", ui.spinBox_ots_afin_Y.value())
    if (ui.rBtn_afin_arc.isChecked()):
        work.set("afina", "style", "arc")
    else:
        work.set("afina", "style", "pr")
    # shields
    work.set("shields", "otstup_x", ui.spinBox_ots_shit_X.value())
    work.set("shields", "otstup_y", ui.spinBox_ots_shit_Y.value())
    # paz     pass
    # pazpr
    work.set("pazpr", "otstup_x_left", ui.spinBox_ots_pazpr_X_left.value())
    work.set("pazpr", "otstup_x_right", ui.spinBox_ots_pazpr_X_right.value())
    if (ui.rBtn_pazpr_2paz.isChecked()):
        work.set("pazpr", "kolich", 2)
    elif (ui.rBtn_pazpr_3paz.isChecked()):
        work.set("pazpr", "kolich", 3)
    else:
        work.set("pazpr", "kolich", 5)
    # prop
    work.set("prop", "otstup_x_zag", ui.spinBox_prop_zag_X.value())
    work.set("prop", "otstup_y_zag", ui.spinBox_prop_zag_Y.value())

    # обязательная секция для сохранения настроек
    with open("work.ini", "w") as config:
        work.write(config)


# секция для main файла
if __name__ == "__main__":
    versionApp = vers()
    conf = configparser.RawConfigParser()
    conf.read("settings.ini")
    work = configparser.RawConfigParser()
    work.read("work.ini")
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
