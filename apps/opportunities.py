# -*- coding: utf-8 -*-
import flask
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.plotly as py
from plotly import graph_objs as go
import plotly.graph_objs as go

from datetime import date
from datetime import datetime
import dateutil.parser
import string
import time


import pandas as pd
import json
from json import encoder
import numpy as np
import math
from money import Money

import psycopg2
from sqlalchemy import create_engine

from app import app, indicator_one, indicator_four, millify, df_to_table, to_dollar
mapbox_access_token = 'pk.eyJ1IjoibmlhbGxjaGFuZ2V4IiwiYSI6ImNqbHFyc2FjaTJjYXUza3Biem9tamw2enEifQ.iy0uUg8EKAYaFbZuN1iodw'



## FIXED VARIABLES ###

budget_total= 30000

##=======1.0 CONNECT TO DATABASES===========

# Connecting to ChangeX Production PostgreSQL by providing a sqlachemy engine
engine = create_engine('postgresql://uf3hqd001negpr:p1cves5keua9t4a48dq8qqj7nuo@ec2-52-207-134-99.compute-1.amazonaws.com/d30dl84lfuo1q0')
# Connecting to Facebook Ads PostgreSQL by providing a sqlachemy engine
facebook_engine = create_engine('postgresql://cwowexuoevajcl:4e061d2010ae798e5694efa386c7480754b708f8a3da97fd5fe659579c125f02@ec2-54-204-2-26.compute-1.amazonaws.com/dfk5g884idgiqm')





##=======2.0 IMPORT DATA TABLES===========

#Import Main Accounts and Split
accounts = pd.read_sql('SELECT * FROM accounts', engine)
split_accounts_options = accounts['options'].apply(pd.Series)
account_options=pd.concat([accounts.drop(['options'], axis=1), split_accounts_options], axis=1)




##=======3.0 MERGING DATA TABLES===========




##=======3.0 ANALYTICS===========



#1 Project Cost Breakdown Chart

def project_costs_chart(fund_account_value, total_ad_spend, total_active):
    total_ad_spend= json.loads(total_ad_spend)
    total_pack_costs = json.loads(total_active) * 16.00
    staff_daily_rate= 4000.0/22
    total_staff_costs = staff_daily_rate * 88


    labels = ['Ad Spend','Pack Costs','Staff Costs']
    values = [total_ad_spend, total_pack_costs, total_staff_costs]
    colors = ['#E01273', '#EFEEED', '#58B74E']

    trace = go.Pie(labels=labels,
                   values=values,
                   marker=dict(colors=colors),
                   textinfo= 'value+percent',
                   )
    layout = dict(margin=dict(l=15, r=10, t=0, b=65), legend=dict(orientation="h"))

    return dict(data=[trace], layout=layout)




#2 Project Wheel Chart

def wheel_chart(fund_name):

    base_chart = {
        "values": [30000, 6000, 6000, 6000, 6000, 6000],
        "labels": ["-", "€6,000", "€12,000", "€18,000", "€24,000", "€30,000"],
        "domain": {"x": [0, .48]},
        "marker": {
            "colors": [
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)'
            ],
            "line": {
                "width": 1
            }
        },
        "name": "Gauge",
        "hole": .4,
        "type": "pie",
        "direction": "clockwise",
        "rotation": 108,
        "showlegend": False,
        "hoverinfo": "none",
        "textinfo": "label",
        "textposition": "outside"
    }

    meter_chart = {
        "values": [30000, 6000, 6000, 6000, 6000, 6000],
        "labels": ["-", "20%", "40%", "60%", "80%", "Full Budget"],
        "marker": {
            'colors': [
                'rgb(255, 255, 255)',
                'rgb(224,18,115)',
                'rgb(191,227,187)',
                'rgb(156,212,150)',
                'rgb(122,198,114)',
                'rgb(88,183,78)'
            ]
        },
        "domain": {"x": [0, 0.48]},
        "name": "Gauge",
        "hole": .3,
        "type": "pie",
        "direction": "clockwise",
        "rotation": 90,
        "showlegend": False,
        "textinfo": "label",
        "textposition": "inside",
        "hoverinfo": "none"
    }
    h = 0.24
    k = 0.5
    r = 0.15
    my_raw_value=80
    # Map my_raw_value to degrees. my_raw_value is between 0 and 300
    theta = (30000 - 8709) * 180 / 30000
    # and then into radians
    theta = theta * math.pi / 180
    x = h + r*math.cos(theta)
    y = k + r*math.sin(theta)
    path_new = 'M 0.235 0.5 L ' + str(x) + ' ' + str(y) + ' L 0.245 0.5 Z'


    layout = {
        'autosize': True,
        #'width': 208,
        #'height': 130.6,
        'margin': {
            'l': 150,
            'r':15,
            'b':0,
            't':15,
            'pad':4
        },
        'xaxis': {
            'showticklabels': False,
            'showgrid': False,
            'zeroline': False,
        },
        'yaxis': {
            'showticklabels': False,
            'showgrid': False,
            'zeroline': False,
        },
        'shapes': [
            {
                'type': 'path',
                'path': path_new,
                'fillcolor': 'rgb(224,18,115)',
                'line': {
                    'width': 0.5
                },
                'xref': 'paper',
                'yref': 'paper'
            }
        ],
        'annotations': [
            {
                'xref': 'paper',
                'yref': 'paper',
                'x': 0.23,
                'y': 0.45,
                'text': '',
                'showarrow': False
            }
        ]
    }
    # we don't want the boundary now
    base_chart['marker']['line']['width'] = 0
    return dict(data=[base_chart, meter_chart], layout=layout)



