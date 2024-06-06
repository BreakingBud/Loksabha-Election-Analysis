import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
file_path = 'results_2024_winners.csv'
data = pd.read_csv(file_path)

# Data preprocessing
data['Margin Votes'] = data['Margin Votes'].str.replace(',', '').replace('-', '0').astype(int)

# Remove brackets from party names
data['Winning Party'] = data['Winning Party'].str.replace(r'\(.*?\)', '', regex=True).str.strip()

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
data['Party Abbreviation'] = data['Winning Party'].map(party_abbreviations).fillna(data['Winning Party'])

# Calculate the number of seats won by each party
party_seats = data['Winning Party'].value_counts().reset_index()
party_seats.columns = ['Winning Party', 'Seats']

# Merge to get abbreviations in the party_seats dataframe
party_seats = party_seats.merge(pd.DataFrame(list(party_abbreviations.items()), columns=['Winning Party', 'Party Abbreviation']), on='Winning Party')

# Streamlit app
st.title('Loksabha Election Results 2024 - Seats Won by Each Party')

# Treemap of number of seats won by each party using plotly
fig = px.treemap(party_seats, path=['Party Abbreviation'], values='Seats', color='Seats',
                 color_continuous_scale='Viridis', title='Number of Seats Won by Each Party',
                 hover_data={'Winning Party': True, 'Seats': True})

st.plotly_chart(fig)
