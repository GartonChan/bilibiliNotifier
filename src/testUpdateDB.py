# -*- coding: utf-8 -*-

import json
from config import headers, cookies, userAgents
from db import *
import random
from crawler import crawling

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
    addUpdatePosts(updateQueue)
