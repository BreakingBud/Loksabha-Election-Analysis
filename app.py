import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# Load the data
file_path = 'results_2024_winners.csv'
data = pd.read_csv(file_path)

# Data preprocessing
data['Margin Votes'] = data['Margin Votes'].str.replace(',', '').replace('-', '0').astype(int)
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
data['Party Abbreviation'] = data['Winning Party'].map(party_abbreviations).fillna(data['Winning Party'])

# Calculate the number of seats won by each party
party_seats = data['Winning Party'].value_counts().reset_index()
party_seats.columns = ['Winning Party', 'Seats']
party_seats = party_seats.merge(pd.DataFrame(list(party_abbreviations.items()), columns=['Winning Party', 'Party Abbreviation']), on='Winning Party')

# Streamlit app
st.set_page_config(page_title='Lok Sabha Results', layout='wide')

# Collapsible hamburger menu
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Heat Map", "State Wise Analysis"],
        icons=["map", "bar-chart"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
    )

st.title('Lok Sabha Results')

# Heat Map Page
if selected == "Heat Map":
    st.header('Number of Seats Won by Each Party - Heat Map')
    fig = px.treemap(party_seats, path=['Party Abbreviation'], values='Seats', color='Seats',
                     color_continuous_scale='Viridis', title='Number of Seats Won by Each Party',
                     hover_data={'Winning Party': True, 'Seats': True})
    st.plotly_chart(fig)

# State Wise Analysis Page
elif selected == "State Wise Analysis":
    st.header('State Wise Analysis')

    # Dropdown menu for selecting state
    states = data['State'].unique()
    selected_state = st.selectbox('Select a State', states)

    # Filter data based on selected state
    state_data = data[data['State'] == selected_state]
    state_party_seats = state_data['Winning Party'].value_counts().reset_index()
    state_party_seats.columns = ['Winning Party', 'Seats']
    state_party_seats = state_party_seats.merge(pd.DataFrame(list(party_abbreviations.items()), columns=['Winning Party', 'Party Abbreviation']), on='Winning Party')

    # Heatmap for selected state
    st.header(f'Number of Seats Won by Each Party in {selected_state}')
    fig_state = px.treemap(state_party_seats, path=['Party Abbreviation'], values='Seats', color='Seats',
                           color_continuous_scale='Viridis', title=f'Number of Seats Won by Each Party in {selected_state}',
                           hover_data={'Winning Party': True, 'Seats': True})
    st.plotly_chart(fig_state)
