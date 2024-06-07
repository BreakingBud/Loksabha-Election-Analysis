import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load data
df = pd.read_csv('results_2024_winners.csv')

# Ensure 'Winning Party' column is correctly referenced
party_column_name = 'Winning Party'

# Data processing
seat_counts = df[party_column_name].value_counts().reset_index()
seat_counts.columns = ['party', 'seats']

# Streamlit app
st.title('Loksabha Election Results 2024')

# Plotly half-donut chart
fig_donut = go.Figure(go.Pie(
    labels=seat_counts['party'],
    values=seat_counts['seats'],
    hole=0.4,
    direction='clockwise',
    sort=False,
    startangle=180
))

fig_donut.update_traces(
    hoverinfo="label+percent+value",
    textinfo="none"
)

fig_donut.update_layout(
    title='Seats Won by Each Party',
    showlegend=False,
    annotations=[dict(text='Seats', x=0.5, y=0.5, font_size=20, showarrow=False)],
    height=600,
    width=800
)

fig_donut.update_layout(
    margin=dict(t=0, b=0, l=0, r=0),
    annotations=[dict(text='Seats', x=0.5, y=0.5, font_size=20, showarrow=False)],
)

st.plotly_chart(fig_donut)

# Display party-wise seat details
st.subheader('Detailed Results by Party')
for index, row in seat_counts.iterrows():
    st.write(f"**{row['party']}**: {row['seats']} seats")
