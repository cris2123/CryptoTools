import argparse
import requests
import os

from itertools import chain


class Error(Exception):
    pass

class InvalidType(Error):

    # def __init__(self,msg):
    #     self.msg=msg
    #     print(msg)
    pass

class NotCoinSelected(Error):
    pass

class coinMarket:

    def __init__(self):

        """ For now will be empty

        fiat: A set of fiat currencies used to check the value of our crypto
        againts it.
        """

        self.fiat={"AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK",\
        "EUR","GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN",\
        "MYR", "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB",\
        "TRY", "TWD", "ZAR"}

        self.response=""

        self.coinNames={}

        self.getAllCoins()

    # def connect(self):
    #
    #     self.response=requests.get(
    #         "https://api.coinmarketcap.com/v1/global/")
    #
    #     """ Metodo para conectarse al api de
    #     coin market """

    def getAllCoins(self):


        self.response=requests.get("https://api.coinmarketcap.com/v1/ticker/?limit=0")
        allData=self.response.json()

        for data in allData:

            self.coinNames[data["name"]]=(data["symbol"],data["id"])

        with open("currencyData.json",'w') as jsonFile:
            jsonFile.write(str(data))


    def getCoin(self,coin):

        """ Get a specific coin data that do you want to explore

            coin: string value which represent a coin you could input. Coin abreviation
            or coin name (work on in soon)
        """

        try:
            if not coin:
                raise NotCoinSelected
            else:
                if(type(coin) is not (str)):
                    raise InvalidType

        except NotCoinSelected:
            print("You need to input a coin")
        except InvalidType:
            print("Coin value must be a string")

        else:

            if coin in self.coinNames.keys():

                (_,coinId)=self.coinNames[str(coin)]

                URL="https://api.coinmarketcap.com/v1/ticker/" + str(coinId) +"/"
                self.response=requests.get(URL)
                data=self.response.json()

                print(data)

            #coinTuple[1],isCoin=
            respuesta =list(chain.from_iterable( (coinList[1], coin in coinList )
                for coinList in self.coinNames.values() if coin in coinList ))

            print(respuesta)
            # if(isCoin):
            #
            #     print(isCoin)
            #     # URL="https://api.coinmarketcap.com/v1/ticker/" + str(coinId) +"/"
            #     # self.response=requests.get(URL)
            #     # data=self.response.json()
            #     # print("Logre llegar aqui")


    def getData( self,coin="",limit=100,fiat=""):

        try:
            print(type(coin))
            if (type(coin) is not (list)) and (type(coin) is not (str)):

                raise InvalidType("Parameter is not correct")

        except InvalidType:

            print("Data type not valid")


        if coin == "":
            print("Entre aqui")
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
    # # #Market.connect()
    Market.getCoin(coin="SBD")
    #Market.getAllCoins()

    # x={"Bitcoin":("BTC","bitcoin")}
    # coinId,isCoin=chain.from_iterable((d[1], "BTC" in d) for d in x.values() )
    #respuesta=[ "BTC" in d for d in x.values()]
    #coinId,isCoin=tuple(chain.from_iterable((d[1], coin in coinList) for coinList in self.coinNames.values() ))
    # print(coinId)
    # print(isCoin)
    #print(id_p)
    #
    # print(x.values())

    #print("Hola mundo")
