# -*- coding: utf-8 -*-
import flask
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
from plotly import graph_objs as go
import plotly.graph_objs as go

from datetime import date
from datetime import datetime
import dateutil.parser

import pandas as pd
import json
from json import encoder
import numpy as np
import math
from money import Money

import psycopg2
from sqlalchemy import create_engine

from app import app, indicator_one, indicator_four, millify, df_to_table
mapbox_access_token = 'pk.eyJ1IjoibmlhbGxjaGFuZ2V4IiwiYSI6ImNqbHFyc2FjaTJjYXUza3Biem9tamw2enEifQ.iy0uUg8EKAYaFbZuN1iodw'





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

def budget_wheel_chart(fund_name):
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
    theta = (30000 - 15000) * 180 / 30000
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
                'text': '50',
                'showarrow': False
            }
        ]
    }
    # we don't want the boundary now
    base_chart['marker']['line']['width'] = 0
    return dict(data=[base_chart, meter_chart], layout=layout)



##=======4.0 HTML LAYOUT===========

layout = [

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
                    html.P("Project Progress"),
                    dcc.Graph(
                        id="budget_wheel_chart_id_2",
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
                        "Top Lost opportunities",
                        style={
                            "color": "#2a3f5f",
                            "fontSize": "13px",
                            "textAlign": "center",
                            "marginBottom": "0",
                        },
                    ),
                    html.Div(
                        id="top_lost_opportunities",
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
    return  budget_remaining





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
    return total_paid_out








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
    Output("ad_cost_per_approved_id", "children"), [Input("fund_slug_dropdown", "value")]
)
def ad_cost_approved_callback(fund_namee):
    cost_per_approved_starter_eur_amount=fund_namee
    return cost_per_approved_starter_eur_amount



# updates Second Row Third Indicator (Cost Per Active Starter)
@app.callback(
    Output("cost_per_active_id", "children"),
     [Input("total_ad_spend_id", "children"),
     Input("number_active_id", "children")],
)

def ad_cost_active_callback(total_ad_spend, number_active):
    cost_per_active_starter=json.loads(total_ad_spend)/json.loads(number_active)
    return cost_per_active_starter




# updates Second Row Fourth Indicator (Number Waiting on Pack)

@app.callback(
    Output("waiting_on_pack_id", "children"), [Input("fund_slug_dropdown", "value")]
)
def wait_on_pack_callback(fund_namee):
    waiting_on_pack=fund_namee
    return waiting_on_pack



# updates Second Row Fifth Indicator (Number Waiting on Call)

@app.callback(
    Output("waiting_call_id", "children"), [Input("fund_slug_dropdown", "value")]
)
def wait_on_call_callback(fund_namee):
    number_waiting_call=fund_namee
    return number_waiting_call




# updates Second Row Sixth Indicator (Number Waiting on Pack)

@app.callback(
    Output("pack_wait_time_id", "children"), [Input("fund_slug_dropdown", "value")]
)
def pack_wait_time_callback(fund_namee):
    pack_wait_days=fund_namee
    return pack_wait_days




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
    return fund_remaining






# updates Second Row Ninth Indicator (Allocated)
@app.callback(
    Output("allocated_funding_id", "children"), [Input("fund_slug_dropdown", "value")]
)
def fund_allocated_callback(fund_namee):
    filtered_accounts = account_options[account_options['parent_account_id']==fund_namee]
    allocated_accounts=filtered_accounts[(filtered_accounts['state']=='allocated') | (filtered_accounts['state']=='approved')]
    total_allocated=allocated_accounts['balance_cents'].sum()/100
    return total_allocated



# update budget wheel chart
@app.callback(
    Output("budget_wheel_chart_id", "figure"),
    [Input("fund_slug_dropdown", "value")],
)
def budget_wheel_callback(fund_name):
    return budget_wheel_chart(fund_name)






# update dotted map figure based on fund selected in dropdown
@app.callback(
    Output("starter_map", "figure"),
    [Input("fund_slug_dropdown", "value")],
)
def map_callback(fund_name):
    fund=fund_name
    return fund


# update active starter funnel based on fund selected in dropdown
@app.callback(
    Output("active_funnel", "figure"),
    [Input("fund_slug_dropdown", "value")],
)
def funnel_callback(fund_account):
    active_fund=fund_account
    return active_fund


# update acquisition figure based on fund selected in dropdown
@app.callback(
    Output("acquisition_source", "figure"),
    [Input("fund_slug_dropdown", "value")],
)
def acquisition_callback(fund_account_value):
    fund_account=fund_account_value
    return fund_account


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
    [Input("fund_slug_dropdown", "value")],
)
def idea_demand_table_callback(fund_namee):
    table=fund_namee
    return table





#Update Starters Per Idea Table
#

@app.callback(
    Output("staters_per_idea_id", "children"),
    [Input("fund_slug_dropdown", "value")],
)
def idea_starters_table_callback(fund_namee):
    idea_starters=fund_namee
    return idea_starters





# updates starter applicant table based on 'State' df updates
@app.callback(
    Output("starter_applicant_table", "children"),
    [Input("state_dropdown", "value"), Input("fund_slug_dropdown", "value")],
)
def table_state_callback(state, fund_account_number):
        table_state=fund_account_number
        return table_state
