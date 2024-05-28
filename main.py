from user_config import mids
from user_config import emailSubject, sender_email, receiver_email
from user_config import smtp_port, smtp_server, login, password

from src.crawler import crawling
from src.smtpSender import *
from src.db import *
from src.apiUpdater import updateAPIs

import time, json
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

# vlist is the sending buffer
# use pickle to persistent storage, clear it after sending.
import pickle
def writeVlistFile(vlist: list):
    with open("tmp/vlist.tmp", "wb") as f:
        pickle.dump(vlist, f)

def readVlistFile():
    vlist = None
    with open("tmp/vlist.tmp", "rb") as f:
        vlist = pickle.load(f)
    return vlist

def appendVlistFile(vlist: list):
    curVlist= readVlistFile()
    curVlist.extend(vlist)
    writeVlistFile(curVlist)
    return True

def getDatetimeStr():
    return (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
def checkUpdates():  # output into vlist from updateQueue
    print(getDatetimeStr())
    apisDict = None
    with open("tmp/apisDict.tmp", "r") as f:
        apisDict = json.load(f)
    # print(apisDict)
    
    updateQueue = []
    updateQueue = crawling(apisDict, updateQueue)
    print("len of updateQueue = ", len(updateQueue))
    
    if len(updateQueue):
        vlist = []  # cached ones means not sent yet
        for each in updateQueue:
            tmp = {
                "mid": each.mid,
                "bvid": each.bvid,
                "created": each.created,
                "title": each.title,
                "pic": each.pic,
                "length": each.length,
                "play": each.play,
            }
            vlist.append(tmp)
            
        if appendVlistFile(vlist):
            addUpdatePosts(updateQueue)
        print("Updated to post.db and vlist.tmp. Num of update = ", len(updateQueue))
    else:
        print("No posts update today")

def generateAndNotify():
    vlist = readVlistFile()
    if len(vlist):
        emailMsg = generateEmailMsg(emailSubject, sender_email,
                                    receiver_email, vlist)
        for i in range(30):
            ret = notify(smtp_port, smtp_server,
                         login, password, emailMsg)
            if ret:           
                writeVlistFile([])
                break
            else:
                print("Retry after 30 seconds ...")
                time.sleep(30)
                continue
        # vlist = []  # clear it if success
    else:
        print("No elements in vlist.")
    
if __name__ == '__main__':
    print("Bilibili Notifier Service is Running...")
    # checkAndNotify()  # debugging
    # BlockingScheduler
    scheduler = BlockingScheduler()
    # scheduler.add_job(checkAndNotify, 'cron', day_of_week='0-6', hour=12, minute=00)
    scheduler.add_job(checkUpdates, 'cron', day_of_week='0-6', hour=18, minute=45)
    scheduler.add_job(generateAndNotify, 'cron', day_of_week='0-6', hour=19, minute=00)

    scheduler.add_job(updateAPIs, 'cron', day_of_week='1,3,5', hour=18, minute=00, args=[mids])
    print("Scheduler Start, please check settings of jobs")
    scheduler.start()
