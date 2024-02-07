import csv 

class Travel():
    """
    A class used to represent a Travel
    Attributes : rtrn_state = 'true' or 'false
    """
    def __init__(self,date:str,start:str,end:str,distance:str,rtrn_state:str) -> None:
        self.date = date
        self.start = start
        self.end = end
        self.distance = distance
        self.rtrn_state = rtrn_state

    def __init__(self,list:list) -> None:
        self.date = list[0]
        self.start = list[1]
        self.end = list[2]
        self.distance = list[3]
        self.rtrn_state = list[4]

    def getPrmtrsDict(self) -> dict:
        """Return the travel parameters with a dict object"""
        prmtrs = {'date':self.date,
                  'distance':self.distance,
                  'return_state':self.rtrn_state}   
        return(prmtrs)
    
class Data():
    """A class used to get and set saved file datas"""    
    def __init__(self) -> None:
        pass
    
    def findDataList(self,root:str,text_to_find:str) -> list[list[str]]:
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
    
    def getAllDataList(self,root) -> list[list[str]]:
        # Retourne une liste contenant une liste par ligne du fichier
        with open(root,'r')as csv_file:
            reader = csv.reader(csv_file,delimiter=';')
            list_reader = list(reader)
        return(list_reader[1:])        
    
class Roots():
    def __init__(self) -> None:
        self.historic_path = './data/historic.csv'

