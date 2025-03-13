"""
source link: https://interactivebrokers.github.io/tws-api/historical_bars.html
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract #Needed why dealing with any types of asset
from threading import Thread
import pandas as pd
import time
import datetime

#remove unnessary warnings if needed

import warnings
warnings.filterwarnings('ignore')

##-------------------------------------------------------------------------

class Strategy (EClient, EWrapper):
    
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self,self)
        #transform into dataframe
        self.df = pd.DataFrame(columns= ['Time', 'Open', 'Close', 'Volume'])

    #Handle incoming historical data response via Ewrapper
    def historicalData(self, reqId, bar):
        print('Req ID:', reqId)
        dictionary = {'Time': bar.date, 'Open': bar.open, 'Close': bar.close, 'Volume': bar.volume}     #So Pandas can directly interpret this dictionary structure and insert the values into the matching columns: Time, Open, Close, Volume.
        self.df = self.df.append(dictionary, ignore_index = True)
        print(f'Time: {bar.date}, Open: {bar.open}, Close: {bar.close}, Volume: {bar.volume}')
        
    #Handle Completion of Data Retrieval via Ewrapper
    def historicalDataEnd(self, reqId, start, end):
        print('\nHistorical Data Successfully Retrieved\n')
        print(self.df.head())
        current_date = datetime.datetime.now().strftime("%Y%m%d")
        filename = f"{contract.symbol}_{current_date}.csv"
        self.df.to_csv(filename, index=False)


##-------------------------------------------------------------------------

#Object
application = Strategy()

application.connect(host= 'localhost', port= 7497, clientId= 1)  

time.sleep(1)

#Thread
Thread(target= application.run, daemon= True).start()

print('Connection?', application.isConnected())


#Object for contract's historical data 
contract = Contract()
contract.symbol = 'UBS'
contract.currency = 'USD'
contract.secType = 'STK'
contract.exchange = 'SMART'
contract.primaryExchange = 'NYSE'

# Request for historical data - EClient
application.reqHistoricalData(reqId= 100,
                              contract= contract,
                              endDateTime= '20250312 23:59:59',     #The request's end date and time (the empty string indicates current present moment).
                              durationStr= '5 D',                              #The amount of time (or Valid Duration String units) to go back from the request's given end date and time
                              barSizeSetting='30 mins',                        #Time frame per bar/row
                              whatToShow= 'TRADES',                            #type of data to retrieve, for alternatives (See Historical Data Types)
                              useRTH= True,                                    # 1 = only regular trading hours (RTH)
                              formatDate= 1,                                   # The format in which the incoming bars' date should be presented
                              keepUpToDate= False,                             # Whether a subscription is made to return updates of unfinished real time bars as they are available (True)
                              chartOptions= [])

time.sleep(30)

#Only if wnat to cancel the request
#application.cancelHistoricalData(100)

#Discount
application.disconnect()

