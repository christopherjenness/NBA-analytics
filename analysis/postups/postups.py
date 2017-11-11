import pandas as pd
import plotly as py
import plotly.graph_objs as go


def load_data():
    df = pd.read_csv('data/2017.csv')
    return df


def make_plot(df):
    TEAMS = list(df.TEAM.unique())
    TEAMS.sort()

    trace = go.Scatter(x=df['POST UPS'], y=df['PASS'],
                       text=df['\ufeffPLAYER'], mode='markers',
                       hoverinfo='text', marker={'color': 'blue'})

    layout = go.Layout(hovermode='closest',
                       title='How often do players pass out of post ups',
                       xaxis={'title': 'Post ups'},
                       yaxis={'title': 'Passes out of post ups'})

    data = [trace]

    buttons = []
    for team in TEAMS:
        buttons.append({'args': ['marker.color', [df['TEAM']
                                                  .map({team: 'red'})
                                                  .fillna('blue')]],
                        'label': team,
                        'method': 'restyle'})

    updatemenus = list([{'active': 1, 'buttons': buttons}])

    layout['updatemenus'] = updatemenus

    # Plot and embed in ipython notebook!
    fig = go.Figure(data=data, layout=layout)
    py.offline.plot(fig, filename='basic-scatter')


if __name__ == '__main__':
    df = load_data()
    make_plot(df)
