import requests
import json

config = None
with open("./Config.json", "r") as fp:
    config = json.load(fp)
ncrConfig = config['ncrConfig']
baseUrl = ncrConfig['gateway-url']

url = "https://gateway-staging.ncrcloud.com/transaction-document/transaction-documents/da23854c-6136-4b48-be9f-2291d15a97d6"

headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    'Authorization': ncrConfig['authCode'],
    'nep-application-key': ncrConfig['nep-application-key'],
    'nep-organization': "ncr-market",
    'nep-service-version': "2.2.0:2",
    'cache-control': "no-cache",
    }

headersNoVersion = {
    'Content-Type': "application/json",
    'Authorization': ncrConfig['authCode'],
    'nep-application-key': ncrConfig['nep-application-key'],
    'nep-organization': "ncr-market",
    'cache-control': "no-cache",
    }

def getTransactionById(id):
    url = "{}/transaction-document/transaction-document/{}".format(baseUrl, id)
    response = requests.request("GET", url, headers=headers)
    return response.json()

def getTransactionsBySite(siteId):
    url = "{}/transaction-document/transaction-documents/find/".format(baseUrl)
    response = requests.request("POST", url, data=json.dumps({'siteInfoIds': [siteId]}), headers=headers)
    return response.json()

def getTransactionsByDoc(docId):
    url = "{}/transaction-document/transaction-documents/{}".format(baseUrl, docId)
    response = requests.request("GET", url, headers=headers)
    return response.json()

def getItemById(itemId):
    url = "{}/catalog/items/{}".format(baseUrl, itemId)
    response = requests.request("GET", url, headers=headers)
    return response.json()

def getSiteById(siteId):
    url = "{}/site/sites/{}".format(baseUrl, siteId)
    response = requests.request("GET", url, headers=headersNoVersion)
    return response.json()
