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

<<<<<<< HEAD
# Connecting to ChangeX Production PostgreSQL by providing a sqlachemy engine
engine = create_engine('postgresql://u84avvruuk8j29:paarpd5h2ndt2pf2iiaunfjcglj@ec2-52-44-72-54.compute-1.amazonaws.com/dbjqf1hr7j51et')
# Connecting to Facebook Ads PostgreSQL by providing a sqlachemy engine
||||||| merged common ancestors
=======
# Connecting to ChangeX Production PostgreSQL by providing a sqlachemy engine
engine = create_engine('postgresql://uf3hqd001negpr:p1cves5keua9t4a48dq8qqj7nuo@ec2-52-207-134-99.compute-1.amazonaws.com/d30dl84lfuo1q0')
# Connecting to Facebook Ads PostgreSQL by providing a sqlachemy engine
>>>>>>> 0cc5586a91531f10992bb2503c131818f6d17aec
facebook_engine = create_engine('postgresql://cwowexuoevajcl:4e061d2010ae798e5694efa386c7480754b708f8a3da97fd5fe659579c125f02@ec2-54-204-2-26.compute-1.amazonaws.com/dfk5g884idgiqm')



<<<<<<< HEAD


##=======2.0 IMPORT DATA TABLES===========

user_orders = pd.read_sql('SELECT * FROM user_orders', engine)                  #12 Rows
applications = pd.read_sql('SELECT * FROM solution_applications', engine)       #11860 Rows
users = pd.read_sql('SELECT * FROM users', engine)                              #22000 Rows
onboarding_steps = pd.read_sql('SELECT * FROM onboarding_steps', engine)        #102 Rows
completed_onboarding_steps = pd.read_sql('SELECT * FROM completed_onboarding_steps', engine)    #1785 Rows
locations = pd.read_sql('SELECT * FROM locations', engine)                      #15,506 Rows
user_location_roles = pd.read_sql('SELECT * FROM user_location_roles', engine)  #18,000 Rows
location_roles = pd.read_sql('SELECT * FROM location_roles', engine)            #191 Rows
authentications = pd.read_sql('SELECT * FROM authentications', engine)          #13,375 Rows
solutions = pd.read_sql('SELECT * FROM solutions', engine)                      #70 Rows
accounts = pd.read_sql('SELECT * FROM accounts', engine)                        #102 Rows
account_entries = pd.read_sql('SELECT * FROM account_entries', engine)          #355 Rows
location_invites = pd.read_sql('SELECT * FROM location_invites', engine)        #2856 Rows
#Import Facebook Ad Accounts
ad_accounts = pd.read_sql('SELECT * FROM facebook_ads.ad_accounts', facebook_engine)    #1 Row
ad_campaigns = pd.read_sql('SELECT * FROM facebook_ads.campaigns', facebook_engine)     #313 Rows
ad_sets = pd.read_sql('SELECT * FROM facebook_ads.ad_sets', facebook_engine)            #678 Rows
ads = pd.read_sql('SELECT * FROM facebook_ads.ads', facebook_engine)                    #1,590 Rows
insights = pd.read_sql('SELECT * FROM facebook_ads.insights', facebook_engine)          #14,323 Rows




||||||| merged common ancestors
##=======1.0 IMPORT DATA TABLES===========

user_orders = pd.read_sql('SELECT * FROM user_orders', engine)
applications = pd.read_sql('SELECT * FROM solution_applications', engine)
users = pd.read_sql('SELECT * FROM users', engine)
onboarding_steps = pd.read_sql('SELECT * FROM onboarding_steps', engine)
completed_onboarding_steps = pd.read_sql('SELECT * FROM completed_onboarding_steps', engine)
locations = pd.read_sql('SELECT * FROM locations', engine)
user_location_roles = pd.read_sql('SELECT * FROM user_location_roles', engine)
location_roles = pd.read_sql('SELECT * FROM location_roles', engine)
authentications = pd.read_sql('SELECT * FROM authentications', engine)
solutions = pd.read_sql('SELECT * FROM solutions', engine)
accounts = pd.read_sql('SELECT * FROM accounts', engine)
account_entries = pd.read_sql('SELECT * FROM account_entries', engine)
location_invites = pd.read_sql('SELECT * FROM location_invites', engine)

#Import Facebook Ad Accounts
ad_accounts = pd.read_sql('SELECT * FROM facebook_ads.ad_accounts', facebook_engine)
ad_campaigns = pd.read_sql('SELECT * FROM facebook_ads.campaigns', facebook_engine)
ad_sets = pd.read_sql('SELECT * FROM facebook_ads.ad_sets', facebook_engine)
ads = pd.read_sql('SELECT * FROM facebook_ads.ads', facebook_engine)
insights = pd.read_sql('SELECT * FROM facebook_ads.insights', facebook_engine)




=======
>>>>>>> 0cc5586a91531f10992bb2503c131818f6d17aec

<<<<<<< HEAD
##=======3.0 MERGING DATA TABLES===========
||||||| merged common ancestors
##=======2.0 MERGING DATA TABLES===========
=======
>>>>>>> 0cc5586a91531f10992bb2503c131818f6d17aec

<<<<<<< HEAD
#Step 1:    Split accounts Options Column into Seperate Series.Finally use pd.concat to join back the other columns:
split_options = accounts['options'].apply(pd.Series)
account_options=pd.concat([accounts.drop(['options'], axis=1), split_options], axis=1)
||||||| merged common ancestors
#Step 1
#Split accounts Options Column into Seperate Series.Finally use pd.concat to join back the other columns:
split_options = accounts['options'].apply(pd.Series)
account_options=pd.concat([accounts.drop(['options'], axis=1), split_options], axis=1)
=======
##=======2.0 IMPORT DATA TABLES===========
>>>>>>> 0cc5586a91531f10992bb2503c131818f6d17aec

<<<<<<< HEAD
#Step 2    Merge accounts with locations data (local group)
account_location=account_options.merge(locations, left_on='location_id', right_on='id')

#Step3      Combine user_location_roles table with location_roles (Chamption and joiner)
user_location_roles_merged=user_location_roles.merge(location_roles, left_on='location_role_id', right_on='id')

#Step4      Merge account_location data with user location roles (roles & users)
user_roles_location_account=account_location.merge(user_location_roles_merged, left_on='location_id', right_on='location_id')

#Step5      Merge starter applications with users who created them
applications_user=applications.merge(users, left_on='user_id', right_on='id')

