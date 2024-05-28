# This script is used for sending email manually

from user_config import emailSubject, sender_email, receiver_email
from user_config import smtp_port, smtp_server, login, password
from src.smtpSender import *
import time

# sending buffer
# clear it after sending
# vlist = [] # use pickle to persistent storage
import pickle
def writeVlistFile(vlist: list):
    with open('tmp/vlist.tmp', "wb") as f:
        pickle.dump(vlist, f)

def readVlistFile():
    vlist = None
    with open('tmp/vlist.tmp', "rb") as f:
        vlist = pickle.load(f)
    return vlist

def generateAndNotify():
    vlist = readVlistFile()
    for each in vlist:
        print(each)
    if len(vlist):
        emailMsg = generateEmailMsg(emailSubject, sender_email,
                                    receiver_email, vlist)
        for i in range(10):
            ret = notify(smtp_port, smtp_server,
                         login, password, emailMsg)
            if ret:           
                writeVlistFile([])
                break
            else:
                time.sleep(30)
                print("Retry after 30 seconds")
                continue
        # vlist = []  # clear it if success
    else:
        print("No elements in vlist.")
    
#----- Notify Manually -----
generateAndNotify()
