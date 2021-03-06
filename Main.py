import sys
# python dependencies
# these dont need any installation
import logging

root = logging.getLogger()
logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s %(name)s - %(levelname)s - %(message)s  (line %(lineno)s) ', level=logging.INFO)
root.addHandler(logging.StreamHandler(sys.stdout))


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
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import DataBaseUtils



wineCategories = ["443-wine"]

def main(args):
    queryURL = args[0]
    #queryURL = "https://www.catawiki.com/c/873-automobilia-motobilia"
    #queryURL = "https://www.catawiki.com/c/437-whisky/927-area/107557-western-highlands/"
    # open a new google chrome window
    update_only = False
    if len(args)>1 and args[1] and args[1]=='update':
        update_only = True
    driver = webdriver.Chrome()
    driver.set_window_size(1200, 800)

    driver.get(queryURL)
    logging.info("url to scrap {0}".format(queryURL))

    # wait for loading
    time.sleep(0.2)

    # find div with page related classes
    driver.find_element_by_id("cookie_bar_agree_button").click()
    time.sleep(0.2)
    allArticleUrls = []

    pageUrl = None
    lastPageNum =None
    category = queryURL.split("/")[-1]

    def actionForEachArticle(allArticleUrlsTemp, category):
        allArticles = []
        for i in range(len(allArticleUrlsTemp)):# coz numbering the image with i+1 .
            try:
                url = allArticleUrlsTemp[i]
                logging.info("for article {0}".format(url))
                driver.get(url)
                time.sleep(0.2)
                sdata = dict()
                sdata['url'] = url
                sdata['description'] = driver.find_element_by_class_name("c-page__heading").text
                expertsEstimate = driver.find_elements_by_xpath("//div//*[contains(text(),'s estimate')]")
                if expertsEstimate:
                    sdata['expert_estimate'] = expertsEstimate[0].text.split('estimate')[1].strip()

                currentBid = driver.find_elements_by_xpath("//div[@class='be-lot-current-bid']//div//*[contains(text(),'Current bid')]")
                if currentBid:
                    sdata['current_bid'] =  currentBid[0].text.replace("Current bid ","")

                picture = driver.find_elements_by_xpath("//div[@class='be-lot-image-gallery__image']/img")[0].get_attribute("src")

                winningBid = driver.find_elements_by_xpath("//div[@class='lot-closed-banner__lot-winning-bid']")
                if winningBid:
                    sdata['winning_bid'] = winningBid[0].text.replace("Winning Bid:","")

                folderName = "databases/categories/{0}/images".format(category)

                if category in wineCategories:
                    #lotDetailsButton = driver.find_elements_by_xpath("//button[@class='be-accordion__button' ]")[0].click()
                    for x in driver.find_elements_by_xpath("//section[@id='specifications']//button[@class='be-accordion__button' ]"):
                        child = x.find_elements_by_xpath("./child::*")[0]
                        if child.get_attribute("class") == 'be-accordion__header':
                            x.click()
                            time.sleep(5)

                    for x in  driver.find_elements_by_xpath("//div[@class ='be-lot-specification']"):
                        children = x.find_elements_by_xpath("./child::*")
                        sdata["{0}".format(children[0].text)] = children[1].text
                        #logging.info(sdata[children[0].text])

                if not os.path.exists(folderName):
                    # create the folder
                    os.makedirs(folderName)

                pictureExt = picture.split(".")[-1]
                pictureName = url.split("/")[-1]
                sdata['image_location'] = folderName+"/{0}.{1}".format(pictureName,pictureExt)
                urllib.request.urlretrieve(picture, sdata['image_location'])
                if update_only:
                    DataBaseUtils.update(category,sdata)
                else:
                    DataBaseUtils.create(category, sdata)
            except Exception as e:
                logging.info("error happending while processing an article url {0}".format(allArticleUrlsTemp[i]))
                logging.error(e)

#testing
    #actionForEachArticle([ 'https://www.catawiki.com/l/43028841-2019-grattamacco-rosso-bolgheri-6-bottles-0-75l'], "443-wine")

    def eachPageAction(url):
        driver.get(url)
        time.sleep(0.2)
        articleThumbNails = driver.find_elements_by_xpath("//div//article[@class='c-lot-card__container']/a")
        articleUrls = list(map(lambda  x:x.get_attribute("href"),articleThumbNails))
        #logging.info("article ursl of page{0}".format(articleUrls))
        return articleUrls
    #
    if update_only:
        allArticleUrls = DataBaseUtils.fetchUrls(category)
        if not allArticleUrls:
            logging.info("no existing urls found")
    else:
        try:
            pageResultDiv = driver.find_element_by_class_name("pages")
            lastPage = pageResultDiv.find_elements_by_tag_name("a")[-1]
            lastPageNum = lastPage.text
            lastPageUrl = str(lastPage.get_attribute("href"))

            pageNum = lastPageUrl.rfind(lastPageNum)
            pageUrl = lastPageUrl[0:pageNum]  # truncate page number part so taht it can be used repeatitively
            lastPageNum=int(lastPageNum)
            #testing
            #lastPageNum=2 #testing.

            for i in range(1,lastPageNum+1):
                eachPageUrl = pageUrl+str(i)
                logging.info("page number {0}".format(i))
                articleUrls = eachPageAction(eachPageUrl)
                allArticleUrls.extend(articleUrls)

        except NoSuchElementException as e:
            logging.error(e)
            articleUrls = eachPageAction(queryURL)
            allArticleUrls.extend(articleUrls)
    logging.info(" before removing duplicates length {0}".format(len(allArticleUrls)))
    allArticleUrls=list(set(allArticleUrls))
    logging.info(" after removing duplicates length {0}".format(len(allArticleUrls)))
    actionForEachArticle(allArticleUrls, category)
    driver.close()

if __name__ == "__main__":
    main(sys.argv[1:])
