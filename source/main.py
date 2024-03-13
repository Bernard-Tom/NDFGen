import sys
import os
from PyQt5.QtWidgets import (
    QWidget,QMainWindow,QApplication, QHBoxLayout,QStackedWidget
    )

from custom_widget import *

class MainWindow(QMainWindow):
    """Main window of the application"""
    def __init__(self) -> None:
        super().__init__()
        self.__title = 'NDF Gen'
        self.__width = 800
        self.__height = 800
        self.ui_components()

    def ui_components(self)-> None:
        """Set graphical components"""
        self.setWindowTitle(self.__title)
        self.setFixedWidth(self.__width)
        self.setFixedHeight(self.__height)

        layout = QHBoxLayout()
        main_widget = QWidget(self)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        stackWidget = QStackedWidget()
        historic_win = HistoricWin()
        stackWidget.addWidget(historic_win)
        layout.addWidget(stackWidget)

def main() -> None:
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()

def setup() -> bool:
    cwd = os.getcwd()
    print()

if __name__ == '__main__':
    setup()
