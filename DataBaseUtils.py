import logging
import sqlite3
from datetime import datetime, timedelta, date, timezone

sql_create_scrap_data = """CREATE TABLE IF NOT EXISTS ScrapData (
                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   url text NOT NULL UNIQUE  ,
                                   description text,
                                   expert_estimate varchar(10),
                                   current_bid varchar(10),
                                   winning_bid varchar(10),
                                   image_location varchar(100),
                                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,
                                   updated_at DATETIME DEFAULT CURRENT_TIMESTAMP  
                                   
                               );"""

def createTable(sql_create_scrap_data, conn):
    try:
        c = conn.cursor()
        c.execute(sql_create_scrap_data)
        c.close()
        conn.commit()
    except sqlite3.Error as e:
        print(e)



def createConnection(dbName):
    db_file = r"databases/categories/{}.db".format(dbName)
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        #logging.info(conn)
    except sqlite3.Error as e:
        print(e)
    return conn


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
        conn = createConnection(category)
        createTable(sql_create_scrap_data, conn)
        #print(sdata)

        #check if the row exists already. if not , create a row.
        selectRow =''' select id from ScrapData where url =? '''
        cur = conn.cursor()
        cur.execute(selectRow,(sdata.url,))
        records = cur.fetchall()
        if(len(records)>0): # record already exists so,
            pass
        else:

            insertRow = ''' insert into ScrapData(url, description,expert_estimate, current_bid, winning_bid, image_location , updated_at ) values(?,?,?,?,?,?,?) '''
            cur = conn.cursor()
            cur.execute(insertRow,(sdata.url, sdata.description, sdata.expert_estimate,sdata.current_bid, sdata.winning_bid, sdata.image_location, str(datetime.now())))
            cur.close()

    except sqlite3.Error as e:
        print(e)
    finally:
        conn.commit()
        conn.close()


def update(category, sdata):
    try:
        conn = createConnection(category)
        createTable(sql_create_scrap_data, conn)
        #print(sdata)

        #check if the row exists already. if not , create a row.
        selectRow =''' select id, winning_bid from ScrapData where url =? '''
        cur = conn.cursor()
        cur.execute(selectRow,(sdata.url,))
        records = cur.fetchall()
        if(len(records)>0): # record already exists so,
            id = records[0][0]
            winning_bid = records[0][1]
            if winning_bid is None or len(winning_bid.strip()) == 0:
                updateRow = ''' update ScrapData set winning_bid=?, image_location=? where id=?'''
                cur = conn.cursor()
                cur.execute(updateRow,(sdata.winning_bid, sdata.image_location, id))
                cur.close()
        else:
            pass

    except sqlite3.Error as e:
        print(e)
    finally:
        conn.commit()
        conn.close()