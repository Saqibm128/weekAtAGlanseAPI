from flask import Flask, request, render_template
from addict import Dict
import ncr
import db
import json

app = Flask(__name__)

@app.route("/health")
def health():
    return "We are working!"

@app.route("/populateDB", methods=["POST"])
def populateDB():
    return "Use the script! This takes too long to work as REST call!"

# @app.route("/transaction/category", methods=['POST'])
# def

@app.route("/category/<siteid>", methods=['GET', 'POST'])
def getCategories(siteid):
    if request.method == 'GET':
        res = db.readSQL("SELECT * FROM categories where siteid = N\'{}\'".format(siteid))
        return json.dumps(res[0])
    elif request.method == 'POST':
        category = request.json['category']
        res = db.writeSQL("INSERT into categories (siteId, description) values ({}, N\'{}\')".format(siteid, category))

@app.route("/transaction/all", methods=["GET"])
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
    day = request.json['day'] #0 - 6
    hour = request.json['hour'] #0 - 23

    returnVal = []
    for catI in range(len(categories)):
        cat = categories[catI]
        returnVal.append( {'siteId': siteId, 'category': cat, 'day': day, 'hour': hour, 'freq': hardCodedVals[catI]} )

    return json.dumps(returnVal)

@app.route("/transaction/transactionStats", methods=['POST'])
def transactionStatsData():
    siteId = request.json['siteId']
    day = request.json['day'] #0 - 6
    hour = request.json['hour'] #0 - 23
    cat = request.json['category']
    return json.dumps({'siteId': siteId, 'category': cat, 'day': day, 'hour': hour, 'avgPrice': 10.99, 'var': 1.2})

# @app.route("/siteEvents", methods=["GET"])
# def eventsBySiteDateRange():
#


if __name__ == "__main__":
    app.run(debug=True, port=8080)