#2 Progress Wheel Chart

def progress_wheel_chart(fund_name):
    base_chart = {
        "values": [65, 13, 13, 13, 13, 13],
        "labels": ["-", "13", "26", "39", "52", "65"],
        "domain": {"x": [0, .48]},
        "marker": {
            "colors": [
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)'
            ],
            "line": {
                "width": 1
            }
        },
        "name": "Gauge",
        "hole": .4,
        "type": "pie",
        "direction": "clockwise",
        "rotation": 108,
        "showlegend": False,
        "hoverinfo": "none",
        "textinfo": "label",
        "textposition": "outside"
    }

    meter_chart = {
        "values": [65, 13, 13, 13, 13, 13],
        "labels": ["-", "20%", "40%", "60%", "80%", "Nearly There!"],
        "marker": {
            'colors': [
                'rgb(255, 255, 255)',
                'rgb(225,242,223)',
                'rgb(191,227,187)',
                'rgb(156,212,150)',
                'rgb(122,198,114)',
                'rgb(88,183,78)'
            ]
        },
        "domain": {"x": [0, 0.48]},
        "name": "Gauge",
        "hole": .3,
        "type": "pie",
        "direction": "clockwise",
        "rotation": 90,
        "showlegend": False,
        "textinfo": "label",
        "textposition": "inside",
        "hoverinfo": "none"
    }
    h = 0.24
    k = 0.5
    r = 0.15
    my_raw_value=80
    # Map my_raw_value to degrees. my_raw_value is between 0 and 300
    theta = (65 - 11) * 180 / 65
    # and then into radians
    theta = theta * math.pi / 180
    x = h + r*math.cos(theta)
    y = k + r*math.sin(theta)
    path_new = 'M 0.235 0.5 L ' + str(x) + ' ' + str(y) + ' L 0.245 0.5 Z'


    layout = {
        'autosize': True,
        #'width': 208,
        #'height': 130.6,
        'margin': {
            'l': 150,
            'r':15,
            'b':0,
            't':15,
            'pad':4
        },
        'xaxis': {
            'showticklabels': False,
            'showgrid': False,
            'zeroline': False,
        },
        'yaxis': {
            'showticklabels': False,
            'showgrid': False,
            'zeroline': False,
        },
        'shapes': [
            {
                'type': 'path',
                'path': path_new,
                'fillcolor': 'rgb(224,18,115)',
                'line': {
                    'width': 0.5
                },
                'xref': 'paper',
                'yref': 'paper'
            }
        ],
        'annotations': [
            {
                'xref': 'paper',
                'yref': 'paper',
                'x': 0.23,
                'y': 0.45,
                'text': '',
                'showarrow': False
            }
        ]
    }
    # we don't want the boundary now
    base_chart['marker']['line']['width'] = 0
    return dict(data=[base_chart, meter_chart], layout=layout)





#Acquisition_chart function

def acquisition_chart(unjasoned_data):
    unjasoned_jasoned_data=json.loads(unjasoned_data)
    unjasoned_df=pd.DataFrame.from_dict(unjasoned_jasoned_data)
    aquisition_source=unjasoned_df[['state','utm_source']]
    Facebook_Mapping = {'':'Organic','intercom': 'Intercom','FacebookPaid_GIY': 'FacebookAds','FacebookPaid_IdeaFund': 'FacebookAds', 'FacebookPaid_Poetry': 'FacebookAds','FacebookPaid_MNFund': 'FacebookAds','FacebookPaid_WelcomingWeek': 'FacebookAds','FacebookPaid_StreetFeast': 'FacebookAds','FacebookPaid_Kaboom': 'FacebookAds','FacebookPaid_MensShed': 'FacebookAds'}
    mapped_aquisition_source=aquisition_source['utm_source'].map(Facebook_Mapping)
    mapped_aquisition_source_active=pd.concat([aquisition_source.drop(['utm_source'], axis=1), mapped_aquisition_source], axis=1)
    mapped_aquisition_source_active.groupby('utm_source').count()

    temp_aquisition = mapped_aquisition_source_active["utm_source"].value_counts()

    temp_y0 = []
    temp_y1 = []
    for val in temp_aquisition.index:
        true_y0=(mapped_aquisition_source_active[mapped_aquisition_source_active["utm_source"]==val] =='paid') | (mapped_aquisition_source_active[mapped_aquisition_source_active["utm_source"]==val] =='approved')
        temp_y0.append(np.sum(true_y0['state']))

        true_y1=(mapped_aquisition_source_active[mapped_aquisition_source_active["utm_source"]==val] =='failed') | (mapped_aquisition_source_active[mapped_aquisition_source_active["utm_source"]==val] =='rejected')
        temp_y1.append(np.sum(true_y1['state']))

    trace2 = go.Bar(
        x = temp_aquisition.index,
        y = temp_y1,
        marker=dict(
                color='rgb(88,183,78)',
                ),
        name='Failed Projects'
    )
    trace3 = go.Bar(
        x = temp_aquisition.index,
        y = temp_y0,
        marker=dict(
                color='rgb(224,18,115)',
                ),
        name='Paid Projects'
    )

    aquisition_data = [trace2, trace3]
    acqusition_layout = go.Layout(
        #title = "Number of Paid Projects By Aquisition Source",
        barmode='stack',
        autosize=True,
        margin=go.layout.Margin(
            l=40,
            r=40,
            b=40,
            t=40,
            pad=4
            )
    )
    return go.Figure(data=aquisition_data, layout=acqusition_layout)





