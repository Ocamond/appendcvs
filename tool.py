import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QLabel, QFileDialog, QWidget
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QUrl
import pandas as pd

class ListBoxWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.resize(450, 300)
        self.move(170,70)

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
                # https://doc.qt.io/qt-5/qurl.html
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
        self.resize(800, 600)

        self.listbox_view = ListBoxWidget(self)

        self.Concatbutton = QPushButton('Concat', self)
        self.Concatbutton.setGeometry(130,420,181,91)
        self.Concatbutton.clicked.connect(lambda: self.concatandsave())

        self.Savebutton = QPushButton("Save ", self)
        self.Savebutton.setGeometry(470,420,181,91)
        self.Savebutton.clicked.connect(lambda: self.saveas())


    def concatandsave(self):
        items = []
        combined_csv = {}
        for index in range(self.listbox_view.count()):
            items.append(self.listbox_view.item(index))
        combined_csv = pd.concat([pd.read_csv(item.text(), sep=";", dtype="unicode") for item in items])
        widget= QWidget()
        option=QFileDialog.Options()
        file=QFileDialog.getSaveFileName(widget,"Save File as...","standard.csv","All Files (*)",options=option)
        combined_csv.to_csv( file[0], index=False, encoding='utf-8-sig')



if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = AppDemo()
    demo.show()

    sys.exit(app.exec_())