import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDesktopWidget, QMessageBox
# from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class Mess(QWidget):

    def __init__(self):
        super().__init__()
        # self.title = 'PyQt5 messagebox - pythonspot.com'
        # self.resize(320, 200)
        # self.center()
       # self.MesProgComplete()

    def MesProgComplete(self, title, message):
        # self.resize(520, 300)
        self.center()

        # buttonReply = QMessageBox.about(self, title, message, QMessageBox.Ok) # со знаком вопроса
        # buttonReply = QMessageBox.about(self, title, message)  # без иконки
        buttonReply = QMessageBox.information(self, title, message, QMessageBox.Ok) # со знаком вопроса
        if buttonReply == QMessageBox.Ok:
            print('Ok')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):

        self.resize(320, 200)
        self.center()

        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)

        buttonReply = QMessageBox.question(self, 'PyQt5 message', "Do you like PyQt5?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            print('Yes clicked.')
        else:
            print('No clicked.')

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Mess()
    sys.exit(app.exec_())
