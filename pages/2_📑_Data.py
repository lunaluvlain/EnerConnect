import pandas as pd
import streamlit as st

# Page configuration
st.set_page_config(page_title="Data | EnerConnect", layout="wide")

# Load dataset
df = st.session_state.get("df", None)
if df is None:
    st.error("Data not found. Please upload the dataset first.")
else:
    # Total cities and overall electricity consumption
    total_cities = df['City'].nunique()
    total_consumption = df['Consumption of Electricity (in lakh units)-Total Consumption'].sum()

    # Average electricity consumption
    average_consumption = df['Consumption of Electricity (in lakh units)-Total Consumption'].mean()

    # Highest and lowest electricity consumption
    highest_consumption = df.loc[df['Consumption of Electricity (in lakh units)-Total Consumption'].idxmax()]
    lowest_consumption = df.loc[df['Consumption of Electricity (in lakh units)-Total Consumption'].idxmin()]

    # Judul dan deskripsi halaman
    st.title("💡 Electricity Consumption Analysis 💡")
    st.markdown(f"""
        This page provides a detailed analysis of electricity consumption across cities. 
        There are a total of {total_cities}  in the dataset.
        You can explore metrics such as total consumption, average consumption, and 
        categorical breakdowns of electricity usage. Additionally, you can download the 
        processed dataset for further analysis.
    """)
    st.markdown('<hr style="border: 2px solid orange;">', unsafe_allow_html=True)

    # Display key metrics
    col1, col2  = st.columns(2, gap ='large')
    with col1 :
        st.info("Total Electricity Consumption", icon = '📌')
        st.metric(label="in Lakh Units", value=f"{total_consumption:.2f}")
    
    with col2 :
        st.info("Average Electricity Consumption", icon = '📌')
        st.metric(label="in Lakh Units", value=f"{average_consumption:.2f}")
    
    col3, col4 = st.columns(2, gap ='large')
    with col3:
        st.info("City with Highest Consumption", icon='📌')
        st.metric(label="in Lakh Units", value=f"{highest_consumption['City']} : {highest_consumption['Consumption of Electricity (in lakh units)-Total Consumption']:.2f}")

    with col4:
        st.info("City with Lowest Consumption", icon='📌')
        st.metric(label="in Lakh Units", value=f"{lowest_consumption['City']} : {lowest_consumption['Consumption of Electricity (in lakh units)-Total Consumption']:.2f}")

    st.markdown('<hr style="border: 2px solid orange;">', unsafe_allow_html=True)

    # Bar chart for electricity distribution
    st.subheader("🌆 Electricity Consumption Distribution")
    st.bar_chart(df.set_index('City')['Consumption of Electricity (in lakh units)-Total Consumption'])

    # Tambahkan CSS untuk membuat judul kolom rata tengah
    st.markdown("""
        <style>
        table {
            width: 100%;
        }
        th {
            text-align: center !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Filter by consumption category
    st.subheader("🌆 Analysis by Consumption Category")
    categories = {
        'Domestic': 'Consumption of Electricity (in lakh units)-Domestic purpose',
        'Commercial': 'Consumption of Electricity (in lakh units)-Commercial purpose',
        'Industry': 'Consumption of Electricity (in lakh units)-Industry purpose',
        'Public Water Work & Street Light': 'Consumption of Electricity (in lakh units)-Public Water Work & Street Light',
        'Others': 'Consumption of Electricity (in lakh units)-Others'
    }

    category_selected = st.selectbox("Select Consumption Category", list(categories.keys()))
    category_column = categories[category_selected]

    if category_column in df.columns:
        filtered_data = df[['City', category_column]].sort_values(by=category_column, ascending=False).reset_index(drop=True)
        filtered_data['No.'] = filtered_data.index + 1
        filtered_data[category_column] = filtered_data[category_column].round(2)

        st.write(filtered_data[['No.', 'City', category_column]].to_html(index=False, escape=False), unsafe_allow_html=True)
    else:
        st.error(f"Column for {category_selected} not found in the dataset.")

    # Converting latitude and longitude if necessary
    df['Latitude'] = pd.to_numeric(df['Latitude'].astype(str).str.replace(',', '.', regex=False), errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'].astype(str).str.replace(',', '.', regex=False), errors='coerce')

    category_cols = list(categories.values())
    for col in category_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df[category_cols] = df[category_cols].fillna(df[category_cols].mean())

    df['Consumption of Electricity (in lakh units)-Total Consumption'] = df[category_cols].sum(axis=1)
    df['Total Consumption (MWh)'] = (df['Consumption of Electricity (in lakh units)-Total Consumption'] * 100).round(2)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Group cities by electricity consumption
    low_consumption = df[df['Total Consumption (MWh)'] < 50000]
    medium_consumption = df[(df['Total Consumption (MWh)'] >= 50000) & (df['Total Consumption (MWh)'] <= 200000)]
    high_consumption = df[df['Total Consumption (MWh)'] > 200000]

    for group in [low_consumption, medium_consumption, high_consumption]:
        group.reset_index(drop=True, inplace=True)  # Reset index
        group['No.'] = group.index + 1
        group[category_cols + ['Total Consumption (MWh)']] = group[category_cols + ['Total Consumption (MWh)']].round(2)

    # Display tables
    st.subheader("🌆 Low Electricity Consumption (< 50,000 MWh)")
    st.write(low_consumption[['No.', 'City', *category_cols, 'Total Consumption (MWh)']].to_html(index=False, escape=False), unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)

    st.subheader("🌆 Medium Electricity Consumption (50,000 - 200,000 MWh)")
    st.write(medium_consumption[['No.', 'City', *category_cols, 'Total Consumption (MWh)']].to_html(index=False, escape=False), unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)

    st.subheader("🌆 High Electricity Consumption (> 200,000 MWh)")
    st.write(high_consumption[['No.', 'City', *category_cols, 'Total Consumption (MWh)']].to_html(index=False, escape=False), unsafe_allow_html=True)

    # Download button for the dataset
    @st.cache_data
    def convert_df(df):
        return df.round(2).to_csv(index=False).encode('utf-8')

    csv = convert_df(df)
    st.download_button(label="Download Dataset", data=csv, file_name='dataset.csv', mime='text/csv')

    st.markdown("""
    <div style="text-align: center; color: gray;">
        <small>© 2024 EnerConnect. All rights reserved.</small>
    </div>
    """, unsafe_allow_html=True)