#3 Starter Map Chart

def map_chart(filtered_accounts_applications):
    unjasoned_data=json.loads(filtered_accounts_applications)
    filtered_accounts_applications_df=pd.DataFrame.from_dict(unjasoned_data)
    site_lat = filtered_accounts_applications_df.latitude
    site_lon = filtered_accounts_applications_df.longitude
    locations_name = filtered_accounts_applications_df.location_name
    map_data = [
    go.Scattermapbox(
        lat=site_lat,
        lon=site_lon,
        mode='markers',
        marker=dict(
            size=9,
            color='rgb(224, 18, 115)',
            opacity=0.7
        ),
        text=locations_name,
        hoverinfo='text'
    ),
    ]

    map_layout = go.Layout(
        autosize=True,
        hovermode='closest',
        showlegend=False,
        margin=go.layout.Margin(
            l=15,
            r=15,
            b=15,
            t=15,
            pad=4
        ),
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=46,
            lon=-92
        ),
        pitch=0,
        zoom=5,
        style='light'
        ),
    )
    return dict(data=map_data, layout=map_layout)




def active_funnel_chart(applications_steps):
    temp_application_steps = applications_steps["step_type"].value_counts()

    trace1 = go.Bar(
        x = temp_application_steps.index,
        y = temp_application_steps.values,
        marker=dict(
                color='rgb(88,183,78)',
                ),
        name='Fund Starters'
    )
    plot_layout = go.Layout(
        autosize=True,
        #width=450,
        #height=250,
        barmode='stack',
        margin=go.layout.Margin(
            l=40,
            r=40,
            b=40,
            t=40,
            pad=4
            )
        )
    return go.Figure(data=[trace1], layout=plot_layout)





##=======4.0 HTML LAYOUT===========