#Step6      Merge starter applications and user data with the locations that they created
applications_user_locations=applications_user.merge(locations, left_on='solution_location_id', right_on='id')

#Step7      Now it's time to combine the two. Merge accounts_location data with application_users_location data
account_location_application_user=account_location.merge(applications_user_locations, left_on='location_id', right_on='solution_location_id')

#Step8      Time to add some extra data from the Authentications Info into Seperate Series
split_authentications_info = authentications['info'].map(json.loads).apply(pd.Series)
authentications_info=pd.concat([authentications.drop(['info'], axis=1), split_authentications_info], axis=1)
authentications_info_last=authentications_info.drop_duplicates(['user_id'], keep='last')

#Step9      Now we add the authentications info onto our new master table (account_location_application_user)
applicant_data=account_location_application_user.merge(authentications_info_last, left_on='user_id', right_on='user_id', how='left')

#Step10     Split Screening Questions into Seperate Columns and add concatenate onto applicant_data table
split_screening_info = applicant_data['options'].apply(pd.Series)
applicant_data=pd.concat([applicant_data.drop(['options'], axis=1), split_screening_info], axis=1)

#Step11     Narrow applicant data down to just that which is important for analysis (feature shortlist) -> This table becomes mainstay for most analytics carried out
applicant_features=applicant_data[['parent_account_id','state','balance_cents','name_x','created_at_y_x','latitude_x','longitude_x','visibility_x','solution_id_x_y','stage','utm_source','utm_medium','active_tracking_count','sign_in_count','avatar_file_name','first_name_y','last_name_y','can_invite','intentions','previous_changemaker','location_id','id_x_y','solution_location_id',
'id_y_y','id_x','receive_starter_pack','starter_pack_sent_at','received_starter_call_at']]
||||||| merged common ancestors
#Step 2
account_location=account_options.merge(locations, left_on='location_id', right_on='id')

#Step3
#Combine user_location_roles table with location_roles (Chamption and joiner)
user_location_roles_merged=user_location_roles.merge(location_roles, left_on='location_role_id', right_on='id')

#Step4
user_roles_location_account=account_location.merge(user_location_roles_merged, left_on='location_id', right_on='location_id')

#Step5
applications_user=applications.merge(users, left_on='user_id', right_on='id')

#Step6
applications_user_locations=applications_user.merge(locations, left_on='solution_location_id', right_on='id')

#Step7
account_location_application_user=account_location.merge(applications_user_locations, left_on='location_id', right_on='solution_location_id')

#Step8
#Split Authentications Info into Seperate Series
split_authentications_info = authentications['info'].map(json.loads).apply(pd.Series)
authentications_info=pd.concat([authentications.drop(['info'], axis=1), split_authentications_info], axis=1)
authentications_info_last=authentications_info.drop_duplicates(['user_id'], keep='last')

#Step9
applicant_data=account_location_application_user.merge(authentications_info_last, left_on='user_id', right_on='user_id', how='left')

#Step10
#Split Screening Questions into Seperate Columns
split_screening_info = applicant_data['options'].apply(pd.Series)
applicant_data=pd.concat([applicant_data.drop(['options'], axis=1), split_screening_info], axis=1)

#Step11
#Narrow applicant data down to just that which is important for analysis (feature shortlist)
applicant_features=applicant_data[['parent_account_id','state','balance_cents','name_x','created_at_y_x','latitude_x','longitude_x','visibility_x','solution_id_x_y','stage','utm_source','utm_medium','active_tracking_count','sign_in_count','avatar_file_name','first_name_y','last_name_y','can_invite','intentions','previous_changemaker','location_id','id_x_y','solution_location_id',
'id_y_y','id_x','receive_starter_pack','starter_pack_sent_at','received_starter_call_at']]
=======
#Import Main Accounts and Split
accounts = pd.read_sql('SELECT * FROM accounts', engine)
split_accounts_options = accounts['options'].apply(pd.Series)
account_options=pd.concat([accounts.drop(['options'], axis=1), split_accounts_options], axis=1)
>>>>>>> 0cc5586a91531f10992bb2503c131818f6d17aec

<<<<<<< HEAD
#Step 12    Make user_orders into useable format. Split Options Column into Seperate Series and use pd.concat to join back the other columns:
split_options = user_orders['options'].apply(pd.Series)
user_order_options=pd.concat([user_orders.drop(['options'], axis=1), split_options], axis=1)
||||||| merged common ancestors


#Step 12 (Aside: make user_orders into useable format)
#Split Options Column into Seperate Series
split_options = user_orders['options'].apply(pd.Series)
#Finally use pd.concat to join back the other columns:
user_order_options=pd.concat([user_orders.drop(['options'], axis=1), split_options], axis=1)
=======


>>>>>>> 0cc5586a91531f10992bb2503c131818f6d17aec

##=======3.0 MERGING DATA TABLES===========








##=======3.0 ANALYTICS===========

<<<<<<< HEAD
#1.0 Fund Budget
fund_row=user_order_options.loc[user_order_options['slug']=='greaterminnesotafund']
row_index=fund_row.index
fund_budget=user_order_options.loc[row_index]['amount'].iloc[0]

#2.0 Fund name
fund_name=user_order_options.loc[row_index]['description'].iloc[0]

#3.0 Number Days Elapsed
start_date=user_order_options.loc[row_index]['start_date'].iloc[0].iloc[0]
current_date=date.today()
time_elapsed= current_date-start_date


#4.0 Total Paid Out
#see below

#5.0 Total Fund Remaining
#total_fund_remaining = fund_budget - total_paid_out

#6.0 Total Fund Allocated
#See Below
filtered_fund_accounts=accounts.loc[accounts['parent_account_id'] == 10.0]
list_of_accounts=filtered_fund_accounts['id'].tolist()
filtered_fund_paid_accounts=accounts[accounts['parent_account_id'].isin(list_of_accounts)]


#7.0 Number Paid accounts
number_paid_accounts=filtered_fund_paid_accounts.shape[0]

#8.0 Number Steps Completed
number_steps_completed=completed_onboarding_steps['location_id'].value_counts()
applicant_features_steps=applicant_features.merge(number_steps_completed.to_frame(), left_on='location_id', right_index=True).rename(columns = {'location_id_y': 'steps_complete'})

