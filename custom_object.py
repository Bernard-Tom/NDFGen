import csv 
from datetime import datetime

class Adress():
    def __init__(self,name,street,postal,city) -> None:
        self.name=name
        self.street = street
        self.postal=postal
        self.city=city

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
        return(self.list)
    
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

    def saveTravel(self,root,travel:Travel) -> None:
        data = self.getDataList(root)
        start_adress = travel.start_adress
        end_adress = travel.end_adress
        new_row = [travel.date,start_adress.name,start_adress.street,start_adress.postal,start_adress.city,end_adress.name,end_adress.street,end_adress.postal,end_adress.city,travel.distance,travel.price,travel.rtrn_state]
        data.append(new_row)
        sorted_data = self.getSortedlList(data[1:]) # no take the header
        for i in range(len(data)-1):
            data[i+1] = sorted_data[i]
        self.writeData(root,data)

class Roots():
    def __init__(self) -> None:
        self.historic = './data/historic.csv'
        self.adress = './data/adress.csv'

