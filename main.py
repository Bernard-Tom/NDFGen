import sys
from PyQt5.QtWidgets import (
    QWidget,QMainWindow,QApplication, QHBoxLayout,QStackedWidget
    )

from historic_window import *

class MainWindow(QMainWindow):
    """Main window of the application"""
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('NDFGen')
        self.UIComponents()

    def UIComponents(self)-> None:
        """Set graphical components"""
        layout = QHBoxLayout()
        main_widget = QWidget(self)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        stackWidget = QStackedWidget()
        self.historic_win = HistoricWin()
        stackWidget.addWidget(self.historic_win)
        layout.addWidget(stackWidget)

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()

if __name__ == '__main__':
    main()
