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

@app.route("/transaction/byIds", methods=['GET'])
def getTransactionsByIds():
    args = request.args.to_dict()
    print(args)
    min = args['startId']
    max = args['endId']
    res = db.readSQL("SELECT individualTransactions.id as id, individualTransactions.dayOfWeek as day, individualTransactions.hourOfDay as hour, \
                     individualItems.price as price, description as description, individualTransactions.siteId as siteId\
                     FROM individualTransactions join individualItems on individualItems.id = indItemId where individualTransactions.id >= {} and individualTransactions.id <= {}".format(min, max))
    toReturn = []
    for row in res:
        toReturn.append({'id': row[0], 'day':row[1], 'hour': row[2], 'price': row[3], 'description': row[4], 'siteId': row[5]})
    return json.dumps(toReturn)

@app.route("/transaction/category/autogen/all", methods=['POST'])
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

@app.route("/category", methods=["POST"])
def createCategory():
    siteId = request.json['siteId']
    categoryName = request.json['category']
    db.writeSQL("insert into categories (siteId, description) values (N\'{}\', N\'{}\')".format(siteId, categoryName))
    return json.dumps({"status": "success"})

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

@app.route("/transaction/stats/all", methods=["POST"])
def allTransactionData():
    if "day" in request.json.keys() and "hour" in request.json.keys():
        day = request.json['day'] #0 - 6
        hour = request.json['hour'] #0 - 23
        data = db.readSQL("SELECT sum(price), individualTransactions.categoryId, categories.description, longitude, latitude, individualTransactions.siteId FROM individualTransactions \
               join individualItems on individualItems.id = individualTransactions.indItemId \
               join categories on categories.id = individualTransactions.categoryId \
               join sites on individualTransactions.siteId = sites.id \
               where dayOfWeek = {} and hourOfDay = {} \
               group by individualTransactions.siteId, individualTransactions.categoryId, categories.description, longitude, latitude".format(day, hour))
    else:
        data = db.readSQL("SELECT sum(price), individualTransactions.categoryId, categories.description, longitude, latitude, individualTransactions.siteId FROM individualTransactions \
               join individualItems on individualItems.id = individualTransactions.indItemId \
               join categories on categories.id = individualTransactions.categoryId \
               join sites on individualTransactions.siteId = sites.id \
               group by individualTransactions.siteId, individualTransactions.categoryId, categories.description, longitude, latitude")
    toRet = Dict()
    i = 0;
    sumPricesBySiteId = Dict()
    for row in data:
        toRet[i].siteId = row[5]
        toRet[i].totalSales = row[0]
        toRet[i].categoryId = row[1]
        toRet[i].description = row[2]
        toRet[i].longitude = row[3]
        toRet[i].latitude = row[4]
        i += 1
        if row[5] in sumPricesBySiteId.keys():
            sumPricesBySiteId[row[5]] += row[0]
        else:
            sumPricesBySiteId[row[5]] = row[0]
    for j in range(i):
        toRet[j].proportionOfSiteSales = toRet[j].totalSales / sumPricesBySiteId[toRet[j].siteId]
    return json.dumps(toRet)

@app.route("/transaction/transaction_freqs", methods=["POST"])
def transactionFreqs():
    siteId = request.json['siteId']
    if "day" in request.json.keys() and "hour" in request.json.keys():
        day = request.json['day'] #0 - 6
        hour = request.json['hour'] #0 - 23

        data = db.readSQL("SELECT sum(price), individualTransactions.categoryId, categories.description, longitude, latitude FROM individualTransactions \
                   join individualItems on individualItems.id = individualTransactions.indItemId \
                   join categories on categories.id = individualTransactions.categoryId \
                   join sites on individualTransactions.siteId = sites.id \
                   where individualTransactions.siteId = N\'{}\' and dayOfWeek = {} and hourOfDay = {} group by individualTransactions.categoryId, categories.description, longitude, latitude".format(siteId, day, hour))
        toRet = Dict()
        i = 0;
        for row in data:
            toRet[i].siteId = siteId
            toRet[i].totalSales = row[0]
            toRet[i].categoryId = row[1]
            toRet[i].description = row[2]
            toRet[i].longitude = row[3]
            toRet[i].latitude = row[4]
            i += 1
        return json.dumps(toRet)
    else:
        data = db.readSQL("SELECT sum(price), individualTransactions.categoryId, categories.description, longitude, latitude FROM individualTransactions \
                   join individualItems on individualItems.id = individualTransactions.indItemId \
                   join categories on categories.id = individualTransactions.categoryId \
                   join sites on individualTransactions.siteId = sites.id \
                   where individualTransactions.siteId = N\'{}\' group by individualTransactions.categoryId, categories.description, longitude, latitude".format(siteId))
        toRet = Dict()
        i = 0;
        for row in data:
            toRet[i].siteId = siteId
            toRet[i].totalSales = row[0]
            toRet[i].categoryId = row[1]
            toRet[i].description = row[2]
            toRet[i].longitude = row[3]
            toRet[i].latitude = row[4]
            i += 1
        return json.dumps(toRet)


@app.route("/transaction/transactionStats", methods=['POST'])
def transactionStatsData():

    day = request.json['day'] #0 - 6
    hour = request.json['hour'] #0 - 23
    cat = request.json['categoryId']
    if 'siteId' in request.json.keys():
        siteId = request.json['siteId']

        res = db.readSQL("SELECT individualTransactions.id, price FROM individualTransactions JOIN individualItems on indItemId = individualItems.id where dayOfWeek = {} and hourOfDay = {} and categoryId = {} and siteId = N\'{}\'".format(day, hour, cat, siteId))

    else:
        siteId = None
        res = db.readSQL("SELECT individualTransactions.id, price FROM individualTransactions  JOIN individualItems on indItemId = individualItems.id where dayOfWeek = {} and hourOfDay = {} and categoryId = {}".format(day, hour, cat))

    prices = []
    for row in res:
        prices.append(row[1])
    if len(prices) <= 1:
        varPrice = 0
    else:
        varPrice = variance(prices)
    if 'siteId' in request.json.keys():
        return json.dumps({'siteId': siteId, 'category': cat, 'day': day, 'hour': hour, 'avgPrice': mean(prices), 'var': varPrice})
    else:
        return json.dumps({'category': cat, 'day': day, 'hour': hour, 'avgPrice': mean(prices), 'var': varPrice})


# @app.route("/siteEvents", methods=["GET"])
# def eventsBySiteDateRange():
#


if __name__ == "__main__":
    app.run(debug=True, port=8080, host= '0.0.0.0')
