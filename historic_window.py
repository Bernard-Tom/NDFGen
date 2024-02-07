from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QWidget
from custom_widget import *

class TravelEditorWin(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.UIComponents()

    def UIComponents(self)-> None:
        """Set graphical components"""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        start_editor = AdressEditorWidget('start')
        end_editor = AdressEditorWidget('end')

        main_layout.addWidget(start_editor)
        main_layout.addWidget(end_editor)

class HistoricWin(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.root = Roots()
        self.UIComponents()

    def UIComponents(self) -> None:
        """Set graphical components"""
        self.main_layout = QVBoxLayout() 
        self.setLayout(self.main_layout)

        self.search_bar = SearchBarWidget(self.root.historic)
        self.search_bar.search_signal.connect(self.onSearchSignal)
        self.my_scroll = QScrollArea()
        self.list_widget = TravelListWidget(self.root.historic)
        self.my_scroll.setWidget(self.list_widget)

        self.btn_layout = QHBoxLayout()
        add_btn = QPushButton('Ajouter')
        add_btn.clicked.connect(self.addTravel)
        gen_btn = QPushButton('Générer')
        self.btn_layout.addWidget(add_btn)
        self.btn_layout.addWidget(gen_btn)

        self.main_layout.addWidget(self.search_bar)
        self.main_layout.addWidget(self.my_scroll)
        self.main_layout.addLayout(self.btn_layout)

    def onSearchSignal(self) -> None:
        self.list_widget.update(self.search_bar.result_list)

    def addTravel(self) -> None:
        self.editor_win = TravelEditorWin()
        self.editor_win.show()