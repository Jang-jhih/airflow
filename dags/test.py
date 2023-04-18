import pickle
import os
import pandas as pd
year = 2019
season = 1

file = 'pack20191.pickle'
file_name = os.path.join('history', 'financial_statement', file)
df = pd.read_pickle(file_name)