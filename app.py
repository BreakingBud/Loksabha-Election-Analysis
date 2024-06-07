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

# Create half-donut chart
fig_donut = go.Figure(go.Pie(
    labels=seat_counts['party'],
    values=seat_counts['seats'],
    hole=0.5,
    startangle=180,
    direction='clockwise',
    sort=False,
))

fig_donut.update_traces(
    textinfo='none',
    hoverinfo='label+value+percent'
)

fig_donut.update_layout(
    title='Seats Won by Each Party',
    showlegend=True,
    annotations=[dict(text='Seats', x=0.5, y=0.5, font_size=20, showarrow=False)],
    height=400,
    width=800
)

# Mask the bottom half of the donut to create a half-donut effect
fig_donut.update_layout(
    shapes=[
        dict(
            type="rect",
            x0=-0.5,
            y0=-1.5,
            x1=1.5,
            y1=0,
            xref="paper",
            yref="paper",
            fillcolor="black",
            line=dict(
                width=0
            ),
        )
    ]
)

st.plotly_chart(fig_donut)

# Display party-wise seat details
st.subheader('Detailed Results by Party')
for index, row in seat_counts.iterrows():
    st.write(f"**{row['party']}**: {row['seats']} seats")
