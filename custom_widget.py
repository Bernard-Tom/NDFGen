from PyQt5.QtWidgets import (
    QWidget, QLineEdit, QLabel, QPushButton, QVBoxLayout, 
    QGroupBox,QListWidget,QButtonGroup,QRadioButton,QFormLayout,
    QCheckBox,QGridLayout,QListWidgetItem,QSpacerItem,QSizePolicy,
    QCompleter,QHBoxLayout,QScrollArea,
    )
from PyQt5.QtCore import pyqtSignal,Qt

from custom_object import *

import os

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

        # Btn 
        self.btn_layout = QHBoxLayout()
        self.btn_grp = QButtonGroup()
        self.btn_grp.setExclusive(True)
        self.house_btn = QRadioButton('house')
        self.local_btn = QRadioButton('Cap Sciences')
        self.new_btn = QRadioButton('new')
        self.new_btn.setChecked(True)

        self.btn_grp.addButton(self.house_btn)
        self.btn_grp.addButton(self.local_btn)
        self.btn_grp.addButton(self.new_btn)

        self.btn_grp.buttonClicked.connect(self.onBtnClicked)
        self.btn_layout.addWidget(self.new_btn)
        self.btn_layout.addWidget(self.house_btn)
        self.btn_layout.addWidget(self.local_btn)

        # Line Edit
        self.name_edit = QLineEdit()
        completer_list = self.getCompleterLists(self.adress_list)
        adress_name_list = completer_list[0]
        adress_street_list = completer_list[1]

        self.name_completer = QCompleter(adress_name_list)
        self.name_completer.setFilterMode(Qt.MatchContains)
        self.name_completer.activated.connect(self.onSearch)
        self.name_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.name_edit.setCompleter(self.name_completer)

        self.street_edit = QLineEdit()
        self.street_completer = QCompleter(adress_street_list)
        self.street_completer.setFilterMode(Qt.MatchContains)
        self.street_completer.activated.connect(self.onSearch)
        self.street_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.street_edit.setCompleter(self.street_completer)

        self.postal_edit = QLineEdit()
        self.city_edit = QLineEdit()

        self.form_layout = QFormLayout()
        self.form_layout.addRow('Nom',self.name_edit)
        self.form_layout.addRow('Adresse',self.street_edit)
        self.form_layout.addRow('Code Postale',self.postal_edit)
        self.form_layout.addRow('Localité',self.city_edit)

        self.main_layout.addLayout(self.btn_layout)
        self.main_layout.addLayout(self.form_layout)

    def getCompleterLists(self,adress_list:list[Adress]) -> list[list]:
        name_list = []
        street_list = []
        for adress in adress_list:
            name_list.append(adress.name)
            street_list.append(adress.street)
        return(name_list,street_list)

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

    def onSearch(self,text) -> None:
        """When user find an adress name in Completer -> set full adress prmtr"""
        for adress in self.adress_list:
            if text == adress.name or text == adress.street:
                self.name_edit.setText(adress.name)
                self.street_edit.setText(adress.street)
                self.postal_edit.setText(adress.postal)
                self.city_edit.setText(adress.city)

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

        self.btn_lay = QHBoxLayout()
        self.btn_grp = QButtonGroup()
        self.btn_grp.setExclusive(True)
        self.btn_p1 = QRadioButton('0.42')
        self.btn_p1.setChecked(True)
        self.btn_p2 = QRadioButton('1.68')
        self.btn_grp.addButton(self.btn_p1)
        self.btn_grp.addButton(self.btn_p2)
        self.btn_lay.addWidget(self.btn_p1)
        self.btn_lay.addWidget(self.btn_p2)

        self.price_edit = QLineEdit()
        self.return_btn = QCheckBox('Aller / Retour')

        self.main_layout.addRow('Date : DD/MM/YYYY',self.date_edit)
        self.main_layout.addRow('Distance : km',self.distance_edit)
        self.main_layout.addRow('Prix Kilométrique : euro/km',self.btn_lay)
        self.main_layout.addRow(self.return_btn)

####  Set Data
    def setDate(self,date:str) -> None:
        self.date_edit.setText(date)

    def setDistance(self,distance:str) -> None:
        self.distance_edit.setText(distance)

    def setPrice(self,price:str) -> None:
        for btn in self.btn_grp.buttons():
            if price == btn.text():
                btn.setChecked(True)

    def setReturnState(self,rtrn_state:str) -> None:
        if rtrn_state == 'true':
            self.return_btn.setChecked(True)
        else: self.return_btn.setChecked(False)

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
        try: 
            float(self.distance_edit.text())
            return(self.distance_edit.text())
        except: return(False)

    def getPrice(self) -> str:
        try:
            float(self.btn_grp.checkedButton().text())
            return(self.btn_grp.checkedButton().text())
        except: return(False)

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
        self.setFixedWidth(720)
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
        self.editor_win = TravelEditorWin()
        self.editor_win.setUserTravel(self.travel)
        self.editor_win.close_signal.connect(self.onEditorClose)
        self.editor_win.show()

    def onEditorClose(self):
        self.edit_signal.emit()

