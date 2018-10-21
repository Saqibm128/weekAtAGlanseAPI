import pymssql
import json

config = None
with open("./Config.json", "r") as fp:
    config = json.load(fp)

dbConfig = config['sqlserverConfig']

def getCursor():
    conn = pymssql.connect(
        server=dbConfig["server"],
        port=1433,
        user=dbConfig["user"],
        password=dbConfig["password"],
        database=dbConfig["database"]
    )
    return conn.cursor(), conn

def writeSQL(query, cursor=None):
    print("writing ", query)
    if cursor == None:
        cursor, conn = getCursor()
    cursor.execute(query)
    conn.commit()

def readSQL(query, cursor=None):
    print("reading", query)
    if cursor == None:
        cursor, conn = getCursor()
    cursor.execute(query)
    return cursor.fetchall()

# writeSQL("CREATE table transactionEvents (id int auto_increment primary key, indItemId,  )")
# writeSQL("CREATE table individualTransactions (id int identity(1, 1) primary key, indItemId varchar(255), transactionTime datetime)")
# writeSQL("CREATE table categories (id int identity(1, 1) primary key, siteId varchar(255), description varchar(255))")
# writeSQL("ALTER table individualEvents add timeTransaction datetime")
# writeSQL("CREATE table entityCategoryMap (id int identity(1,1), categoryId int, entityName varchar(255), itemId int)")
# writeSQL("CREATE table sites (id siteId varchar(255), longitude float, latitude float)")
# writeSQL("CREATE table entityTransactionMap (id int identity(1,1), entityId int, transactionId int)")
# writeSQL("CREATE table individualItems (id int identity(1, 1) primary key, ncrItemId varchar(255), price float, description varchar(255))")
# writeSQL("CREATE table individualTransactions (id INT identity(1,1) PRIMARY KEY, indItemId int, dayOfWeek int, hourOfDay int, categoryId int, siteId varchar(255),  categoryUserApproved varchar(255))")
# print(readSQL("SELECT * from transactionEvents where eventId = 10"))