#9.0 Number Joiners Per Group
number_joiners_group=user_location_roles['location_id'].value_counts()
applicant_features_joiners=applicant_features_steps.merge(number_joiners_group.to_frame(), left_on='location_id', right_index=True).rename(columns = {'location_id_y': 'team_size'})

#9.0 Number Days Elapsed
applicant_features_joiners['days_elapsed']=date.today()-applicant_features_joiners['created_at_y_x']

#10.0 Applicant Table
applicant_table=applicant_features_joiners[['first_name_y','last_name_y','state','parent_account_id','steps_complete','team_size','sign_in_count','intentions','location_id','solution_id_x_y']]
applicant_table_paid=applicant_table.loc[applicant_table['state'] != 'active']
applicant_table_paid[applicant_table_paid.first_name_y != 'Niamh']
applicant_table_paid[applicant_table_paid.first_name_y != 'Niall']
applicant_table_paid=applicant_table_paid.sort_values(['steps_complete'],ascending=False)
applicant_table_paid=applicant_table_paid.sort_values(['state'])
applicant_table_converted=df_to_table(applicant_table_paid)




#11.0 Starter Activation Funnel

def active_funnel_chart(fund_account):
    merged_onboarding_steps=completed_onboarding_steps.merge(onboarding_steps, left_on='onboarding_step_id', right_on='id')
    applicant_table_paid_fund = applicant_table_paid[applicant_table_paid['parent_account_id']==fund_account]
    list_of_locations=applicant_table_paid_fund['location_id'].tolist()
    applications_steps=merged_onboarding_steps[merged_onboarding_steps['location_id'].isin(list_of_locations)]
    #applications_steps['step_type'].value_counts()
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



#12.0 Acquisition Source

def acquisition_chart(fund_account_value):
    applicant_features_joiners_fund=applicant_features_joiners[applicant_features_joiners['parent_account_id']==fund_account_value]
    aquisition_source=applicant_features_joiners_fund[['state','utm_source']]
    Facebook_Mapping = {'':'Organic','intercom': 'Intercom','FacebookPaid_GIY': 'FacebookAds','FacebookPaid_IdeaFund': 'FacebookAds', 'FacebookPaid_Poetry': 'FacebookAds','FacebookPaid_MNFund': 'FacebookAds','FacebookPaid_WelcomingWeek': 'FacebookAds','FacebookPaid_StreetFeast': 'FacebookAds','FacebookPaid_Kaboom': 'FacebookAds','FacebookPaid_MensShed': 'FacebookAds'}
    mapped_aquisition_source=aquisition_source['utm_source'].map(Facebook_Mapping)
    mapped_aquisition_source_active=pd.concat([aquisition_source.drop(['utm_source'], axis=1), mapped_aquisition_source], axis=1)
    #mapped_aquisition_source_active.groupby('utm_source').count()
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




#13.0 Starter Map Data


def pinned_map(fund_name):
    #Need to filter dataframe by fund name

    applicant_features_joiners_fund=applicant_features_joiners[applicant_features_joiners['parent_account_id']==fund_name]
    site_lat = applicant_features_joiners_fund.latitude_x.iloc[:,0]
    site_lon = applicant_features_joiners_fund.longitude_x.iloc[:,0]
    locations_name = applicant_features_joiners_fund.last_name_y

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


#14.0 Idea Starter List

def idea_starters_table(fund_namee):
    paid_starters_filtered=applicant_table_paid[applicant_table_paid['parent_account_id']==fund_namee]
    paid_starters=paid_starters_filtered[paid_starters_filtered['state']=='paid']
    solutions_mapping=solutions[['id','name']]
    paid_starters_idea=paid_starters.merge(solutions_mapping, left_on='solution_id_x_y', right_on='id')
    idea_starter_list=paid_starters_idea['name']
    idea_list=idea_starter_list.value_counts()
    idea_list_dataframe=idea_list.to_frame(name='#Starters')
    idea_list_index=idea_list_dataframe.reset_index(level=0, inplace=True)
    idea_list_table=df_to_table(idea_list_index)
    return idea_list_table


#15.0 Percentage Packs Delivered
non_rejected_applicants=applicant_features_joiners[applicant_features_joiners['state']!='rejected']
want_starter_pack=non_rejected_applicants[non_rejected_applicants['receive_starter_pack']==True]
number_want_pack=want_starter_pack['receive_starter_pack'].count()


starter_pack_delivered=non_rejected_applicants[non_rejected_applicants['starter_pack_sent_at'] != 'NaT']
number_received_pack=starter_pack_delivered['starter_pack_sent_at'].count()
waiting_on_pack=number_want_pack-number_received_pack
sent_starter_pack=number_received_pack/number_want_pack

pack_pie_labels = ['Waiting on Pack','Recieved Pack']
pack_pie_values = [waiting_on_pack,number_received_pack]
pack_pie_trace = go.Pie(labels=pack_pie_labels, values=pack_pie_values)


#16.0 Pack Wait Time
pack_wait_time=want_starter_pack['starter_pack_sent_at'] - want_starter_pack['created_at_y_x']
pack_wait_time=pack_wait_time.mean()


#17.0 Percentage Starters Called
starters_called=applicant_features_joiners[applicant_features_joiners['received_starter_call_at']!='NaT']
number_starters_called=starters_called['received_starter_call_at'].count()
total_number_applicants=applicant_features_joiners['id_x'].count()
number_waiting_call=total_number_applicants-number_starters_called
#percentage_starters_called=number_starters_called/total_number_applicants
call_pie_labels = ['Waiting on Call','Recieved Call']
call_pie_values = [number_waiting_call,number_starters_called]
call_pie_trace = go.Pie(labels=call_pie_labels, values=call_pie_values)



#18.0 Starter Call Wait Time
starter_call_wait_time=applicant_features_joiners['received_starter_call_at'] - applicant_features_joiners['created_at_y_x']
call_wait_time=starter_call_wait_time.mean()

#19.0 Starter Time left
number_days_left=pd.Timedelta('30 days')-applicant_features_joiners['days_elapsed']
#number_days_left[number_days_left < pd.Timedelta('0 days')] = 0


#### FACEBOOK ANALYTICS #######
#Filter to find ad campaigns only associated with Minnesota Fund
slug='MN Fund'
fund_ads=campaign_insights[campaign_insights['name_x'].str.contains(slug)]

#19. Facebook Ad Spent
total_fund_spend = fund_ads['spend'].sum()

#20. Total People Reached
total_people_reached = fund_ads['reach'].sum()