layout = [

    html.Div([
        dcc.Store(id='memory_output', storage_type='local'),

    ]),

    # top controls
    html.Div(
        [
            html.Div(
                dcc.Dropdown(
                    id="fund_slug_dropdown",
                    options=[
                        {"label": "Minnesota_Fund", "value": 10.0},
                        {"label": "AIB_Cork_Fund", "value": 24.0},
                    ],
                    value=10.0,
                    clearable=False,
                ),
                className="two columns",
            ),

            html.Div(
                dcc.Dropdown(
                    id="state_dropdown",
                    options=[
                        {"label": "Allocated", "value": "allocated"},
                        {"label": "Rejected", "value": "rejected"},
                        {"label": "Failed", "value": "failed"},
                        {"label": "Succeeded", "value": "succeeded"},
                        {"label": "Paid", "value": "paid"},
                        {"label": "Active", "value": "active"},
                        {"label": "All", "value": "all"},



                    ],
                    value="all",
                    clearable=False,
                ),
                className="two columns",
            ),
            html.Div(
                dcc.Dropdown(
                    id="fund_name_dropdown",
                    options=[
                        {"label": "Minnesota Fund", "value": "greaterminnesotafund"},
                        {"label": "AIB Cork Fund", "value": "None"},
                        {"label": "Microsoft Arizona", "value": "microsoft"},

                    ],
                    value="greaterminnesotafund",
                    clearable=False,
                ),
                className="two columns",
            ),


        ],
        className="row",
        style={"marginBottom": "10"},
    ),

    # Hidden div inside the app that stores the intermediate values
    #html.Div(id='delivery_cost_id', style={'display': 'none'}),

    # indicators row div
    html.Div(
        [
            indicator_four(
                "#00cc96", "Budeget Remaining", "budget_remaining_id"
            ),
            indicator_four(
                "#119DFF", "Delivery Cost", "delivery_cost_id"
            ),
            indicator_four(
                "#EF553B", "Number of Active", "number_active_id",
            ),
        ],
        className="row",
    ),


    #Top Row of Charts DIV
    html.Div(
        [
            html.Div(
                [
                    html.P("Project Budget"),
                    dcc.Graph(
                        id="budget_wheel_chart_id",
                        style={
                        "height": "90%",
                        "width": "98%"
                        },
                        #figure=wheel_fig,
                        config=dict(displayModeBar=False),
                    )
                ],
                className="four columns chart_div",
                ),

            html.Div(
                [
                    html.P("Project Costs"),
                        dcc.Graph(
                            id='project_costs_id',
                            style={"height": "90%", "width": "98%"},
                            config=dict(displayModeBar=False),
                            )
                            ],
                className="four columns chart_div"
            ),


            html.Div(
                [
                    html.P("Progress(#Active Projects)"),
                    dcc.Graph(
                        id="progress_wheel_chart_id",
                        style={
                        "height": "90%",
                        "width": "98%"
                        },
                        #figure=wheel_fig,
                        config=dict(displayModeBar=False),
                    )
                ],
                className="four columns chart_div",
                ),

        ],
        className="row",
        style={"marginTop": "5px"}
    ),



#Second Indicators row div
html.Div(
    [
        indicator_one(
            "#00cc96", "Total Ad Spend", "total_ad_spend_id"
        ),
        indicator_one(
            "#119DFF", "Ad Spend/Approved", "ad_cost_per_approved_id"
        ),
        indicator_one(
            "#EF553B", "Ad Spend Per Active", "cost_per_active_id"
        ),
        indicator_one(
            "#00cc96", "#Waiting on Pack", "waiting_on_pack_id"
        ),
        indicator_one(
            "#119DFF", "#Calls Scheduled", "waiting_call_id"
        ),
        indicator_one(
            "#EF553B",
            "Pack Wait (Days)",
            "pack_wait_time_id",
        ),
        indicator_one(
            "#00cc96", "Fund Left", "fund_left_id"
        ),
        indicator_one(
            "#119DFF", "Paid Out", "paid_out_id"
        ),
        indicator_one(
            "#EF553B", "Allocated", "allocated_funding_id",
        ),
    ],
    className="row",
    style={"marginTop": "5px"}
),




    #charts row div
    html.Div(
        [
            html.Div(
                [
                    html.P("Active Starter Funnel"),
                    dcc.Graph(
                        id="active_funnel",
                        style={
                        "height": "90%",
                        "width": "98%"
                        },
                        config=dict(displayModeBar=False),
                    )
                ],
                className="four columns chart_div",
                ),

            html.Div(
                [
                    html.P("Fund Starter Map"),
                        dcc.Graph(
                            id='starter_map',
                            style={"height": "90%", "width": "98%"},
                            config=dict(displayModeBar=False),
                            )
                            ],
                className="four columns chart_div"
            ),


            html.Div(
                [
                    html.P("Starter Acquisition Source"),
                    dcc.Graph(
                        id='acquisition_source',
                        style={"height": "90%", "width": "98%"},
                        config=dict(displayModeBar=False),
                        )
                ],
                className="four columns chart_div",
                ),

        ],
        className="row",
        style={"marginTop": "5px"}
    ),



    # 3 x Tables Div

    # tables row div
    html.Div(
        [
            html.Div(
                [
                    html.P(
                        "Idea Demand",
                        style={
                            "color": "#2a3f5f",
                            "fontSize": "13px",
                            "textAlign": "center",
                            "marginBottom": "0",
                        },
                    ),
                    html.Div(
                        id="idea_demand_id",
                        style={"padding": "0px 13px 5px 13px", "marginBottom": "5"},
                    ),

                ],
                className="four columns",
                style={
                    "backgroundColor": "white",
                    "border": "1px solid #C8D4E3",
                    "borderRadius": "3px",
                    "height": "100%",
                    "overflowY": "scroll",
                },
            ),
            html.Div(
                [
                    html.P(
                        "Groups By Stage",
                        style={
                            "color": "#2a3f5f",
                            "fontSize": "13px",
                            "textAlign": "center",
                            "marginBottom": "0",
                        },
                    ),
                    html.Div(
                        id="groups_per_state",
                        style={"padding": "0px 13px 5px 13px", "marginBottom": "5"},
                    )
                ],
                className="four columns",
                style={
                    "backgroundColor": "white",
                    "border": "1px solid #C8D4E3",
                    "borderRadius": "3px",
                    "height": "100%",
                    "overflowY": "scroll",
                },
            ),

            html.Div(
                [
                    html.P(
                        "Starters Per Idea",
                        style={
                            "color": "#2a3f5f",
                            "fontSize": "13px",
                            "textAlign": "center",
                            "marginBottom": "0",
                        },
                    ),
                    html.Div(
                        id="staters_per_idea_id",
                        style={"padding": "0px 13px 5px 13px", "marginBottom": "5"},
                    )
                ],
                className="four columns",
                style={
                    "backgroundColor": "white",
                    "border": "1px solid #C8D4E3",
                    "borderRadius": "3px",
                    "height": "100%",
                    "overflowY": "scroll",
                },
            ),



        ],
        className="row",
        style={"marginTop": "5px", "max height": "200px"},
    ),






    # Main applicant tables row div
    html.Div(
        [
            html.Div(
                [
                    html.P(
                        "Fund Applicants",
                        style={
                            "color": "#2a3f5f",
                            "fontSize": "13px",
                            "textAlign": "center",
                            "marginBottom": "0",
                        },
                    ),
                    html.Div(
                        id="starter_applicant_table",
                        style={"padding": "0px 13px 5px 13px", "marginBottom": "5"},
                    ),

                ],
                className="row",
                style={
                    "backgroundColor": "white",
                    "border": "1px solid #C8D4E3",
                    "borderRadius": "3px",
                    "height": "100%",
                    "overflowY": "scroll",
                },
            ),



        ],
        className="row",
        style={"marginTop": "5px", "max height": "200px"},
    ),



]









