import pandas as pd
import matplotlib.pyplot as plt
import os

cwd = os.getcwd()
print(cwd)

df16 = pd.read_csv(f"{cwd}/src/players/data/2016.csv")
df17 = pd.read_csv(f"{cwd}/src/players/data/2017.csv")
df18 = pd.read_csv(f"{cwd}/src/players/data/2018.csv")
df19 = pd.read_csv(f"{cwd}/src/players/data/2019.csv")
df20 = pd.read_csv(f"{cwd}/src/players/data/2020.csv")

"""
print(f"16: {len(df16)}")
print(f"17: {len(df17)}")
print(f"18: {len(df18)}")
print(f"19: {len(df19)}")
print(f"20: {len(df20)}")
"""


def nationality(nationality, df):
    return df[df["nationality"] == nationality]


england = nationality("England", df16)
england[:]["value_eur"] *= 0.000001
england.rename(columns={"value_eur": "value_eur_mln"}, inplace=True)
# print(england["age"])
plt.scatter(england["overall"], england["value_eur_mln"])
plt.xlabel("Overall")
plt.ylabel("Value in mln euro")
plt.show()
