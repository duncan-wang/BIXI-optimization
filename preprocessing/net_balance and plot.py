# -*- coding: utf-8 -*-
"""
MGCS662 Project 
Bixi Net Balance

"""
#==============================Import Packages=================================
import pandas as pd
import plotly.express as px
import random
import datetime
import numpy as np
import timeit


#================================Bike Data=====================================
bike = pd.read_csv("C:/Users/becky/OneDrive/Desktop/net_balance/OD_2019-07.csv")
bike["start_date"] = bike["start_date"].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
bike["end_date"] = bike["end_date"].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

bike['start_date_only'] = [d.date() for d in bike['start_date']]
bike['start_time_only'] = [d.time() for d in bike['start_date']]
bike['end_date_only'] = [d.date() for d in bike['end_date']]
bike['end_time_only'] = [d.time() for d in bike['end_date']]

bike["start_date_only"] = bike["start_date_only"].apply(lambda x: datetime.datetime.strptime(str(x), '%Y-%m-%d'))
bike["end_date_only"] = bike["end_date_only"].apply(lambda x: datetime.datetime.strptime(str(x), '%Y-%m-%d'))



#=================================Station Data=================================
stations = pd.read_csv("C:/Users/becky/OneDrive/Desktop/net_balance/Verdun_stations.csv")
list_code = stations["Code"].tolist()


#===================================Time=======================================
#============================Loop Count Difference=============================
def date_bixi(date):
    
    #time
    list_time = [date+" 08:00:00",date+" 08:59:59",
             date+" 09:00:00",date+" 09:59:59",
             date+" 10:00:00",date+" 10:59:59",
             date+" 11:00:00",date+" 11:59:59",
             date+" 12:00:00",date+" 12:59:59",
             date+" 13:00:00",date+" 13:59:59",
             date+" 14:00:00",date+" 14:59:59",
             date+" 15:00:00",date+" 15:59:59",
             date+" 16:00:00",date+" 16:59:59",
             date+" 17:00:00",date+" 17:59:59",
             date+" 18:00:00",date+" 18:59:59",
             date+" 19:00:00",date+" 19:59:59",
             date+" 20:00:00",date+" 20:59:59",
             date+" 21:00:00",date+" 07:59:59"]
    
    #column names
    list_name = ['count_diff_8',
             'count_diff_9',
             'count_diff_10',
             'count_diff_11',
             'count_diff_12',
             'count_diff_13',
             'count_diff_14',
             'count_diff_15',
             'count_diff_16',
             'count_diff_17',
             'count_diff_18',
             'count_diff_19',
             'count_diff_20',
             "count_diff_rest"]
    
    
    
    #create a new dataframe
    net_balance = pd.DataFrame(list_code, columns = ["station_code"])
    
    
    #choose a specific day
    bike_1 = bike[(bike.start_date_only == date)&(bike.end_date_only == date)]
    
    
    #loop over time range during aday
    for i in range (0,len(list_time),2):
        bike_2 = bike_1[(bike_1.start_date >= datetime.datetime.strptime(list_time[i], '%Y-%m-%d %H:%M:%S')) \
                        & (bike_1.start_date <= datetime.datetime.strptime(list_time[i+1], '%Y-%m-%d %H:%M:%S'))]
        
        
        
    #start station at time i
        #only start-station within the specific region
        bike_start = bike_2[bike_2['start_station_code'].isin(list_code)]
        bike_start = bike_start[["start_date","start_station_code"]]
        
        #merge two datasets
        starting_join_1 = pd.merge(bike_start, stations, how="left", left_on="start_station_code", right_on="Code")
        
        #frequency of each station
        freq_1=starting_join_1[["start_station_code"]].groupby(["start_station_code"]).size().reset_index(name='counts').sort_values(by=["counts"], ascending=False)
        
        #append station that has not been used during that hour
        list_code_start = freq_1["start_station_code"].tolist()
        not_in_start = list(set(list_code) - set(list_code_start))
        for j in not_in_start:
            freq_1 = freq_1.append({'start_station_code':j,"counts":0},ignore_index=True)
            freq_1.reset_index()
        

    
    
        
    #end station at time i
        bike_3 = bike_1[(bike_1.end_date >= datetime.datetime.strptime(list_time[i], '%Y-%m-%d %H:%M:%S')) \
                        & (bike_1.end_date <= datetime.datetime.strptime(list_time[i+1], '%Y-%m-%d %H:%M:%S'))]
        
        #only end-station within the specific region
        bike_end = bike_3[bike_3['end_station_code'].isin(list_code)]
        bike_end = bike_end[["end_date","end_station_code"]]
        
        #merge two datasets
        ending_join_1 = pd.merge(bike_end, stations, how="left", left_on="end_station_code", right_on="Code")
        
        #frequency of each station
        freq_2=ending_join_1[["end_station_code"]].groupby(["end_station_code"]).size().reset_index(name='counts').sort_values(by=["counts"], ascending=False)
        
        #append station that has not been used during that hour
        list_code_end = freq_2["end_station_code"].tolist()
        not_in_end = list(set(list_code) - set(list_code_end))
        for j in not_in_end:
            freq_2 = freq_2.append({'end_station_code':j,"counts":0},ignore_index=True)
            freq_2.reset_index()
        
    
    
    
    #Compute the difference
        freq_2 = freq_2.rename(columns={"counts":"count_EOD"})
        freq_1 = freq_1.rename(columns={"counts":"count_BOD"})
        freq_join = pd.merge(freq_2,freq_1, how="outer", left_on="end_station_code",right_on="start_station_code")
        freq_join["count_diff"] = freq_join["count_EOD"] - freq_join["count_BOD"]
        freq_list = pd.Series(freq_join["count_diff"].tolist())
        
    
    #Append the count_diff to net_balance dataframe
        net_balance[list_time[i]] = freq_list 
                
    
        
    #Export as csv
    net_balance.to_csv("C:/Users/becky/OneDrive/Desktop/net_balance" + date + ".csv")
        
    
    return net_balance
    

