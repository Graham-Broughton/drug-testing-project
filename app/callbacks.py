import os
import sys
from datetime import date

import dotenv
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CFG

CFG = CFG()
dotenv.load_dotenv()
CFG.DATE = date(2023, 3, 1)

from app import app

df = pd.read_csv(os.path.join(CFG.PROCESSED_DATA_PATH, f"df-processed-{CFG.DATE}.csv"), parse_dates=['visit date'])   
latlng = pd.read_csv(os.path.join(CFG.PROCESSED_DATA_PATH, 'geodata\latlng.csv'))
ftirs = [x for x in df.columns.tolist() if x.startswith('ftir')]
for col in ftirs:
    df[col] = df[col].astype(str)


# City & Site Barchart
@app.callback(
    Output("sample-counts", "figure"),
    Input("sample-category-radio", "value"),
    Input('summary-date-range', 'start_date'),
    Input('summary-date-range', 'end_date'))
def sample_counts(sample_category_radio, start_date, end_date):
    newdf = df[(df['visit date'] >= start_date) & (df['visit date'] <= end_date)]
    flitered_df = newdf.value_counts(sample_category_radio).head(10).sort_values(ascending=False)

    fig = go.Figure(go.Bar(
        x=flitered_df.values,
        y=flitered_df.index,
        orientation='h',
    ))
    fig.update_layout(
        title=f"Top Ten Number of Samples per {sample_category_radio}",
        title_x=0.5,
    )
    return fig

# Category Piechart
@app.callback(
    Output('category-piechart', 'figure'),
    Input('summary-date-range', 'start_date'),
    Input('summary-date-range', 'end_date'))
