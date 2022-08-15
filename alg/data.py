import numpy as np
import pandas as pd


def read_file(file):
    df = pd.read_csv("input/{}".format(file))
    df = df.drop(['Unnamed: 0'], axis=1)
    d = df.drop(['profit'], axis=1)
    d = np.array(d)
    rows = []
    for j in range(len(d)):
        row = [0] * 12
        for i in d[j]:
            row[i - 1] = row[i - 1] + 1
        rows.append(row)
    tt = int(len(rows))
    train = rows[:tt]
    X_train = train
    y_train = list(df['profit'][:tt])
    return X_train, y_train, d
