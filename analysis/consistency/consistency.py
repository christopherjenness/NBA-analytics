import pickle
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def set_plot_params(size):
    SIZE = size
    plt.rc('font', size=SIZE)
    plt.rc('axes', titlesize=SIZE)
    plt.rc('axes', labelsize=SIZE)
    plt.rc('xtick', labelsize=SIZE)
    plt.rc('ytick', labelsize=SIZE)
    plt.rc('legend', fontsize=SIZE)


def get_URLS():
    urls = pickle.load(open('scrapper/urls.p', 'rb'))
    return urls


def make_df(baseURL):
    fname = os.path.basename(os.path.splitext(baseURL)[0])
    df = pickle.load(open('scrapper/gamelogs/' + fname + '.p', 'rb'))
    return df


def get_all_dfs(urls):
    dfs = {}
    for url in urls:
        try:
            name = os.path.basename(os.path.splitext(url)[0])
            df = make_df(url)
            dfs[name] = df
        except:
            pass
    return dfs


def get_CV_data(dfs, col):
    vals = []
    CVs = []
    names = []
    for name in dfs:
        df = dfs[name]
        df = df.dropna(subset=['G'])
        df = df[df['G'].astype(str) != 'G']
        CV = df[col].astype(float).std()
        if df.shape[0] > 40:
            CVs.append(CV)
            vals.append(df[col].astype(float).mean())
            names.append(name)
    return vals, CVs, names


def make_plots(dfs):

    vals, CVs, names = get_CV_data(dfs, 'PTS')
    df = pd.DataFrame({'Name': names, 'Mean': vals, 'CV': CVs})
    league = df[df.Name != 'jamesle01']
    LeBron = df[df.Name == 'jamesle01']
    plt.figure()
    plt.scatter(league['Mean'], league['CV'], s=20,
                alpha=0.4, c='black', label='League')
    plt.scatter(LeBron['Mean'], LeBron['CV'], s=70,
                alpha=1, c='red', label='LeBron')
    plt.legend(loc=4)
    plt.ylabel('Standard Deviation')
    plt.xlabel('PTS per game')
    plt.xlim(0)
    plt.ylim(0)
    plt.title('LeBron is a consistent Scorer')
    plt.tight_layout()
    plt.savefig('plots/PTS')

    vals, CVs, names = get_CV_data(dfs, 'FTA')
    df = pd.DataFrame({'Name': names, 'Mean': vals, 'CV': CVs})
    league = df[df.Name != 'jamesle01']
    LeBron = df[df.Name == 'jamesle01']
    plt.figure()
    plt.scatter(league['Mean'], league['CV'], s=20,
                alpha=0.4, c='black', label='League')
    plt.scatter(LeBron['Mean'], LeBron['CV'], s=70,
                alpha=1, c='red', label='LeBron')
    plt.legend(loc=4)
    plt.ylabel('Standard Deviation')
    plt.xlabel('FTA per game')
    plt.xlim(0)
    plt.ylim(0)
    plt.title('LeBron consistently gets to the line')
    plt.tight_layout()
    plt.savefig('plots/FTA')

    vals, CVs, names = get_CV_data(dfs, 'TRB')
    df = pd.DataFrame({'Name': names, 'Mean': vals, 'CV': CVs})
    league = df[df.Name != 'jamesle01']
    LeBron = df[df.Name == 'jamesle01']
    plt.figure()
    plt.scatter(league['Mean'], league['CV'], s=20,
                alpha=0.4, c='black', label='League')
    plt.scatter(LeBron['Mean'], LeBron['CV'], s=70,
                alpha=1, c='red', label='LeBron')
    plt.legend(loc=4)
    plt.ylabel('Standard Deviation')
    plt.xlabel('Rebounds per game')
    plt.xlim(0)
    plt.ylim(0)
    plt.title('LeBron consistently gets rebounds')
    plt.tight_layout()
    plt.savefig('plots/TRB')

    vals, CVs, names = get_CV_data(dfs, 'STL')
    df = pd.DataFrame({'Name': names, 'Mean': vals, 'CV': CVs})
    league = df[df.Name != 'jamesle01']
    LeBron = df[df.Name == 'jamesle01']
    plt.figure()
    plt.scatter(league['Mean'], league['CV'], s=20,
                alpha=0.4, c='black', label='League')
    plt.scatter(LeBron['Mean'], LeBron['CV'], s=70,
                alpha=1, c='red', label='LeBron')
    plt.legend(loc=4)
    plt.ylabel('Standard Deviation')
    plt.xlabel('STL per game')
    plt.xlim(0)
    plt.ylim(0)
    plt.title('LeBron consistently gets steals')
    plt.tight_layout()
    plt.savefig('plots/STL')

if __name__ == '__main__':
    urls = get_URLS()
    dfs = get_all_dfs(urls)
    set_plot_params(20)
    make_plots(dfs)
