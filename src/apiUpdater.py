from src.config import url_template, working_dir

from datetime import datetime
from seleniumwire import webdriver
from seleniumwire.utils import decode as sw_decode
from selenium.webdriver.chrome.options import Options
import json

# Option Setting
op = Options()
op.add_argument("--mute-audio")
op.add_argument("--headless")
op.add_argument("--disable-gpu")
op.add_argument("window-size=1280x1024")
op.add_argument("--start-maximized")
# op.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
op.add_argument("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

import time
def updateAPIbymid(mid):
    api = None
    url = url_template + str(mid)
    browser = webdriver.Chrome(options=op)
    browser.get(url)
    
    try:
        button = browser.find_element_by_css_selector('div.bili-mini-close-icon')
        print("Found bili-mini-close-icon element")
        button.click()
    except:
        pass
        # print("Not found bili-mini-close-icon element")
    
    for request in browser.requests:
        if request.response:
            if 'search?' in request.url:
                api = request.url        
    
    return api

# using a for loop here is just executing in order
# todo: multi-thread support
def updateAPIs(mids: list):
    apisDict = {}
    with open(working_dir + "tmp/apisDict.tmp", "r") as fp:
        apisDict = json.load(fp)
    
    for mid in mids:  
        if mid == '':  # sanity check
            continue
        api = updateAPIbymid(mid)  # val may be None
        # so, need to be care of using apisDict
        if api is None:
            print("mid:{} got None for api".format(mid))
            for i in range(3):
                if api is None:
                    time.sleep(10)
                    print("mis:{} retry {}/3".format(mid, i+1))
                    api = updateAPIbymid(mid)
                else:
                    break
        if api:  # else keep the old value in the tmp file
            print("mid:{} updated api".format(mid))
            apisDict[mid] = api  
        else:
            print("mid:{} fails to update and keeps the old value".format(mid))
        
    datestr = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # tmpfilename = "apisDict_"+ datestr + ".tmp"
    with open(working_dir + "tmp/apisDict.tmp", "w") as fp:
        json.dump(apisDict, fp)
    
    print("updateAPIs finished at {}".format(datestr))
    return apisDict

def main():
    print("This is for module testing, please carefully uncomment.")
    # updateAPIs(mids)

if __name__ == "__main__":
    main()
