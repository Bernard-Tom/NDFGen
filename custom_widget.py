from PyQt5.QtWidgets import (
    QWidget, QLineEdit, QLabel, QPushButton, QVBoxLayout, 
    QGroupBox,QListWidget,QButtonGroup,QRadioButton,QFormLayout,
    QCheckBox,QGridLayout,QListWidgetItem,QSpacerItem,QSizePolicy,
    QCompleter
    )
from PyQt5.QtCore import pyqtSignal,Qt

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
        self.house_btn = QRadioButton('house')
        self.local_btn = QRadioButton('local')
        self.school_btn = QRadioButton('school')
        self.school_btn.setChecked(True)

        self.btn_grp.addButton(self.house_btn)
        self.btn_grp.addButton(self.local_btn)
        self.btn_grp.addButton(self.school_btn)

        self.btn_grp.buttonClicked.connect(lambda:self.onBtnClicked(self.btn_grp.checkedButton()))

        self.search_bar = QLineEdit()

        self.completer = QCompleter(self.adress_list)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.search_bar.setCompleter(self.completer)

        self.main_layout.addWidget(self.house_btn)
        self.main_layout.addWidget(self.local_btn)
        self.main_layout.addWidget(self.school_btn)
        self.main_layout.addWidget(self.search_bar)

    def getSpecAdress(self,string_to_find) -> list:
        for list in self.data.getDataList(self.root.spec_adress):
            if string_to_find in list:
                return(list[1])

    def onBtnClicked(self,btn:QRadioButton)-> None:
        if btn == self.house_btn or btn == self.local_btn:
             adress = self.getSpecAdress(btn.text())
             self.search_bar.setText(adress)
             self.search_bar.setEnabled(False)
        if btn == self.school_btn:
            self.search_bar.setEnabled(True)
            self.search_bar.setText('')

    def setAdress(self,adress:str) ->None:
        self.search_bar.setText(adress)

    def getAdress(self) -> str:
        return(self.search_bar.text())

    def tryUserData(self) -> bool:
        if self.search_bar.text() != '':
            return(True)
        else: return(False)

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
        self.price_edit = QLineEdit()
        self.return_btn = QCheckBox('Aller / Retour')

        self.main_layout.addRow('Date',self.date_edit)
        self.main_layout.addRow('Distance',self.distance_edit)
        self.main_layout.addRow('Prix Kilométrique',self.price_edit)
        self.main_layout.addRow(self.return_btn)

####  Set Data
    def setDate(self,date:str) -> None:
        self.date_edit.setText(date)

    def setDistance(self,distance:str) -> None:
        self.distance_edit.setText(distance)

    def setPrice(self,price) -> None:
        self.price_edit.setText(price)

    def setReturnState(self,rtrn_state:str) -> None:
        if rtrn_state == 'true':
            self.return_btn.setChecked(True)
        else: self.return_btn.setChecked(False)

####  Get Data
    def getDate(self) -> str | bool:
        return(self.date_edit.text())
    
    def getDistance(self) -> str:
        return(self.distance_edit.text())

    def getPrice(self) -> str:
        return(self.price_edit.text())

    def getReturnState(self) -> str:
        if self.return_btn.isChecked(): return_state = 'true'
        else: return_state = 'false'
        return(return_state)
    
#### Try Data
    def tryDate(self,string:str) -> bool:
        if len(string) != 10: 
            return(False)
        if [2,5] != [n for (n,e) in enumerate(string) if e =='/']:
            return(False)
        try:
            int(string[:2])
            int(string[3:5])
            int(string[6:10])
            return(True)
        except: return(False)

    def tryInt(self,string) -> bool:
        try:
            int(string)
            return(True)
        except: return(False)

    def tryUserData(self) -> bool:
        if self.tryDate(self.date_edit.text()) and self.tryInt(self.distance_edit.text()) and self.tryInt(self.price_edit.text()):
            return(True)
        else:
            return(False)

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
        self.price_label = QLabel(self.travel.price)
        self.rtrn_label = QLabel(self.return_txt)

        edit_btn = QPushButton('...')
        edit_btn.setFixedWidth(30)
        edit_btn.clicked.connect(self.onEditClicked)

        layout.addWidget(self.start_label,0,0)
        layout.addWidget(self.end_label,0,1)
        layout.addWidget(self.distance_label,1,0)
        layout.addWidget(self.rtrn_label,1,1)
        layout.addWidget(self.price_label,0,2)
        layout.addWidget(edit_btn,1,2)

    def onEditClicked(self) -> None:
        pass

    def onEditorClose(self) -> None:
        pass

    def getDataString(self) -> str:
        return(self.travel.getString())

class TravelListWidget(QWidget):
    """Custom Widget used to show the list of Travel widget list"""
    edit_signal = pyqtSignal(Travel)
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
            travel = Travel(e)
            travel_widget = TravelWidget(travel)
            travel_widget.edit_signal.connect(lambda:self.editSignal(travel))
            widget_list.append(travel_widget)
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

    def updateDisplay(self,text_to_find:str) -> None:      
        """Show and hide widgets"""
        for widget in self.widget_list:
            if text_to_find.lower() in widget.travel.getString().lower():
                widget.setVisible(True)
            else : widget.setVisible(False)

    def editSignal(self,travel:Travel) -> None:
        self.edit_signal.emit(travel)