def category_piechart(start_date, end_date):
    newdf = df[(df['visit date'] >= start_date) & (df['visit date'] <= end_date)]
    fig = go.Figure(go.Pie(
        labels=newdf.category.value_counts().index,
        values=newdf.category.value_counts().values,
        hole=0.65
    ))
    fig.update_traces(hoverinfo='label+value', textinfo='percent', textfont_size=12,
                    marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(
        showlegend=False,
        annotations=[
            dict(text="Categories", x=0.5, y=0.5, font_size=20, showarrow=False)
        ])
    return fig

@app.callback(
    Output('total-sample-chart', 'figure'),
    Input('summary-date-range', 'start_date'),
    Input('summary-date-range', 'end_date'))
def total_sample_chart(start_date, end_date):
    newdf = df[(df['visit date'] >= start_date) & (df['visit date'] <= end_date)]
    
    fig = go.Figure(go.Pie(
        labels=list('samples'),
        values=list(len(newdf)),
        hole=0.65
    ))
    fig.update_traces(hoverinfo='label+value', textinfo='percent', textfont_size=12,
                    marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(
        showlegend=False,
        annotations=[
            dict(text="Total<br>Samples", x=0.5, y=0.5, font_size=20, showarrow=False)
        ])
    return fig

@app.callback(
    Output('total-opioids', 'figure'),
    Input('summary-date-range', 'start_date'),
    Input('summary-date-range', 'end_date'))
def total_opioids(start_date, end_date):
    newdf = df[(df['visit date'] >= start_date) & (df['visit date'] <= end_date)]
    fig = go.Figure(go.Pie(
        labels=newdf['total_opioids'].replace({1: "Positive", 0: "Negative"}).value_counts().index,
        values=newdf['total_opioids'].value_counts().values,
        hole=0.65
    ))
    fig.update_traces(hoverinfo='label+value', textinfo='percent', textfont_size=12,
                    marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(
        showlegend=False,
        annotations=[
            dict(text="Opioids<br>Present", x=0.5, y=0.5, font_size=20, showarrow=False)
        ])
    return fig

@app.callback(
    Output('total-benzos', 'figure'),
    Input('summary-date-range', 'start_date'),
    Input('summary-date-range', 'end_date'))
def total_benzos(start_date, end_date):
    newdf = df[(df['visit date'] >= start_date) & (df['visit date'] <= end_date)]
    fig = go.Figure(go.Pie(
        labels=newdf['total_benzos'].replace({1: "Positive", 0: "Negative"}).value_counts().index,
        values=newdf['total_benzos'].value_counts().values,
        hole=0.65
    ))
    fig.update_traces(hoverinfo='label+value', textinfo='percent', textfont_size=12,
                    marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(
        showlegend=False,
        annotations=[
            dict(text="Benzos<br>Present", x=0.5, y=0.5, font_size=20, showarrow=False)
        ])
    return fig

@app.callback(
    Output('unexpected-opioids', 'figure'),
    Input('summary-date-range', 'start_date'),
    Input('summary-date-range', 'end_date'))
def unexpected_opioids(start_date, end_date):
    newdf = df[(df['visit date'] >= start_date) & (df['visit date'] <= end_date)]
    no_opioid = newdf[~(df['category'] == 'Opioid') | (df['category'] == 'Polysubstance')].index
    no_opioid = newdf.iloc[no_opioid]

    fig = go.Figure(go.Pie(
        labels=no_opioid['total_opioids'].replace({1: "Positive", 0: "Negative"}).value_counts().index,
        values=no_opioid['total_opioids'].value_counts().values,
        hole=0.65
    ))
    fig.update_traces(hoverinfo='value+percent', textinfo='label', textfont_size=12,
                    marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(
        showlegend=False,
        annotations=[
            dict(text="Unexpected<br>Opioids", x=0.5, y=0.5, font_size=20, showarrow=False)
        ])
    return fig

@app.callback(
    Output('unexpected-benzos', 'figure'),
    Input('summary-date-range', 'start_date'),
    Input('summary-date-range', 'end_date'))
def unexpected_benzos(start_date, end_date):
    newdf = df[(df['visit date'] >= start_date) & (df['visit date'] <= end_date)]
    no_benzo = newdf[~(df['category'] == 'Depressant')].index
    no_benzo = newdf.iloc[no_benzo]

    fig = go.Figure(go.Pie(
        labels=no_benzo['total_benzos'].replace({1: "Positive", 0: "Negative"}).value_counts().index,
        values=no_benzo['total_benzos'].value_counts().values,
        hoverinfo='label+value+percent',
        textinfo=None,
        hole=0.65
    ))
    fig.update_traces(hoverinfo='value+percent', textinfo='label', textfont_size=12,
                    marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(
        showlegend=False,
        annotations=[
            dict(text="Unexpected<br>Benzos", x=0.5, y=0.5, font_size=20, showarrow=False)
        ])
    return fig

@app.callback(
    Output('benzos-in-opioids', 'figure'),
    Input('summary-date-range', 'start_date'),
    Input('summary-date-range', 'end_date'))
def benzos_in_opioids(start_date, end_date):
    newdf = df[(df['visit date'] >= start_date) & (df['visit date'] <= end_date)]
    total_opioids = newdf[df['total_opioids'] == 1]

    fig = go.Figure(go.Pie(
        labels=total_opioids['total_benzos'].replace({1: "Positive", 0: "Negative"}).value_counts().index,
        values=total_opioids['total_benzos'].value_counts().values,
        hole=0.65
    ))
    fig.update_traces(hoverinfo='value+percent', textinfo='label', textfont_size=20,
                    marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(
        showlegend=False,
        annotations=[
            dict(text="Benzos in<br>Opioids", x=0.5, y=0.5, font_size=20, showarrow=False)
        ])
    return fig

# @app.callback(
#     Output('texture-colour', 'figure'),
#   Input('summary-date-range', 'value')
# )
# def texture_colour():
#     pass

@app.callback(
    Output("geographic-chart", "figure"),
    Input('geographic-date-selector', 'start_date'),
    Input('geographic-date-selector', 'end_date'))
def geographic_chart(start_date, end_date):
    colors = ["royalblue","crimson","lightseagreen","orange","lightgrey"]
    limits = [(0, 1), (1, 4), (4, 10), (10, 18), (18, 35)]
    token = os.getenv('MAPBOX_TOKEN')

    newdf = df[(df['visit date'] >= start_date) & (df['visit date'] <= end_date)]
    counts = newdf.value_counts('city')
    latlng_df = latlng.merge(counts.to_frame(), on='city').rename({0: 'count'}, axis=1)

    latlng_df['text'] = latlng_df['city'] + '<br>' + 'Count: ' + latlng_df['count'].astype(str)
    latlng_df = latlng_df.sort_values('count', ascending=False).reset_index(drop=True)

    fig = go.Figure()

    for i in range(len(limits)):
        lim = limits[i]
        df_sub = latlng_df[lim[0]:lim[1]]
        fig.add_trace(go.Scattermapbox(
            lon = df_sub['lng'],
            lat = df_sub['lat'],
            text = df_sub['text'],
            marker = go.scattermapbox.Marker(
                size = np.log(df_sub['count']) ** 3.5,
                color = colors[i],
                sizemode = 'area'
            ),
            hoverinfo='text',
        ))

    fig.update_layout(
        margin={"r": 0, "t": 20, "l": 0, "b": 20},
        showlegend = False,
        hovermode='closest',
        mapbox=dict(
            accesstoken=token,
            bearing=12,
            center=go.layout.mapbox.Center(
                lat=51.2,
                lon=-122.3
            ),
            pitch=0,
            zoom=4.9
        ))
    return fig