#21. Total Unique Impressions
total_unique_impressions = fund_ads['unique_impressions'].sum()

#22. Total Link Clicks
total_link_clicks = fund_ads['link_clicks'].sum()

#23. Average Frequency
average_frequency = fund_ads['frequency'].mean()

#25. Ad Spend Per idea
fund_ads['name_x'].astype(str)
idea_mapping = {'Cycling Without Age (MN Fund)':71,'GIY (Bluecross MN Fund #2)':78,'GIY MN Fund': 78, 'Kaboom (MN Fund)':10, "Men's Shed (MN Fund)": 48,'Poetry in Park (Bluecross MN Fund #2)':61,'Poetry in Park (MN Fund)': 61,'Repair Cafe (Bluecross MN Fund #2)':73,'Repair Café (MN Fund)':73,'Street Feast Bluecross (MN Fund #2)':65,'StreetFeast  (MN Fund)': 65}
fund_ads['name_x']=fund_ads['name_x'].map(idea_mapping)
ad_spend_per_idea=fund_ads.groupby(['name_x'])['spend'].sum()
ad_spend_per_idea_df=ad_spend_per_idea.reset_index()
||||||| merged common ancestors
#1.0 Fund Budget
fund_row=user_order_options.loc[user_order_options['slug']=='greaterminnesotafund']
row_index=fund_row.index
fund_budget=user_order_options.loc[row_index]['amount'].iloc[0]

#2.0 Fund name
#fund_name=user_order_options.loc[row_index]['description'].iloc[0]

#3.0 Number Days Elapsed
#start_date=user_order_options.loc[row_index]['start_date'].iloc[0].iloc[0]
#current_date=date.today()
#time_elapsed= current_date-start_date


#4.0 Total Paid Out
#see below

#5.0 Total Fund Remaining
#total_fund_remaining = fund_budget - total_paid_out

#6.0 Total Fund Allocated
#See Below
filtered_fund_accounts=accounts.loc[accounts['parent_account_id'] == 10.0]
list_of_accounts=filtered_fund_accounts['id'].tolist()
filtered_fund_paid_accounts=accounts[accounts['parent_account_id'].isin(list_of_accounts)]




#7.0 Number Paid accounts
number_paid_accounts=filtered_fund_paid_accounts.shape[0]

#8.0 Number Steps Completed
number_steps_completed=completed_onboarding_steps['location_id'].value_counts()
applicant_features_steps=applicant_features.merge(number_steps_completed.to_frame(), left_on='location_id', right_index=True).rename(columns = {'location_id_y': 'steps_complete'})

#9.0 Number Joiners Per Group
number_joiners_group=user_location_roles['location_id'].value_counts()
applicant_features_joiners=applicant_features_steps.merge(number_joiners_group.to_frame(), left_on='location_id', right_index=True).rename(columns = {'location_id_y': 'team_size'})

#9.0 Number Days Elapsed
applicant_features_joiners['days_elapsed']=date.today()-applicant_features_joiners['created_at_y_x']

#10.0 Applicant Table
applicant_table=applicant_features_joiners[['first_name_y','last_name_y','state','parent_account_id','steps_complete','team_size','sign_in_count','intentions','location_id','solution_id_x_y']]
applicant_table_paid=applicant_table.loc[applicant_table['state'] != 'active']
applicant_table_paid[applicant_table_paid.first_name_y != 'Niamh']
applicant_table_paid[applicant_table_paid.first_name_y != 'Niall']
applicant_table_paid=applicant_table_paid.sort_values(['steps_complete'],ascending=False)
applicant_table_paid=applicant_table_paid.sort_values(['state'])
applicant_table_converted=df_to_table(applicant_table_paid)




#11.0 Starter Activation Funnel

def active_funnel_chart(fund_account):
    merged_onboarding_steps=completed_onboarding_steps.merge(onboarding_steps, left_on='onboarding_step_id', right_on='id')
    applicant_table_paid_fund = applicant_table_paid[applicant_table_paid['parent_account_id']==fund_account]
    list_of_locations=applicant_table_paid_fund['location_id'].tolist()
    applications_steps=merged_onboarding_steps[merged_onboarding_steps['location_id'].isin(list_of_locations)]
    #applications_steps['step_type'].value_counts()
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



#12.0 Acquisition Source

def acquisition_chart(fund_account_value):
    applicant_features_joiners_fund=applicant_features_joiners[applicant_features_joiners['parent_account_id']==fund_account_value]
    aquisition_source=applicant_features_joiners_fund[['state','utm_source']]
    Facebook_Mapping = {'':'Organic','intercom': 'Intercom','FacebookPaid_GIY': 'FacebookAds','FacebookPaid_IdeaFund': 'FacebookAds', 'FacebookPaid_Poetry': 'FacebookAds','FacebookPaid_MNFund': 'FacebookAds','FacebookPaid_WelcomingWeek': 'FacebookAds','FacebookPaid_StreetFeast': 'FacebookAds','FacebookPaid_Kaboom': 'FacebookAds','FacebookPaid_MensShed': 'FacebookAds'}
    mapped_aquisition_source=aquisition_source['utm_source'].map(Facebook_Mapping)
    mapped_aquisition_source_active=pd.concat([aquisition_source.drop(['utm_source'], axis=1), mapped_aquisition_source], axis=1)
    #mapped_aquisition_source_active.groupby('utm_source').count()
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




#13.0 Starter Map Data


def pinned_map(fund_name):
    #Need to filter dataframe by fund name

    applicant_features_joiners_fund=applicant_features_joiners[applicant_features_joiners['parent_account_id']==fund_name]
    site_lat = applicant_features_joiners_fund.latitude_x.iloc[:,0]
    site_lon = applicant_features_joiners_fund.longitude_x.iloc[:,0]
    locations_name = applicant_features_joiners_fund.last_name_y

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


#14.0 Idea Starter List

def idea_starters_table(fund_namee):
    paid_starters_filtered=applicant_table_paid[applicant_table_paid['parent_account_id']==fund_namee]
    paid_starters=paid_starters_filtered[paid_starters_filtered['state']=='paid']
    solutions_mapping=solutions[['id','name']]
    paid_starters_idea=paid_starters.merge(solutions_mapping, left_on='solution_id_x_y', right_on='id')
    idea_starter_list=paid_starters_idea['name']
    idea_list=idea_starter_list.value_counts()
    idea_list_dataframe=idea_list.to_frame(name='#Starters')
    idea_list_index=idea_list_dataframe.reset_index(level=0, inplace=True)
    idea_list_table=df_to_table(idea_list_index)
    return idea_list_table


