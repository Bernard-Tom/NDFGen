from PyQt5.QtWidgets import (
    QWidget,QLineEdit,QPushButton,QScrollArea,QHBoxLayout,
    QVBoxLayout,QSpacerItem,QSizePolicy
    )
from PyQt5.QtCore import  Qt, pyqtSignal

from custom_widget import *

class TravelEditorWin(QWidget):
    close_signal = pyqtSignal()
    def __init__(self) -> None:
        super().__init__()
        self.data = Data()
        self.root = Roots()
        self.UIComponents()

    def UIComponents(self)-> None:
        """Set graphical components"""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.start_editor = AdressEditorWidget('start')
        self.end_editor = AdressEditorWidget('end')
        self.prmtr_editor = PrmtrEditorWidget()

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
        return(Travel([date,start,end,distance,return_state])) # A modifier

    def save(self):
        travel = self.getUserTravel()
        self.data.saveTravel(self.root.historic,travel.getList()) # A modifier
        self.close_signal.emit()

class HistoricWin(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.root = Roots()
        self.data = Data()
        self.UIComponents()
        #self.update()

    def UIComponents(self) -> None:
        """Set graphical components"""
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.search_bar = QLineEdit()
        self.search_bar.textChanged.connect(self.onSearchSignal)

        self.travel_list_widget = TravelListWidget(self.root.historic)

        self.my_scroll = QScrollArea()
        self.my_scroll.setWidgetResizable(True)
        self.my_scroll.setWidget(self.travel_list_widget)
        
        # Buttons
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
        """Delete all widgets of layout then add new widgets from travel_list"""
        self.travel_list_widget.updateDisplay(self.search_bar.text())

    def addTravel(self) -> None:
        self.editor_win = TravelEditorWin()
        self.editor_win.show()
        self.editor_win.close_signal.connect(self.onEditorClose)

    def onEditorClose(self) -> None:
        self.editor_win.close()
        self.travel_list_widget.updateLayout()