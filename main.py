import sys

from PyQt6.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('NDFGen')
        self.UIComponents()

    def UIComponents(self):
        layout = QHBoxLayout()
        main_widget = QWidget(self)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        stackWidget = QStackedWidget(self)
        layout.addWidget(stackWidget)

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()

if __name__ == '__main__':
    main()
