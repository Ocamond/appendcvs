import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QPushButton, QFileDialog, \
    QWidget, QLabel, QComboBox
from PyQt5.QtCore import Qt, QRect
from PyQt5 import QtGui
import pandas as pd


class ListBoxWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.resize(321, 261)
        self.move(40, 50)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            links = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    links.append(str(url.toLocalFile()))
                else:
                    links.append(str(url.toString()))
            self.addItems(links)
        else:
            event.ignore()


class AppDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(613, 387)

        # list
        self.listbox_view = ListBoxWidget(self)

        # button
        self.Concatbutton = QPushButton('Concatenation', self)
        self.Concatbutton.setGeometry(440, 80, 111, 41)
        self.Concatbutton.clicked.connect(lambda: self.concatandsave())

        self.Savebutton = QPushButton("Save as...", self)
        self.Savebutton.setGeometry(440, 270, 111, 41)
        self.Savebutton.clicked.connect(lambda: self.savefile())

        # combobox
        self.columnselect = QComboBox(self)
        self.columnselect.setGeometry(QRect(440, 170, 111, 41))
        self.columnselect.setObjectName("comboBox")
        self.columnselect.addItem("column1")
        self.columnselect.addItem("column2")

        # label
        self.Draglabel = QLabel(self)
        self.Draglabel.setObjectName("Draglabel")
        self.Draglabel.setText("Drag & Drop field")
        self.Draglabel.setGeometry(QRect(100, 20, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.Draglabel.setFont(font)
        self.Draglabel.setAlignment(Qt.AlignCenter)

        self.Concatlabel = QLabel(self)
        self.Concatlabel.setText("Concat files")
        self.Concatlabel.setObjectName("Concatlabel")
        self.Concatlabel.setGeometry(QRect(400, 50, 191, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.Concatlabel.setFont(font)
        self.Concatlabel.setAlignment(Qt.AlignCenter)

        self.columnlabel = QLabel(self)
        self.columnlabel.setText("Groupby column")
        self.columnlabel.setObjectName("Concatlabel")
        self.columnlabel.setGeometry(QRect(400, 140, 191, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.columnlabel.setFont(font)
        self.columnlabel.setAlignment(Qt.AlignCenter)

        self.Savelabel = QLabel(self)
        self.Savelabel.setText("Save as...")
        self.Savelabel.setObjectName("Concatlabel")
        self.Savelabel.setGeometry(QRect(400, 240, 191, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.Savelabel.setFont(font)
        self.Savelabel.setAlignment(Qt.AlignCenter)

    def concatandsave(self):
        items = []
        for index in range(self.listbox_view.count()):
            items.append(self.listbox_view.item(index))
        combined_csv = pd.concat([pd.read_csv(item.text(), sep=";", dtype="unicode") for item in items])
        return combined_csv

    def savefile(self):
        csv = self.concatandsave()
        widget = QWidget()
        option = QFileDialog.Options()
        file = QFileDialog.getSaveFileName(widget, "Save File as...", "standard.csv", "All Files (*)", options=option)
        csv.to_csv(file[0], index=False, encoding='utf-8-sig')

    def groupby(self):
        csv = self.concatandsave()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = AppDemo()
    demo.show()

    sys.exit(app.exec_())
