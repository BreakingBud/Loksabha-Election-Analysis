import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from streamlit_option_menu import option_menu

# Load the data
file_path_1 = 'results_2024_winners.csv'
file_path_2 = 'results_2024.csv'

try:
    data_winners = pd.read_csv(file_path_1)
except pd.errors.EmptyDataError:
    st.error("The file results_2024_winners.csv is empty or not found.")
    st.stop()

try:
    data_constituencies = pd.read_csv(file_path_2)
except pd.errors.EmptyDataError:
    st.error("The file results_2024.csv is empty or not found.")
    st.stop()

# Data preprocessing for winners data
data_winners['Margin Votes'] = data_winners['Margin Votes'].str.replace(',', '').replace('-', '0').astype(int)
data_winners['Winning Party'] = data_winners['Winning Party'].str.replace(r'\(.*?\)', '', regex=True).str.strip()

# Generate abbreviations for each party
def generate_abbreviation(name):
    words = name.split()
    if len(words) == 1:
        return name[:3].upper()
    else:
        return ''.join([word[0] for word in words]).upper()

party_names = data_winners['Winning Party'].unique()
party_abbreviations = {name: generate_abbreviation(name) for name in party_names}
data_winners['Party Abbreviation'] = data_winners['Winning Party'].map(party_abbreviations).fillna(data_winners['Winning Party'])

# Calculate the number of seats won by each party
party_seats = data_winners['Winning Party'].value_counts().reset_index()
party_seats.columns = ['Winning Party', 'Seats']
party_seats = party_seats.merge(pd.DataFrame(list(party_abbreviations.items()), columns=['Winning Party', 'Party Abbreviation']), on='Winning Party')

# Streamlit app
st.set_page_config(page_title='Lok Sabha Results', layout='wide')

# Collapsible hamburger menu
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Seat Distribution", "State Wise Analysis", "Constituency Analysis"],
        icons=["map", "bar-chart", "pie-chart"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
    )

st.title('Lok Sabha Results')

# Seat Distribution Page
if selected == "Seat Distribution":
    st.header('Distribution of 543 Seats')
    
    # Creating semi-circle coordinates
    theta = np.linspace(0, np.pi, 543)
    radius = 1
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)

    # Creating colors for each dot based on the party
    color_map = {
        party: color for party, color in zip(party_names, px.colors.qualitative.Plotly[:len(party_names)])
    }
    data_winners['Color'] = data_winners['Winning Party'].map(color_map)

    # Creating scatter plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='markers',
        marker=dict(
            size=10,
            color=data_winners['Color'],
            line=dict(width=2)
        ),
        text=data_winners['Winning Party'],
        hoverinfo='text'
    ))

    fig.update_layout(
        title='543 Constituencies Represented as Dots in a Semi-Circle',
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        showlegend=False,
        height=600
    )

    st.plotly_chart(fig)

# State Wise Analysis Page
elif selected == "State Wise Analysis":
    st.header('State Wise Analysis')

    # Dropdown menu for selecting state
    states = data_winners['State'].unique()
    selected_state = st.selectbox('Select a State', states)

    # Filter data based on selected state
    state_data = data_winners[data_winners['State'] == selected_state]
    state_party_seats = state_data['Winning Party'].value_counts().reset_index()
    state_party_seats.columns = ['Winning Party', 'Seats']
    state_party_seats = state_party_seats.merge(pd.DataFrame(list(party_abbreviations.items()), columns=['Winning Party', 'Party Abbreviation']), on='Winning Party')

    # Heatmap for selected state
    st.header(f'Number of Seats Won by Each Party in {selected_state}'
