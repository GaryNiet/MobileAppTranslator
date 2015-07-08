__author__ = 'gnt'
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import Qt,QtCore

class TextEdit(QTextEdit):
    enterPressed = pyqtSignal()

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Return:
            self.enterPressed.emit()

