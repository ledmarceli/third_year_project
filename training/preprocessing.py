import pandas as pd

#Read CSV
human = pd.read_csv("datasets/human.csv", header=None)
computer = pd.read_csv("datasets/computer.csv", header=None)

#Remove perfect decisions in difficult positions from human:
human = human[~((human.iloc[:,0] == 0) & (human.iloc[:,4] > -0.2))]
human = human[~((human.iloc[:,1] == 0) & (human.iloc[:,0] < 0.1) & (human.iloc[:,4] > -0.2))]
human = human[~((human.iloc[:,2] == 0) & (human.iloc[:,0] < 0.1) & (human.iloc[:,4] > -0.2))]

#Remove common rows from computer
common_rows = pd.merge(human, computer, how='inner')
common_rows_indices = computer[computer.isin(common_rows.to_dict('list')).all(1)].index
computer = computer[~computer.index.isin(common_rows_indices)]

#Remove very imprecise values from computer (that's a processing error)
computer = computer[computer.iloc[:, 0] < 0.1]
computer = computer[computer.iloc[:, 1] < 0.075]
computer = computer[computer.iloc[:, 2] < 0.05]
computer = computer[computer.iloc[:, 3] < 0.025]

#Remove forced moves from computer
computer = computer[~((computer.iloc[:,0] == 0) & (computer.iloc[:,1] < -0.5))]
computer = computer[~((computer.iloc[:,0] == 0) & (computer.iloc[:,2] < -0.5))]

print(human.shape[0])
print(computer.shape[0])

#Save
human.to_csv("datasets/human_filtered.csv", index=False)
computer.to_csv("datasets/computer_filtered.csv", index=False)

