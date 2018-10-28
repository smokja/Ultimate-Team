# Importing the libraries
import pandas as pd

# Importing and slicing the dataset
dataset = pd.read_csv('final_data/players.csv')
x = dataset.iloc[:, [1,4,6,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]].values

# replace Club and League string with number
y = [int(v.replace(" Club", "").replace("s","")) for v in x[:, 1]]
x[:, 1] = y
y = [int(v.replace(" League", "").replace("s","")) for v in x[:, 2]]
x[:, 2] = y

print(x)