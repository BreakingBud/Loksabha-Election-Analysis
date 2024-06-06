import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

# Heatmap of number of seats won by each party
plt.figure(figsize=(12, 8))
heatmap_data = party_seats.pivot_table(index='Winning Party', values='Seats')
sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='Blues', linewidths=.5)
plt.title('Number of Seats Won by Each Party')
st.pyplot(plt)
