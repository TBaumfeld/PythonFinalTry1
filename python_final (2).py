# -*- coding: utf-8 -*-
"""Python Final"""

!pip install pandas
import pandas as pd
#"""
#Name:       Teddy Baumfeld
#CS230:      Section 2
#Data:       Skyscrapers.csv
#URL:        Link to your web application on Streamlit Cloud (if posted)

#Description:
#This program creates various tables, graphs, and charts to display interesting comparisons within the data about skyscrapers within the united states.

!pip install pandas
import pandas as pd
df = pd.read_csv('skyscrapers(in).csv', index_col = 0)
df[["statistics.rank" , "statistics.height"]].plot.line(x = "statistics.rank" , y = "statistics.height")

#[DA4] Filter data by one condition
#[DA7] Add/drop/select/create new/group columns
df["before.2000"] = df["status.started.year"] < 2000
df#["before.2000"]

#Sort data in ascending or descending order, by one or more columns
df[["location.city" , "statistics.height"]].groupby("location.city").mean().sort_values("statistics.height" , ascending = False).head(10)

#[DA3] Find Top largest or smallest values of a column CHECK
df[["location.city" , "statistics.height"]].head(10)

#[DA5] Filter data by two or more conditions with AND or OR  CHECK
df.loc[(df["status.completed.year"]< 1900)&(df["status.completed.year"]> 0)]



#[PY1] A function with two or more parameters, one of which has a default value, called at least twice (once with the default value, and once without)
#[PY3] Error checking with try/except
def make_pivot_table(row, col = "status.current", data = "statistics.height"):
      temp = df[[row, col, data]].loc[df[data]> 0].groupby([col, row]).mean().reset_index()
      temp = temp.pivot(columns = col, index = row, values = data)
      for i in temp.columns:
          for j in temp.index:
              try:
                  temp.loc[j, i] = int(temp.loc[j, i])
              except:
                  temp.loc[j, i] = 0
      return temp.reset_index

#[DA6] Analyze data with pivot tables
make_pivot_table("material")

#[DA6] Analyze data with pivot tables
make_pivot_table("material", data = "status.started.year")

cities = list (df["location.city"])
cities_dict = {}
for city in cities:
    if city not in cities_dict.keys():
      cities_dict[city] = 0
    else:
        cities_dict[city] += 1
cities_list = [x for x in cities_dict.keys() if type (x) is str]
cities_list

import pandas as pd
import matplotlib.pyplot as plt


df_filtered = df[df['status.completed.year'] != 0]


plt.figure(figsize=(12, 6))
plt.scatter(df_filtered['status.completed.year'], df_filtered['statistics.height'],
            c=df_filtered['status.completed.year'], cmap='viridis', alpha=0.7, label='Buildings')

plt.xlabel('Year Completed', fontsize=12)
plt.ylabel('Height (statistics.height)', fontsize=12)
plt.title('Building Height vs. Year Completed', fontsize=14)
plt.colorbar(label='Year Completed')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.show()

import plotly.graph_objects as go


city_heights = df.groupby('location.city').agg({
    'statistics.height': 'mean',
    'location.latitude': 'mean',
    'location.longitude': 'mean'
}).reset_index()


fig = go.Figure(data=go.Scattergeo(
    lon = city_heights['location.longitude'],
    lat = city_heights['location.latitude'],
    text = city_heights['location.city'],
    mode = 'markers',
    marker = dict(
        size = city_heights['statistics.height'] / 10,
        color = city_heights['statistics.height'],
        colorscale = 'Viridis',
        colorbar_title = "Average Height",
        line_width = 0.5
    )))

fig.update_layout(
    title_text = 'US Skyscrapers by City and Height',
    geo = dict(
        scope = 'usa',
        showland = True,
        landcolor = "rgb(212, 212, 212)",
        subunitcolor = "rgb(255, 255, 255)",
        countrycolor = "rgb(255, 255, 255)",
        showlakes = True,
        lakecolor = "rgb(255, 255, 255)",
        showsubunits = True,
        showcountries = True,
        resolution = 50,
        lonaxis_showgrid = True,
        lataxis_showgrid = True,
        projection_type = 'albers usa'
    ))

fig.show()

#[PY2] A function that returns more than one value
#[PY4] A list comprehension
def get_city_and_height(row):

    return row['location.city'], row['statistics.height']

city_height_pairs = [get_city_and_height(row) for index, row in df.iterrows()]


city_height_df = pd.DataFrame(city_height_pairs[:5], columns=["City", "Height"])
city_height_df
