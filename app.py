import streamlit as st
import pandas as pd
import plotly.express as px
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
        options=["Heat Map", "State Wise Analysis", "Constituency Analysis"],
        icons=["map", "bar-chart", "pie-chart"],
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
    
    selected_party = st.selectbox('Select a Party to View Details', party_seats['Winning Party'])
    party_details = data_winners[data_winners['Winning Party'] == selected_party]
    st.dataframe(party_details)

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
    st.header(f'Number of Seats Won by Each Party in {selected_state}')
    fig_state = px.treemap(state_party_seats, path=['Party Abbreviation'], values='Seats', color='Seats',
                           color_continuous_scale='Viridis', title=f'Number of Seats Won by Each Party in {selected_state}',
                           hover_data={'Winning Party': True, 'Seats': True})
    st.plotly_chart(fig_state)
    
    selected_party_state = st.selectbox('Select a Party to View Details', state_party_seats['Winning Party'])
    party_state_details = state_data[state_data['Winning Party'] == selected_party_state]
    st.dataframe(party_state_details)

# Constituency Analysis Page
elif selected == "Constituency Analysis":
    st.header('Constituency Analysis')

    # Dropdown menu for selecting state
    states = data_constituencies['State'].unique()
    selected_state = st.selectbox('Select a State', states)

    # Filter constituencies based on selected state
    constituencies = data_constituencies[data_constituencies['State'] == selected_state]['PC Name'].unique()
    selected_constituency = st.selectbox('Select a Constituency', constituencies)

    # Filter data based on selected state and constituency
    constituency_data = data_constituencies[(data_constituencies['State'] == selected_state) & (data_constituencies['PC Name'] == selected_constituency)]

    # Winner information
    winner_data = constituency_data.loc[constituency_data['Total Votes'].idxmax()]
    winner_name = winner_data['Candidate']
    winner_party = winner_data['Party']

    # Treemap for vote share
    st.header(f'Vote Share in {selected_constituency}')
    fig_constituency = px.treemap(constituency_data, path=['Party'], values='Vote Share', color='Vote Share',
                                  color_continuous_scale='Viridis', title=f'Vote Share in {selected_constituency}',
                                  hover_data={'Total Votes': True, 'Candidate': True})
    st.plotly_chart(fig_constituency)

    # Display winner information
    st.write(f"**Winner:** {winner_name}")
    st.write(f"**Party:** {winner_party}")
    
    selected_candidate = st.selectbox('Select a Candidate to View Details', constituency_data['Candidate'])
    candidate_details = constituency_data[constituency_data['Candidate'] == selected_candidate]
    st.dataframe(candidate_details)
