import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('results_2024_winners.csv')

# Data processing
seat_counts = df['party'].value_counts().reset_index()
seat_counts.columns = ['party', 'seats']

# Streamlit app
st.title('Loksabha Election Results 2024')

# Plotly pie chart
fig_pie = px.pie(seat_counts, names='party', values='seats', title='Seats Won by Each Party')
st.plotly_chart(fig_pie)

# Display party information with Plotly bar chart
fig_bar = px.bar(seat_counts, x='party', y='seats', title='Seats Won by Each Party', text='seats')
fig_bar.update_traces(texttemplate='%{text}', textposition='outside')
fig_bar.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

st.plotly_chart(fig_bar)

# Display party-wise seat details
st.subheader('Detailed Results by Party')
for index, row in seat_counts.iterrows():
    st.write(f"**{row['party']}**: {row['seats']} seats")
