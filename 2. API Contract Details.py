from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from threading import Thread
import time

##-------------------------------------------------------------------------

### Create Class
class Strategy (EClient, EWrapper):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self,self)

    #Receive contract details in TWS (in thread)
    #Use EClient class to receive response
    def contractDetails(self, reqId, contractDetails):
        print(' \nReqId: ', reqId, '\nContract Details: ', contractDetails)

    def contractDetailsEnd(self, reqId):
        print(' \nReqId: ', reqId, 'Contract Details Ended')


##-------------------------------------------------------------------------

### Create Object

application = Strategy()

application.connect(host= 'localhost', port= 7497, clientId= 1)  

time.sleep(1)

#Thread
Thread(target= application.run, daemon= True).start()

print('Connection?', application.isConnected())

#Create object for contract
usd_jpy = Contract()

#forex pair: JPY.USD
usd_jpy.symbol = 'USD'
usd_jpy.currency = 'JPY'
usd_jpy.secType = 'CASH'
usd_jpy.exchange = 'IDEALPRO'

#Request Contract details
application.reqContractDetails(reqId=101, contract= usd_jpy)

time.sleep(10)

#Disconnect after completion
application.disconnect()


##-------------------------------------------------------------------------

###For other asset types

# Equity
# contract = Contract()
# contract.symbol = "MSFT"
# contract.secType = "STK"
# contract.currency = "USD"
# contract.exchange = "SMART"
# contract.primaryExchange = "ISLAND"

# Index
# contract = Contract()
# contract.symbol = 'NIFTY50'
# contract.secType = 'IND'
# contract.currency = 'INR'
# contract.exchange = 'NSE'

# Futures Contract
# contract = Contract()
# contract.symbol = 'ES'
# contract.secType = 'FUT'
# contract.currency = 'USD'
# contract.exchange = 'GLOBEX'
# contract.lastTradeDateOrContractMonth = '202101'

# Options Contract
# contract = Contract()
# contract.symbol = 'GOOG'
# contract.secType = 'OPT'
# contract.exchange = 'SMART'
# contract.currency = 'USD'
# contract.lastTradeDateOrContractMonth = '20201023'
# contract.strike = 1555
# contract.right = 'C'
# contract.multiplier = '100'