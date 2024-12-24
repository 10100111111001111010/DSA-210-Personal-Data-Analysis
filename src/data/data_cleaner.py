import pandas as pd


csvFile = pd.read_csv('../../data/raw/watch-history.csv')
cols = ['title', 'datetime']
csvFile = csvFile[cols]

print(csvFile)
