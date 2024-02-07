from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget
from custom_object import Travel
from custom_object import *

class AdressEditorWidget(QGroupBox):
    def __init__(self,title) -> None:
        super().__init__()
        self.root = Roots()
        self.setTitle(title)
        self.UIComponents()
        self.setStyleSheet('QGroupBox:title {'
                 'subcontrol-origin: margin;'
                 'subcontrol-position: top center;'
                 'padding-left: 10px;'
                 'padding-right: 10px; }'
                 )

    def UIComponents(self) -> None:
        """Set graphical components"""
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.btn_grp = QButtonGroup()
        self.btn_grp.setExclusive(True)
        self.house_btn = QRadioButton('Maison')
        self.local_btn = QRadioButton('Local')
        self.school_btn = QRadioButton('Ecole')

        self.btn_grp.addButton(self.house_btn)
        self.btn_grp.addButton(self.local_btn)
        self.btn_grp.addButton(self.school_btn)

        self.search_bar = SearchBarWidget(self.root.adress)
        self.search_bar.search_signal.connect(self.onSearchSignal)
        self.list_widget = AdressListWidget(self.root.adress)

        self.main_layout.addWidget(self.house_btn)
        self.main_layout.addWidget(self.local_btn)
        self.main_layout.addWidget(self.school_btn)
        self.main_layout.addWidget(self.search_bar)
        self.main_layout.addWidget(self.list_widget)

    def onSearchSignal(self) -> None:
        self.list_widget.update(self.search_bar.result_list)

    def getAdress(self) -> str:
        return(self.search_bar.getAdress())

class PrmtrEditorWidget(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setTitle('Parametres')
        self.UIComponents()
        self.setStyleSheet('QGroupBox:title {'
                 'subcontrol-origin: margin;'
                 'subcontrol-position: top center;'
                 'padding-left: 10px;'
                 'padding-right: 10px; }'
                 )

    def UIComponents(self):
        self.main_layout = QFormLayout()
        self.setLayout(self.main_layout)
        
        self.date_edit = QLineEdit()
        self.distance_edit = QLineEdit()
        self.return_btn = QCheckBox('Aller / Retour')

        self.main_layout.addRow('Date',self.date_edit)
        self.main_layout.addRow('Distance',self.distance_edit)
        self.main_layout.addRow(self.return_btn)

    def getDate(self) -> str:
        return(self.date_edit.text())
    
    def getDistance(self) -> str:
        return(self.distance_edit.text())
    
    def getreturnState(self) -> str:
        if self.return_btn.isChecked(): return_state = 'true'
        else: return_state = 'false'
        return(return_state)

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
        self.setFixedWidth(500)

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
        self.result_list = self.data.findList(self.root,self.text()) # [['a','b'],['a','b]]
        self.search_signal.emit()

    def getAdress(self) -> str:
        return(self.text())

class AdressListWidget(QListWidget):
    def __init__(self,root) -> None:
        super().__init__()
        self.data = Data()
        self.root = root
        self.setFixedHeight(60)

    def update(self,return_list:list) -> None:
        self.clear()
        for e in return_list:
            item = QListWidgetItem(e[0])
            self.addItem(item)

class TravelListWidget(QWidget):
    def __init__(self,root) -> None:
        super().__init__()
        self.data = Data()
        self.root = root
        self.UIComponents()

    def UIComponents(self) -> None:
        """Set graphical components"""
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.update(self.data.getAllTravelList(self.root)[1:])

    def update(self,return_list:list) -> None:
        """Delete all widgets of layout then add new widgets from travel_list"""
        if self.main_layout.count() != 0:  
            for i in range(self.main_layout.count()):
                self.main_layout.itemAt(i).widget().deleteLater()
        for e in return_list:
            travel = Travel(e)
            travel_widget = TravelWidget(travel)
            self.main_layout.addWidget(travel_widget)
