import pandas as pd
import numpy as np
import networkx as nx
import streamlit as st
from math import radians, sin, cos, sqrt, atan2
import pydeck as pdk
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Fullscreen

# Page configuration
st.set_page_config(page_title="Electricity | EnerConnect", layout="wide")

# Streamlit session state to retrieve data
if 'df' not in st.session_state:
    st.error("Data not found! Please visit the Home page first.")
else:
    df = st.session_state.df

# Title and description of the app
st.title("Electricity Distribution Optimization :zap:")
st.markdown("""
This page visualizes the electricity distribution network using the Minimum Spanning Tree (MST) algorithm. 
You can select a starting city, view the optimal distribution route, explore the network, view the connected cities, and examine the corresponding edge weights. 
The cost displayed is a combination of these factors, with the distance given a weight of 60% and electricity consumption a weight of 40%.
""")
st.subheader("Select the Starting City")
starting_city = st.selectbox("Choose one :", df['City'])

# Function to calculate distance using Haversine formula
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in km
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat / 2) ** 2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c  # Distance in kilometers

# Function to calculate edge weight based on distance and consumption
def calculate_edge_weight(row1, row2, distance_weight=0.6, consumption_weight=0.4):
    lat1, lon1 = float(row1['Latitude']), float(row1['Longitude'])
    lat2, lon2 = float(row2['Latitude']), float(row2['Longitude'])
    avg_consumption = (row1['Total Consumption (MWh)'] + row2['Total Consumption (MWh)']) / 2
    distance = calculate_distance(lat1, lon1, lat2, lon2)
    weight = (distance * distance_weight) + (avg_consumption * consumption_weight)
    return weight

# Create adjacency list with edge weights
def build_adjacency_list(df, distance_weight=0.6, consumption_weight=0.4):
    adjacency_list = {i: [] for i in range(len(df))}
    for i, row1 in df.iterrows():
        for j, row2 in df.iterrows():
            if i != j:
                weight = calculate_edge_weight(row1, row2, distance_weight, consumption_weight)
                adjacency_list[i].append((j, weight))  # Add edge with weight to the adjacency list
    return adjacency_list

# Map city to index
city_to_index = {city: idx for idx, city in enumerate(df['City'])}
index_to_city = {idx: city for city, idx in city_to_index.items()}

# Build the adjacency list using the provided weights
adjacency_list = build_adjacency_list(df)

# Prim's Algorithm for MST
def prim_mst(start_city_idx):
    visited = [False] * len(df)  # Track visited cities
    edges = []  # Store edges of the MST
    path = []  # Store the sequence of cities visited (path)
    visited[start_city_idx] = True  # Mark the start city as visited
    mst_cost = 0  # Total cost of the MST

    while len(edges) < len(df) - 1:  # Until we have n-1 edges in the MST
        min_edge = (None, None, float('inf'))  # Initialize with an infinitely large weight
        for u in range(len(df)):  # Iterate over all cities
            if visited[u]:  # Only process cities that have been visited
                for v, weight in adjacency_list[u]:  # Iterate over neighbors of city u
                    if not visited[v] and weight < min_edge[2]:  # Check if the neighbor v has not been visited and has a smaller weight
                        min_edge = (u, v, weight)  # Update the minimum edge

        u, v, weight = min_edge  # Extract the edge with the minimum weight
        if v is not None:  # If a valid edge is found
            visited[v] = True  # Mark the destination city as visited
            edges.append((u, v, weight))  # Add the edge to the MST
            path.append((index_to_city[u], index_to_city[v]))  # Add the path to the path list
            mst_cost += weight  # Add the weight to the total MST cost

    return edges, mst_cost, path  # Return the edges, total cost, and path sequence

# Convert selected city to index
start_city_idx = city_to_index[starting_city]

# Run Prim's Algorithm with the selected city
edges, total_cost, path = prim_mst(start_city_idx)

# Visualization with Pydeck
edges_for_display = [(index_to_city[u], index_to_city[v], f"Weight: {d:.2f}") for u, v, d in edges]
text_annotations = [{"position": [row['Longitude'], row['Latitude']], "text": row['City']} for _, row in df.iterrows()]

# Tabs for results
tab1, tab2, tab3 = st.tabs(["🗺️ Network Visualization", "⚖️ Edge Weights", "📈 Results"])

