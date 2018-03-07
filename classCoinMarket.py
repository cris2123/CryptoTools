import requests
import requests_cache
import time

from itertools import chain
from sys import exit
from userExceptions import InvalidType, NotCoinSelected, FiatInvalidType, FiatNotValid

class coinMarket:

    def __init__(self,fiat=""):

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

        requests_cache.install_cache(cache_name='coinMarket_cache', backend='sqlite', expire_after=120)

        ## funcion para obtener todos las monedas en coin market
        now = time.ctime(int(time.time()))
        self.getCoinNames(fiat)



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

    def getCoinNames(self,fiat=""):

        allData=self.getAllCoins(fiat=fiat)

        with open("currencyData.json",'w') as jsonFile:
            jsonFile.write(str(allData))

        if(allData):

            for data in allData:

                self.coinNames[data["name"]]=(data["symbol"],data["id"])

        self.wholeContent=allData

    def getAllCoins(self,fiat=""):

        currencyFiat=self._checkValidFiat(fiat)

        if(currencyFiat):

            URL="https://api.coinmarketcap.com/v1/ticker/?"+str(currencyFiat)+"&limit=0"


        else:

            URL="https://api.coinmarketcap.com/v1/ticker/?limit=0"

        try:

            now = time.ctime(int(time.time()))
            self.response=requests.get(URL)
            print ("Time: {0} / Used Cache: {1}".format(now, self.response.from_cache))

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
                    self.parseData(data[0],fiat)


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

        coinInformation=[]

        for tupleCoin in arrayValidCoins:

            if(tupleCoin[1]==True):

                for item in self.wholeContent:

                    if(item["id"]==tupleCoin[0]):

                        coinInformation.append(item)
            else:

                #coinInformation.append("coin: "+ tupleCoin[0]+" is not a valid one")
                print("coin: "+ tupleCoin[0]+" is not a valid one")

        for coin in coinInformation:

            self.parseData(coin,fiat)



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

    def parseData(self,coin,fiat=""):

        print("\n")
        print("ID: "+str(coin["id"]))
        print("Name: "+ str(coin["name"]))
        print("Symbol: " +str(coin["symbol"]))
        print("Rank: "+str(coin["rank"]))
        print("Available Supply: "+str(coin["available_supply"]))
        print("Total Supply: "+str(coin["total_supply"]))
        print("Price USD: " +str(coin["price_usd"]))
        print("Price BTC: "+str(coin["price_btc"]))
        print("Market Cap USD: "+str(coin["market_cap_usd"]))
        print("Percent Change for 1 hour : "+str(coin["percent_change_1h"]))
        print("Percent Change for 24 hour : "+str(coin["percent_change_24h"]))
        print("Percent Change for 7 days : "+str(coin["percent_change_7d"]))

        if(fiat!=""):

            price_string="price_"
            market_string="market_cap_"
            lowerFiat=fiat.lower()
            price_string=price_string+lowerFiat
            market_string=market_string+lowerFiat

            print("Price "+str(fiat)+": "+str(coin[price_string]))
            print("Market Cap "+str(fiat)+": "+str(coin[market_string]))




        print("\n")
