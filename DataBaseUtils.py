import logging
import pymongo
import Main


def createConnection(dbName):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = myclient[dbName]
    return db

# if __name__ == "__main__":
#     try:
#         conn = createConnection("goodCat")
#         createTable(sql_create_scrap_data, conn)
#         insertRow = "insert into ScrapData(url,description) values({0},{1})".format('abcde','efgh')
#         insertRow=''' INSERT INTO ScrapData(url,description)
#                       VALUES(?,?) '''
#         insertRow = ''' insert into ScrapData(url, description,expert_estimate, current_bid, winning_bid, image_location , updated_at ) values(?,?,?,?,?,?,?) '''
#         c= conn.cursor()
#         c.execute(insertRow,('accxxc','sdddd','2','3','3',None,datetime.now()))
#         c.close()
#         conn.commit()
#         conn.close()
#     except sqlite3.Error as e:
#         print(e)

def create(category, sdata):
    try:
        db = createConnection(category)
        collection = db["ScrapData"]
        collection.create_index([("url",pymongo.TEXT)],unique=True)
        collection.insert_one(sdata)
    except Exception as e:
        logging.error(e)
    finally:
        pass

def fetchUrls(category):
    db = createConnection(category)
    collection = db["ScrapData"]
    query = {"winning_bid": None}
    docs = collection.find(query,{"url":1})
    docs = list(map(lambda x:x['url'],docs))
    return docs


def update(category, sdata):
    try:
        db = createConnection(category)
        collection = db["ScrapData"]
        if "winning_bid" in sdata:
            collection.update_one({"url":sdata['url']},{"$set":{"winning_bid": sdata["winning_bid"]}})
            logging.info("winnig bid updated")
        else:
            logging.info("winnig bid Not updated")

    except Exception as e:
        logging.error(e)
    finally:
        pass