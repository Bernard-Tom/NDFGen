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
        return(' '.join(self.getList()[:3]))  # without distance and rtrn_state
    
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
    
    def getAdressList(self,root) -> list[str]:
        with open(root,'r')as csv_file:
            adress_list = []
            reader = csv.reader(csv_file,delimiter=';')
            list_reader = list(reader)
            for row in list_reader:
                adress_list.append(row[0])
        return(adress_list)   
    
    def writeData(self,root:str,data:list) -> None:
        with open(root,'w',newline="")as csv_file:
            writer = csv.writer(csv_file,delimiter=';')
            for row in data:
                writer.writerow(row)

    def saveTravel(self,root,row:list) -> None:
        data = self.getDataList(root)
        data.append(row)
        self.writeData(root,data)

class Roots():
    def __init__(self) -> None:
        self.historic = './data/historic.csv'
        self.adress = './data/adress.csv'
        self.spec_adress = './data/spec_adress.csv'

