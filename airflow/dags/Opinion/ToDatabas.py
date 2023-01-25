
import os  
import pymongo
import pandas as pd
import pickle


def IsIndocker():
    return os.path.exists("/.dockerenv")



class DataBase:
    
    def __init__(self,table_name,):

        self.date_range_record_file = os.path.join('history', 'date_range.pickle')
   
        self.table_name = table_name
        
        
    

    def table_date_range(self):
        if os.path.isfile(self.date_range_record_file):
            with open(self.date_range_record_file, 'rb') as f:
                dates = pickle.load(f)
                if self.table_name in dates:
                    return dates[self.table_name]
                else:
                    # return [None, None]
                    return None
        else:
            # return [None, None]
            return None

    def Mongodb(self,df):
        # user = os.getenv("user") 
        # password = os.getenv("password")
        host = os.getenv("host")
        port = os.getenv("port")

        client = pymongo.MongoClient(f'mongodb://{host}:{port}/')
        db = client['Opinion']
        collection = db[self.table_name]
        db.collection.insert_many(df.to_dict('records'))

        DataBase(self.table_name).UpdateRange(df)
