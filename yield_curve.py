import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import quandl
from datetime import datetime

app = dash.Dash()

df = quandl.get('USTREASURY/YIELD-Treasury-Yield-Curve-Rates', rows=1).transpose()
today = df.columns[0]
x_vals = np.arange(len(df)) + 1
today_as_human = datetime.strftime(today,"%B %d, %Y")

bandxaxis = go.XAxis(
    title="Tenor",
    range=[0, len(df) + 1],
    showgrid=True,
    showline=True,
    ticks="", 
    showticklabels=True,
    mirror=True,
    linewidth=2,
    ticktext=df.index.values,
    tickvals=[i for i in range(1,len(df)+1)]
)

app.layout = html.Div([
    dcc.Graph(
        id='yield-curve',
        figure={
            'data': [
                go.Scatter(
                    x=x_vals,
                    y=df[today].values,
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=str(today)
                ) 
            ],
            'layout': go.Layout(
                title='U.S. Treasury Yields for {}'.format(today_as_human),
                xaxis=bandxaxis, 
                yaxis={'title': 'Yield'},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
            
        }
    )
])

if __name__=='__main__':
    app.run_server()
