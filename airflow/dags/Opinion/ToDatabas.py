import pymongo
import os  
import collections  # From Python standard library.
import bson
from bson.codec_options import CodecOptions
from airflow.providers.mongo.hooks.mongo import MongoHook
from bson.json_util import dumps
import json
import numpy as np
import pandas as pd


def IsIndocker():
    return os.path.exists("/.dockerenv")


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

class Mongo_CRUD:
    def __init__(self,conn_id,table_name,mongo_db):
        # Mongo_CRUD(conn_id = "mongoid",mongo_db = "DataRange",table_name=table_name)
        self.pdtype = pd.DataFrame
        
        self.hook = MongoHook(conn_id)
        self.mongo_db = mongo_db
        self.table_name = table_name


    def Create(self,docs):
        
        # hook.Create(docs=df)
        
        if isinstance(docs, self.pdtype):
            docs=docs.to_dict('records')

            # hook.insert_many(docs,mongo_db=mongo_db, mongo_collection=table_name )

            self.hook.insert_many(docs=docs
                    ,mongo_db=self.mongo_db
                    # ,mongo_collection='Stock'
                    ,mongo_collection=self.table_name 
                    )
            print(f'Seccess to create {self.table_name}')


        elif isinstance(docs, int):
            # docs = json.dumps({self.table_name: docs}, cls=NpEncoder)

            doc = {self.table_name: docs}
            # cursor = self.hook.find(query,mongo_collection,mongo_db="DataRange")

            self.hook.insert_one(mongo_collection="DataRange", doc=doc, mongo_db="DataRange")


        # else:
        #     print(f"Error")


    def Read(self,query):
        try:
            cursor = self.hook.find(query,mongo_collection=self.table_name,mongo_db=self.mongo_db
)

            JSON = json.loads(dumps(cursor))
            return JSON
        except Exception as e:
            print(e)

    def Update(self,filter_doc,update_doc):
        try:
            self.hook.update_one(filter_doc
                            , update_doc
                            , mongo_db=self.mongo_db
                            ,mongo_collection=self.table_name)
        except Exception as e:
            print(e)

    def Delete():
        pass


def UpdateRange(df,table_name,mongo_db):

    page = df.sort_values('date',ascending = False)['date'].iloc[0]
    hook = Mongo_CRUD(conn_id = "mongoid",mongo_db = "DataRange",table_name=table_name)
    hook.Create(docs=page)
    
    