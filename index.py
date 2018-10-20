from flask import Flask, request, render_template
from addict import Dict
import ncr
import db
import json
import microsoft
from statistics import variance, mean

app = Flask(__name__)

@app.route("/health")
def health():
    return "We are working!"

@app.route("/populateDB/{siteId}", methods=["POST"])
def populateDB(siteDd):
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
            db.writeSQL(query)

@app.route("/transaction/all", methods=['GET'])
def getAllTransactions():
    res = db.readSQL("SELECT * FROM individualTransactions join individualItems on individualItems.id = indItemId")
    toReturn = []
    for row in toReturn:
        toReturn.append({''})
    return json.dumps(toReturn)

@app.route("/transaction/category/autogen", methods=['POST'])
def autogenAll():
    if request.json is not None and 'ids' in request.json.keys() and len(request.json['ids']) != 0:
        ids = request.json['ids']
    else:
        ids = db.readSQL("SELECT id from individualTransactions");
        ids = [tranId[0] for tranId in ids]
    for tranId in ids:
        microsoft.generateConceptForTransaction(tranId)
    return 'completed'


@app.route("/transaction/category", methods=['POST'])
def setCategory():
    categoryId = request.json['categoryId']
    transactionId = request.json['transactionId']
    res = db.writeSQL("UPDATE individualTransactions SET categoryId = {} where id = {}".format(categoryId, transactionId))

@app.route("/category/<siteid>", methods=['GET', 'POST'])
def getCategories(siteid):
    if request.method == 'GET':
        res = db.readSQL("SELECT * FROM categories where siteid = N\'{}\'".format(siteid))
        toReturn = []
        for row in res:
            toReturn.append({'categoryId':row[0], 'siteID':row[1], 'description':row[2]})
        return json.dumps(toReturn)
    elif request.method == 'POST':
        category = request.json['category']
        res = db.writeSQL("INSERT into categories (siteId, description) values ({}, N\'{}\')".format(siteid, category))

@app.route("/transaction/stats/all", methods=["GET"])
def allTransactionData():
    siteId = request.json['siteId']
    day = request.json['day'] #0 - 6
    hour = request.json['hour'] #0 - 23
    cat = request.json['category']

    return json.dumps([{'siteId': siteId, 'category': cat, 'day': day, 'hour': hour, 'avgPrice': 10.99, 'var': 1.2, "percentProfit": 0.10}])

@app.route("/transaction/transaction_freqs", methods=["POST"])
def transactionFreqs():
    categories = ['food', 'luxury', 'transportation', 'healthcare', 'other']
    hardCodedVals = [0.4, 0.1, 0.2, 0.2, 0.1]

    siteId = request.json['siteId']
    if "day" in request.json.keys() and "hour" in request.json.keys():
        day = request.json['day'] #0 - 6
        hour = request.json['hour'] #0 - 23

        data = db.readSQL("SELECT sum(price), individualTransactions.categoryId, categories.description FROM individualTransactions \
                   join individualItems on individualItems.id = individualTransactions.indItemId \
                   join categories on categories.id = individualTransactions.categoryId \
                   where individualTransactions.siteId = N\'{}\' and dayOfWeek = {} and hourOfDay = {} group by individualTransactions.categoryId, categories.description".format(siteId, day, hour))
        toRet = Dict()
        i = 0;
        for row in data:
            toRet[i].siteId = siteId
            toRet[i].totalSales = row[0]
            toRet[i].categoryId = row[1]
            toRet[i].description = row[2]
            i += 1
        return json.dumps(toRet)
    else:
        data = db.readSQL("SELECT sum(price), individualTransactions.categoryId, categories.description FROM individualTransactions \
                   join individualItems on individualItems.id = individualTransactions.indItemId \
                   join categories on categories.id = individualTransactions.categoryId \
                   where individualTransactions.siteId = N\'{}\' group by individualTransactions.categoryId, categories.description".format(siteId))
        toRet = Dict()
        i = 0;
        for row in data:
            toRet[i].siteId = siteId
            toRet[i].totalSales = row[0]
            toRet[i].categoryId = row[1]
            toRet[i].description = row[2]
            i += 1
        return json.dumps(toRet)


@app.route("/transaction/transactionStats", methods=['POST'])
def transactionStatsData():

    day = request.json['day'] #0 - 6
    hour = request.json['hour'] #0 - 23
    cat = request.json['category']
    if 'siteId' in request.json.keys():
        siteId = request.json['siteId']
        res = db.readSQL("SELECT id, (select price from individualItems where individualItems.id=individualTransactions.indItemId) as price FROM individualTransactions where dayOfWeek = {} and hourOfDay = {} and category = N\'{}\' and siteId = N\'{}\'".format(day, hour, cat, siteId))

    else:
        siteId = None
        res = db.readSQL("SELECT id, (select price from individualItems where individualItems.id=individualTransactions.indItemId) as price FROM individualTransactions where dayOfWeek = {} and hourOfDay = {} and category = N\'{}\'".format(day, hour, cat))

    prices = []
    for row in res:
        prices.append(row[1])
    if 'siteId' in request.json.keys():
        return json.dumps({'siteId': siteId, 'category': cat, 'day': day, 'hour': hour, 'avgPrice': mean(prices), 'var': variance(prices)})
    else:
        return json.dumps({'category': cat, 'day': day, 'hour': hour, 'avgPrice': mean(prices), 'var': variance(prices)})


# @app.route("/siteEvents", methods=["GET"])
# def eventsBySiteDateRange():
#


if __name__ == "__main__":
    app.run(debug=True, port=8080, host= '0.0.0.0')
