from PyQt5.QtWidgets import (
    QWidget,QLineEdit,QPushButton,QScrollArea,QHBoxLayout,
    QVBoxLayout
    )
from PyQt5.QtCore import  pyqtSignal

from custom_object import *
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

        self.err_label= QLabel()
        self.err_label.setStyleSheet('color:red')
        self.err_label.setAlignment(Qt.AlignHCenter)

        save_btn = QPushButton('Enregistrer')
        save_btn.clicked.connect(self.save)

        main_layout.addWidget(self.start_editor)
        main_layout.addWidget(self.end_editor)
        main_layout.addWidget(self.prmtr_editor)
        main_layout.addWidget(self.err_label)
        main_layout.addWidget(save_btn)

    def setUserTravel(self,travel:Travel):
        self.start_editor.setAdress(travel.start)
        self.end_editor.setAdress(travel.end)
        self.prmtr_editor.setDate(travel.date)
        self.prmtr_editor.setDistance(travel.distance)
        self.prmtr_editor.setPrice(travel.price)
        self.prmtr_editor.setReturnState(travel.rtrn_state)

    def getUserTravel(self) -> Travel | bool:
        """Try if user data are correct"""
        if self.start_editor.tryUserData() and self.end_editor.tryUserData():
            start = self.start_editor.getAdress()
            end = self.end_editor.getAdress() 
            if self.prmtr_editor.tryUserData():
                date = self.prmtr_editor.getDate()
                distance = self.prmtr_editor.getDistance()
                price = self.prmtr_editor.getPrice()
                return_state = self.prmtr_editor.getReturnState()
                travel = Travel([date,start,end,distance,price,return_state])
                self.err_label.setText('')
                return(travel)
            else: 
                self.err_label.setText('Prmtr format error')
                return(False)
        else:
            self.err_label.setText('adresse format error')
            return(False)

    def save(self):
        if self.getUserTravel() != False:
            travel = self.getUserTravel()
            self.data.saveTravel(self.root.historic,travel.list) # A modifier
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
        self.travel_editor_win = TravelEditorWin()
        self.travel_editor_win.show()
        self.travel_editor_win.close_signal.connect(self.onEditorClose)

    def onEditorClose(self) -> None:
        self.travel_editor_win.close()
        self.travel_list_widget.updateLayout()