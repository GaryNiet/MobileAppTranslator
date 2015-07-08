__author__ = 'gnt'
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import Qt
from PyQt4 import QtGui

appStyle="""

QTableView::item:selected
{
    color: white;
    background: #0063cd;
}
"""


class translationTable(QTableWidget):
    # signals
    clearTable = pyqtSignal()
    keyPressed = pyqtSignal(QEvent)


    def __init__(self, *args):
        QTableWidget.__init__(self, 0, 3)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setStyleSheet(appStyle)
        self.labels = ["Base Language", "Developer Comment", "translation"]
        self.setHorizontalHeaderLabels(self.labels)
        self.setWordWrap(True)
        self.domainResults = []
        self.strings = []
        self.strings.append([])
        self.strings.append([])
        self.filters = []

        self.clearTable.connect(self.clearContents)
        self.cellPressed.connect(self.selectFullRow)
        self.cellChanged.connect(self.selectFullRow)
        self.cellClicked.connect(self.selectFullRow)


    def selectFullRow(self, row, column):
        self.selectRow(row)

    def selectNextRow(self):
        self.selectFullRow(self.currentRow()+1, 0)


    def resizeEvent(self, event):
        self.setColumnWidth(0, event.size().width()/3)
        self.setColumnWidth(1, event.size().width()/3)
        self.setColumnWidth(2, event.size().width()/3)


    def addTuple(self, base, comment, translation, statusCode):
        rowResults = (base, comment, translation, statusCode)
        self.domainResults.append(rowResults)

    def setTuple(self, base, comment, translation, statusCode, row):
        self.domainResults[row] = (base, comment, translation, statusCode)
        self.setItem(row , 0, Qt.QTableWidgetItem(base))
        self.setItem(row , 1, Qt.QTableWidgetItem(comment))
        self.setItem(row , 2, Qt.QTableWidgetItem(translation))

    def setTranslation(self, translation):
        self.setItem(self.currentRow(), 2, Qt.QTableWidgetItem(translation))

    def setTranslationWithIndex(self, translation, index):
        self.setItem(index, 2, Qt.QTableWidgetItem(translation))


    def wipeTranslations(self):
        for i in range(0, self.rowCount()):
            self.setTranslationWithIndex("",i)


    def addRowToTable(self, base, comment, translation, statusCode, y):
        self.insertRow(y)
        self.setItem(y , 0, Qt.QTableWidgetItem(base))

        self.setItem(y , 1, Qt.QTableWidgetItem(comment))

        self.setItem(y , 2, Qt.QTableWidgetItem(translation))

        self.resizeRowsToContents()


    def reloadTable(self):
        self.clearTable.emit()
        self.setRowCount(0)
        if len(self.filters):
            filteredResults = self.classicFilter(self.filters)
        else:
            filteredResults = self.domainResults
        i = 0
        for result in filteredResults:
            self.addRowToTable(result[0], result[1], result[2], result[3], i)
            i+=1

    # filter functions

    # this filter removes unwanted arguments
    def classicFilter(self, *arg):
        filteredResults = []
        filter = arg[0]
        for result in self.domainResults:
            for i in range(0, len(filter), 2):
                print("filter: " + str(filter[i]))
                if filter[i] == 3:
                    if filter[i] >= 3:
                        filteredResults.append(result)
                else:
                    print(result[filter[i+1]])
                    if result[filter[i + 1]] == filter[i]:
                        filteredResults.append(result)
                        break
        return filteredResults

    def keyPressEvent(self, event):
        self.keyPressed.emit(event)
        super().keyPressEvent(event)

