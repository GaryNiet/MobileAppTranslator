__author__ = 'gnt'
import sys
from PyQt4 import Qt, QtCore
from PyQt4.QtCore import pyqtSignal, pyqtSlot
from translationTable import translationTable
from parse import parser
from textEdit import TextEdit
import iso639

class scriptGUI(Qt.QApplication):

    def __init__(self, args):
        Qt.QApplication.__init__(self, args)

        #languages
        self.iso = iso639
        self.languages = []
        for language in self.iso.data:
            if self.iso.to_iso639_1(language['name']):
                self.languages.append(language['name'])


        #init
        self.parser = parser()

        #ask for xliff

        #add layout
        self.widget = Qt.QWidget()
        self.gridLayout = Qt.QGridLayout()
        self.widget.setLayout(self.gridLayout)

        #init widgets
        self.table = translationTable()
        self.sourceLanguageBox = Qt.QComboBox()
        self.targetLanguageBox = Qt.QComboBox()
        self.toLabel = Qt.QLabel("to")
        self.translateText = TextEdit()
        self.enterButton = Qt.QPushButton("enter")
        self.exportToiOS = Qt.QPushButton("export to iOS")
        self.exportToAndroid = Qt.QPushButton("export to Android")

        #modify widgets
        self.sourceLanguageBox.addItems(self.languages)
        self.targetLanguageBox.addItems(self.languages)

        #place widgets
        self.gridLayout.addWidget(self.table, 1,0,5,5)
        self.gridLayout.addWidget(self.sourceLanguageBox, 0,0, 1,2)
        self.gridLayout.addWidget(self.targetLanguageBox,0,3,1,2)
        self.gridLayout.addWidget(self.toLabel,0,2,1,1)
        self.gridLayout.addWidget(self.translateText, 6,0,4,2)
        self.gridLayout.addWidget(self.enterButton,6,4,1,1)
        self.gridLayout.addWidget(self.exportToiOS,7,4,1,1)
        self.gridLayout.addWidget(self.exportToAndroid,8,4,1,1)

        #show widgets
        self.widget.show()


        self.loadStrings()
        self.setLanguageBoxes()

        #Signals
        self.targetLanguageBox.currentIndexChanged.connect(self.table.wipeTranslations)
        self.translateText.enterPressed.connect(self.nextTranslation)
        self.exportToiOS.clicked.connect(self.createXLIFF)
        self.exportToAndroid.clicked.connect(self.createXML)
        self.targetLanguageBox.currentIndexChanged.connect(self.changeLanguage)
        self.table.keyPressed.connect(self.giveFocusToTextEdit)



        self.exec_()

    def giveFocusToTextEdit(self, event):
        self.translateText.setFocus()
        self.translateText.append(event.text())


    def changeLanguage(self):
        self.parser.changeLanguage(self.iso.to_iso639_1(self.targetLanguageBox.currentText()))

    def createXLIFF(self):
        self.parser.saveIOS(self.iso.to_iso639_1(self.targetLanguageBox.currentText()))

    def createXML(self):
        self.parser.saveAndroid(self.iso.to_iso639_1(self.targetLanguageBox.currentText()))

    def nextTranslation(self):
        self.table.setTranslation(self.translateText.toPlainText())
        arrayRow = self.table.currentRow()
        self.parser.translate(self.translateText.toPlainText(), arrayRow)
        self.table.selectNextRow()
        self.translateText.clear()


    def loadStrings(self):
        self.strings = self.parser.returnLocalizableStrings()
        for string in self.strings:
            self.table.addRowToTable(string[0], string[2], string[1], 1, 0)

    def setLanguageBoxes(self):
        languageIndex = self.languages.index(self.iso.to_name(self.parser.getSourceLanguage()))
        self.sourceLanguageBox.setCurrentIndex(languageIndex)
        languageIndex = self.languages.index(self.iso.to_name(self.parser.getTargetLanguage()))
        self.targetLanguageBox.setCurrentIndex(languageIndex)




if __name__ == "__main__":
    app = scriptGUI(sys.argv)