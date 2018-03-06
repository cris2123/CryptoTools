import argparse
import requests
import os
import json

from itertools import chain
from sys import exit
from userExceptions import InvalidType, NotCoinSelected, FiatInvalidType, FiatNotValid

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
        self.wholeContent=""

        ## funcion para obteenr todos las monedas en coin market
        self.getCoinNames()


    def _checkValidFiat(self,fiat):

        """ Source code to check if fiat currency is valid"""

        currencyFiat=""

        try:

            if(fiat!="" or fiat==None):
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

    def getCoinNames(self):

        allData=self.getAllCoins()

        with open("currencyData.json",'w') as jsonFile:
            jsonFile.write(str(allData))

        if(allData):

            for data in allData:

                self.coinNames[data["name"]]=(data["symbol"],data["id"])

        self.wholeContent=allData

    def getAllCoins(self,fiat=""):

        currencyFiat=self._checkValidFiat(fiat)

        if(currencyFiat):

            URL="https://api.coinmarketcap.com/v1/ticker/?limit=0"+"&"+currencyFiat

        else:

            URL="https://api.coinmarketcap.com/v1/ticker/?limit=0"

        try:

            self.response=requests.get(URL)

            if(self.response.status_code != requests.codes.ok):

                self.response.raise_for_status()

            else:

                return(self.response.json())

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

    def getListCoins(self,coins,fiat=""):

        arrayValidCoins=[]

        for coin in coins:

            if coin in self.coinNames.keys():

                arrayValidCoins.append((self.coinNames[coin][1],True))

            else:

                results =list(chain.from_iterable( (coinList[1], coin in coinList )
                    for coinList in self.coinNames.values() if coin in coinList ))

                if(len(results)==0):
                    arrayValidCoins.append((coin,False))
                else:
                    arrayValidCoins.append(tuple(results))


        print(arrayValidCoins)
        currencyFiat=self._checkValidFiat(fiat)


        print(currencyFiat)

        coinInformation=[]

        # with open("global.json",'w') as jsonFile:
        #     jsonFile.write(str(data))


        for item in self.wholeContent:

            for tupleCoin in arrayValidCoins:


                if(tupleCoin[1]==True):
                    print("Llegue a tupleCoin[1]:")
                    if(item["id"]==tupleCoin[0]):
                        print("Tuple coin es:"+ str(tupleCoin[0]))
                        coinInformation.append(item)

                else:
                    coinInformation.append("coin: "+ tupleCoin[0]+" is not a valid one")

            if(len(coinInformation)==len(coins)):
                break;

            #coinInformation=[item for tupleCoin in arrayValidCoins if tupleCoin[1]==True and item["id"]==tupleCoin[0]  ]

        for d in coinInformation:

            print(d)
            print("\n")

        #print(data)

        #
        #
        # if(currencyFiat):
        #
        #     URL="https://api.coinmarketcap.com/v1/ticker/?limit=0"+"&"+currencyFiat
        #
        # else:
        #
        #     URL="https://api.coinmarketcap.com/v1/ticker/?limit=0"
        #
        # try:
        #
        #     self.response=requests.get(URL)
        #
        #     if(self.response.status_code != requests.codes.ok):
        #
        #         self.response.raise_for_status()
        #
        #     else:
        #         data=self.response.json()
        #
        #         ### Check if a list of coins are valid
        #         ### Make a request to the api
        #         ### With data iterate over a list of dictionaries
        #         ### check for every dictionarie if a key of a list match
        #         #### put that data on a ariable and append it.
        #
        #         # for d in data:
        #         #
        #         #     if(d[""])
        #
        #
        # except Exception as e:
        #     print(e)
        #
        # else:
        #     pass



        #### funcion que obtenga todas las monedas y funcion que procese
        #### las monedas existentes con sus id

        #for coin in coins:

    def getGlobalData(self,fiat=""):

        currencyFiat=self._checkValidFiat(fiat)

        if(currencyFiat):

            URL="https://api.coinmarketcap.com/v1/global/"+"?"+currencyFiat

        else:

            URL="https://api.coinmarketcap.com/v1/global/"

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


    #### Parser para la linea de comandos
    parser=argparse.ArgumentParser()

    parser.add_argument("-c", "--coin", type=str,
	help="search for data of a coin by name or symbol on coinMarket")

    parser.add_argument("-cl","--coin-lists",type=list,
    help="search for data of a list of coins by name or symbol on coinMarket")

    parser.add_argument("-f","--fiat",type=str,help="get data of a coin in alternative currency")

    args = vars(parser.parse_args())

    #### Clase para el API de CoinMarket
    Market=coinMarket()

    #Market.getCoin(coin=args["coin"],fiat=args["fiat"])
    #Market.getAllCoins(fiat=2)
    #Market.getGlobalData(fiat=args["fiat"])
    coins=["Bitcoin","Steem Dollars","Ethereum","CRIS"]
    # print(type(coins))
    Market.getListCoins(coins,fiat="")
