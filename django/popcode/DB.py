import pymongo

MGC = pymongo.MongoClient("mongodb://popcode:popcode@194.87.217.205:27017/")
DB = MGC["popcode"]
