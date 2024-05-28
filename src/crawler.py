# -*- coding: utf-8 -*-
from src.config import headers, cookies, userAgents
from src.db import *

import random
import requests
import time
import json

def crawling(apisDict: dict, updateQueue):
    for k in apisDict:  # k is key (mid)
        apiURL = apisDict[k]
        if apiURL is not None:
            # headers['User-Agent'] = random.choice(userAgents)
            headers['Referer'] = "https://space.bilibili.com/{}/video".format(k)  # change to mid's referer
            # print(tmp_headers)
            try:
                res = requests.get(apiURL, headers=headers, cookies=cookies)
            except requests.exceptions.ConnectionError:
                print("Connection refused")
                break
            
            if res.status_code == 200:
                json_data = res.json()  # get json data from APIURL
                   
                try:
                    videos = json_data['data']['list']['vlist']
                    for each in videos:
                        new_post = Post(mid=each['mid'],
                            bvid=each['bvid'],
                            created=each['created'],
                            title=each['title'],
                            pic=each['pic'],
                            length=each['length'],
                            play=each['play'])
                        
                        # print(new_post)
                        if not isPostExisted(new_post):
                            updateQueue.append(new_post)
                        else:
                            pass
                            # print("Existed post: ", new_post)

                except:
                    print("failed with wrong json_data: ", json_data)
                interval = (random.random()+2)*5
                print("mid={} finished, let's wait for {} seconds".format(k, interval))
                time.sleep(interval)  # sleep for a random time (10 ~ 15)
            # except:
            #     print('Exceptions in request.get(), to sleep for longer or change headers') 
        else:  # apiURL is None
            print("mid = {}, apiURL is None".format(k))
    return updateQueue

def main():
    apisDict = None
    with open("apisDict.tmp", "r") as f:
        apisDict = json.load(f)
    # print(apisDict)
    updateQueue = []
    updateQueue = crawling(apisDict, updateQueue)
    return updateQueue

if __name__ == '__main__':
    updateQueue = main()
    print(len(updateQueue))  # test done.

