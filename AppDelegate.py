import sys
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QMessageBox, QApplication, QWidget, QTabWidget, QGridLayout
from SettingsWidget import SettingsWidget
from PlotWidget import PlotWidget


class App(QMainWindow):

    def __init__(self):
        super().__init__()

        self.title = 'Электропунтурная диагностика'
        self.left = 0
        self.top = 0
        self.width = 700
        self.height = 600
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Подтвердите действие',
                                     "Вы уверены, что хотите закрыть программу?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QGridLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = SettingsWidget(parent)
        # self.tab2 = PlotWidget(parent)

        # Add tabs
        self.tabs.addTab(self.tab1, "")
        # self.tabs.addTab(self.tab2, "")


        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())