#15.0 Percentage Packs Delivered
non_rejected_applicants=applicant_features_joiners[applicant_features_joiners['state']!='rejected']
want_starter_pack=non_rejected_applicants[non_rejected_applicants['receive_starter_pack']==True]
number_want_pack=want_starter_pack['receive_starter_pack'].count()


starter_pack_delivered=non_rejected_applicants[non_rejected_applicants['starter_pack_sent_at'] != 'NaT']
number_received_pack=starter_pack_delivered['starter_pack_sent_at'].count()
waiting_on_pack=number_want_pack-number_received_pack
sent_starter_pack=number_received_pack/number_want_pack

pack_pie_labels = ['Waiting on Pack','Recieved Pack']
pack_pie_values = [waiting_on_pack,number_received_pack]
pack_pie_trace = go.Pie(labels=pack_pie_labels, values=pack_pie_values)


#16.0 Pack Wait Time
pack_wait_time=want_starter_pack['starter_pack_sent_at'] - want_starter_pack['created_at_y_x']
pack_wait_time=pack_wait_time.mean()


#17.0 Percentage Starters Called
starters_called=applicant_features_joiners[applicant_features_joiners['received_starter_call_at']!='NaT']
number_starters_called=starters_called['received_starter_call_at'].count()
total_number_applicants=applicant_features_joiners['id_x'].count()
number_waiting_call=total_number_applicants-number_starters_called
#percentage_starters_called=number_starters_called/total_number_applicants
call_pie_labels = ['Waiting on Call','Recieved Call']
call_pie_values = [number_waiting_call,number_starters_called]
call_pie_trace = go.Pie(labels=call_pie_labels, values=call_pie_values)



#18.0 Starter Call Wait Time
starter_call_wait_time=applicant_features_joiners['received_starter_call_at'] - applicant_features_joiners['created_at_y_x']
call_wait_time=starter_call_wait_time.mean()

#19.0 Starter Time left
number_days_left=pd.Timedelta('30 days')-applicant_features_joiners['days_elapsed']
#number_days_left[number_days_left < pd.Timedelta('0 days')] = 0


#### FACEBOOK ANALYTICS #######
#Filter to find ad campaigns only associated with Minnesota Fund
slug='MN Fund'
fund_ads=campaign_insights[campaign_insights['name_x'].str.contains(slug)]

#19. Facebook Ad Spent
total_fund_spend = fund_ads['spend'].sum()

#20. Total People Reached
total_people_reached = fund_ads['reach'].sum()

#21. Total Unique Impressions
total_unique_impressions = fund_ads['unique_impressions'].sum()

#22. Total Link Clicks
total_link_clicks = fund_ads['link_clicks'].sum()

#23. Average Frequency
average_frequency = fund_ads['frequency'].mean()

#25. Ad Spend Per idea
fund_ads['name_x'].astype(str)
idea_mapping = {'Cycling Without Age (MN Fund)':71,'GIY (Bluecross MN Fund #2)':78,'GIY MN Fund': 78, 'Kaboom (MN Fund)':10, "Men's Shed (MN Fund)": 48,'Poetry in Park (Bluecross MN Fund #2)':61,'Poetry in Park (MN Fund)': 61,'Repair Cafe (Bluecross MN Fund #2)':73,'Repair Café (MN Fund)':73,'Street Feast Bluecross (MN Fund #2)':65,'StreetFeast  (MN Fund)': 65}
fund_ads['name_x']=fund_ads['name_x'].map(idea_mapping)
ad_spend_per_idea=fund_ads.groupby(['name_x'])['spend'].sum()
ad_spend_per_idea_df=ad_spend_per_idea.reset_index()
=======
>>>>>>> 0cc5586a91531f10992bb2503c131818f6d17aec






<<<<<<< HEAD
def idea_demand_table(fund_namee):
    filtered_applicant_features_joiners=applicant_features_joiners[applicant_features_joiners['parent_account_id']==fund_namee]
    aquisition_source_idea=filtered_applicant_features_joiners[['state','utm_source','solution_id_x_y']]
    Facebook_Mapping = {'':'Organic','intercom': 'Intercom','FacebookPaid_GIY': 'FacebookAds','FacebookPaid_IdeaFund': 'FacebookAds', 'FacebookPaid_Poetry': 'FacebookAds','FacebookPaid_MNFund': 'FacebookAds','FacebookPaid_WelcomingWeek': 'FacebookAds','FacebookPaid_StreetFeast': 'FacebookAds','FacebookPaid_Kaboom': 'FacebookAds','FacebookPaid_MensShed': 'FacebookAds'}
    aquisition_source_idea['utm_source']=aquisition_source_idea['utm_source'].map(Facebook_Mapping)

    aquisition_source_idea_fb=aquisition_source_idea[aquisition_source_idea['utm_source']=='FacebookAds']
    facebook_starters_per_idea=aquisition_source_idea_fb.groupby(['solution_id_x_y'])['utm_source'].count()
    facebook_starters_per_idea_df=facebook_starters_per_idea.reset_index()
    merged_ads_starter_data=facebook_starters_per_idea_df.merge(ad_spend_per_idea_df, left_on='solution_id_x_y', right_on='name_x')
    merged_ads_starter_data['cost_per_approved']= merged_ads_starter_data['spend']/ merged_ads_starter_data['utm_source']
    merged_ads_starter_data_converted=df_to_table(merged_ads_starter_data)

    return merged_ads_starter_data_converted




#31. Cost Per Active Starter Per Idea
#active_idea_facebook=aquisition_source_idea_fb[aquisition_source_idea_fb['state']=='paid']
#active_facebook_starters_per_idea=active_idea_facebook.groupby(['solution_id_x_y'])['utm_source'].count()
#active_facebook_starters_per_idea_df=active_facebook_starters_per_idea.reset_index()
#merged_active_ads_starter_data=active_facebook_starters_per_idea_df.merge(ad_spend_per_idea_df, left_on='solution_id_x_y', right_on='name_x')
#merged_active_ads_starter_data['cost_per_approved']= merged_active_ads_starter_data['spend']/ merged_active_ads_starter_data['utm_source']


#32. Project Cost Breakdown
#Filter to find ad campaigns only associated with Minnesota Fund


