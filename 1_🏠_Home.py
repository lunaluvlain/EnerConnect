import streamlit as st
import pandas as pd
import pydeck as pdk

# Page configuration
st.set_page_config(page_title="Home | EnerConnect", layout="wide")

# Title and introduction
st.title("Electricity Consumption Analysis Across Indian Cities 🗺️")
st.image("Listrik.jpg")
st.markdown('<hr style="border: 2px solid orange;">', unsafe_allow_html=True)
st.markdown("""
India, a rapidly developing country, faces growing energy demands and significant challenges in ensuring efficient power distribution across its vast and diverse geography. From bustling metropolitan areas to remote rural villages, optimizing electricity networks is essential to support economic growth, improve energy accessibility, and reduce operational costs.

As India strives for sustainable and inclusive development, improving electricity distribution networks plays a pivotal role in building a robust infrastructure for the future. 
Join us in exploring how innovative solutions can transform India's energy landscape and shape its path toward progress.
""")

# Load dataset 
file_path = "DATASET DAA.csv"  
df = pd.read_csv(file_path, sep=',')  

# Convert Latitude and Longitude to strings, replace commas with dots, and convert to float
df['Latitude'] = df['Latitude'].astype(str).str.replace(',', '.', regex=False).astype(float)
df['Longitude'] = df['Longitude'].astype(str).str.replace(',', '.', regex=False).astype(float)

# Convert columns to numeric
category_cols = [
    'Consumption of Electricity (in lakh units)-Domestic purpose',
    'Consumption of Electricity (in lakh units)-Commercial purpose',
    'Consumption of Electricity (in lakh units)-Industry purpose',
    'Consumption of Electricity (in lakh units)-Public Water Work & Street Light',
    'Consumption of Electricity (in lakh units)-Others'
]

# Convert specified columns to numeric
for col in category_cols + ['Consumption of Electricity (in lakh units)-Total Consumption']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Fill missing values with the mean for the consumption columns
df[category_cols] = df[category_cols].fillna(df[category_cols].mean())

# Recalculate total consumption
df['Consumption of Electricity (in lakh units)-Total Consumption'] = df[category_cols].sum(axis=1)

# Convert total consumption to MWh
df['Total Consumption (MWh)'] = (df['Consumption of Electricity (in lakh units)-Total Consumption'] * 100).round(2)

# Normalize the consumption data for color scaling
df['color'] = df['Total Consumption (MWh)'].apply(
    lambda x: [250, 250, 0, 200] if x < 50000 else  # yellow for <50,000
              [255, 165, 0, 200] if 50000 <= x <= 200000 else  # Orange for 50,001 - 200,000
              [255, 0, 0, 200]  # Red for >200,000
)

# Store the dataframe in session state
st.session_state.df = df

# Create the tooltip content
tooltip = {
    "text": """{City} 
    Domestic Consumption: {Consumption of Electricity (in lakh units)-Domestic purpose} lakh units
    Commercial Consumption: {Consumption of Electricity (in lakh units)-Commercial purpose} lakh units
    Industry Consumption: {Consumption of Electricity (in lakh units)-Industry purpose} lakh units
    Public Consumption: {Consumption of Electricity (in lakh units)-Public Water Work & Street Light} lakh units
    Others Consumption: {Consumption of Electricity (in lakh units)-Others} lakh units
    Total Consumption (MWh): {Total Consumption (MWh)} MWh
    """,
    "style": {"backgroundColor": "steelblue", "color": "white"},
}

# Create the Pydeck layer
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position=["Longitude", "Latitude"],
    get_color="color",  # Use the 'color' column for dynamic colors
    get_radius=50000,  # Radius in meters
    pickable=True,
    auto_highlight=True,
)

# Define the map view
view_state = pdk.ViewState(
    latitude=df['Latitude'].mean(),
    longitude=df['Longitude'].mean(),
    zoom=5,
    pitch=0,
)

# Create the map
map = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip,  # Apply tooltip
)

# Display the map
st.markdown('<hr style="border: 2px solid orange;">', unsafe_allow_html=True)
st.subheader("Electricity Distribution Map")
st.write("Interactive map showing electricity distribution across various cities in India.")
st.pydeck_chart(map)

# Add legend with a more attractive design
st.markdown("""
    <div style="font-size: 16px; font-weight: bold;">Legend :</div>
    <div style="font-size: 14px;">
        <ul>
            <li><span style="color: #F2E300;">🟡</span> : Low Consumption (< 50,000 MWh)</li>
            <li><span style="color: #FFA500;">🟠</span> : Medium Consumption (50,000 - 200,000 MWh)</li>
            <li><span style="color: #FF0000;">🔴</span> : High Consumption (> 200,000 MWh)</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; color: gray;">
    <small>© 2024 EnerConnect. All rights reserved.</small>
</div>
""", unsafe_allow_html=True)