with tab1:
    st.subheader("Network Visualization on the Map")
    
    # Prepare data for pydeck visualization
    city_data = []
    for idx, row in df.iterrows():
        popup_text = f"City: {row['City']}<br>Consumption: {row['Total Consumption (MWh)']} MWh"
        # Set the color to white for the starting city, otherwise blue
        color = [255, 255, 255] if row['City'] == starting_city else [0, 0, 255]
        city_data.append({
            "coordinates": [row['Longitude'], row['Latitude']],
            "popup": popup_text,
            "radius": 10000,
            "color": color,  # Use the color here
        })


    edge_data = []
    for u, v, weight in edges:
        city1 = df.loc[df['City'] == index_to_city[u]].iloc[0]
        city2 = df.loc[df['City'] == index_to_city[v]].iloc[0]
        edge_data.append({
            "source_position": [city1['Longitude'], city1['Latitude']],
            "target_position": [city2['Longitude'], city2['Latitude']],
            "weight": f"{weight:.2f}",
            "popup": f"Connected Cities: {city1['City']} ↔ {city2['City']}<br>Weight: {weight:.2f}"
        })


    # City markers with popups
    city_layer = pdk.Layer(
        "ScatterplotLayer",
        data=city_data,
        get_position="coordinates",
        get_color="color",
        get_radius="radius",
        pickable=True,
    )

    # Edges with popups
    edge_layer = pdk.Layer(
        "LineLayer",
        data=edge_data,
        get_source_position="source_position",
        get_target_position="target_position",
        get_color=[255, 165, 0],
        get_width=2,
        pickable=True,
    )

    # Combine layers into a deck
    deck = pdk.Deck(
        layers=[city_layer, edge_layer],
        initial_view_state=pdk.ViewState(
            latitude=df['Latitude'].mean(),
            longitude=df['Longitude'].mean(),
            zoom=5,
        ),
        tooltip={
            "html": "{popup}",
            "style": {"backgroundColor": "steelblue", "color": "white"},
        },
    )
    st.pydeck_chart(deck)

with tab2:
    st.subheader("Edge Weights Table")
    edge_info = [{"Origin City": index_to_city[u], "Destination City": index_to_city[v], "Weight (Cost)": f"{weight:.2f}"} for u, v, weight in edges]
    edge_df = pd.DataFrame(edge_info)
    st.table(edge_df)

with tab3:
    st.metric(label="Total Cost of Minimum Spanning Tree (MST)", value=f"💰 {total_cost:.2f}")

    st.markdown("### Route of Cities in MST")

    # Dictionary untuk menyimpan rute per kota asal
    city_connections = {}

    # Grouping the edges by origin city
    for u, v, _ in edges:
        origin_city = index_to_city[u]
        destination_city = index_to_city[v]

        # Tambahkan destinasi ke kota asal yang sesuai
        if origin_city not in city_connections:
            city_connections[origin_city] = []
        city_connections[origin_city].append(destination_city)

    # Menyimpan nomor langkah progresif untuk kota yang sudah ditampilkan
    displayed_cities = set()
    step_counter = 1  # Nomor langkah dimulai dari 1

    for origin_city, destinations in city_connections.items():
        # Jika kota asal belum ditampilkan, tampilkan dan gunakan nomor langkah progresif yang baru
        if origin_city not in displayed_cities:
            displayed_cities.add(origin_city)

            # Tampilkan langkah progresif untuk kota asal dengan nomor besar dan font tebal
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <div style="font-size: 20px; font-weight: bold; color: #FFA500; margin-right: 10px;">
                        {step_counter}
                    </div>
                    <div style="font-size: 18px; color: #444;">
                        <strong>{origin_city}</strong>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            step_counter += 1  # Increment step for the next city

        # Tampilkan setiap rute yang berhubungan dengan kota asal tersebut dengan emoji penanda
        for destination_city in destinations:
            # Tampilkan rute dengan emoji bintang dan tanda panah yang lebih elegan
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px; background-color: #FFFAF0; border-radius: 8px; padding: 8px;">
                    <div style="font-size: 20px; margin-right: 10px;">
                        ⭐
                    </div>
                    <div style="font-size: 16px; color: #444;">
                        <strong>{origin_city} → {destination_city}</strong>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    # Kesimpulan
    st.markdown("""
    ### Conclusion
    The electricity distribution network, starting from the selected city, has been optimized using the Minimum Spanning Tree (MST) algorithm. This approach minimizes the total distribution cost by balancing both distance and electricity consumption.
    This model aids in making informed decisions regarding electricity distribution, contributing to more efficient and cost-effective energy management. Feel free to explore other starting city options to identify the most efficient route.
    """)

st.markdown("""
<div style="text-align: center; color: gray;">
    <small>© 2024 EnerConnect. All rights reserved.</small>
</div>
""", unsafe_allow_html=True)