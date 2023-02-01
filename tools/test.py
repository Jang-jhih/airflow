import pymongo
import os


def IsIndocker():
    return os.path.exists("/.dockerenv")

if IsIndocker():
    host = "mongodb"
else:
    host = "localhost"

myclient = pymongo.MongoClient(f"mongodb://airflow:airflow@{host}:27017/?authMechanism=DEFAULT")

db = myclient['DataRange']
collect = db['DataRange']

for post in collect.find():
    print(post)

# db.coll.find({"Stock":{'$exists': 1}})
# collect.find({ ln: { $exists: true} });
# collect.find({"Stock":{'$exists': 1}})