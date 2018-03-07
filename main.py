#!/usr/bin/python
import argparse
import os
from classCoinMarket import coinMarket



# determine platform-specific user cache directory


if __name__=="__main__":


    #### Parser para la linea de comandos
    parser=argparse.ArgumentParser()

    parser.add_argument("-c", "--coin", type=str,
	help="search for data of a coin by name or symbol on coinMarket")

    parser.add_argument("-f","--fiat",default="",type=str,help="get data of a coin in alternative currency")

    parser.add_argument("-cl",'--coinList',nargs='+',
    help="search for data of a list of coins by name or symbol on coinMarket")

    parser.add_argument("-w",'--website',default="coinMarket",type=str,
    help="select a website to parse or use api calls (for now only coin market)")

    parser.add_argument("-g","--globalData",default=False,help="Get global cryptocurrency market data")

    args = vars(parser.parse_args())

    ### Clase para el API de CoinMarket

    Market=coinMarket(fiat=args["fiat"])

    if(args["globalData"]!=False):
        Market.getGlobalData(fiat=args["fiat"])

    if args["coin"]!=None and args["coinList"]!=None:

        if(args["coin"] not in args["coinList"]):
            args["coinList"].append(args["coin"])

        Market.getListCoins(coins=args["coinList"],fiat=args["fiat"])

    elif(args["coin"]!=None and args["coinList"]==None):

        Market.getCoin(coin=args["coin"],fiat=args["fiat"])

    elif(args["coin"]==None and args["coinList"]!=None):

        Market.getListCoins(coins=args["coinList"],fiat=args["fiat"])