##=======5.0 CALLBACK FUNCTIONS===========



# updates First Row left indicator
@app.callback(Output("budget_remaining_id", "children"),
            [Input("fund_slug_dropdown", "value"),
            Input("delivery_cost_id", "children")])

def budget_remaining_callback(fund_account_number, project_cost):
    total_project_budget= 30000
    delivery_cost_unjasoned= json.loads(project_cost)
    budget_remaining = total_project_budget - delivery_cost_unjasoned

    budget_remaining_rounded=round(budget_remaining)
    return  to_dollar(budget_remaining_rounded)





# updates first row middle indicator value based on df updates
@app.callback(
    Output("delivery_cost_id", "children"),
    [Input("fund_slug_dropdown", "value"),
     Input("total_ad_spend_id", "children"),
     Input("number_active_id", "children")],
)
def delivery_cost_indicator_callback(fund_slug_value, total_ad_spend, number_active_groups):
    fund_slug_dropdown=fund_slug_value
    total_ad_spend_unjasoned= json.loads(total_ad_spend)
    total_pack_costs = json.loads(number_active_groups) * 16.00
    team_size=2
    number_weeks=52
    days_per_week=1
    cost_per_day= (40000.0/52)/5
    total_staff_costs=team_size*number_weeks*days_per_week*cost_per_day
    total_costs= total_ad_spend_unjasoned +total_pack_costs + total_staff_costs
    return json.dumps(total_costs)



# updates first row right indicator value based on df updates
@app.callback(
    Output("number_active_id", "children"),
    [Input("fund_slug_dropdown", "value")],
)
def total_active_callback(fund_slug_value):
    filtered_accounts = account_options[account_options['parent_account_id']==fund_slug_value]
    paid_accounts=filtered_accounts[filtered_accounts['state']=='paid']
    number_active_groups=paid_accounts['state'].value_counts().values[0]
    number_active_float=number_active_groups.astype(np.float64)
    return json.dumps(number_active_float)




# updates Second Row Eight Indicator (Paid Out)

@app.callback(
    Output("paid_out_id", "children"), [Input("fund_slug_dropdown", "value")],
)
def fund_paid_out_callback(fund_id):
    filtered_accounts = account_options[account_options['parent_account_id']==fund_id]
    filtered_list_of_accounts=filtered_accounts['id'].tolist()
    filtered_fund_paid_accounts=accounts[accounts['parent_account_id'].isin(filtered_list_of_accounts)]
    total_paid_out=filtered_fund_paid_accounts['balance_cents'].sum()/100
    return to_dollar(total_paid_out)








# updates Second Row First Indicator (Total Ad Spend)
@app.callback(
    Output("total_ad_spend_id", "children"), [Input("fund_slug_dropdown", "value")]
)
def total_ad_spend_callback(fund_namee):
    fund_name=fund_namee
    ad_insights = pd.read_sql_query("""SELECT spend FROM facebook_ads.insights  WHERE ad_id IN (SELECT id FROM facebook_ads.ads  WHERE adset_id IN (SELECT id FROM facebook_ads.ad_sets  WHERE campaign_id IN (SELECT id FROM facebook_ads.campaigns  WHERE name LIKE %s ))) """ , facebook_engine,params=("%MN Fund%",))
    total_ad_spend=ad_insights['spend'].sum()
    rounded_total_ad_spend=round(total_ad_spend)
    return json.dumps(rounded_total_ad_spend)




# updates Second Row Second Indicator (Cost Per Approved Starter)
@app.callback(
    Output("ad_cost_per_approved_id", "children"),
     [Input("total_ad_spend_id", "children"),
     Input('memory_output', 'data')],
)
def ad_cost_approved_callback(total_ad_spend, filtered_accounts_applications):
    unjasoned_filtered_accounts_applications=json.loads(filtered_accounts_applications)
    filtered_accounts_applications_df=pd.DataFrame.from_dict(unjasoned_filtered_accounts_applications)
    aquisition_source=filtered_accounts_applications_df[['state','utm_source']]
    Facebook_Mapping = {'':'Organic','intercom': 'Intercom','FacebookPaid_GIY': 'FacebookAds','FacebookPaid_IdeaFund': 'FacebookAds', 'FacebookPaid_Poetry': 'FacebookAds','FacebookPaid_MNFund': 'FacebookAds','FacebookPaid_WelcomingWeek': 'FacebookAds','FacebookPaid_StreetFeast': 'FacebookAds','FacebookPaid_Kaboom': 'FacebookAds','FacebookPaid_MensShed': 'FacebookAds'}
    mapped_aquisition_source=filtered_accounts_applications_df['utm_source'].map(Facebook_Mapping)
    mapped_aquisition_source_active=pd.concat([aquisition_source.drop(['utm_source'], axis=1), mapped_aquisition_source], axis=1)
    facebook_approved_starters=mapped_aquisition_source_active[mapped_aquisition_source_active['utm_source'] == 'FacebookAds']
    number_fb_approved=facebook_approved_starters['utm_source'].count()
    total_ad_spend=json.loads(total_ad_spend)
    cost_per_approved=total_ad_spend/number_fb_approved
    return to_dollar(cost_per_approved)



