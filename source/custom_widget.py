from PyQt5.QtWidgets import (
    QWidget, QLineEdit, QLabel, QPushButton, QVBoxLayout, 
    QGroupBox,QButtonGroup,QRadioButton,QFormLayout,
    QCheckBox,QSpacerItem,QSizePolicy,QComboBox,
    QCompleter,QHBoxLayout,QScrollArea,QFileDialog
    )
from PyQt5.QtCore import pyqtSignal,Qt
from PyQt5.QtGui import QFont

from custom_object import *
import calendar

from datetime import datetime

import os
from pathlib import Path

class AdressEditorWidget(QGroupBox):
    """Custom wigdget used to edit Adress in Travel Editor Window"""
    edit_signal = pyqtSignal()
    def __init__(self,title) -> None:
        super().__init__()
        self.data = Data()
        self.adress_list = self.data.getAdressList()
        self.adress_edited = False
        self.setWidgetStyle(title)
        self.UIComponents()

    def setWidgetStyle(self,title) -> None:
        self.setTitle(title)
        self.setStyleSheet('QGroupBox:title {'
                 'subcontrol-origin: margin;'
                 'subcontrol-position: top center;'
                 'padding-left: 10px;'
                 'padding-right: 10px; }'
                 )

    def UIComponents(self) -> None:
        """Set graphical components"""
        # Btn
        self.house_btn = QRadioButton('house')
        self.local_btn = QRadioButton('Cap Sciences')
        self.new_btn = QRadioButton('new')
        self.new_btn.setChecked(True)

        # Btn Grp
        self.btn_grp = QButtonGroup()
        self.btn_grp.setExclusive(True)
        self.btn_grp.addButton(self.house_btn)
        self.btn_grp.addButton(self.local_btn)
        self.btn_grp.addButton(self.new_btn)

        # Line Edit
        self.name_edit = QLineEdit()
        self.street_edit = QLineEdit()
        self.postal_edit = QLineEdit()
        self.city_edit = QLineEdit()

        # Completers
        completer_list = self.getCompleterLists(self.adress_list)
        adress_name_list = completer_list[0]
        adress_street_list = completer_list[1]

        self.name_completer = QCompleter(adress_name_list)
        self.street_completer = QCompleter(adress_street_list)

        self.name_completer.setFilterMode(Qt.MatchContains)
        self.street_completer.setFilterMode(Qt.MatchContains)

        self.name_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.street_completer.setCaseSensitivity(Qt.CaseInsensitive)

        self.name_edit.setCompleter(self.name_completer)
        self.street_edit.setCompleter(self.street_completer)

        # Connect
        self.btn_grp.buttonClicked.connect(self.onBtnClicked)
        
        self.name_completer.activated.connect(self.onSearch)
        self.street_completer.activated.connect(self.onSearch)

        self.name_edit.textChanged.connect(self.edit_signal.emit)
        self.street_edit.textChanged.connect(self.edit_signal.emit)
        self.postal_edit.textChanged.connect(self.edit_signal.emit)
        self.city_edit.textChanged.connect(self.edit_signal.emit)

        # Layout
        self.btn_layout = QHBoxLayout()
        self.btn_layout.addWidget(self.new_btn)
        self.btn_layout.addWidget(self.house_btn)
        self.btn_layout.addWidget(self.local_btn)

        self.form_layout = QFormLayout()
        self.form_layout.addRow('Nom',self.name_edit)
        self.form_layout.addRow('Adresse',self.street_edit)
        self.form_layout.addRow('Code Postale',self.postal_edit)
        self.form_layout.addRow('Localité',self.city_edit)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.btn_layout)
        self.main_layout.addLayout(self.form_layout)
        self.setLayout(self.main_layout)

    def getCompleterLists(self,adress_list:list[Adress]) -> list[list]:
        """Return just name and street adress of Adress for completer"""
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
                self.setAdress(adress)

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
        try:
            if name and street and city and postal != '':
                int(postal)
                adress = Adress(name,street,postal,city)
                return(adress)
            else: return False
        except: return(False)

