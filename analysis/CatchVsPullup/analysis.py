import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_data():
    df_pullup = pd.read_csv('data/2018pullup.csv')
    df_catch = pd.read_csv('data/2018catchshoot.csv')
    df = (pd.merge(df_pullup, df_catch, on='PLAYER',
                   suffixes=['_pull', '_catch'])
          .loc[lambda x: x['3PA_pull'] > 50]
          .loc[lambda x: x['3PA_catch'] > 50])
    return df


def make_plot(df):
    plt.figure(figsize=(8, 8))
    plt.scatter(df['3P%_pull'], df['3P%_catch'])
    plt.xlim(20, 50)
    plt.ylim(20, 55)
    plt.title('Under-rated 3PT shooters', loc='left')
    plt.xlabel('Pull up 3PT%')
    plt.ylabel('Catch and shoot 3PT%')

    top_players = df.sort_values('3P%_catch').tail(4)
    for label, x, y in zip(top_players['PLAYER'],
                           top_players['3P%_pull'],
                           top_players['3P%_catch']):
        plt.annotate(
            label,
            xy=(x, y), xytext=(7, 0),
            textcoords='offset points', ha='left', va='top',
        )
    plt.savefig('plots/pullups', dpi=800)


if __name__ == '__main__':
    df = load_data()
    make_plot(df)
