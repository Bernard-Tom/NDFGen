from PyQt5.QtWidgets import (
    QWidget, QLineEdit, QLabel, QPushButton, QVBoxLayout, 
    QGroupBox,QListWidget,QButtonGroup,QRadioButton,QFormLayout,
    QCheckBox,QGridLayout,QListWidgetItem,QSpacerItem,QSizePolicy,
    QCompleter,QHBoxLayout
    )
from PyQt5.QtCore import pyqtSignal,Qt

from custom_object import *

class AdressEditorWidget(QGroupBox):
    """Custom wigdget used to edit Adress in Travel Editor Window"""
    def __init__(self,title) -> None:
        super().__init__()
        self.root = Roots()
        self.data = Data()
        self.adress_list = self.data.getAdressList(self.root.adress)
        self.setTitle(title)
        self.UIComponents()

    def UIComponents(self) -> None:
        """Set graphical components"""
        self.setStyleSheet('QGroupBox:title {'
                 'subcontrol-origin: margin;'
                 'subcontrol-position: top center;'
                 'padding-left: 10px;'
                 'padding-right: 10px; }'
                 )
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.btn_layout = QHBoxLayout()
        self.btn_grp = QButtonGroup()
        self.btn_grp.setExclusive(True)
        self.house_btn = QRadioButton('house')
        self.local_btn = QRadioButton('local')
        self.new_btn = QRadioButton('new')
        self.new_btn.setChecked(True)

        self.btn_grp.addButton(self.house_btn)
        self.btn_grp.addButton(self.local_btn)
        self.btn_grp.addButton(self.new_btn)

        self.btn_grp.buttonClicked.connect(self.onBtnClicked)
        self.btn_layout.addWidget(self.new_btn)
        self.btn_layout.addWidget(self.house_btn)
        self.btn_layout.addWidget(self.local_btn)

        self.name_edit = QLineEdit()
        self.street_edit = QLineEdit()
        self.postal_edit = QLineEdit()
        self.city_edit = QLineEdit()

        self.form_layout = QFormLayout()
        self.form_layout.addRow('Nom',self.name_edit)
        self.form_layout.addRow('Adresse',self.street_edit)
        self.form_layout.addRow('Code Postale',self.postal_edit)
        self.form_layout.addRow('Localité',self.city_edit)

        #self.completer = QCompleter(self.adress_list)
        #self.completer.setCaseSensitivity(Qt.CaseInsensitive)

        self.main_layout.addLayout(self.btn_layout)
        self.main_layout.addLayout(self.form_layout)

    def onBtnClicked(self)-> None:
        btn = self.btn_grp.checkedButton()
        if btn == self.house_btn or btn == self.local_btn:
            for adress in self.adress_list:
                if adress.name == btn.text():
                    self.setAdress(adress)
            self.enableFormLay(False)
        if btn == self.new_btn:
            adress = Adress('','','','')
            self.setAdress(adress)
            self.enableFormLay(True)

    def enableFormLay(self,state:bool) -> None:
        for i in range(self.form_layout.count()):
            self.form_layout.itemAt(i).widget().setEnabled(state)

    def setAdress(self,adress:Adress) -> None:
        self.name_edit.setText(adress.name)
        self.street_edit.setText(adress.street)
        self.postal_edit.setText(adress.postal)
        self.city_edit.setText(adress.city)

    def getAdress(self) -> Adress:
        name = self.name_edit.text()
        street = self.street_edit.text()
        postal = self.postal_edit.text()
        city = self.city_edit.text()
        if name != '' and street != '' and city != '':
            try:
                int(postal)
                adress = Adress(name,street,postal,city)
                return(adress)
            except: return(False)
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

        self.main_layout.addRow('Date : DD/MM/YYYY',self.date_edit)
        self.main_layout.addRow('Distance : km',self.distance_edit)
        self.main_layout.addRow('Prix Kilométrique : euro/km',self.price_edit)
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

    def tryInt(self,string) -> bool:
        try:
            int(string)
            return(True)
        except: return(False)