class PrmtrEditorWidget(QGroupBox):
    """Custom wigdget used to edit prmtrs in Travel Editor Window"""
    def __init__(self) -> None:
        super().__init__()
        self.setWidgetStyle()
        self.data = Data()
        self.UIComponents()

    def setWidgetStyle(self) -> None:
        self.setTitle('Parametres')
        self.setStyleSheet('QGroupBox:title {'
                 'subcontrol-origin: margin;'
                 'subcontrol-position: top center;'
                 'padding-left: 10px;'
                 'padding-right: 10px; }'
                 )

    def UIComponents(self) -> None:
        """Set graphical components"""
        # Widgets
        self.date_edit = QLineEdit()
        self.distance_edit = QLineEdit()
        self.btn_p1 = QRadioButton('0.42')
        self.btn_p1.setChecked(True)
        self.btn_p2 = QRadioButton('1.68')
        self.price_edit = QLineEdit()
        self.return_btn = QCheckBox('Aller / Retour')

        # Btn Grp
        self.btn_grp = QButtonGroup()
        self.btn_grp.setExclusive(True)
        self.btn_grp.addButton(self.btn_p1)
        self.btn_grp.addButton(self.btn_p2)

        # Lay
        self.btn_lay = QHBoxLayout()
        self.btn_lay.addWidget(self.btn_p1)
        self.btn_lay.addWidget(self.btn_p2)

        self.main_layout = QFormLayout()
        self.main_layout.addRow('Date : DD/MM/YYYY',self.date_edit)
        self.main_layout.addRow('Distance : km',self.distance_edit)
        self.main_layout.addRow('Prix Kilométrique : euro/km',self.btn_lay)
        self.main_layout.addRow(self.return_btn)
        self.setLayout(self.main_layout)

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

    def setPreviousDate(self) -> None:
        data = self.data.getTravelList()
        if len(data) != 0:
            last_travel = data[len(data)-1]
            self.setDate(last_travel.date)

####  Get Data
    def getDate(self) -> str | bool:
        try:
            date = self.date_edit.text()
            travel_date = datetime.strptime(date,'%d/%m/%Y')
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
    
class TravelEditorWin(QWidget):
    close_signal = pyqtSignal()
    delet_signal = pyqtSignal()
    def __init__(self) -> None:
        super().__init__()
        self.old_travel = None
        self.data = Data()
        self.adress_list = self.data.getAdressList()
        self.UIComponents()

    def UIComponents(self)-> None:
        """Set graphical components"""
        # Widgets
        self.start_editor = AdressEditorWidget('Départ')
        self.end_editor = AdressEditorWidget('Arrivée')
        self.prmtr_editor = PrmtrEditorWidget()
        self.err_label= QLabel()
        save_btn = QPushButton('Enregistrer')
        delete_btn = QPushButton('Supprimer')

        # Style
        self.err_label.setStyleSheet('color:red')
        self.err_label.setAlignment(Qt.AlignHCenter)

        # Connect
        save_btn.clicked.connect(self.save)
        delete_btn.clicked.connect(self.deleteTravel)

        self.start_editor.edit_signal.connect(self.onAdressEdit)
        self.end_editor.edit_signal.connect(self.onAdressEdit)

        # Lay
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.start_editor)
        main_layout.addWidget(self.end_editor)
        main_layout.addWidget(self.prmtr_editor)
        main_layout.addWidget(self.err_label)
        main_layout.addWidget(save_btn)
        main_layout.addWidget(delete_btn)
        self.setLayout(main_layout)

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

    def onAdressEdit(self) -> None:
        """If adress in adress editor changed -> check if distance can be show by reading in travel.csv"""
        start_adress = self.start_editor.getAdress()
        end_adress = self.end_editor.getAdress()
        if (start_adress and end_adress != False) and (start_adress.name != end_adress.name):
            distance = self.data.getTravelDistance(start_adress.name,end_adress.name)
            if distance != False:
                self.prmtr_editor.setDistance(distance)
            else: self.prmtr_editor.setDistance('')
        else: self.prmtr_editor.setDistance('')

    def getUserTravel(self) -> Travel | bool:
        date = self.prmtr_editor.getDate()
        start_adress = self.start_editor.getAdress()
        end_adress = self.end_editor.getAdress()
        distance = self.prmtr_editor.getDistance()
        price = self.prmtr_editor.getPrice()
        return_state = self.prmtr_editor.getReturnState()
        if date and start_adress and end_adress and distance and price and return_state is not False:
            return Travel(date,start_adress,end_adress,distance,price,return_state) 
        else: return(False)

    def save(self):
        travel = self.getUserTravel()
        if travel != False:
            self.data.saveToHistoric(self.old_travel,travel)
            self.data.saveAdress(travel.start_adress) # Save adress in adress.csv if they are new ones
            self.data.saveAdress(travel.end_adress)
            self.data.saveToTravel(travel) # Save travel in travel.csv if it's new one
            self.close_signal.emit()
        else: self.err_label.setText('format error')

    def deleteTravel(self):
        if self.old_travel != None:
            self.data.deleteTravel(self.old_travel)
            self.close_signal.emit()

