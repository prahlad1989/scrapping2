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
        print(conn)
    except sqlite3.Error as e:
        print(e)
    return conn


if __name__ == "__main__":
    try:
        conn = createConnection("goodCat")
        createTable(sql_create_scrap_data, conn)
        insertRowStmt = """ insert into ScrapData(url, description,expert_estimate, current_bid, winning_bid, image_location , updated_at ) values('ddddd', 'descirtpion1', '100', '{0}') """.format(str(datetime.now()))
        c= conn.cursor()
        c.execute(insertRowStmt)
        c.close()
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(e)

def update(category, sdata):
    conn = createConnection(category)
    createTable(sql_create_scrap_data, conn)
    #check if the row exists already. if not , create a row.
    insertRowStmt = """ insert into ScrapData(url, description, expert_estimate , updated_at ) values('ddddd', 'descirtpion1', '100', '{0}') """.format(
        str(datetime.now()))