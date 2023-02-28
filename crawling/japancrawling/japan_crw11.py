#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#google 고화질 크롤링

from selenium import webdriver
import time
import selenium
from selenium.webdriver.common.keys import Keys
import urllib.request
import time
import cv2
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import numpy as np
from urllib.request import Request, urlopen
from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote_plus
import os
import json
import re
from rmv import rmv

def url_to_image(url, readFlag=cv2.IMREAD_COLOR):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
#     resp = urllib.request.urlopen(url)


    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    try:
        req = urllib.request.Request(url, headers=hdr)
    except:
        return "false"
    try:
        page = urlopen(req)
    except:
        return "false"
#     try:
#         page = urlopen(req)
#     except:
#         print("error")
    try:
        content = page.read()
    except:
        return "false"
    
    try:
        image = np.asarray(bytearray(content), dtype="uint8")
    #     image = np.asarray(bytearray(urlopen(resp).read), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return image
    except:
        return "false"

def gglcrawling(driver,gender,age,page):
    #gender
    #0 : male 1 : female
    
    #age : 0~7
    if gender == 0:
        male = "male"
    else:
        male = "female"
        
    pageurl = "https://cloudcasting.jp/client/home/search?minAge="+str(age*10)+"&maxAge="+str(age*10+9)+"&gender="+male+"&search=1&sortColumn=priority&order=desc&number="+str(page)
    driver.get(pageurl)
    time.sleep(2)
    
    if driver.current_url != pageurl:
        return 0

    pageString = driver.page_source
    bsObj = BeautifulSoup(pageString, "lxml")
                                                    
    imglist = driver.find_elements(by=By.XPATH, value='''/html/body/div[2]/div[3]/div[2]/ul[2]/li/div[2]/a''')

    urllist = []
    for img in imglist:
        urllist.append(img.get_attribute('href'))

    for url in urllist:
        url = url+'/photo'
        
        driver.get(url)
        time.sleep(1)
        
        #name 일본어
        name = driver.find_element(by=By.XPATH, value="""//*[@id="side_profile"]/div/div[1]/h1""").text

        imgs = driver.find_elements(by=By.XPATH, value="""/html/body/div[2]/div[1]/div[1]/div[2]/div[1]/div/ul/li/a/img""")
        
        name = name.replace(' ','_',1)
        name = name.replace('　','_',1)
        name = name.replace(' ','')
        name = name.replace('　','')
        try: 
            os.mkdir('/data/notebook/Japancrw/img/'+name)
        except:
            continue
#             os.mkdir('/data/notebook/Japancrw/img/'+name+'1')
#             name = name+'1'
#             print(name)

        picnum=0

        for img in imgs:
            img = img.get_attribute('src')
            
            if img == "null" or 'gif' in img:
                rmv('/data/notebook/Japancrw/img/'+name)
                break
            
            image = url_to_image(img)
            
            if image != "false":
                try:
                    cv2.imwrite('/data/notebook/Japancrw/img/'+name+'/'+str(picnum)+'.jpg',image)
                    picnum+=1
                except:
                    pass
            else:
                print(image)
        if gender == 0:
            sex = "male"
        else:
            sex = "female"
        data = {
                    'name' : name,
                    'age' : str(age*10)+'-'+str(age*10+10),
                    'gender' : sex
                }
        try:
            with open('/data/notebook/Japancrw/img/'+name+'/'+name+'.json', 'w') as f:
                 f.write(json.dumps(data))
        except:
            pass
    driver.close()
    