def project_costs_chart(fund_account_value):
    slug='MN Fund'
    fund_ads=campaign_insights[campaign_insights['name_x'].str.contains(slug)]
    total_fund_spend = fund_ads['spend'].sum()
    #Total Pack Costs
    unit_pack_cost= 16.70
    total_pack_cost = number_received_pack * unit_pack_cost
    #Total Staff Costs
    staff_daily_rate= 4000.0/22
    total_staff_costs = staff_daily_rate * 88

    labels = ['Ad Spend','Pack Costs','Staff Costs']
    values = [total_fund_spend, total_pack_cost, total_staff_costs]
    colors = ['#E01273', '#EFEEED', '#58B74E']

    trace = go.Pie(labels=labels,
                   values=values,
                   marker=dict(colors=colors),
                   textinfo= 'value+percent',
                   )
    layout = dict(margin=dict(l=15, r=10, t=0, b=65), legend=dict(orientation="h"))

    return dict(data=[trace], layout=layout)



## Project Budget Gauge Wheel Visualisation

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


wheel_fig = {"data": [base_chart, meter_chart],"layout": layout}
#py.iplot(fig, filename='gauge-meter-chart')




||||||| merged common ancestors
def idea_demand_table(fund_namee):
    filtered_applicant_features_joiners=applicant_features_joiners[applicant_features_joiners['parent_account_id']==fund_namee]
    aquisition_source_idea=filtered_applicant_features_joiners[['state','utm_source','solution_id_x_y']]
    Facebook_Mapping = {'':'Organic','intercom': 'Intercom','FacebookPaid_GIY': 'FacebookAds','FacebookPaid_IdeaFund': 'FacebookAds', 'FacebookPaid_Poetry': 'FacebookAds','FacebookPaid_MNFund': 'FacebookAds','FacebookPaid_WelcomingWeek': 'FacebookAds','FacebookPaid_StreetFeast': 'FacebookAds','FacebookPaid_Kaboom': 'FacebookAds','FacebookPaid_MensShed': 'FacebookAds'}
    aquisition_source_idea['utm_source']=aquisition_source_idea['utm_source'].map(Facebook_Mapping)

    aquisition_source_idea_fb=aquisition_source_idea[aquisition_source_idea['utm_source']=='FacebookAds']
    facebook_starters_per_idea=aquisition_source_idea_fb.groupby(['solution_id_x_y'])['utm_source'].count()
    facebook_starters_per_idea_df=facebook_starters_per_idea.reset_index()
    merged_ads_starter_data=facebook_starters_per_idea_df.merge(ad_spend_per_idea_df, left_on='solution_id_x_y', right_on='name_x')
    merged_ads_starter_data['cost_per_approved']= merged_ads_starter_data['spend']/ merged_ads_starter_data['utm_source']
    merged_ads_starter_data_converted=df_to_table(merged_ads_starter_data)

    return merged_ads_starter_data_converted




#31. Cost Per Active Starter Per Idea
#active_idea_facebook=aquisition_source_idea_fb[aquisition_source_idea_fb['state']=='paid']
#active_facebook_starters_per_idea=active_idea_facebook.groupby(['solution_id_x_y'])['utm_source'].count()
#active_facebook_starters_per_idea_df=active_facebook_starters_per_idea.reset_index()
#merged_active_ads_starter_data=active_facebook_starters_per_idea_df.merge(ad_spend_per_idea_df, left_on='solution_id_x_y', right_on='name_x')
#merged_active_ads_starter_data['cost_per_approved']= merged_active_ads_starter_data['spend']/ merged_active_ads_starter_data['utm_source']


#32. Project Cost Breakdown
#Filter to find ad campaigns only associated with Minnesota Fund


def project_costs_chart(fund_account_value):
    slug='MN Fund'
    fund_ads=campaign_insights[campaign_insights['name_x'].str.contains(slug)]
    total_fund_spend = fund_ads['spend'].sum()
    #Total Pack Costs
    unit_pack_cost= 16.70
    total_pack_cost = number_received_pack * unit_pack_cost
    #Total Staff Costs
    staff_daily_rate= 4000.0/22
    total_staff_costs = staff_daily_rate * 88

    labels = ['Ad Spend','Pack Costs','Staff Costs']
    values = [total_fund_spend, total_pack_cost, total_staff_costs]
    colors = ['#E01273', '#EFEEED', '#58B74E']

    trace = go.Pie(labels=labels,
                   values=values,
                   marker=dict(colors=colors),
                   textinfo= 'value+percent',
                   )
    layout = dict(margin=dict(l=15, r=10, t=0, b=65), legend=dict(orientation="h"))

    return dict(data=[trace], layout=layout)



## Project Budget Gauge Wheel Visualisation

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


wheel_fig = {"data": [base_chart, meter_chart],"layout": layout}
#py.iplot(fig, filename='gauge-meter-chart')




