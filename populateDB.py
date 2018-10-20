import ncr
import db
import re
from datetime import datetime



siteId = "7c54465e9f5344598276ec1f941f5a3c"
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
        epoch_time = (utc_time - datetime(1970, 1, 1)).total_seconds()
        print(epoch_time)
        query = "INSERT into \"dbo\".\"individualTransactions\" (indItemId, transactionTime, siteId) values ({}, dateadd(S, {}, '1970-01-01'), N\'{}\' )".format(possibleMatch[0][0], epoch_time, siteId)
        print(query)
        db.writeSQL(query)
