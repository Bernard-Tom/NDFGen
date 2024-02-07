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
        self.start_editor = AdressEditorWidget('start')
        self.end_editor = AdressEditorWidget('end')
        self.prmtr_editor = PrmtrEditorWidget()

        btn_layout = QVBoxLayout()
        save_btn = QPushButton('Enregistrer')
        save_btn.clicked.connect(self.save)

        main_layout.addWidget(self.start_editor)
        main_layout.addWidget(self.end_editor)
        main_layout.addWidget(self.prmtr_editor)
        main_layout.addWidget(save_btn)

    def getUserTravel(self) -> Travel:
        start = self.start_editor.getAdress()
        end = self.end_editor.getAdress()
        date = self.prmtr_editor.getDate()
        distance = self.prmtr_editor.getDistance()
        return_state = self.prmtr_editor.getreturnState()
        return(Travel([date,start,end,distance,return_state]))

    def save(self):
        travel = self.getUserTravel()
        print(travel)

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