# returns modal (hidden by default)
def modal():
    return html.Div(
        html.Div(
            [
                html.Div(
                    [

                        # modal header
                        html.Div(
                            [
                                html.Span(
                                    "New Opportunity",
                                    style={
                                        "color": "#506784",
                                        "fontWeight": "bold",
                                        "fontSize": "20",
                                    },
                                ),
                                html.Span(
                                    "×",
                                    id="opportunities_modal_close",
                                    n_clicks=0,
                                    style={
                                        "float": "right",
                                        "cursor": "pointer",
                                        "marginTop": "0",
                                        "marginBottom": "17",
                                    },
                                ),
                            ],
                            className="row",
                            style={"borderBottom": "1px solid #C8D4E3"},
                        ),


                        # modal form
                        html.Div(
                            [

                                # left div
                                html.Div(
                                    [
                                        html.P(
                                            [
                                                "Name"
                                            ],
                                            style={
                                                "float": "left",
                                                "marginTop": "4",
                                                "marginBottom": "2",
                                            },
                                            className="row",
                                        ),
                                        dcc.Input(
                                            id="new_opportunity_name",
                                            placeholder="Name of the opportunity",
                                            type="text",
                                            value="",
                                            style={"width": "100%"},
                                        ),

                                        html.P(
                                            [
                                                "StageName"
                                            ],
                                            style={
                                                "textAlign": "left",
                                                "marginBottom": "2",
                                                "marginTop": "4",
                                            },
                                        ),
                                        dcc.Dropdown(
                                            id="new_opportunity_stage",
                                            options=[
                                                {
                                                    "label": "Prospecting",
                                                    "value": "Prospecting",
                                                },
                                                {
                                                    "label": "Qualification",
                                                    "value": "Qualification",
                                                },
                                                {
                                                    "label": "Needs Analysis",
                                                    "value": "Needs Analysis",
                                                },
                                                {
                                                    "label": "Value Proposition",
                                                    "value": "Value Proposition",
                                                },
                                                {
                                                    "label": "Id. Decision Makers",
                                                    "value": "Closed",
                                                },
                                                {
                                                    "label": "Perception Analysis",
                                                    "value": "Perception Analysis",
                                                },
                                                {
                                                    "label": "Proposal/Price Quote",
                                                    "value": "Proposal/Price Quote",
                                                },
                                                {
                                                    "label": "Negotiation/Review",
                                                    "value": "Negotiation/Review",
                                                },
                                                {
                                                    "label": "Closed/Won",
                                                    "value": "Closed Won",
                                                },
                                                {
                                                    "label": "Closed/Lost",
                                                    "value": "Closed Lost",
                                                },
                                            ],
                                            clearable=False,
                                            value="Prospecting",
                                        ),

                                        html.P(
                                            "Source",
                                            style={
                                                "textAlign": "left",
                                                "marginBottom": "2",
                                                "marginTop": "4",
                                            },
                                        ),
                                        dcc.Dropdown(
                                            id="new_opportunity_source",
                                            options=[
                                                {"label": "Web", "value": "Web"},
                                                {
                                                    "label": "Phone Inquiry",
                                                    "value": "Phone Inquiry",
                                                },
                                                {
                                                    "label": "Partner Referral",
                                                    "value": "Partner Referral",
                                                },
                                                {
                                                    "label": "Purchased List",
                                                    "value": "Purchased List",
                                                },
                                                {"label": "Other", "value": "Other"},
                                            ],
                                            value="Web",
                                        ),

                                        html.P(
                                            [
                                                "Close Date"
                                            ],
                                            style={
                                                "textAlign": "left",
                                                "marginBottom": "2",
                                                "marginTop": "4",
                                            },
                                        ),
                                        html.Div(
                                            dcc.DatePickerSingle(
                                                id="new_opportunity_date",
                                                min_date_allowed=date.today(),
                                                # max_date_allowed=dt(2017, 9, 19),
                                                initial_visible_month=date.today(),
                                                date=date.today(),
                                            ),
                                            style={"textAlign": "left"},
                                        ),

                                    ],
                                    className="six columns",
                                    style={"paddingRight": "15"},
                                ),


                                # right div
                                html.Div(
                                    [
                                        html.P(
                                            "Type",
                                            style={
                                                "textAlign": "left",
                                                "marginBottom": "2",
                                                "marginTop": "4",
                                            },
                                        ),
                                        dcc.Dropdown(
                                            id="new_opportunity_type",
                                            options=[
                                                {
                                                    "label": "Existing Customer - Replacement",
                                                    "value": "Existing Customer - Replacement",
                                                },
                                                {
                                                    "label": "New Customer",
                                                    "value": "New Customer",
                                                },
                                                {
                                                    "label": "Existing Customer - Upgrade",
                                                    "value": "Existing Customer - Upgrade",
                                                },
                                                {
                                                    "label": "Existing Customer - Downgrade",
                                                    "value": "Existing Customer - Downgrade",
                                                },
                                            ],
                                            value="New Customer",
                                        ),

                                        html.P(
                                            "Amount",
                                            style={
                                                "textAlign": "left",
                                                "marginBottom": "2",
                                                "marginTop": "4",
                                            },
                                        ),
                                        dcc.Input(
                                            id="new_opportunity_amount",
                                            placeholder="0",
                                            type="number",
                                            value="",
                                            style={"width": "100%"},
                                        ),

                                        html.P(
                                            "Probability",
                                            style={
                                                "textAlign": "left",
                                                "marginBottom": "2",
                                                "marginTop": "4",
                                            },
                                        ),
                                        dcc.Input(
                                            id="new_opportunity_probability",
                                            placeholder="0",
                                            type="number",
                                            max=100,
                                            step=1,
                                            value="",
                                            style={"width": "100%"},
                                        ),

                                    ],
                                    className="six columns",
                                    style={"paddingLeft": "15"},
                                ),
                            ],
                            className="row",
                            style={"paddingTop": "2%"},
                        ),


                        # submit button
                        html.Span(
                            "Submit",
                            id="submit_new_opportunity",
                            n_clicks=0,
                            className="button button--primary add"
                        ),
                    ],
                    className="modal-content",
                    style={"textAlign": "center"},
                )
            ],
            className="modal",
        ),
        id="opportunities_modal",
        style={"display": "none"},
    )
=======
>>>>>>> 0cc5586a91531f10992bb2503c131818f6d17aec

##=======4.0 HTML LAYOUT===========




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




<<<<<<< HEAD




##=======5.0 CALLBACK FUNCTIONS===========



# updates First Row left indicator
@app.callback(
    Output("budget_remaining_id", "children"), [Input("fund_slug_dropdown", "value")]
)
def budget_remaining_callback(fund_namee):
        slug='MN Fund'
        fund_ads=campaign_insights[campaign_insights['name_x'].str.contains(slug)]
        total_fund_spend = fund_ads['spend'].sum()
||||||| merged common ancestors
@app.callback(
    Output("budget_remaining_id", "children"), [Input("fund_slug_dropdown", "value")]
)
def budget_remaining_callback(fund_namee):
        slug='MN Fund'
        fund_ads=campaign_insights[campaign_insights['name_x'].str.contains(slug)]
        total_fund_spend = fund_ads['spend'].sum()
=======
>>>>>>> 0cc5586a91531f10992bb2503c131818f6d17aec




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


<<<<<<< HEAD
||||||| merged common ancestors
# updates Second Row First Indicator (Total Ad Spend)
=======


# updates Second Row Eight Indicator (Paid Out)
>>>>>>> 0cc5586a91531f10992bb2503c131818f6d17aec


# updates Second Row First Indicator (Total Ad Spend)
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
    total_fund_remaining_eur_amount=fund_namee
    return total_fund_remaining_eur_amount


<<<<<<< HEAD
# updates Second Row Eight Indicator (Paid Out)

