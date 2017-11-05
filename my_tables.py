from PyQt5.QtWidgets import QTableWidgetItem

class My_tables():
    """My_tables для удобной работы с виджетом QTableWidget"""

    def __init__(self, list_tables):
        # super(My_tables, self).__init__()
        self.list_tables = list_tables

    # отдать список со значениями, взятый из таблицы
    def getTable(self, table_name):
        tc = self.list_tables.get(table_name)
        lines = tc[1]
        table = []
        for i in range(0, lines):
            if tc[0].item(i, 0).text() != '':
                table.append([int(tc[0].item(i, 0).text()), int(tc[0].item(i, 1).text())])
            else:
                break
        return table

    def cleanAll(self):
        """Очищает все таблицы (подготавливает) при помощи cleanTable"""
        for value in self.list_tables:
            self.cleanTable(value)

    def cleanTable(self, table_name):
        tc = self.list_tables.get(table_name)
        for i in range(0, tc[1]):
            for j in range(0, tc[2]):
                tc[0].setItem(i, j, QTableWidgetItem(""))

    # тестовая функция для проверки где и чего
    def printing(self, table_name):
        tc = self.list_tables.get(table_name)
        for i in range(0, tc[1]):
            for j in range(0, tc[2]):
                item = tc[0].item(i, j)
                if item is None:
                    valu = 'None'
                else:
                    valu = item.text()

                print('(' + str(i) + ',' + str(j) + ') = ' + valu)

    # очистка линии (используется, если записна какая-либо хрень в ячейках или
    # не хватает одного из значений)
    def cleanLine(self, table_name, num):
        table = self.list_tables.get(table_name)[0]
        table.setItem(num, 0, QTableWidgetItem(""))
        table.setItem(num, 1, QTableWidgetItem(""))

    # обмен линий
    def changeLines(self, table_name, one, two):
        tc = self.list_tables.get(table_name)
        table = tc[0]
        cell_one = [table.item(one, 0).text(), table.item(one, 1).text()]
        cell_two = [table.item(two, 0).text(), table.item(two, 1).text()]
        cell_one, cell_two = cell_two, cell_one
        table.setItem(one, 0, QTableWidgetItem(cell_one[0]))
        table.setItem(one, 1, QTableWidgetItem(cell_one[1]))
        table.setItem(two, 0, QTableWidgetItem(cell_two[0]))
        table.setItem(two, 1, QTableWidgetItem(cell_two[1]))

    # правильная сортировка по убыванию, так же в момент сортировки, убирает
    # всякие касяки (защита от дурака)
    def sorting(self, table_name):
        tc = self.list_tables.get(table_name)
        table = tc[0]
        for i in range(0, tc[1]):
            for j in range(0, tc[1] - 1):

                item00 = table.item(j, 0)
                item10 = table.item(j + 1, 0)
                item01 = table.item(j, 1)
                item11 = table.item(j + 1, 1)

                if item00.text().isdigit() and item01.text().isdigit():
                    num00 = int(table.item(j, 0).text())
                else:
                    self.cleanLine(table_name, j)
                    self.changeLines(table_name, j, j + 1)
                    continue

                if item10.text().isdigit() and item11.text().isdigit():
                    num10 = int(table.item(j + 1, 0).text())
                else:
                    self.cleanLine(table_name, j + 1)
                    continue

                if num10 > num00:
                    self.changeLines(table_name, j, j + 1)
                elif num10 == num00:

                    if item01.text().isdigit():
                        num01 = int(table.item(j, 1).text())
                    else:
                        self.cleanLine(table_name, j)
                        self.changeLines(table_name, j, j + 1)
                        continue

                    if item11.text().isdigit():
                        num11 = int(table.item(j + 1, 1).text())
                    else:
                        self.cleanLine(table_name, j + 1)
                        continue

                    if num11 > num01:
                        self.changeLines(table_name, j, j + 1)
