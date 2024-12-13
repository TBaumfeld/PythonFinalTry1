import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st

# Function to create a pivot table (unchanged from original code)
def make_pivot_table(row, col="status.current", data="statistics.height"):
    temp = df[[row, col, data]].loc[df[data] > 0].groupby([col, row]).mean().reset_index()
    temp = temp.pivot(columns=col, index=row, values=data)
    for i in temp.columns:
        for j in temp.index:
            try:
                temp.loc[j, i] = int(temp.loc[j, i])
            except:
                temp.loc[j, i] = 0
    return temp.reset_index

# Function to get city and height pairs (unchanged from original code)
def get_city_and_height(row):
    return row['location.city'], row['statistics.height']


st.title("Skyscraper Data Visualization")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, index_col=0)
    
    # Play/Pause functionality (Placeholder - Add interactive elements here)
    play_pause_button = st.button("Play/Pause")

    # Line plot
    st.subheader("Skyscraper Rank vs. Height")
    st.line_chart(df[["statistics.rank", "statistics.height"]].set_index("statistics.rank"))

    # Scatter plot
    st.subheader("Building Height vs. Year Completed")
    df_filtered = df[df['status.completed.year'] != 0]
    fig, ax = plt.subplots()
    ax.scatter(df_filtered['status.completed.year'], df_filtered['statistics.height'],
               c=df_filtered['status.completed.year'], cmap='viridis', alpha=0.7, label='Buildings')
    ax.set_xlabel('Year Completed')
    ax.set_ylabel('Height')
    ax.set_title('Building Height vs. Year Completed')
    plt.colorbar(label='Year Completed')
    st.pyplot(fig)

    # Map plot
    st.subheader("US Skyscrapers by City and Height")
    city_heights = df.groupby('location.city').agg({
        'statistics.height': 'mean',
        'location.latitude': 'mean',
        'location.longitude': 'mean'
    }).reset_index()

    fig = go.Figure(data=go.Scattergeo(
        lon=city_heights['location.longitude'],
        lat=city_heights['location.latitude'],
        text=city_heights['location.city'],
        mode='markers',
        marker=dict(
            size=city_heights['statistics.height'] / 10,
            color=city_heights['statistics.height'],
            colorscale='Viridis',
            colorbar_title="Average Height",
            line_width=0.5
        )))

    fig.update_layout(
        title_text='US Skyscrapers by City and Height',
        geo=dict(
            scope='usa',
            showland=True,
            landcolor="rgb(212, 212, 212)",
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)",
            showlakes=True,
            lakecolor="rgb(255, 255, 255)",
            showsubunits=True,
            showcountries=True,
            resolution=50,
            lonaxis_showgrid=True,
            lataxis_showgrid=True,
            projection_type='albers usa'
        ))
    st.plotly_chart(fig)


    # Add more visualizations or data exploration as needed
else:
    st.write("Please upload a CSV file.")