# updates Second Row Third Indicator (Cost Per Active Starter)
@app.callback(
    Output("cost_per_active_id", "children"),
     [Input("total_ad_spend_id", "children"),
     Input("number_active_id", "children")]
)

def ad_cost_active_callback(total_ad_spend, number_active):
    cost_per_active_starter=json.loads(total_ad_spend)/json.loads(number_active)
    return to_dollar(cost_per_active_starter)




# updates Second Row Fourth Indicator (Number Waiting on Pack)

@app.callback(
    Output("waiting_on_pack_id", "children"),
    [Input('memory_output', 'data')]
)
def wait_on_pack_callback(filtered_accounts_applications):
    unjasoned_filtered_accounts_applications=json.loads(filtered_accounts_applications)
    filtered_accounts_applications_df=pd.DataFrame.from_dict(unjasoned_filtered_accounts_applications)
    non_rejected_applicants=filtered_accounts_applications_df[filtered_accounts_applications_df['state']!='rejected']
    want_starter_pack=non_rejected_applicants[non_rejected_applicants['receive_starter_pack']==True]
    number_want_pack=want_starter_pack['receive_starter_pack'].count()
    number_received_pack=non_rejected_applicants['starter_pack_sent_at'].count()
    waiting_on_pack=number_want_pack-number_received_pack

    return waiting_on_pack



# updates Second Row Fifth Indicator (Number Waiting on Call)

@app.callback(
    Output("waiting_call_id", "children"),
    [Input('memory_output', 'data')]
)
def wait_on_call_callback(filtered_accounts_applications):
    unjasoned_filtered_accounts_applications=json.loads(filtered_accounts_applications)
    filtered_accounts_applications_df=pd.DataFrame.from_dict(unjasoned_filtered_accounts_applications)
    number_starters_called=filtered_accounts_applications_df['received_starter_call_at'].count()

    return number_starters_called




# updates Second Row Sixth Indicator (Number Waiting on Pack)

@app.callback(
    Output("pack_wait_time_id", "children"),
    [Input('memory_output', 'data')]
)
def pack_wait_time_callback(filtered_accounts_applications):
#    unjasoned_filtered_accounts_applications=json.loads(filtered_accounts_applications)
#    filtered_accounts_applications_df=pd.DataFrame.from_dict(unjasoned_filtered_accounts_applications)
#    print(filtered_accounts_applications_df)
#    non_rejected_applicants=filtered_accounts_applications_df[filtered_accounts_applications_df['state']!='rejected']
#    want_starter_pack=non_rejected_applicants[non_rejected_applicants['receive_starter_pack']==True]
#    pack_wait_time=want_starter_pack['starter_pack_sent_at'] - want_starter_pack['created_at']
#    average_wait_time=pack_wait_time.mean()
#    #average_wait_time=average_wait_time.days
    return 10


# updates Second Row Sevent Indicator (Fund Left )

@app.callback(
    Output("fund_left_id", "children"), [Input("fund_name_dropdown", "value"), Input("fund_slug_dropdown", "value")]
)
def fund_left_callback(fund_name_slug, fund_account_number):
    filtered_accounts = account_options[account_options['parent_account_id']==fund_account_number]
    filtered_list_of_accounts=filtered_accounts['id'].tolist()
    filtered_fund_paid_accounts=accounts[accounts['parent_account_id'].isin(filtered_list_of_accounts)]
    total_paid_out=filtered_fund_paid_accounts['balance_cents'].sum()/100

    #Import User Orders Tables
    user_order = pd.read_sql('SELECT slug, options, replications FROM user_orders', engine)
    split_user_options = user_order['options'].apply(pd.Series)
    user_order_options=pd.concat([user_order.drop(['options'], axis=1), split_user_options], axis=1)
    fund_row=user_order_options.loc[user_order_options['slug'] == fund_name_slug]
    row_index=fund_row.index
    fund_budget=user_order_options.loc[row_index]['amount'].iloc[0]
    fund_remaining=fund_budget-total_paid_out
    return to_dollar(fund_remaining)






