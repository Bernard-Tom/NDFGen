from PyQt6.QtWidgets import *
from custom_widget import *

class HistoricWin(QWidget):
    def __init__(self):
        super().__init__()
        self.root = Roots()
        self.UIComponents()

    def UIComponents(self):
        self.main_layout = QVBoxLayout() 
        self.setLayout(self.main_layout)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.search_bar = SearchBarWidget(self.root.historic_path)
        self.search_bar.search_signal.connect(self.onSearchSignal)
        self.my_scroll = QScrollArea()
        self.hist_list_widget = HistoricListWidget()
        self.my_scroll.setWidget(self.hist_list_widget)

        self.main_layout.addWidget(self.search_bar)
        self.main_layout.addWidget(self.my_scroll)

    def onSearchSignal(self):
        self.hist_list_widget.updateLayout(self.search_bar.result_list)