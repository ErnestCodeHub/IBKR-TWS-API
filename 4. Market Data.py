"""
The tick data from IBKR is not actually tick by tick in real time, but a snapshot of the tick data of the past few seconds.

In addition, the real time tick data is only available when the market is live

source link: https://interactivebrokers.github.io/tws-api/md_request.html

#Output ticks from the TWS
    1 : Bid Price
    2 : Ask Price
    6 : Day's High Price
    7 : Day's Low Price
    9 : Yesterday's Close Price
"""
        

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from threading import Thread
import time

##-------------------------------------------------------------------------

class Strategy (EClient,EWrapper):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self,self)

    #Handle tick data from TWS via Ewrapper
    def tickPrice(self, reqId, tickType, price, attrib):
        cTime = time.strftime("%H:%M:%S", time.localtime())
        print(f'ID: {reqId}, Time: {cTime}, TickType: {tickType}, Price: {price}')


##-------------------------------------------------------------------------

#Object
application = Strategy()

application.connect(host= 'localhost', port= 7497, clientId= 1)

time.sleep(1)

Thread(target=application.run, daemon= True).start()

print('Connection', application.isConnected())

#Object for Contract
contract = Contract()
contract.symbol = 'EUR'
contract.currency = 'USD'
contract.secType = 'CASH'
contract.exchange = 'IDEALPRO'


#Request market data from TWS
application.reqMktData(reqId= 100,
                       contract= contract,
                       genericTickList= '',
                       snapshot=False,
                       regulatorySnapshot=False,
                       mktDataOptions=[])

time.sleep(10)

#Send request to cancel market data
#application.cancelMktData(reqId= 100)

application.disconnect()