# updates Second Row Ninth Indicator (Allocated)
@app.callback(
    Output("allocated_funding_id", "children"), [Input("fund_slug_dropdown", "value")]
)
def fund_allocated_callback(fund_namee):
    filtered_accounts = account_options[account_options['parent_account_id']==fund_namee]
    allocated_accounts=filtered_accounts[(filtered_accounts['state']=='allocated') | (filtered_accounts['state']=='approved')]
    total_allocated=allocated_accounts['balance_cents'].sum()/100
    return to_dollar(total_allocated)



# update budget wheel chart
@app.callback(
    Output("budget_wheel_chart_id", "figure"),
    [Input("fund_slug_dropdown", "value")],
)
def budget_wheel_callback(fund_name):
    return wheel_chart(fund_name)


# update project progress wheel chart
@app.callback(
    Output("progress_wheel_chart_id", "figure"),
    [Input("fund_slug_dropdown", "value")],
)
def progress_wheel_callback(fund_name):
    return progress_wheel_chart(fund_name)




# update dotted map figure based on fund selected in dropdown
@app.callback(
    Output("starter_map", "figure"),
    [Input('memory_output', 'data')],
)
def map_callback(filtered_accounts_applications):
    return map_chart(filtered_accounts_applications)


# update active starter funnel based on fund selected in dropdown
@app.callback(
    Output("active_funnel", "figure"),
    [Input('memory_output', 'data')],
)
def funnel_callback(filtered_accounts_applications):
    unjasoned_filtered_accounts_applications=json.loads(filtered_accounts_applications)
    filtered_accounts_applications_df=pd.DataFrame.from_dict(unjasoned_filtered_accounts_applications)
    list_of_locations=filtered_accounts_applications_df['solution_location_id'].tolist()

    onboarding_steps = pd.read_sql('SELECT * FROM onboarding_steps', engine)
    completed_onboarding_steps = pd.read_sql('SELECT * FROM completed_onboarding_steps', engine)
    merged_onboarding_steps=completed_onboarding_steps.merge(onboarding_steps, left_on='onboarding_step_id', right_on='id')

    applications_steps=merged_onboarding_steps[merged_onboarding_steps['location_id'].isin(list_of_locations)]

    return active_funnel_chart(applications_steps)


# update acquisition figure based on fund selected in dropdown
@app.callback(
    Output("acquisition_source", "figure"),
    [Input('fund_slug_dropdown', 'value'),
    Input('memory_output', 'data')])

def acquisition_callback(fund_account_value,data):
    return acquisition_chart(data)


# update project costs Pie Chart breakdown
@app.callback(
    Output("project_costs_id", "figure"),
    [Input("fund_slug_dropdown", "value"),
     Input("total_ad_spend_id", "children"),
     Input("number_active_id", "children")]
)
def project_costs_callback(fund_account_value, total_ad_spend, total_active):
    return project_costs_chart(fund_account_value, total_ad_spend, total_active)




#Update Idea Demand Table

@app.callback(
    Output("idea_demand_id", "children"),
    [Input("fund_slug_dropdown", "value"),
    Input('memory_output', 'data')],
)
def idea_demand_table_callback(fund_namee, data):
    unjasoned_filtered_accounts_applications=json.loads(data)
    filtered_accounts_applications_df=pd.DataFrame.from_dict(unjasoned_filtered_accounts_applications)

    filtered_accounts_paid = filtered_accounts_applications_df[filtered_accounts_applications_df['state']=='paid']
    count_filtered_accounts=filtered_accounts_paid['solution_id'].value_counts()
    count_filtered_accounts_df=count_filtered_accounts.to_frame(name='active_groups')


    campaign_spend = pd.read_sql_query('SELECT campaigns.name, insights.spend FROM facebook_ads.insights INNER JOIN facebook_ads.ads ON insights.ad_id = ads.id INNER JOIN facebook_ads.ad_sets ON ads.adset_id = ad_sets.id INNER JOIN facebook_ads.campaigns ON ad_sets.campaign_id = campaigns.id WHERE campaigns.name LIKE %s' , facebook_engine,params=("%MN Fund%",))
    idea_mapping = {'Cycling Without Age (MN Fund)':71,'GIY (Bluecross MN Fund #2)':78,'GIY MN Fund': 78, 'Kaboom (MN Fund)':10, "Men's Shed (MN Fund)": 48,'Poetry in Park (Bluecross MN Fund #2)':61,'Poetry in Park (MN Fund)': 61,'Repair Cafe (Bluecross MN Fund #2)':73,'Repair Café (MN Fund)':73,'Street Feast Bluecross (MN Fund #2)':65,'StreetFeast  (MN Fund)': 65}
    campaign_spend['name']=campaign_spend['name'].map(idea_mapping)
    total_spend_per_idea=campaign_spend.groupby('name').sum()
    solutions = pd.read_sql('SELECT id, name FROM solutions', engine)
    total_spend_per_idea_name=total_spend_per_idea.merge(solutions, left_index=True, right_on='id')

    spend_per_active=total_spend_per_idea_name.merge(count_filtered_accounts_df, left_on='id', right_index=True)
    spend_per_active['cost_per_active']=spend_per_active['spend']/spend_per_active['active_groups']

    aquisition_source_idea=filtered_accounts_applications_df[['state','utm_source','solution_id']]
    Facebook_Mapping = {'':'Organic','intercom': 'Intercom','FacebookPaid_GIY': 'FacebookAds','FacebookPaid_IdeaFund': 'FacebookAds', 'FacebookPaid_Poetry': 'FacebookAds','FacebookPaid_MNFund': 'FacebookAds','FacebookPaid_WelcomingWeek': 'FacebookAds','FacebookPaid_StreetFeast': 'FacebookAds','FacebookPaid_Kaboom': 'FacebookAds','FacebookPaid_MensShed': 'FacebookAds'}
    mapped_aquisition_source_idea=aquisition_source_idea['utm_source'].map(Facebook_Mapping)
    mapped_aquisition_source_active_idea=pd.concat([aquisition_source_idea.drop(['utm_source'], axis=1), mapped_aquisition_source_idea], axis=1)
    fb_approved_per_idea=mapped_aquisition_source_active_idea[mapped_aquisition_source_active_idea['utm_source']=='FacebookAds']
    approved_per_idea=fb_approved_per_idea['solution_id'].value_counts()
    approved_per_idea_df=approved_per_idea.to_frame(name='approved')

    total_spend_approved_active=spend_per_active.merge(approved_per_idea_df, left_on='id', right_index=True)
    total_spend_approved_active['cost_per_approved']=total_spend_approved_active['spend'] / total_spend_approved_active['approved']
    total_spend_approved_active['Failed Multiplier']=total_spend_approved_active['cost_per_active'] / total_spend_approved_active['cost_per_approved']
    ad_performance_table=total_spend_approved_active[['name','spend','cost_per_approved','cost_per_active','Failed Multiplier']]
    cols = ['spend','cost_per_approved','cost_per_active','Failed Multiplier']
    ad_performance_table[cols]=ad_performance_table[cols].applymap(np.int64)

    return df_to_table(ad_performance_table)