####  Get Data
    def getDate(self) -> str | bool:
        date = self.date_edit.text()
        if len(date) != 10: 
            return(False)
        if [2,5] != [n for (n,e) in enumerate(date) if e =='/']:
            return(False)
        try:
            int(date[:2])
            int(date[3:5])
            int(date[6:10])
            return(date)
        except: return(False)
    
    def getDistance(self) -> str:
        if self.tryInt(self.distance_edit.text()):
            return(self.distance_edit.text())
        else: return(False)

    def getPrice(self) -> str:
        if self.tryInt(self.price_edit.text()):
            return(self.price_edit.text())
        else: return(False)

    def getReturnState(self) -> str:
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
        self.setFixedWidth(700)
        self.setContentsMargins(10,10,10,10)

    def setRtrnState(self) -> None:
        if self.travel.rtrn_state == 'true': self.return_txt='Aller Retour'
        else : self.return_txt = 'Aller Simple'  

    def UIComponents(self) -> None:
        """Set graphical components"""
        main_lay = QVBoxLayout()
        self.setLayout(main_lay)

        top_lay = QHBoxLayout()
        bottom_lay = QHBoxLayout()

        start_lay = QVBoxLayout()
        end_lay = QVBoxLayout()

        self.start_name_label = QLabel(self.travel.start_adress.name)
        self.start_name_label.setAlignment(Qt.AlignHCenter)
        self.start_street_label = QLabel(self.travel.start_adress.getStreetString())
        self.start_street_label.setAlignment(Qt.AlignHCenter)

        self.arrow_label = QLabel('-->')
        self.arrow_label.setAlignment(Qt.AlignCenter)

        self.end_name_label = QLabel(self.travel.end_adress.name)
        self.end_name_label.setAlignment(Qt.AlignHCenter)
        self.end_street_label = QLabel(self.travel.end_adress.getStreetString())
        self.end_street_label.setAlignment(Qt.AlignHCenter)

        self.distance_label = QLabel(self.travel.distance+' km')
        self.price_label = QLabel(self.travel.price+' euro/km')
        self.rtrn_label = QLabel(self.return_txt)

        self.edit_btn = QPushButton('...')
        self.edit_btn.setFixedWidth(30)
        self.edit_btn.clicked.connect(self.onEditClicked)

        start_lay.addWidget(self.start_name_label)
        start_lay.addWidget(self.start_street_label)
        end_lay.addWidget(self.end_name_label)
        end_lay.addWidget(self.end_street_label)

        top_lay.addLayout(start_lay)
        top_lay.addWidget(self.arrow_label)
        top_lay.addLayout(end_lay)

        bottom_lay.addWidget(self.distance_label)
        bottom_lay.addWidget(self.price_label)
        bottom_lay.addWidget(self.rtrn_label)
        bottom_lay.addWidget(self.edit_btn)

        main_lay.addLayout(top_lay)
        main_lay.addLayout(bottom_lay)

    def onEditClicked(self) -> None:
        pass

    def onEditorClose(self) -> None:
        pass

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

    def getTravelWidgetList(self) -> list[TravelWidget]:
        """Get all row list from csv file"""
        widget_list = []
        for travel in self.data.getTravelList(self.root):
            travel_widget = TravelWidget(travel)
            widget_list.append(travel_widget)
        return(widget_list)
    
    def updateLayout(self) -> None:
        """Delete all widget and add new widget from file reading"""
        self.widget_list = self.getTravelWidgetList()
        if self.main_layout.count() != 0:
            for i in range(self.main_layout.count()):
                item = self.main_layout.itemAt(i)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else: self.main_layout.removeItem(item)
        if len(self.widget_list) != 0:            
            for widget in self.widget_list:
                self.main_layout.addWidget(widget)
            spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.main_layout.addItem(spacer)

    def updateDisplay(self,text_to_find:str) -> None:      
        """Show and hide widgets"""
        for widget in self.widget_list:
            start_string = widget.travel.start_adress.getFullString().lower()
            end_string = widget.travel.end_adress.getFullString().lower()
            if text_to_find.lower() in start_string or text_to_find.lower() in end_string:
                widget.setVisible(True)
            else: widget.setVisible(False)

    def editSignal(self,travel:Travel) -> None:
        self.edit_signal.emit(travel)