from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.order_cancel import OrderCancel
from threading import Thread,Timer  #Timer is added to cancel Order if needed after place order
import time

##-------------------------------------------------------------------------

class Strategy (EClient, EWrapper):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self,self)

    #Handle reponse from TWS via Ewrapper
    def openOrder(self, orderId, contract, order, orderState):
        print(f'n\Order open for {contract} with orderid {orderId}')

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print(f'n\Order Status for OrderID: {orderId}, Status: {status}, Filled: {filled}, AverageFilledPrice: {avgFillPrice}')

    def execDetails(self, reqId, contract, execution):
        """
        Receive datailed when the orders are executed (partial or complete)
        """
        print(f'n\Order Executed:', execution.orderId)

##-------------------------------------------------------------------------

#object
application = Strategy()

application.connect(host= 'localhost', port= 7497, clientId= 5)

time.sleep(1)

Thread(target=application.run,daemon= True).start()

print('Connected?', application.isConnected())

#Define Order ID, which is different from request ID
OID = 35

#Object for Contract
contract = Contract()
contract.symbol = 'EUR'
contract.currency = 'USD'
contract.secType = 'CASH'
contract.exchange = 'IDEALPRO'

#Object for order
order = Order()
order.action = 'BUY'
order.totalQuantity = 10000
order.orderType = 'MKT'

#for limit order
#order.lmtPrice = '1.5000'

#Request function via Eclient method
application.placeOrder(orderId= OID,
                       contract= contract,
                       order= order)

time.sleep(5)

#Cancel order after 15 seconds if order is not executed
Timer(15, application.cancelOrder, [OID, OrderCancel()]).start()

time.sleep(25)

application.disconnect()

