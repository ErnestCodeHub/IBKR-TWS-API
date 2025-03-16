from ibapi.client import EClient
from ibapi.wrapper import EWrapper

from threading import Thread
import time

##-------------------------------------------------------------------------

class Strategy(EClient, EWrapper):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)

    #Handle position response from TWS vis Eclient
    def position(self, account, contract, position, avgCost):
        print(f'\nAccount: {account} \nContract: {contract.localSymbol}')
        print(f'Position: {position} \nAvg Cost: {avgCost}')
    
    def positionEnd(self):
        print('\nPositions Retrieved.')
    
##-------------------------------------------------------------------------

application = Strategy()

application.connect(host='localhost', port=7497, clientId=1)

time.sleep(1)

Thread(target=application.run, daemon=True).start()
print('Connected?', application.isConnected())

# Request positions from the TWS
application.reqPositions()

time.sleep(5)


application.disconnect()