#Update Starters Per Idea Table

@app.callback(
    Output("staters_per_idea_id", "children"),
    [Input("fund_slug_dropdown", "value")],
)
def idea_starters_table_callback(fund_namee):
    solution_name_ids = pd.read_sql('SELECT id, name FROM solutions', engine)
    filtered_accounts = account_options[account_options['parent_account_id']==fund_namee]
    filtered_accounts_paid = filtered_accounts[filtered_accounts['state']=='paid']
    count_filtered_accounts=filtered_accounts_paid['solution_id'].value_counts()
    count_filtered_accounts_df=count_filtered_accounts.to_frame(name='#Active')

    filtered_accounts_allocated = filtered_accounts[filtered_accounts['state']!= 'paid']
    count_filtered_accounts_allocated=filtered_accounts_allocated['solution_id'].value_counts()
    count_filtered_accounts_allocated_df=count_filtered_accounts_allocated.to_frame(name='#Allocated')

    merged_active_names=count_filtered_accounts_df.merge(solution_name_ids, left_index=True, right_on='id')
    merged_active_approved=merged_active_names.merge(count_filtered_accounts_allocated_df, left_on='id', right_index=True)
    active_ideas=merged_active_approved[['name','#Allocated','#Active']]

    active_ideas_table=df_to_table(active_ideas)
    return active_ideas_table



# updates starter applicant table based on 'State' df updates
@app.callback(
    Output("groups_per_state", "children"),
    [Input("fund_slug_dropdown", "value")],
)
def group_stages_callback(fund_account_number):
        filtered_accounts = account_options[account_options['parent_account_id']==fund_account_number]
        state_count=filtered_accounts['state'].value_counts()
        state_count_df=state_count.to_frame(name='#Groups')
        state_count_df.reset_index(level=0, inplace=True)
        state_count_df.columns =['State','#Groups']

        state_count_table=df_to_table(state_count_df)
        return state_count_table




# updates starter applicant table based on 'State' df updates
@app.callback(
    Output("starter_applicant_table", "children"),
    [Input("state_dropdown", "value"), Input("fund_slug_dropdown", "value")],
)
def table_state_callback(state, fund_account_number):
        table_state=fund_account_number
        return table_state



# Callback to read in accounts_applications_users and store in new store dash_core_component
@app.callback(
    Output('memory_output', 'data'),
    [Input("fund_slug_dropdown", "value")])

def applicant_data_callback(fund_account_number):
        accounts_applications = pd.read_sql("SELECT accounts.balance_cents, accounts.parent_account_id, accounts.state, solution_applications.first_name, solution_applications.last_name, solution_applications.created_at, solution_applications.location_name, solution_applications.solution_id, solution_applications.solution_location_id, solution_applications.latitude, solution_applications.longitude, solution_applications.utm_source, solution_applications.receive_starter_pack, solution_applications.starter_pack_sent_at, solution_applications.received_starter_call_at  FROM accounts INNER JOIN solution_applications ON (accounts.options->>'location_id')::int = solution_applications.solution_location_id", engine)
        data = accounts_applications[accounts_applications['parent_account_id']==fund_account_number]
        return data.to_json()