class TravelWidget(QGroupBox):
    """Custom wigdget used to show Travel object"""
    edit_signal = pyqtSignal()
    def __init__(self,travel:Travel) -> None:
        super().__init__()
        self.travel = travel
        self.setWidget()
        self.UIComponents()

    def setWidget(self) -> None:
        self.setTitle(self.travel.date)
        self.setFixedHeight(100)
        self.setFixedWidth(720)
        self.setContentsMargins(10,10,10,10)
        self.setStyleSheet("QGroupBox {border: 2px solid #000000;}")

    def getRtrnState(self) -> str:
        if self.travel.rtrn_state == 'true': return('Aller Retour')
        else : return('Aller Simple')  

    def UIComponents(self) -> None:
        """Set graphical components"""
        # Widgets
        self.start_name_label = QLabel(self.travel.start_adress.name)
        self.start_street_label = QLabel(self.travel.start_adress.getStreetString())
        self.arrow_label = QLabel('-->')
        self.end_name_label = QLabel(self.travel.end_adress.name)
        self.end_street_label = QLabel(self.travel.end_adress.getStreetString())
        self.distance_label = QLabel(self.travel.distance+' km')
        self.price_label = QLabel(self.travel.price+' euro/km')
        self.rtrn_label = QLabel(self.getRtrnState())
        self.edit_btn = QPushButton('...')

        # Font
        font = QFont()
        font.setBold(True)
        self.start_name_label.setFont(font)
        self.end_name_label.setFont(font)

        # Alignment
        self.start_name_label.setAlignment(Qt.AlignHCenter)
        self.start_street_label.setAlignment(Qt.AlignHCenter)
        self.arrow_label.setAlignment(Qt.AlignCenter)
        self.end_name_label.setAlignment(Qt.AlignHCenter)
        self.end_street_label.setAlignment(Qt.AlignHCenter)

        # Size
        self.edit_btn.setFixedWidth(30)

        # Connect
        self.edit_btn.clicked.connect(self.onEditClicked)

        # Layout
        start_lay = QVBoxLayout()
        start_lay.addWidget(self.start_name_label)
        start_lay.addWidget(self.start_street_label)

        end_lay = QVBoxLayout()
        end_lay.addWidget(self.end_name_label)
        end_lay.addWidget(self.end_street_label)
        
        top_lay = QHBoxLayout()
        top_lay.addLayout(start_lay)
        top_lay.addWidget(self.arrow_label)
        top_lay.addLayout(end_lay)
        
        bottom_lay = QHBoxLayout()
        bottom_lay.addWidget(self.distance_label)
        bottom_lay.addWidget(self.price_label)
        bottom_lay.addWidget(self.rtrn_label)
        bottom_lay.addWidget(self.edit_btn)

        main_lay = QVBoxLayout()
        main_lay.addLayout(top_lay)
        main_lay.addLayout(bottom_lay)
        self.setLayout(main_lay)

    def onEditClicked(self) -> None:
        self.editor_win = TravelEditorWin()
        self.editor_win.setUserTravel(self.travel)
        self.editor_win.close_signal.connect(self.edit_signal.emit)
        #self.editor_win.delet_signal.connect()
        self.editor_win.show()

