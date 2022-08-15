import pandas as pd


crops_siv = pd.read_csv("crops.csv", ";")


all_coef = []
coef = crops_siv[crops_siv["культура"] == "овес"][crops_siv["попередник"] == "ячмінь"]
coef = coef["доцільність"].to_numpy()[0]
print(coef)
