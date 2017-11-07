import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def load_data():
    df = (pd.read_csv('data/shot_logs.csv')
          .assign(true3=lambda x: x['SHOT_DIST'] >=23.7)
          )
    return df


df = load_data()

FG_dist = (df.groupby('CLOSE_DEF_DIST')['PTS'].mean() / 3).head(80)

plt.scatter(x=FG_dist.index, y=FG_dist.values)
plt.show()