class TravelListWidget(QWidget):
    """Custom Widget used to show the list of Travel widget list"""
    edit_signal = pyqtSignal(Travel)
    def __init__(self) -> None:
        super().__init__()
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
        for travel in self.data.getTravelList():
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

class GenWin(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.UIComponents()

    def UIComponents(self) -> None:
        # Widgets
        self.year_label = QLineEdit('2024')
        self.start_date_label = QLineEdit()
        self.end_date_label = QLineEdit()
        self.month_selector = self.getSelector()
        gen_btn = QPushButton('Générer')

        # Connect
        self.month_selector.currentIndexChanged.connect(self.onComboChange)
        gen_btn.clicked.connect(self.generate)

        # Lay
        form_lay = QFormLayout()
        form_lay.addRow('Année',self.year_label)
        form_lay.addRow('Mois',self.month_selector)
        form_lay.addRow('Date de début', self.start_date_label)
        form_lay.addRow('Date de fin', self.end_date_label)

        main_lay = QVBoxLayout()
        main_lay.addLayout(form_lay)
        main_lay.addWidget(gen_btn)
        self.setLayout(main_lay)

    def getSelector(self) -> QComboBox:
        selector = QComboBox()
        for month in list(calendar.month_name):
            selector.addItem(month)
        return(selector)

    def onComboChange(self,index) -> None:
        if index != 0: state = False
        else: state = True
        self.start_date_label.setEnabled(state)
        self.end_date_label.setEnabled(state)

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
        month_nb = self.month_selector.currentIndex()
        year = self.year_label.text()
        if month_nb != 0:
            end_day = calendar.monthrange(int(year),month_nb)[1]
            if month_nb < 10: month_nb = f'0{month_nb}'
            start_date = f'01/{month_nb}/{year}'
            end_date = f'{end_day}/{month_nb}/{year}'
        else:
            if not(self.tryDate(self.start_date_label.text()) and self.tryDate(self.end_date_label.text())): 
                print("error")
                pass
            else:
                start_date = self.start_date_label.text()
                end_date = self.end_date_label.text() 
        excel_win = Excel(start_date,end_date)
        excel_win.save()
        self.close()     
        
class HistoricWin(QWidget):
    """Class used to show all travel for historic"""
    def __init__(self) -> None:
        super().__init__()
        self.data = Data()
        self.UIComponents()

    def UIComponents(self) -> None:
        """Set graphical components"""
        # Widgets
        self.search_bar = QLineEdit()
        self.travel_list_widget = TravelListWidget()
        self.my_scroll = QScrollArea()
        add_btn = QPushButton('Ajouter')
        gen_btn = QPushButton('Générer')

        # Scroll
        self.my_scroll.setWidgetResizable(True)
        self.my_scroll.setWidget(self.travel_list_widget)

        # Connect
        self.search_bar.textChanged.connect(self.onSearchSignal)
        add_btn.clicked.connect(self.addTravel)
        gen_btn.clicked.connect(self.generate)
        
        # Lay
        self.btn_layout = QHBoxLayout()
        self.btn_layout.addWidget(add_btn)
        self.btn_layout.addWidget(gen_btn)

        self.main_layout = QVBoxLayout()   
        self.main_layout.addWidget(self.search_bar)
        self.main_layout.addWidget(self.my_scroll)
        self.main_layout.addLayout(self.btn_layout)
        self.setLayout(self.main_layout) 

    def onSearchSignal(self) -> None: 
        """Delete all widgets of layout then add new widgets from travel_list"""
        self.travel_list_widget.updateDisplay(self.search_bar.text())

    def addTravel(self) -> None:
        self.travel_editor_win = TravelEditorWin()
        self.travel_editor_win.prmtr_editor.setPreviousDate()
        self.travel_editor_win.show()
        self.travel_editor_win.close_signal.connect(self.onEditorClose)

    def onEditorClose(self) -> None:
        self.travel_editor_win.close()
        self.travel_list_widget.updateLayout()

    def generate(self) -> None:
        self.gen_win = GenWin()
        self.gen_win.show()
