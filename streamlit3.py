import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Streamlit app
st.title("Skyscraper Data Analysis")

# Load the data
df = pd.read_csv('skyscrapers(in).csv', index_col=0)

# Display the dataframe
if st.checkbox('Show raw data'):
    st.subheader('Raw Data')
    st.write(df)


# Line chart
st.subheader("Skyscrapers Rank vs. Height")
st.line_chart(df[["statistics.rank", "statistics.height"]].set_index('statistics.rank'))

# Create a new column (before 2000)
df["before.2000"] = df["status.started.year"] < 2000

# Show data filtered by the new column
if st.checkbox('Show buildings completed before 2000'):
    st.subheader('Buildings Completed Before 2000')
    st.write(df[df["before.2000"]])


# Top 10 cities by average height
st.subheader("Top 10 Cities by Average Height")
top_cities = df[["location.city", "statistics.height"]].groupby("location.city").mean().sort_values("statistics.height", ascending=False).head(10)
st.write(top_cities)

# Function to create a pivot table
def make_pivot_table(row, col="status.current", data="statistics.height"):
    temp = df[[row, col, data]].loc[df[data] > 0].groupby([col, row]).mean().reset_index()
    temp = temp.pivot(columns=col, index=row, values=data)
    for i in temp.columns:
        for j in temp.index:
            try:
                temp.loc[j, i] = int(temp.loc[j, i])
            except:
                temp.loc[j, i] = 0
    return temp


# Pivot table examples
st.subheader("Pivot Tables")
if st.checkbox('Show Pivot Table by Material'):
    st.write(make_pivot_table("material"))
if st.checkbox('Show Pivot Table by Material and Started Year'):
    st.write(make_pivot_table("material", data = "status.started.year"))


# Scatter plot
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
st.pyplot(plt)


# Map plot
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

st.plotly_chart(fig)

def get_city_and_height(row):
    return row['location.city'], row['statistics.height']

city_height_pairs = [get_city_and_height(row) for index, row in df.iterrows()]

city_height_df = pd.DataFrame(city_height_pairs[:5], columns=["City", "Height"])
st.write(city_height_df)
