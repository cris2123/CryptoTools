import argparse
import requests
import os

from itertools import chain
from sys import exit
from ErrorFiles import InvalidType, NotCoinSelected, FiatInvalidType, FiatNotValid

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


    def _checkValidFiat(self,fiat):

        """ Source code to check if fiat currency is valid"""

        currencyFiat=""

        try:

            if(fiat!=""):
                if(type(fiat)!=str):
                    print("Fiat invalid type")
                    raise FiatInvalidType
                else:

                    if(fiat not in self.fiat):
                        raise FiatNotValid
                    else:
                        currencyFiat="convert="+fiat

        except FiatInvalidType:
            print("Fiat type must be a string")
            exit(0)

        except FiatNotValid:
            print("Fiat type not available")
            exit(0)

        else:
            return(currencyFiat)


    def _checkValidCoin(self,coin):

        isValidCoin=False

        try:
            if not coin:
                raise NotCoinSelected
            else:
                if(type(coin) is not (str)):
                    raise InvalidType

        except NotCoinSelected:
            print("You need to input a coin")
            exit(0)

        except InvalidType:
            print("Coin value must be a string")
            exit(0)

        else:
            isValidCoin=True

        return(isValidCoin)


    def getAllCoins(self,fiat=""):

        currencyFiat=self._checkValidFiat(fiat)

        if(currencyFiat):

            URL="https://api.coinmarketcap.com/v1/ticker/?limit=0"+"&"+currencyFiat

            try:

                self.response=requests.get(URL)

                if(self.response.status_code != requests.codes.ok):

                    self.response.raise_for_status()

                else:

                    allData=self.response.json()

                    for data in allData:

                        self.coinNames[data["name"]]=(data["symbol"],data["id"])

                    with open("currencyData.json",'w') as jsonFile:
                        jsonFile.write(str(data))

            except Exception as e:

                print(e)
                exit(0)

        else:

            URL="https://api.coinmarketcap.com/v1/ticker/?limit=0"

            try:
                self.response=requests.get(URL)

                if(self.response.status_code != requests.codes.ok):

                    self.response.raise_for_status()

                else:

                    allData=self.response.json()

                    for data in allData:

                        self.coinNames[data["name"]]=(data["symbol"],data["id"])

                    with open("currencyData.json",'w') as jsonFile:
                        jsonFile.write(str(data))

            except Exception as e:

                print(e)
                exit(0)

    def getCoin(self,coin,fiat=""):

        """ Get a specific coin data that do you want to explore

            coin: string value which represent a coin you could input. Coin abreviation
            or coin name (work on in soon)
        """

        isValidCoin  = self._checkValidCoin(coin)

        currencyFiat = self._checkValidFiat(fiat)

        if(isValidCoin):

            if coin in self.coinNames.keys():

                (_,coinId)=self.coinNames[str(coin)]

            else:

                results =list(chain.from_iterable( (coinList[1], coin in coinList )
                    for coinList in self.coinNames.values() if coin in coinList ))

                if(len(results)!=0):
                    coinId=results[0]
                else:
                    coinId=None
                    print("La moneda no existe")

            if(currencyFiat):

                URL="https://api.coinmarketcap.com/v1/ticker/"+str(coinId)+"/?"+currencyFiat

                try:

                    self.response=requests.get(URL)

                    if(self.response.status_code != requests.codes.ok):

                        self.response.raise_for_status()

                    else:
                        data=self.response.json()
                        print(data)

                except Exception as e:

                    print(e)

            else:

                URL="https://api.coinmarketcap.com/v1/ticker/"+str(coinId)+"/"

                try:

                    self.response=requests.get(URL)

                    if(self.response.status_code != requests.codes.ok):

                        self.response.raise_for_status()

                    else:
                        data=self.response.json()
                        print(data)

                except Exception as e:
                    print(e)


    def getData( self,coin="",limit=100,fiat=""):

        try:
            print(type(coin))
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

    def getGlobalData(self,fiat=""):

        currencyFiat=self._checkValidFiat(fiat)

        if(currencyFiat):

            URL="https://api.coinmarketcap.com/v1/global/"+"?"+currencyFiat

            try:

                self.response = requests.get(URL)

                if(self.response.status_code != requests.codes.ok):

                    self.response.raise_for_status()

                else:

                    data = self.response.json()
                    with open("global.json",'w') as jsonFile:
                        jsonFile.write(str(data))

            except Exception as e:

                print(e)
                exit(0)

        else:

            ### Converting to fiat currency selected

            URL="https://api.coinmarketcap.com/v1/global/"


            self.response = requests.get(URL)

            try:

                self.response = requests.get(URL)

                if(self.response.status_code != requests.codes.ok):

                    self.response.raise_for_status()

                else:

                    data = self.response.json()
                    with open("global.json",'w') as jsonFile:
                        jsonFile.write(str(data))

            except Exception as e:

                print(e)
                exit(0)

if __name__=="__main__":

    Market=coinMarket()

    # # #Market.connect()
    #Market.getCoin(coin="SBD",fiat="EUR")
    #Market.getAllCoins(fiat=2)
    Market.getGlobalData(fiat=2)
