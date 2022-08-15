import pandas as pd
from pandas import read_csv


def parse_data(file):
    path = "C:/Users/admin/eclipse-workspace/.metadata/.plugins/org.eclipse.wst.server.core/tmp0/wtpwebapps/project/"

    dataset_read = pd.read_excel(path + "input/{}".format(file), index_col=0)
    dataset = dataset_read.drop(['profit'], axis=1)
    dataset = pd.DataFrame(dataset).to_numpy()

    crops_data = read_csv(path + "data/crops_codes.csv", ";")
    effects_data = read_csv(path + "data/effects.csv", ";")
    crops_siv = read_csv(path + "data/crops.csv", ";")
    years_data = read_csv(path + "data/years.csv", ";")

    effects = dict()
    for index, row in effects_data.iterrows():
        effects[row['культура']] = [row['1'], row['2'], row['3'], row['4']]

    crops = dict()
    for index, row in crops_data.iterrows():
        crops[row['культура']] = row['код']

    years = dict()
    for index, row in years_data.iterrows():
        years[row['культура']] = row['рік']

    crops_reverse = dict()
    for index, row in crops_data.iterrows():
        crops_reverse[row['код']] = row['культура']

    dataset_readable = []
    for i in range(len(dataset)):
        dataset_readable.append([])
        for j in range(len(dataset[i])):
            dataset_readable[-1].append(crops[dataset[i][j]])

    rows = []
    for j in range(len(dataset_readable)):
        row = [0] * 12
        for i in dataset_readable[j]:
            row[i - 1] = row[i - 1] + 1
        rows.append(row)
    tt = int(len(rows))
    train = rows[:tt]
    X_train = train
    y_train = list(dataset_read['profit'][:tt])

    return dataset, crops_reverse, effects, crops_siv, years, X_train, y_train