class TravelListWidget(QWidget):
    """Custom Widget used to show the list of Travel widget list"""
    edit_signal = pyqtSignal(Travel)
    def __init__(self) -> None:
        super().__init__()
        self.root = Roots()
        self.data = Data()
        self.widget_list = []
        self.UIComponents()

    def UIComponents(self) -> None:
        """Set graphical components"""
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.updateLayout()

    def getlWidgetList(self) -> list[TravelWidget]:
        """Get all row list from csv file"""
        widget_list = []
        for travel in self.data.getTravelList(self.root.historic):
            travel_widget = TravelWidget(travel)
            widget_list.append(travel_widget)
        return(widget_list)
    
    def updateLayout(self) -> None:
        """Delete all widget and add new widget from file reading"""
        self.widget_list = self.getlWidgetList()
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
                widget.edit_signal.connect(self.editSignal)
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

    def editSignal(self) -> None:
        self.updateLayout()

class TravelEditorWin(QWidget):
    close_signal = pyqtSignal()
    def __init__(self) -> None:
        super().__init__()
        self.data = Data()
        self.root = Roots()
        self.adress_list = self.data.getAdressList(self.root.adress)
        self.UIComponents()
        self.old_travel = None

    def UIComponents(self)-> None:
        """Set graphical components"""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.start_editor = AdressEditorWidget('Départ')
        self.end_editor = AdressEditorWidget('Arrivée')
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

    def getAdressNameList(self,adress_list) -> str:
        adress_name_list = []
        for adress in adress_list:
            adress_name_list.append(adress.name)
        return(adress_name_list)

    def setUserTravel(self,travel:Travel):
        self.old_travel=travel
        self.start_editor.setAdress(travel.start_adress)
        self.end_editor.setAdress(travel.end_adress)
        self.prmtr_editor.setDate(travel.date)
        self.prmtr_editor.setDistance(travel.distance)
        self.prmtr_editor.setPrice(travel.price)
        self.prmtr_editor.setReturnState(travel.rtrn_state)
        
    def getUserTravel(self) -> Travel | bool:
        date = self.prmtr_editor.getDate()
        start_adress = self.start_editor.getAdress()
        end_adress = self.end_editor.getAdress()
        distance = self.prmtr_editor.getDistance()
        price = self.prmtr_editor.getPrice()
        return_state = self.prmtr_editor.getReturnState()
        if not(start_adress and end_adress and distance and price):
            return(False)
        else: 
            if return_state == 'true':
                distance = str(float(distance)*2)
            travel = Travel(date,start_adress,end_adress,distance,price,return_state)
            return(travel)

    def save(self):
        travel = self.getUserTravel()
        if travel != False:
            self.data.saveTravel(self.root.historic,self.old_travel,travel)
            # If adress in travel are new -> save adress in adress.csv
            adress_name_list = self.getAdressNameList(self.adress_list)
            for adress in [travel.start_adress,travel.end_adress]:
                if not(adress.name in adress_name_list):
                    self.data.saveAdress(self.root.adress,adress)
            self.close_signal.emit()
        else: self.err_label.setText('format error')

class GenWin(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.root = Roots()
        self.UIComponents()

    def UIComponents(self) -> None:
        main_lay = QVBoxLayout()
        self.setLayout(main_lay)

        form_lay = QFormLayout()
        self.start_date_label = QLineEdit()
        self.end_date_label = QLineEdit()
        form_lay.addRow('Date de début', self.start_date_label)
        form_lay.addRow('Date de fin', self.end_date_label)
        gen_btn = QPushButton('Générer')
        gen_btn.clicked.connect(self.generate)
        main_lay.addLayout(form_lay)
        main_lay.addWidget(gen_btn)

    def tryDate(self,date) -> bool:
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

    def generate(self) -> None:
        start_date = self.start_date_label.text()
        end_date = self.end_date_label.text()
        if self.tryDate(start_date) and self.tryDate(end_date): 
            excel_win = Excel(start_date,end_date)
            self.close()
            #os.system(f"start EXCEL.EXE {self.root.ndf_excel}")
        
class HistoricWin(QWidget):
    """Class used to show all travel for historic"""
    def __init__(self) -> None:
        super().__init__()
        self.root = Roots()
        self.data = Data()
        self.UIComponents()

    def UIComponents(self) -> None:
        """Set graphical components"""
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.search_bar = QLineEdit()
        self.search_bar.textChanged.connect(self.onSearchSignal)

        self.travel_list_widget = TravelListWidget()

        self.my_scroll = QScrollArea()
        self.my_scroll.setWidgetResizable(True)
        self.my_scroll.setWidget(self.travel_list_widget)
        
        # Buttons
        self.btn_layout = QHBoxLayout()
        add_btn = QPushButton('Ajouter')
        add_btn.clicked.connect(self.addTravel)
        gen_btn = QPushButton('Générer')
        gen_btn.clicked.connect(self.generate)
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

    def generate(self) -> None:
        self.gen_win = GenWin()
        self.gen_win.show()

