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

#Import User Orders Tables
user_order = pd.read_sql('SELECT slug, options FROM user_orders', engine)
split_user_options = user_order['options'].apply(pd.Series)
user_order_options=pd.concat([user_order.drop(['options'], axis=1), split_user_options], axis=1)





##=======3.0 MERGING DATA TABLES===========







##=======3.0 ANALYTICS===========








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
                        id="active_funnel_2",
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
                            id='project_costs',
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
                        id="active_funnel_3",
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
@app.callback(
    Output("budget_remaining_id", "children"), [Input("fund_slug_dropdown", "value")]
)
def budget_remaining_callback(fund_namee):
        budget_remaining_eur=fund_namee
        return budget_remaining_eur



# updates first row middle indicator value based on df updates
@app.callback(
    Output("delivery_cost_id", "children"),
    [Input("fund_slug_dropdown", "value")],
)
def delivery_cost_indicator_callback(fund_slug_value):
        total_delivery_cost_eur=fund_slug_value
        return total_delivery_cost_eur



# updates first row right indicator value based on df updates
@app.callback(
    Output("number_active_id", "children"),
    [Input("fund_slug_dropdown", "value")],
)
def total_active_callback(fund_slug_value):
    filtered_accounts = account_options[account_options['parent_account_id']==fund_slug_value]
    paid_accounts=filtered_accounts[filtered_accounts['state']=='paid']
    number_active_groups=paid_accounts['state'].value_counts().values[0]
    return number_active_groups




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
    total_ad_spend_eur_amount=fund_namee
    return total_ad_spend_eur_amount




# updates Second Row Second Indicator (Cost Per Approved Starter)
@app.callback(
    Output("ad_cost_per_approved_id", "children"), [Input("fund_slug_dropdown", "value")]
)
def ad_cost_approved_callback(fund_namee):
    cost_per_approved_starter_eur_amount=fund_namee
    return cost_per_approved_starter_eur_amount



# updates Second Row Third Indicator (Cost Per Active Starter)
@app.callback(
    Output("cost_per_active_id", "children"), [Input("fund_slug_dropdown", "value")]
)
def ad_cost_active_callback(fund_namee):
    cost_per_active_starter_eur_amount=fund_namee
    return cost_per_active_starter_eur_amount




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
    Output("fund_left_id", "children"), [Input("fund_slug_dropdown", "value")]
)
def fund_left_callback(fund_namee):
    fund_row=user_order_options.loc[user_order_options['slug'] == fund_namee]
    row_index=fund_row.index
    fund_budget=user_order_options.loc[row_index]['amount'].iloc[0]
    return fund_budget






# updates Second Row Ninth Indicator (Allocated)
@app.callback(
    Output("allocated_funding_id", "children"), [Input("fund_slug_dropdown", "value")]
)
def fund_allocated_callback(fund_namee):
    filtered_accounts = account_options[account_options['parent_account_id']==fund_namee]
    allocated_accounts=filtered_accounts[(filtered_accounts['state']=='allocated') | (filtered_accounts['state']=='approved')]
    total_allocated=allocated_accounts['balance_cents'].sum()/100
    return total_allocated




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
    Output("project_costs", "figure"),
    [Input("fund_slug_dropdown", "value")],
)
def project_costs_callback(fund_account_value):
    fund_value=fund_account_value
    return fund_value




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
