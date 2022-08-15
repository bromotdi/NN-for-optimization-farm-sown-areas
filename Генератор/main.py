import random
import numpy as np
import pandas as pd


choices = [0.1, 0.2, 0.3, 0.4]

data_size = 100
field_number = 10

rates = pd.read_csv("crops.csv", ";")
years_data = pd.read_csv("years.csv", ";")
prices_data = pd.read_csv("prices.csv", ";")
effects_data = pd.read_csv("effects.csv", ";")
crops_data = pd.read_csv("crops_codes.csv", ";")

years = dict()
for index, row in years_data.iterrows():
    years[row['культура']] = row['рік']

prices = dict()
for index, row in prices_data.iterrows():
    prices[row['культура']] = row['вартість']

effects = dict()
for index, row in effects_data.iterrows():
    effects[row['культура']] = [row['1'], row['2'], row['3'], row['4']]

crops = dict()
for index, row in crops_data.iterrows():
    crops[row['культура']] = row['код']

res = []

for i in range(data_size):
    res.append([])
    total_price = 0
    for j in range(field_number):
        effect = 2
        if len(res) <= 1:
            before = "пшениця"
        else:
            before = res[-2][j]

        choice = np.array([])
        while choice.size == 0:
            p = random.random()
            sum_p = 0
            choice = -1
            while sum_p < p:
                choice += 1
                sum_p += choices[choice]

            effect = choice
            choice = rates[rates["доцільність"] == choice + 1]
            choice = choice[choice["попередник"] == before]
            choice = choice["культура"].to_numpy()

            for crop in choice:
                for y in range(2, years[crop] + 2):
                    if y > len(res):
                        break
                    if res[-y][j] == crop:
                        choice = choice[choice != crop]
                        y -= 1

        choice = random.choice(choice)
        effect = effects[choice][effect]
        total_price += effect * prices[choice]
        res[-1].append(choice)
    res[-1].append(total_price)

columns = [str(i) for i in range(1, field_number + 1)]
columns.append("profit")

df = pd.DataFrame(res, columns=columns)
df.to_excel("dataset_readable.xls")

for i in range(len(res)):
    for j in range(len(res[i]) - 1):
        res[i][j] = crops[res[i][j]]

df = pd.DataFrame(res, columns=columns)
df.to_csv("dataset.csv")
