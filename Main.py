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
    pageResult = driver.find_element_by_class_name("PagerResults").text
    pageSizeInfo = re.findall("\s\d-\d+\s", pageResult)[0].strip()
    print("page size info {0}".format(pageSizeInfo))
    pageSize = pageSizeInfo.split("-")  # 1-25  --> 25
    pageSize = int(pageSize[1])

    totalRecords = int(re.findall("of\s(\d+)", pageResult)[0].strip())
    print("totalRecords {0}".format(totalRecords))

    numOfPages = int(totalRecords / pageSize)
    if (totalRecords % pageSize != 0):
        numOfPages += 1
    time.sleep(0.2)
    queryURL = "https://www.seca.ch/Membership/Members.aspx?page={0}"
    allRows = list()
    for pageNum in range(1, 1 + 1):
        print("page number is{0}".format(pageNum))
        driver.get(queryURL.format(pageNum))
        time.sleep(0.2)
        items = driver.find_elements_by_class_name("default_list_member_item")
        pageLinks = list(map(lambda x: x.find_element_by_tag_name("a").get_attribute("href"), items))
        for eachPageLink in pageLinks:
            driver.get(eachPageLink)
            time.sleep(0.2)
            eachRowDict = OrderedDict()
            eachRowDict['Name'] = driver.find_elements_by_xpath("//div[@class='content_middle']/h1/p")[0].text
            eachRowDict['Street'] = \
            driver.find_elements_by_xpath("//div[@class='content_left']/div[@class='tabs']//table//td")[0].text.split(
                "\n")[0]
            allRows.append(eachRowDict)

    print(pageResultDiv)




if __name__ == "__main__":
    main(sys.argv[1:])
