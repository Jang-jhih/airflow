
import os  
import pymongo
import pandas as pd
import pickle






class DataBase:
    
    def __init__(self,table_name,):
        self.date_range_record_file = os.path.join('history', 'date_range.pickle')
        self.table_name = table_name

        if not os.path.isdir(os.path.join('history')):
            os.mkdir(os.path.join('history'))


    def UpdateRange(self,df):
        
        if not os.path.isfile(self.date_range_record_file):
            pickle.dump({}, open(self.date_range_record_file, 'wb'))
        
        
        TimeStamp = pickle.load(open(self.date_range_record_file, 'rb'))
        TimeStamp[self.table_name] = df.sort_values('date',ascending = False)['date'].iloc[0]
        pickle.dump(TimeStamp, open(self.date_range_record_file, 'wb'))

    def table_date_range(self):
        if os.path.isfile(self.date_range_record_file):
            with open(self.date_range_record_file, 'rb') as f:
                dates = pickle.load(f)
                if self.table_name in dates:
                    return dates[self.table_name]
                else:
                    return [None, None]
        else:
            return [None, None]

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
