import pandas as pd
import numpy as np

#Read csv
file1 = pd.read_csv('datasets/human_filtered.csv', header=None)
file2 = pd.read_csv('datasets/computer_filtered.csv', header=None)

#Add labels
file1['label'] = 0
file2['label'] = 1

#Concatenate
data = pd.concat([file1, file2], ignore_index=True)

#Shuffle
data = data.sample(frac=1, random_state=42).reset_index(drop=True)

#Split
train_data = data.sample(n=10403, random_state=42)
test_data = data.drop(train_data.index).sample(n=1040, random_state=42)

value_counts1 = train_data.iloc[:, -1].value_counts()
value_counts2 = test_data.iloc[:, -1].value_counts()
print(value_counts1)
print(value_counts2)

#To csv
train_data.to_csv('datasets/training.csv', header=None, index=False)
test_data.to_csv('datasets/testing.csv', header=None, index=False)