import argparse
import os
from classCoinMarket import coinMarket


if __name__=="__main__":


    #### Parser para la linea de comandos
    parser=argparse.ArgumentParser()

    parser.add_argument("-c", "--coin", type=str,
	help="search for data of a coin by name or symbol on coinMarket")

    parser.add_argument("-f","--fiat",default="",type=str,help="get data of a coin in alternative currency")

    parser.add_argument("-cl",'--coinList',nargs='+',
    help="search for data of a list of coins by name or symbol on coinMarket")

    args = vars(parser.parse_args())

    ### Clase para el API de CoinMarket
    print(args)

    if args["fiat"]!=None:

        Market=coinMarket(fiat=args["fiat"])

    else:

        Market=coinMarket()

    #Market.getCoin(coin=args["coin"],fiat=args["fiat"])
    #
    # #Market.getAllCoins(fiat=2)
    # #Market.getGlobalData(fiat=args["fiat"])
    # print(args)
    # #coins=["Bitcoin","Steem Dollars","Ethereum","CRIS"]
    # # print(type(coins))
    #print(args)
    Market.getListCoins(coins=args["coinList"],fiat=args["fiat"])
