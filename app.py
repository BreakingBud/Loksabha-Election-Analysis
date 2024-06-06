import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
file_path = 'results_2024_winners.csv'
data = pd.read_csv(file_path)

# Data preprocessing
data['Margin Votes'] = data['Margin Votes'].str.replace(',', '').replace('-', '0').astype(int)

# Generate abbreviations for each party
def generate_abbreviation(name):
    words = name.split()
    if len(words) == 1:
        return name[:3].upper()
    else:
        return ''.join([word[0] for word in words]).upper()

party_names = data['Winning Party'].unique()
party_abbreviations = {name: generate_abbreviation(name) for name in party_names}

# Apply the abbreviations to the data
data['Winning Party'] = data['Winning Party'].map(party_abbreviations).fillna(data['Winning Party'])

# Calculate the number of seats won by each party
party_seats = data['Winning Party'].value_counts().reset_index()
party_seats.columns = ['Winning Party', 'Seats']

# Streamlit app
st.title('Loksabha Election Results 2024 - Seats Won by Each Party')

# Treemap of number of seats won by each party using plotly
fig = px.treemap(party_seats, path=['Winning Party'], values='Seats', color='Seats',
                 color_continuous_scale='Viridis', title='Number of Seats Won by Each Party')

st.plotly_chart(fig)
