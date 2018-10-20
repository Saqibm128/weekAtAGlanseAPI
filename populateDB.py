import ncr



siteId = "7c54465e9f5344598276ec1f941f5a3c"
transactions = ncr.getTransactionsBySite(siteId)
for transaction in transactions['pageContent']:
    tlogId = transaction['tlogId']
    print(tlogId)
    transLog = ncr.getTransactionsByDoc(tlogId)
    print(transLog)
    price = transLog['tlog']['totals']['grandAmount']['amount']
    print(price)
    for item in transLog['tlog']['items']:
        itemId = item['id']
        print(itemId)
        itemName = item['productName']
        print(itemName)
        actualAmount = item['actualAmount']['amount']
        print(actualAmount)
    var_dump(transLog)
    break
