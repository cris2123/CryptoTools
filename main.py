import argparse
import requests


class Error(Exception):
    pass

class InvalidType(Error):

    # def __init__(self,msg):
    #     self.msg=msg
    #     print(msg)
    pass



class coinMarket:

    def __init__(self):

        """ For now will be empty """
        self.response=""

    def connect(self):

        self.response=requests.get(
            "https://api.coinmarketcap.com/v1/global/")

        """ Metodo para conectarse al api de
        coin market """

    def getData( self,coin=""):

        try:

            if (type(coin) is not (list)) and (type(coin) is not (str)):
                raise InvalidType("Parameter is not correct")

        except InvalidType:

            print("Data type not valid")



        if coin == "":
            self.response= requests.get("https://api.coinmarketcap.com/v1/ticker/")
            data=self.response.json()
            with open("currencyData.json",'w') as jsonFile:
                jsonFile.write(str(data))

        elif type(coin) is list:

            self.response = requests.get("https://api.coinmarketcap.com/v1/ticker/?limit=0")
            data=self.response.json()
            with open("currencyData.json",'w') as jsonFile:
                jsonFile.write(str(data))

        else:

            URL="https://api.coinmarketcap.com/v1/ticker/" + str(coin) +"/"
            self.response = requests.get(URL)
            data=self.response.json()
            with open("currencyData.json",'w') as jsonFile:
                jsonFile.write(str(data))



        # data=self.response.json()
        # currencie=""

        # for d in data:
        #     if d["symbol"]=="SBD":
        #         currencie=d


        # print(self.response.json())

    def getGlobalData(self):

        self.response = requests.get("https://api.coinmarketcap.com/v1/global/")

        data = self.response.json()
        with open("global.json",'w') as jsonFile:
            jsonFile.write(str(data))



if __name__=="__main__":

    Market=coinMarket()
    Market.connect()
    Market.getData("SBD")

    print("Hola mundo")
