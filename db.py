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
        host='weekataglanse.database.windows.net:1433',
        database=dbConfig["database"]
    )
    return conn.cursor()

def writeSQL(query, cursor=None):
    if cursor == None:
        cursor = getCursor()
    cursor.execute(query)
    cursor.commit()

def readSql(query, cursor=None):
    if cursor == None:
        cursor = getCursor()
    cursor.execute(query)
    return cursor.fetchall()


print(readSql("SELECT * FROM transactionEvents"))
