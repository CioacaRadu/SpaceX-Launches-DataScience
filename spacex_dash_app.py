# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

dd_options = [{'label': 'All Sites', 'value': 'ALL'}]
for site in spacex_df['Launch Site'].value_counts().index:
    dd_options.append({'label':site, 'value':site})

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)

                                dcc.Dropdown(id='site-dropdown',
                                options=dd_options,
                                value='ALL',
                                placeholder="Select a Launch Site here",
                                searchable=True
                                ),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):

    if entered_site == 'ALL':

        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches by Site')
        
    else:
        test = 1
        sucs = spacex_df.loc[(spacex_df['Launch Site'] == entered_site) & (spacex_df['class'] == 1)]['class'].count()
        fails = spacex_df.loc[(spacex_df['Launch Site'] == entered_site) & (spacex_df['class'] == 0)]['class'].count()
        
        fig = px.pie(values=[sucs, fails], 
        names=['1','0'], 
        title=f'Launch Outcomes for {site}')

    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value")])

def get_scatter_plot(entered_site, slider_value):

    slider_min = slider_value[0]
    slider_max = slider_value[1]

    df_slide = spacex_df.loc[(spacex_df['Payload Mass (kg)'] >= slider_min) & (spacex_df['Payload Mass (kg)'] <= slider_max)]
    
    if entered_site == 'ALL':

        fig = px.scatter(data_frame=df_slide, x='Payload Mass (kg)', 
        y='class', color='Booster Version Category', title='Corr between Payload and Success')
    
    else:

        df_filtered = df_slide.loc[ spacex_df['Launch Site'] == entered_site ]
        fig = px.scatter(data_frame=df_filtered, x='Payload Mass (kg)', 
        y='class', color='Booster Version Category', title=f'Corr between Payload and Success for {entered_site}')

    return fig



# Run the app
if __name__ == '__main__':
    app.run_server()