@app.callback(
    Output("paid_out_id", "children"), [Input("fund_slug_dropdown", "value")]
)
def fund_paid_out_callback(fund_namee):
    filtered_fund_accounts=accounts[accounts['parent_account_id'] == fund_namee]
    list_of_accounts=filtered_fund_accounts['id'].tolist()

    filtered_fund_paid_accounts=accounts[accounts['parent_account_id'].isin(list_of_accounts)]
    total_paid_out=filtered_fund_paid_accounts['balance_cents'].sum()/100

    total_paid_out_cash=Money(total_paid_out,'USD')
    total_paid_out_eur_amount=total_paid_out_cash.format('en_US')
||||||| merged common ancestors
# updates Second Row Eight Indicator (Paid Out)
@app.callback(
    Output("paid_out_id", "children"), [Input("fund_slug_dropdown", "value")]
)
def fund_paid_out_callback(fund_namee):
    filtered_fund_accounts=accounts[accounts['parent_account_id'] == fund_namee]
    list_of_accounts=filtered_fund_accounts['id'].tolist()

    filtered_fund_paid_accounts=accounts[accounts['parent_account_id'].isin(list_of_accounts)]
    total_paid_out=filtered_fund_paid_accounts['balance_cents'].sum()/100

    total_paid_out_cash=Money(total_paid_out,'USD')
    total_paid_out_eur_amount=total_paid_out_cash.format('en_US')
=======
>>>>>>> 0cc5586a91531f10992bb2503c131818f6d17aec




# updates Second Row Ninth Indicator (Allocated)
@app.callback(
    Output("allocated_funding_id", "children"), [Input("fund_slug_dropdown", "value")]
)
def fund_allocated_callback(fund_namee):
<<<<<<< HEAD
    filtered_fund_accounts=accounts[accounts['parent_account_id'] == fund_namee]
    total_fund_allocated=filtered_fund_accounts['balance_cents'].sum()/100

    total_fund_allocated_cash=Money(total_fund_allocated,'USD')
    total_fund_allocated_eur_amount=total_fund_allocated_cash.format('en_US')

    return total_fund_allocated_eur_amount





||||||| merged common ancestors
    filtered_fund_accounts=accounts[accounts['parent_account_id'] == fund_namee]
    total_fund_allocated=filtered_fund_accounts['balance_cents'].sum()/100

    total_fund_allocated_cash=Money(total_fund_allocated,'USD')
    total_fund_allocated_eur_amount=total_fund_allocated_cash.format('en_US')

    return total_fund_allocated_eur_amount





# hide/show modal
@app.callback(
    Output("opportunities_modal", "style"), [Input("new_opportunity", "n_clicks")]
)
def display_opportunities_modal_callback(n):
    if n > 0:
        return {"display": "block"}
    return {"display": "none"}


# reset to 0 add button n_clicks property
@app.callback(
    Output("new_opportunity", "n_clicks"),
    [
        Input("opportunities_modal_close", "n_clicks"),
        Input("submit_new_opportunity", "n_clicks"),
    ],
)
def close_modal_callback(n, n2):
    return 0


# add new opportunity to salesforce and stores new df in hidden div
@app.callback(
    Output("opportunities_df", "children"),
    [Input("submit_new_opportunity", "n_clicks")],
    [
        State("new_opportunity_name", "value"),
        State("new_opportunity_stage", "value"),
        State("new_opportunity_amount", "value"),
        State("new_opportunity_probability", "value"),
        State("new_opportunity_date", "date"),
        State("new_opportunity_type", "value"),
        State("new_opportunity_source", "value"),
        State("opportunities_df", "children"),
    ],
)
def add_opportunity_callback(
    n_clicks, name, stage, amount, probability, date, o_type, source, current_df
):
    if n_clicks > 0:
        if name == "":
            name = "Not named yet"
        query = {
            "Name": name,
            "StageName": stage,
            "Amount": amount,
            "Probability": probability,
            "CloseDate": date,
            "Type": o_type,
            "LeadSource": source,
        }

        sf_manager.add_opportunity(query)

        df = sf_manager.get_opportunities()

        return df.to_json(orient="split")

    return current_df





# updates starter applicant table based on 'State' df updates
@app.callback(
    Output("starter_applicant_table", "children"),
    [Input("state_dropdown", "value"), Input("fund_slug_dropdown", "value")],
)
def table_state_callback(state, fund_account_number):
    if state == 'all':
        applicant_table_paid_fund_filter=applicant_table_paid[applicant_table_paid['parent_account_id']==fund_account_number]
        applicant_table_state_converted=df_to_table(applicant_table_paid_fund_filter)
        return  applicant_table_state_converted
    else:
        applicant_table_paid_fund_filter=applicant_table_paid[applicant_table_paid['parent_account_id']==fund_account_number]
        applicant_table_state=applicant_table_paid_fund_filter[applicant_table_paid_fund_filter['state']==state]
        applicant_table_state_converted=df_to_table(applicant_table_state)
        return applicant_table_state_converted


=======
    filtered_accounts = account_options[account_options['parent_account_id']==fund_namee]
    allocated_accounts=filtered_accounts[(filtered_accounts['state']=='allocated') | (filtered_accounts['state']=='approved')]
    total_allocated=allocated_accounts['balance_cents'].sum()/100
    return total_allocated




>>>>>>> 0cc5586a91531f10992bb2503c131818f6d17aec
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

@app.callback(
    Output("staters_per_idea_id", "children"),
    [Input("fund_slug_dropdown", "value")],
)
def idea_starters_table_callback(fund_namee):
<<<<<<< HEAD
    return idea_starters_table(fund_namee)





# updates starter applicant table based on 'State' df updates
@app.callback(
    Output("starter_applicant_table", "children"),
    [Input("state_dropdown", "value"), Input("fund_slug_dropdown", "value")],
)
def table_state_callback(state, fund_account_number):
    if state == 'all':
        applicant_table_paid_fund_filter=applicant_table_paid[applicant_table_paid['parent_account_id']==fund_account_number]
        applicant_table_state_converted=df_to_table(applicant_table_paid_fund_filter)
        return  applicant_table_state_converted
    else:
        applicant_table_paid_fund_filter=applicant_table_paid[applicant_table_paid['parent_account_id']==fund_account_number]
        applicant_table_state=applicant_table_paid_fund_filter[applicant_table_paid_fund_filter['state']==state]
        applicant_table_state_converted=df_to_table(applicant_table_state)
        return applicant_table_state_converted
||||||| merged common ancestors
    return idea_starters_table(fund_namee)
=======
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
>>>>>>> 0cc5586a91531f10992bb2503c131818f6d17aec
