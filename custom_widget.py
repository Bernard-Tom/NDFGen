from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal
from custom_object import Travel
from custom_object import *

class TravelWidget(QGroupBox):
    """Custom wigdget used to show Travel in list"""
    edit_signal = pyqtSignal()
    def __init__(self,travel:Travel) -> None:
        super().__init__()
        self.travel = travel
        self.setTitle(self.travel.date)
        self.setRtrnState()
        self.UIComponents()
        self.setStyleSheet("QGroupBox {border: 2px solid #000000;}")
        self.setFixedHeight(100)

    def setRtrnState(self) -> None:
        if self.travel.rtrn_state == 'true': self.return_txt='Aller Retour'
        else : self.return_txt = 'Aller Simple'  

    def UIComponents(self) -> None:
        """Set graphical components"""
        layout = QGridLayout(self)
        layout.setRowStretch(0,1)
        self.setLayout(layout)

        self.start_label = QLabel(self.travel.start)
        self.end_label = QLabel(self.travel.end)
        self.distance_label = QLabel(self.travel.distance)
        self.rtrn_label = QLabel(self.return_txt)

        edit_btn = QPushButton('...')
        edit_btn.setFixedWidth(30)
        edit_btn.clicked.connect(self.onEditClicked)

        layout.addWidget(self.start_label,0,0)
        layout.addWidget(self.end_label,0,1)
        layout.addWidget(self.distance_label,1,0)
        layout.addWidget(self.rtrn_label,1,1)
        layout.addWidget(edit_btn,0,2,3,1)

    def onEditClicked(self):
        self.edit_signal.emit()
        
class SearchBarWidget(QLineEdit):
    """
    Class used to implement QLineEdit search bar
    ------
    Can be used for Adress or Travel
    Emit a signal when it find his text in csv file
    """
    search_signal = pyqtSignal()
    def __init__(self,root:str) -> None:
        super().__init__()
        self.root = root
        self.data = Data()
        self.textChanged.connect(self.ontextChanged)

    def ontextChanged(self) -> None:
        """When text changed get list result from csv serach"""
        self.result_list = self.data.findDataList(self.root,self.text())
        self.search_signal.emit()

class HistoricListWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.data = Data()
        self.root = Roots()
        self.UIComponents()

    def UIComponents(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.updateLayout(self.data.getAllDataList(self.root.historic_path))

    def updateLayout(self,travel_list:list):
        """Delete all widgets of layout then add new widgets from travel_list"""
        if self.main_layout.count() != 0: 
            print('delete widgets')  
            for i in range(self.main_layout.count()):
                self.main_layout.itemAt(i).widget().deleteLater()
        for e in travel_list:
            travel = Travel(e)
            travel_widget = TravelWidget(travel)
            print(travel_widget.travel.start)
            self.main_layout.addWidget(travel_widget)

class SearchListWidget(QWidget):
    def __init__(self,data:list): # data : [ str,str...]
        super().__init__()
        self.data = data
        self.UIComponents()
        self.enable(False)

    def UIComponents(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.search_edit = QLineEdit()
        self.search_edit.textChanged.connect(self.onTextChange)
        self.list_widget = QListWidget()
        self.list_widget.itemSelectionChanged.connect(self.onSelectionChange)
        self.list_widget.setFixedHeight(60)

        layout.addWidget(self.search_edit)
        layout.addWidget(self.list_widget)

    def setAdress(self,adress):
        self.search_edit.setText(adress)

    def onTextChange(self,text:str):
        # Actualise la recherche lorsque le text change
        self.list_widget.clear()
        if text != '':
            for e in self.data : # data : [[str],[str]]
                item = QListWidgetItem(e[0])
                if item.text().lower().find(text.lower()) != -1:
                    self.list_widget.addItem(item)
                else : del(item)

    def onSelectionChange(self):
        # Actualise le texte de la searchBar et reset les résultats
        select_str = self.list_widget.currentItem().text()
        self.search_edit.setText(select_str)
        self.list_widget.clear()

    def enable(self,state:bool):
        # Active ou désactive l'édition de la ligne de selection
        self.search_edit.setEnabled(state)

    def getSelectionText(self):
        return(self.search_edit.text())
    
    def newSelection(self):
        # Retourne True si le texte de la searchBar n'est pas dans data
        for e in self.data:
            if self.search_edit.text().lower() == e[0].lower(): return(False)
            else : return(True)