#================================Result========================================
start = timeit.default_timer()
date_bixi("2019-07-11")
stop = timeit.default_timer()
print('Time: ', stop - start)  



#============================Find the dock capacity============================

net_balances= [pd.read_csv(f"C:/Users/becky/OneDrive/Desktop/net_balance/net_balance2019-07-{i:02d}.csv") for i in [8, 9, 10, 11, 12, 13, 14]]


nets = [x.iloc[:,2:] for x in net_balances]    

    
from functools import reduce
merged_net = reduce(lambda x,y: x.merge(y, left_index=True, right_index=True),nets)


merged_net['max_value'] = merged_net.max(axis=1)


# create a list of our conditions
conditions = [
    (merged_net['max_value'] < 5),
    (merged_net['max_value'] < 10) & (merged_net['max_value'] >= 5),
    (merged_net['max_value'] < 15) & (merged_net['max_value'] >= 10),
    (merged_net['max_value'] < 20) & (merged_net['max_value'] >= 15),
    (merged_net['max_value'] < 25) & (merged_net['max_value'] >= 20),
    (merged_net['max_value'] < 30) & (merged_net['max_value'] >= 25),
    (merged_net['max_value'] >= 30)
    ]

# create a list of the values we want to assign for each condition
values = [10, 15, 20, 25, 30, 35, 45]

# create a new column and use np.select to assign values to it using our lists as arguments
merged_net['dock capacity'] = np.select(conditions, values)

# display updated DataFrame
merged_net["dock capacity"]


#export dock capacity
dock_capacity = merged_net[["dock capacity"]]
code = net_balances[0][["station_code"]]
dock_capacity = dock_capacity.merge(code, left_index=True, right_index=True)
dock_capacity.to_csv("C:/Users/becky/OneDrive/Desktop/dock_capacity.csv")



#============================Plot BIXI distribution============================

#Average net balance per hour in Verdun (weekdays)
plot1 = abs(net_balances[0].iloc[:,2:]).mean()
plot1 = plot1.to_frame()
plot1 = plot1.reset_index()
plot1 = plot1.rename(columns={"index":"hour", 0:"average_movement"})

plt = plot1.plot.bar(x='hour', y='average_movement') 


#Average net balance per hour in Verdun (weekend)
plot2 = abs(net_balances[5].iloc[:,2:]).mean()
plot2 = plot2.to_frame()
plot2 = plot2.reset_index()
plot2 = plot2.rename(columns={"index":"hour", 0:"average_movement"})

plt = plot2.plot.bar(x='hour', y='average_movement') 



#Verdun stations

stations = pd.read_csv("C:/Users/becky/OneDrive/Desktop/net_balance/Stations_2019.csv")

list_code = [6427,6341,7144,6425,7060,6379,6426,7057,6309,6705,7059,7145,6706,7056,7143,6715,7058]

conditions = [
    (stations.Code.isin(list_code)),
    (~stations.Code.isin(list_code))
]
values = [1,0]
stations['Verdun'] = np.select(conditions, values)

df = stations

fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", size_max=15, zoom=10,
                  mapbox_style="carto-positron",hover_name="Code",color="Verdun",
                        color_continuous_scale=px.colors.diverging.Fall)
fig.show()













