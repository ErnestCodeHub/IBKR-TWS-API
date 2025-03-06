#Import Library
from ibapi.client import EClient    #to make request
from ibapi.wrapper import EWrapper  # to handle response

from threading import Thread    #to establish additional communication channel
import time
from datetime import datetime

##-------------------------------------------------------------------------

###Define Strategy Class (child class) - inherit from  Eclient and Ewrapper
class Strategy(EClient, EWrapper):

    #initialize both the parent class and inherited classes
    def __init__(self):
        EWrapper.__init__(self)  # Initialize EWrapper part of this class
        EClient.__init__(self, self)  # first self for Eclient, second self for Ewrapper

    #callback method from "Ewrapper class" to handle response
    def currentTime(self, time):
        t = datetime.fromtimestamp(time)    #change time to human readable format
        print('Current time on server:', t)
    

##-------------------------------------------------------------------------

###Create object for the strategy class
application = Strategy()

#Connect method from EClient 
application.connect(host= 'localhost', port= 7497, clientId= 1)     #client ID => used as an identifier for myself (different python file)

time.sleep(1)

###Start a seperate thread intended to receive all response (to handle response)
Thread(target= application.run, daemon= True).start()       # "application.run" => use this method to fetch all the response from TWS
                                                            # "daemon = True" => when application.connect is ended, the thread communication channel will also be ended 

print('\nApplication connected to IB TWS:', application.isConnected())   #check connectivity

###Send a request to TWS and use currenttime (call back method from EWrapper Class) to handle the response 
application.reqCurrentTime()

time.sleep(1)

application.disconnect()


