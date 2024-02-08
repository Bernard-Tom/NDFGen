from PyQt5.QtWidgets import (
    QWidget, QLineEdit, QLabel, QPushButton, QVBoxLayout, 
    QGroupBox,QListWidget,QButtonGroup,QRadioButton,QFormLayout,
    QCheckBox,QGridLayout,QListWidgetItem,QSpacerItem,QSizePolicy,
    QCompleter
    )
from PyQt5.QtCore import pyqtSignal,Qt

from custom_object import Travel
from custom_object import *

class AdressEditorWidget(QGroupBox):
    """Custom wigdget used to edit Adress in Travel Editor Window"""
    def __init__(self,title) -> None:
        super().__init__()
        self.root = Roots()
        self.data = Data()
        self.adress_list = self.data.getAdressList(self.root.adress)[1:]
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

        self.search_bar = QLineEdit()

        self.completer = QCompleter(self.adress_list)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.search_bar.setCompleter(self.completer)

        self.main_layout.addWidget(self.house_btn)
        self.main_layout.addWidget(self.local_btn)
        self.main_layout.addWidget(self.school_btn)
        self.main_layout.addWidget(self.search_bar)

    def getAdress(self) -> str:
        return(self.search_bar.text())

class PrmtrEditorWidget(QGroupBox):
    """Custom wigdget used to edit prmtrs in Travel Editor Window"""
    def __init__(self) -> None:
        super().__init__()
        self.setTitle('Parametres')
        self.UIComponents()
        self.setStyleSheet('QGroupBox:title {'
                 'subcontrol-origin: margin;'
                 'subcontrol-position: top center;'
                 'padding-left: 10px;'
                 'padding-right: 10px; }'
                 )

    def UIComponents(self) -> None:
        """Set graphical components"""
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
    """Custom wigdget used to show Travel object"""
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
        self.setContentsMargins(10,10,10,10)

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

    def onEditClicked(self) -> None:
        self.edit_signal.emit()

    def getDataString(self) -> str:
        return(self.travel.getString())

class TravelListWidget(QWidget):
    """Custom Widget used to show the list of Travel widget list"""
    def __init__(self,root) -> None:
        super().__init__()
        self.root = root
        self.data = Data()
        self.UIComponents()

    def UIComponents(self) -> None:
        """Set graphical components"""
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.updateLayout()

    def getWidgetList(self) -> list[TravelWidget]:
        """Get all row list from csv file"""
        widget_list = []
        for e in self.data.getDataList(self.root)[1:]:
            widget_list.append(TravelWidget(Travel(e)))
        return(widget_list)
    
    def updateLayout(self) -> None:
        """Delete all widget and add new widget from file reading"""
        self.widget_list = self.getWidgetList()
        if self.main_layout.count() != 0:
            for i in range(self.main_layout.count()):
                item = self.main_layout.itemAt(i)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else: self.main_layout.removeItem(item)
                    
        for widget in self.widget_list:
            self.main_layout.addWidget(widget)
        spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)

        print(self.main_layout.count())

    def updateDisplay(self,text_to_find:str) -> None:      
        """Show and hide widgets"""
        for widget in self.widget_list:
            print(widget.travel.getString().lower())
            if text_to_find.lower() in widget.travel.getString().lower():
                widget.setVisible(True)
            else : widget.setVisible(False)
