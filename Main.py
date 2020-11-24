import sys
# python dependencies
# these dont need any installation
# os is used for doing directory operations
import os
# sys is used for retrieving arguments from the terminal
import sys
# time is used for making the script pause and wait
import time
# string is used for string operations
import string
# TODO argparse is used for retrieving arguments from the terminal
import argparse
# pip install urllib3
import urllib.request
# pip install selenium
from collections import OrderedDict

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import re
import xlwt
from xlwt import Workbook

# pip install Pillow
import PIL.Image

import DataBaseUtils
from ScrapData import ScrapData





def main(args):
    print("great {0}".format(args))
    #queryURL = args[0]
    queryURL = "https://www.catawiki.com/c/437-whisky"
    #queryURL = "https://www.catawiki.com/c/437-whisky/927-area/107557-western-highlands/"
    # open a new google chrome window
    driver = webdriver.Chrome()

    driver.set_window_size(1200, 800)

    driver.get(queryURL)

    # wait for loading
    time.sleep(1.0)

    # find div with page related classes
    driver.find_element_by_id("cookie_bar_agree_button").click()
    time.sleep(2.0)
    allArticleUrls = []

    pageUrl = None
    lastPageNum =None

    def actionForEachArticle(allArticleUrls, category):
        allArticles = []
        for i in range(len(allArticleUrls)):
            url = allArticleUrls[i]
            driver.get(url)
            time.sleep(0.2)
            sdata = ScrapData()
            sdata.url = url
            sdata.description = driver.find_element_by_class_name("c-page__heading").text
            expertsEstimate = driver.find_elements_by_xpath("//div//*[contains(text(),'s estimate')]")
            if expertsEstimate:
                sdata.expert_estimate = expertsEstimate[0].text.split('estimate')[1].strip()

            currentBid = driver.find_elements_by_xpath("//div//*[contains(text(),'Current bid')]")
            if currentBid:
                sdata.current_bid =  currentBid[0].text.replace("Current bid ","")

            picture = driver.find_elements_by_xpath("//div[@class='be-lot-image-gallery__image']/img")[0].get_attribute("src")

            winningBid = driver.find_elements_by_xpath("//div[@class='lot-closed-banner__lot-winning-bid']")
            if winningBid:
                sdata.winning_bid = winningBid[0].text.replace("Winning Bid: ")

            folderName = "databases/categories/images"
            if not os.path.exists(folderName):
                # create the folder
                os.makedirs(folderName)

            # change diretory
            os.chdir(folderName)
            pictureExt = sdata.picture.split(".")[-1]
            sdata.image_path = "{0}.{1}".format(i+1,pictureExt)
            urllib.request.urlretrieve(sdata.picture, sdata.image_path)
            DataBaseUtils.update(sdata)






    actionForEachArticle(['https://www.catawiki.com/l/42536249-jack-daniel-s-maxwell-house-original-bottling-b-1990s-150cl'],'whisky')

    def eachPageAction(url):
        driver.get(url)
        time.sleep(0.2)
        articleThumbNails = driver.find_elements_by_xpath("//div//article[@class='c-lot-card__container']/a")
        articleUrls = map(lambda  x:x.get_attribute("href"),articleThumbNails)
        allArticleUrls.extend(articleUrls)



    try:
        pageResultDiv = driver.find_element_by_class_name("pages")
        lastPage = pageResultDiv.find_elements_by_tag_name("a")[-1]
        lastPageNum = lastPage.text
        lastPageUrl = str(lastPage.get_attribute("href"))

        pageNum = lastPageUrl.rfind(lastPageNum)
        pageUrl = lastPageUrl[0:pageNum]
        lastPageNum=int(lastPageNum)
        for i in range(1,lastPageNum+1):
            eachPageUrl = pageUrl+str(i)
            eachPageAction(eachPageUrl)



    except NoSuchElementException as e:
        print(e)
        eachPageAction(queryURL)












    # find div with pageresults   #Displaying results 1-25 (of 546)





if __name__ == "__main__":
    main(sys.argv[1:])
