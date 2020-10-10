import requests
from bs4 import BeautifulSoup
import os

class Data():
    __id = None
    __type = None
    __tr = None
    __en = None

    @property
    def ID(self):
        return self.__id
    @ID.setter
    def ID(self, value):
        self.__id = value

    @property
    def Type(self):
        return self.__type
    @Type.setter
    def Type(self, value):
        self.__type = value
    
    @property
    def Tr(self):
        return self.__tr
    @Tr.setter
    def Tr(self, value):
        self.__tr = value

    @property
    def En(self):
        return self.__en
    @En.setter
    def En(self, value):
        self.__en = value

    def __init__(self, ID=None, Type=None, Tr=None, En=None):
        if ID is not None:
            self.__id = ID
        if Type is not None:
            self.__type = Type
        if Tr is not None:
            self.__tr = Tr
        if En is not None:
            self.__en = En
    
    def __str__(self):
        return f"{self.ID} [{self.Type}], {self.Tr}, {self.En}"
    
class TurengParser():

    def search(self, key):
        link = os.path.join("https://tureng.com/tr/turkce-ingilizce", key.replace(" ", "%20"))
        print(link)
        return self.request(link)

    def request(self, link):    
        response = requests.get(link)
        if response.status_code == 200:
            return self.parse(response.text)
        else:
            raise Exception(f"Request status code: {response.status_code}")
            
    def parse(self, html):
        Items = []
        source = BeautifulSoup(html, "html5lib")

        table = source.find_all("table")[0]
        trs = table.find_all("tr")

        for index_tr, tr in enumerate(trs):
            tds = tr.find_all("td")
            tds = list(filter(lambda x: x.get("class") != None, tds))
            

            if tds:
                data = Data()
                for td in tds:
                    #print("TD:", td.get("class"), td.text)
                    # Type :
                    if(td.get("class") == ["hidden-xs"]):
                        data.Type = td.text
                    # Tr:
                    if(td.get("class") == ['tr', 'ts']):
                        data.Tr = td.text
                    # En:
                    if(td.get("class") == ['en', 'tm']):
                        data.En = td.text
                Items.append(data)
        return Items

if __name__ == '__main__':
    items = TurengParser().search("hello")
    for index, item in enumerate(items):
        print(index, item)
    

