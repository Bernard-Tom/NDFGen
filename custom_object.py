import csv 
from datetime import datetime
import pandas as pd

class Adress():
    def __init__(self,name,street,postal,city) -> None:
        self.name=name
        self.street = street
        self.postal=postal
        self.city=city

    def getFullString(self) -> str:
        return(self.name+' '+self.street+' '+self.postal+' '+self.city)

    def getStreetString(self) -> str:
        return(self.street+' '+self.postal+' '+self.city)

class Travel(): # A modifier
    """
    A class used to represent a Travel
    Attributes : rtrn_state = 'true' or 'false
    """
    def __init__(self,date:str,start_adress:Adress,end_adress:Adress,distance:str,price:str,rtrn_state:str) -> None:
        self.date = date
        self.start_adress = start_adress
        self.end_adress = end_adress
        self.distance = distance
        self.price = price
        self.rtrn_state = rtrn_state
    
    def getList(self) -> list:
        return([self.date,self.start_adress.name,self.start_adress.street,self.start_adress.postal,self.start_adress.city,
                self.end_adress.name,self.end_adress.street,self.end_adress.postal,self.end_adress.city,
                self.distance,self.price,self.rtrn_state])
    
    def getString(self) ->str:
        return(' '.join(self.list[:3]))  # without distance and rtrn_state
    
class Data():
    """A class used to get and set saved file datas"""    
    def __init__(self) -> None:
        pass
    
    def getDataList(self,root) -> list[list[str]]:
        # return a list of file row with header
        with open(root,'r')as csv_file:
            reader = csv.reader(csv_file,delimiter=';')
            list_reader = list(reader)
        return(list_reader) 
    
    def getTravelList(self,root) -> list[Travel]:
        with open(root,'r')as csv_file:
            reader = csv.DictReader(csv_file,delimiter=';')
            list_reader = list(reader)
            travel_list = []
            for row in list_reader:
                date = row['date']
                start_adress = Adress(row['start_name'],row['start_street'],row['start_postal'],row['start_city'])
                end_adress = Adress(row['end_name'],row['end_street'],row['end_postal'],row['end_city'])
                distance = row['distance']
                price = row['price']
                rtrn_state = row['rtrn_state']
                travel = Travel(date,start_adress,end_adress,distance,price,rtrn_state)
                travel_list.append(travel)
        return(travel_list) 

    def getAdressList(self,root) -> list[Adress]:
        with open(root,'r')as csv_file:
            adress_list = []
            reader = csv.DictReader(csv_file,delimiter=';')
            list_reader = list(reader)
            for row in list_reader:
                name = row['name']
                street = row['street']
                postal = row['postal']
                city = row['city']
                adress = Adress(name,street,postal,city)
                adress_list.append(adress)
        return(adress_list)   
    
    def writeData(self,root:str,data:list) -> None:
        with open(root,'w',newline="")as csv_file:
            writer = csv.writer(csv_file,delimiter=';')
            for row in data:
                writer.writerow(row)

    def getSortedlList(self,list:list) -> list:
        """Return a list sorted throw the date"""
        date_dict = {}
        for data in list: 
            date_dict[datetime.strptime(data[0],'%d/%m/%Y')] = data

        for e,i in zip (sorted(date_dict),range(len(sorted(date_dict)))):
            list[i] = date_dict[e]
        return list

    def saveTravel(self,root,old_travel:Travel,travel:Travel) -> None:
        data = self.getDataList(root)
        start_adress = travel.start_adress
        end_adress = travel.end_adress
        new_row = [travel.date,start_adress.name,start_adress.street,start_adress.postal,start_adress.city,end_adress.name,end_adress.street,end_adress.postal,end_adress.city,travel.distance,travel.price,travel.rtrn_state]
        if old_travel != None:
            old_travel_list = old_travel.getList()
            if old_travel_list in data:
                data[data.index(old_travel_list)] = new_row # +1 beacause data return header too 
        else: data.append(new_row)
        sorted_data = self.getSortedlList(data[1:]) # no take the header
        for i in range(len(data)-1):
            data[i+1] = sorted_data[i]
        self.writeData(root,data)

class Roots():
    def __init__(self) -> None:
        self.historic = './data/historic.csv'
        self.adress = './data/adress.csv'

from openpyxl import Workbook
from openpyxl.styles import colors,Font,Border,Side

