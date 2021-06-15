# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns 

import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output

PATH = "./Life_Expectancy_Data_3alpha.csv" 
df = pd.read_csv(PATH) 

# Fill NA in columns with median()

df['Life expectancy '].fillna((df['Life expectancy '].median()), inplace=True)
df['Adult Mortality'].fillna((df['Adult Mortality'].median()), inplace=True)
df[' BMI '].fillna((df[' BMI '].median()), inplace=True)
df['Polio'].fillna((df['Polio'].median()), inplace=True)
df['Diphtheria '].fillna((df['Diphtheria '].median()), inplace=True)
df[' thinness  1-19 years'].fillna((df[' thinness  1-19 years'].median()), inplace=True)
df[' thinness 5-9 years'].fillna((df[' thinness 5-9 years'].median()), inplace=True)


# Fill NA in columns with mean()

df['Alcohol'].fillna((df['Alcohol'].mean()), inplace=True)
df['Hepatitis B'].fillna((df['Hepatitis B'].mean()), inplace=True)
df['Total expenditure'].fillna((df['Total expenditure'].mean()), inplace=True)
df['GDP'].fillna((df['GDP'].mean()), inplace=True)
df['Population'].fillna((df['Population'].mean()), inplace=True)
df['Income composition of resources'].fillna((df['Income composition of resources'].mean()), inplace=True)
df['Schooling'].fillna((df['Schooling'].mean()), inplace=True)

#df.isnull().sum()



app = dash.Dash(__name__)




# 1st Dash App:

app.layout = html.Div([
    # Title
    html.H1("Life Expectancy And Adult Mortality BY Countries"),
    
    # Area to hold the graph
    dcc.Graph(id="graph1"),
    

    
    #  input
    html.Label([
        "Countries By:",
        dcc.RadioItems(
            id="Countries",
            options=[
            {'label': 'Life Expectancy', 'value': 'Life expectancy '},
            {'label': 'Adult Mortality', 'value': 'Adult Mortality'},
                                          
                                      ],
                                      value='Life expectancy ',
                                      
                                  ) ,
    ]),

    
  # 2nd Dash App:  
    html.Div([
    # Title
    html.H1("Life Expectancy Impact Factors"),
    
    # Area to hold the graph
    dcc.Graph(id="graph2"),
        

    # First input
    html.Label([
        "Select a factor:",
        dcc.Dropdown(
            id='x_axis', 
            clearable=False,
            value= "Alcohol", 
            options=[{'label': "Alcohol", 'value': "Alcohol"},
            {'label': "infant Deaths", 'value': "infant deaths"},
            {'label': "Polio", 'value': "Polio"},
            {'label': "Adult Mortality", 'value': "Adult Mortality"},
            {'label': "HIV/AIDS", 'value': " HIV/AIDS"},
            ]
                                        )
    ]),
    # 3ed Dash App(With 2 inputs):
    html.Div([
    # Title
    html.H1("Thinness BY Years"),
    
    # Area to hold the graph
    dcc.Graph(id="graph"),
    
    
    #  input
    html.Label([
        "Years:",
        dcc.Slider(
            id='year',
            min=df['Year'].min(),
            max=df['Year'].max(),
            value=df['Year'].min(),
            marks={str(year): str(year) for year in df['Year'].unique()} ,
            step=None
                                    ),
    ]),
                       # Line Break
                       html.Br([]),
        
        
                        # 2nd input
                       html.Label([
                                   "Thinness",
                                   dcc.RadioItems(
                                       
                                      id="input2",
                                      options=[
                                         {'label': ' thinness  1-19 years', 'value': ' thinness  1-19 years'},
                                          {'label': ' thinness 5-9 years', 'value': ' thinness 5-9 years'},
                                         
                                      ],
                                      value=' thinness 5-9 years',
                                      labelStyle={'display': 'inline-block'}
                                  )   
                                  ]),
# 4th Dash App:
    html.Div([
    # Title
    html.H1("Count Of Status By Countries"),
    
    # Area to hold the graph
    dcc.Graph(id="graph3"),
    
    # input
    html.Label([
        "Choose Status:",
        dcc.RadioItems(
            id="Status",
            options=[
            {'label': 'Developed', 'value': 'Developed'},
            {'label': 'Developing', 'value': 'Developing'},
                                          
                                      ],
                                      value='Developed',
                                      
                                  )
    ]),
    
# 5th Dash App:
    html.Div([
    # Title
    html.H1("Percentage of Disease Immunization Coverage By Year."),
    
    # Area to hold the graph
    dcc.Graph(id="graph4"),
    

    # First input   
    html.Label([
        "Choose disease:",
        dcc.RadioItems(
            id="input1",
            options=[
                {'label': 'Hepatitis B (HepB)', 'value': 'Hepatitis B'},
                {'label': 'Polio (Pol3)', 'value': 'Polio'},
                {'label': 'Diphtheria tetanus toxoid and pertussis (DTP3)', 'value': 'Diphtheria '}
            ],
            value='Hepatitis B',
            labelStyle={'display': 'inline-block'}
        ) 
    ]),
    

    
    
])
])        
])
])    
])

# For with 1st Dash App (Countries Map)
@app.callback(
    Output('graph1', 'figure'),
    Input('Countries', 'value')
)

def update_figure1(selected_show):
    fig = px.choropleth(df, locations="Code",
                    color=selected_show, # lifeExp is a column of gapminder
                    hover_name="Country", # column to add to hover information
                    animation_frame='Year',
                   color_continuous_scale = "Sunset"
                    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    

    
    return fig

# For with 2nd Dash App (Life expectancy scatter plot with diffrent factors selected by user)

@app.callback(
    Output('graph2', 'figure'),
    Input('x_axis', 'value'))

def update_figure2(selected_xaxis):
  
    return px.scatter(
       df,
       x=selected_xaxis,
       y= 'Life expectancy ',
        color='Life expectancy ',
        color_continuous_scale = "Sunset"
      

       )

# For with 3ed Dash App with 2 inputs (show thinness histogram by selected year)
@app.callback(
    Output('graph', 'figure'),
    [Input("year", "value"),
     Input("input2", "value")]
)
def update_figure(selected_year , thinness_years ):
  
    test = df[df['Year'] == selected_year]
    return px.histogram(
       test,
       x=thinness_years,
       color='Status',
       color_discrete_sequence=['indianred' , 'lightyellow']
       )

# For with 4th Dash App (Show Countries with bar plot by selected Status)
@app.callback(
    Output('graph3', 'figure'),
    Input('Status', 'value'))

def update_figure3(selected_Status):

    filtter_data = (df["Population"] >= 10000000) & (df["Status"] == selected_Status)
    return px.histogram(
        df[filtter_data],
        x="Country",
        #color='Country',
        color_discrete_sequence=['indianred']
      

)


# For with 5th Dash App (Show diseases in factors in Each Year with box plot)
@app.callback(
    Output('graph4', 'figure'),
    Input('input1', 'value')
)

def update_figure4(val_input1):
      
    return px.box(
       df,
       x='Year',
       y=val_input1,
       color='Year',
       color_discrete_sequence = px.colors.qualitative.Set3
       )
    
    


    
if __name__ == '__main__':
    app.run_server(debug=True)