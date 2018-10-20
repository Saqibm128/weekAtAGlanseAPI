import ncr
import db
import re
from datetime import datetime
import microsoft



siteIds = ["7c54465e9f5344598276ec1f941f5a3c"]
for siteId in siteIds:
    # siteData = ncr.getSiteById(siteId)
    # siteLong = siteData['coordinates']['longitude']
    # siteLat = siteData['coordinates']['latitude']
    # db.writeSQL("insert into sites values (N\'{}\', {}, {})".format(siteId, siteLong, siteLat))
    transactions = ncr.getTransactionsBySite(siteId)
    for transaction in transactions['pageContent']:
        tlogId = transaction['tlogId']
        transLog = ncr.getTransactionsByDoc(tlogId)
        price = transLog['tlog']['totals']['grandAmount']['amount']
        for item in transLog['tlog']['items']:
            itemId = item['id']
            itemName = item['productName']
            itemName = re.sub('\'', '',itemName)
            actualAmount = item['actualAmount']['amount']
            print("SELECT * from individualItems where ncrItemId = N\'{}\' and price = {}".format(itemId, actualAmount))
            possibleMatch =  db.readSQL("SELECT id from individualItems where ncrItemId = N\'{}\' and price = {}".format(itemId, actualAmount))
            if (len(possibleMatch) == 0):
                print("INSERT into \"dbo\".\"individualItems\" (ncrItemId, price, description) values (N\'{}\', {}, N\"{}\")".format(itemId, actualAmount, itemName))
                db.writeSQL("INSERT into \"dbo\".\"individualItems\" (ncrItemId, price, description) values (N\'{}\', {}, N\'{}\')".format(itemId, actualAmount, itemName))
                possibleMatch =  db.readSQL("SELECT id from individualItems where ncrItemId = N\'{}\' and price = {}".format(itemId, actualAmount))
            transactionTime = transaction['endTransactionDateTimeUtc']
            utc_time = datetime.strptime(transactionTime, "%Y-%m-%dT%H:%M:%SZ")
            query = "INSERT into \"dbo\".\"individualTransactions\" (indItemId, dayOfWeek, hourOfDay, siteId) values ({}, {}, {}, N\'{}\' )".format(possibleMatch[0][0], utc_time.weekday(), utc_time.hour, siteId)
            print(query)
            db.writeSQL(query)
#

ids = db.readSQL("SELECT id from individualTransactions");
ids = [tranId[0] for tranId in ids]
for tranId in ids:
    microsoft.generateConceptForTransaction(tranId)
