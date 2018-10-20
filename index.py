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
    return "Use the script! This takes too long!"
    if not 'siteId' in request.json:
        siteId = "7c54465e9f5344598276ec1f941f5a3c"
    else:
        siteId = request.json['siteId']
    transactions = ncr.getTransactionsBySite(siteId)
    for transaction in transactions['pageContent']:
        tlogId = transaction['tlogId']
        transLog = ncr.getTransactionsByDoc(tlogId)
    return json.dumps(transactions)

# @app.route("/siteEvents", methods=["GET"])
# def eventsBySiteDateRange():



if __name__ == "__main__":
    app.run(debug=True, port=8080)
