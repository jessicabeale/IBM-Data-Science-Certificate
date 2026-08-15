# SpaceX Falcon 9 Launch Records Dashboard
# Interactive Plotly Dash app: filter by launch site and payload mass range,
# view success-rate breakdown (pie chart) and payload-vs-outcome (scatter chart).

import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
spacex_df = pd.read_csv("dataset_part_1.csv")
landing_outcomes = spacex_df['Outcome'].value_counts()
bad_outcomes = set(landing_outcomes.keys()[[1, 3, 5, 6, 7]])
spacex_df['class'] = spacex_df['Outcome'].apply(lambda o: 0 if o in bad_outcomes else 1)
spacex_df = spacex_df.rename(columns={'LaunchSite': 'Launch Site', 'PayloadMass': 'Payload Mass (kg)',
                                       'BoosterVersion': 'Booster Version'})

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# ---------------------------------------------------------------------------
# App layout
# ---------------------------------------------------------------------------
app = dash.Dash(__name__)
app.title = "SpaceX Launch Records Dashboard"

launch_site_options = [{'label': 'All Sites', 'value': 'ALL'}] + [
    {'label': site, 'value': site} for site in sorted(spacex_df['Launch Site'].unique())
]

app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#0B3D91', 'fontSize': 32}),

    dcc.Dropdown(
        id='site-dropdown',
        options=launch_site_options,
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),

    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={i: str(i) for i in range(0, 10001, 2500)},
        value=[min_payload, max_payload]
    ),

    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(
            spacex_df, values='class', names='Launch Site',
            title='Total Successful Launches by Site'
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        outcome_counts = filtered_df['class'].value_counts().rename({1: 'Success', 0: 'Failure'})
        fig = px.pie(
            values=outcome_counts.values, names=outcome_counts.index,
            title=f'Total Launch Outcomes for site {entered_site}'
        )
    return fig


@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")]
)
def update_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)
    filtered_df = spacex_df[mask]

    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]

    fig = px.scatter(
        filtered_df, x='Payload Mass (kg)', y='class',
        color='Booster Version',
        title='Correlation between Payload and Success for ' +
              ('all sites' if entered_site == 'ALL' else entered_site)
    )
    return fig


if __name__ == '__main__':
    app.run(debug=True)