class Excell():
    def __init__(self) -> None: 
        self.title = f'Frais de déplacement du test au test'
        self.code = 'Code DA - 601030'
        self.user_name = 'Ana-Leïla MEJRI'
        self.user_adress = '31 rue du Cardinal 1000 Bruxelles'
        self.user_bank = 'FR97 3000 2059 3600 0019 3213 S77'

        self.start_tab_row = 6
        self.df = pd.read_csv('test.csv',sep=';')
        self.tab_dict = self.getTabDict(self.df)
        self.end_tab_row = self.start_tab_row+len(list(self.tab_dict.values())[0])
        print(self.end_tab_row)

        self.nb_tab_column = len(self.tab_dict)
        self.nb_tab_row = len(self.tab_dict['Date'])

        self.wb = Workbook()
        self.sh = self.wb.active
        
        #self.sh.title = 'onglet'
        self.my_border = Side(border_style="thin", color="000000")
        self.setSheet()
        self.setTab(self.tab_dict)
        self.setBottomTab()

        self.wb.save("NDF.xlsx")
        
    def getTabDict(self,df) -> dict:
        tab_dict={'Date':[],
              'Ecole + Trajet':[],
              'Adresse':[],
              'CP':[],
              'Localité':[],
              'Km/AR':[],
              '€/km':[]}
        
        for csv_key,dict_key in zip (['date','end_name','end_street','end_postal','end_city','distance','price'],tab_dict.keys()):
            tab_dict[dict_key] = list(df[csv_key].values)

        tab_dict['Total'] = []
        for i in range(len(list(tab_dict.values())[0])):
            row_index = self.start_tab_row+1+i
            tab_dict['Total'].append(f'=F{row_index}*G{row_index}')
        return(tab_dict)

    def setSheet(self):
        self.setColumnDim()
        head = {'A1':'Frais de déplacement',
                'G1':self.code,
                'B3':self.user_name,
                'C3':self.user_adress,
                'B4':'Compte bancaire',
                'C4':self.user_bank}
        
        for key in head.keys():
            self.sh[key] = head[key]
            self.sh[key].border = Border(top=self.my_border, left=self.my_border, right=self.my_border, bottom=self.my_border)
            self.sh[key].font = Font(bold=True)

        self.sh.merge_cells('A1:F1')
        self.sh.merge_cells('G1:H1')
        self.sh.merge_cells('C3:H3')
        self.sh.merge_cells('C4:H4')

    
    def setColumnDim(self):
        for dim,column in zip ([20,20,30,10,30,10,10,10],['A','B','C','D','E','F','G','H']):
            self.sh.column_dimensions[column].width = dim

    def setTab(self,tab_dict:dict) -> None:
        for key,column in zip (self.tab_dict.keys(),range(1,len(tab_dict)+1)):
            cell = self.sh.cell(row = self.start_tab_row,column = column, value = key)
            cell.border = Border(top=self.my_border, left=self.my_border, right=self.my_border, bottom=self.my_border)
            cell.font = Font(bold=True)
            for row in range(len(list(tab_dict.values())[0])):
                cell = self.sh.cell(row = self.start_tab_row+1+row, column = column, value = tab_dict[key][row])
                cell.border = Border(top=self.my_border, left=self.my_border, right=self.my_border, bottom=self.my_border)

    def setBottomTab(self):
        tab = {'Déplacement divers':self.end_tab_row+1,
               'Total parkin':self.end_tab_row+2,
               'Total Déplacement':self.end_tab_row+3}
        
        for key in tab.keys():
            self.sh[f'A{tab[key]}'] = key
            self.sh[f'A{tab[key]}'].border = Border(top=self.my_border, left=self.my_border, right=self.my_border, bottom=self.my_border)
            self.sh[f'A{tab[key]}'].font = Font(bold=True)
            self.sh.merge_cells(f'A{tab[key]}:G{tab[key]}')
        
        total = f'=sum(H{self.start_tab_row+1}:H{self.end_tab_row})'
        self.sh.cell(row=tab['Total Déplacement'], column = len(self.tab_dict),value = total)

        #for key in list(self.data.keys()): 
        #    print(key)
        #print(self.df.head())
        #for i in range(len(self.data)):
            #print(i,key)
            #self.sh.cell(row=self.start_tab_row,column=i+1,value=list(self.data)[i])

        #self.sh.cell(row=self.end_tab_row+1,column=self.end_tab_column,value=f'=sum(H{self.start_tab_row}:H{self.end_tab_row})')

        
