import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import squarify

# Load the data
file_path = 'results_2024_winners.csv'
data = pd.read_csv(file_path)

# Data preprocessing
data['Margin Votes'] = data['Margin Votes'].str.replace(',', '').replace('-', '0').astype(int)

# Calculate the number of seats won by each party
party_seats = data['Winning Party'].value_counts().reset_index()
party_seats.columns = ['Winning Party', 'Seats']

# Streamlit app
st.title('Loksabha Election Results 2024 - Seats Won by Each Party')

# Treemap of number of seats won by each party
fig, ax = plt.subplots(1, figsize=(16, 10))
squarify.plot(sizes=party_seats['Seats'], label=party_seats['Winning Party'], alpha=.8, ax=ax)
ax.set_title('Number of Seats Won by Each Party', fontsize=20)
ax.axis('off')
st.pyplot(fig)
