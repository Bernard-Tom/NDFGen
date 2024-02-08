import csv 

class Travel(): # A modifier
    """
    A class used to represent a Travel
    Attributes : rtrn_state = 'true' or 'false
    """
    def __init__(self,list:list) -> None:
        self.date = list[0]
        self.start = list[1]
        self.end = list[2]
        self.distance = list[3]
        self.rtrn_state = list[4]
    
    def getList(self) -> list:
        return([self.date,self.start,self.end,self.distance,self.rtrn_state])
    
    def getString(self) ->str:
        return(' '.join(self.getList()))
    
class Data():
    """A class used to get and set saved file datas"""    
    def __init__(self) -> None:
        pass
    
    def findList(self,root:str,text_to_find:str) -> list[list[str]]:
        """Return a list of a list of string if we find the text in csv file"""
        with open(root,'r') as csv_file:
            reader = csv.reader(csv_file,delimiter=';')
            list_reader = list(reader)
            result_list = []
            for row in list_reader[1:]:
                for e in row: 
                    if text_to_find.lower() in e.lower():
                        result_list.append(row)
                        break
        return(result_list)
    
    def getAllTravelList(self,root) -> list[list[str]]:
        # Retourne une liste contenant une liste par ligne du fichier
        with open(root,'r')as csv_file:
            reader = csv.reader(csv_file,delimiter=';')
            list_reader = list(reader)
        return(list_reader) 
    
    def writeData(self,root:str,data:list) -> None:
        with open(root,'w',newline="")as csv_file:
            writer = csv.writer(csv_file,delimiter=';')
            for row in data:
                writer.writerow(row)

    def saveTravel(self,root,row:list) -> None:
        data = self.getAllTravelList(root)
        data.append(row)
        self.writeData(root,data)

class Roots():
    def __init__(self) -> None:
        self.historic = './data/historic.csv'
        self.adress = './data/adress.csv'

