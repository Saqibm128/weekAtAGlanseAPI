import requests
import json
from addict import Dict
import db
import re

config = None
with open("./Config.json", "r") as fp:
    config = json.load(fp)

key = config['microsoftKey']
taKey = config['microsoftTextKey']

# def generateConceptForTransaction(transactionId):

def generateConceptForTransaction(transactionId):
    res = db.readSQL("SELECT description, categoryUserApproved, indItemId FROM individualTransactions join individualItems on individualItems.id = indItemId where individualTransactions.id = {}".format(transactionId))
    if len(res) == 0:
        raise Exception("No transaction matching the expected id")
    name = res[0][0]
    itemId = res[0][2]
    snippets = searchSnippets(name, count=5)
    snippets.append(name)
    # entities = importantEntities(snippets)
    # for entity in entities.keys():
    #     snippets += (searchSnippets(entity, count=5))
    entities = importantEntities(snippets)
    preexistingConcept = None

    concept = findMaxInDict(entities)
    concept = re.sub("\'", '', concept)
    concept = re.sub('ā', 'a', concept)

    if res[0][1] is None or res[0][1] == "false":
        siteId = db.readSQL("SELECT siteId from individualTransactions where individualTransactions.id = N\'{}\'".format(transactionId))[0][0]
        db.writeSQL("INSERT into categories (siteId, description) VALUES (N\'{}\', N\'{}\')".format(siteId, concept))
        conceptId = db.readSQL("SELECT id FROM categories where siteId = N\'{}\' and description = N\'{}\'".format(siteId, concept))[0][0]
        db.writeSQL("UPDATE individualTransactions SET categoryId = {} where id = {}".format(conceptId, transactionId))
        for entity in entities:
            db.writeSQL("INSERT into entityCategoryMap (categoryId, entityName, itemId) values ({}, N\'{}\', {})".format(conceptId, entity, itemId))
        return concept

    # return entities[0]
    # for snippet in snippets:
    #     db.writeSQL("INSERT into ")

def searchSnippets(query, count=5):
    params = {'q' : query, 'count': count}
    headers = {'Ocp-Apim-Subscription-Key': key}
    resp = requests.get("https://api.cognitive.microsoft.com/bing/v7.0/search", params=params, headers=headers)
    resp = resp.json()
    toRet = []
    for page in resp['webPages']['value']:
        toRet.append(page['snippet'])
    return toRet

def importantEntities(strsToAnalyze):
    headers = {'Ocp-Apim-Subscription-Key': taKey, 'Content-Type': 'application/json'}

    docs = {}
    i = 1
    docs['documents'] = []

    for toAnalyze in strsToAnalyze:
        toappend = {'languange':'en', 'id': '{}'.format(i), 'text': toAnalyze}
        docs['documents'].append(toappend)
        i += 1
    resp = requests.request("POST","https://eastus.api.cognitive.microsoft.com/text/analytics/v2.0/entities", json=docs, headers=headers)
    toRet = {}
    if "documents" in resp.json().keys():
        for doc in resp.json()["documents"]:
            for entity in doc['entities']:
                entity['name'] = re.sub('\'', '', entity['name'])
                if entity['name'] in toRet.keys():
                    toRet[entity['name']] += 1
                else:
                    toRet[entity['name']] = 1
    return toRet

def findMaxInDict(freqs):
    maxKey = None
    for key in freqs.keys():
        if maxKey is None or freqs[maxKey] < freqs[key]:
            maxKey = key
    return maxKey

def categoryEntityLink(entity):
    db.readSQL("SELECT categoryId, description from entityCategoryMap join categories on categories.id = categoryId where entity = N\'{}\'".format(entity))
# def singleCategory(strsToAnalyze)
