import streamlit as st
from PIL import Image

# Page configuration
st.set_page_config(page_title="About Us | EnerConnect", layout="wide")

# Hero Section
st.markdown("""
<div style="text-align: center; background: linear-gradient(45deg, #ff6f00, #ffcc80); padding: 20px; color: white; border-radius: 10px;">
    <h1>🌟 Welcome to EnerConnect 🌟</h1>
    <p style="font-size: 18px; font-style: italic;">Innovating energy for a sustainable future.</p>
</div>
""", unsafe_allow_html=True)

# Main Information Box
st.markdown("""
<div style="background-color: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);">
    <p style="text-align: justify; font-size: 16px; font-family: 'Arial, sans-serif'; color: #808080;">
        <b>EnerConnect</b> is an innovative technology company committed to revolutionizing the electricity distribution system 
        through data-driven approaches and state-of-the-art technology. We believe that efficient and sustainable energy 
        is the key to a brighter and more inclusive future.
    </p>
    <div style="margin-top: 20px; padding: 10px; background-color: #f9f9f9; border-radius: 10px;">
        <div style="display: flex; justify-content: space-around; margin-top: 20px; text-align: center;">
            <div style="width: 25%; color: #808080;">
                <h4 style="color: #555555;">🌱 Mission</h4>
                <p style="font-size: 14px;">To optimize power distribution systems, reduce energy losses, and deliver greener, more sustainable solutions.</p>
            </div>
            <div style="width: 20%; color: #808080;">
                <h4 style="color: #555555;">🚀 Vision</h4>
                <p style="font-size: 14px;">To lead the transition to a smart, reliable, and eco-friendly energy future, setting benchmarks globally.</p>
            </div>
            <div style="width: 40%; color: #808080;">
                <h4 style="color: #555555;">💡 Core Values</h4>
                <p style="font-size: 14px;">
                    <b>Innovation:</b> Pioneering solutions that redefine efficiency.<br>
                    <b>Integrity:</b> Commitment to ethical and transparent practices.<br>
                    <b>Sustainability:</b> Empowering a greener tomorrow for all.
                </p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# FAQs Section
st.markdown('<hr style="border: 2px solid orange; margin-top: 40px;">', unsafe_allow_html=True)
st.subheader("❓ Frequently Asked Questions (FAQs)")

# Grouping FAQ data into relevant categories
faq_data = {
    "General Information": {
        "What services does EnerConenct offer?": "We specialize in optimizing electricity distribution and network analysis",
        "Who can benefit from EnerConnect's services?": "Our solutions are tailored for municipalities, businesses, and communities, making them scalable for both urban and rural regions."
    },
    "About the Analysis": {
        "What is the purpose of this analysis?": (
            "This analysis aims to understand electricity consumption trends across cities. "
            "It helps in identifying areas of high, medium, and low electricity demand, enabling better decision-making "
            "for power distribution and infrastructure planning."
        ),
        "How accurate is the data?": (
            "The data is sourced from authentic records and has been preprocessed to handle missing values. "
            "Any gaps in consumption data have been filled with the average values of the respective categories for accuracy."
        )
    },
    "Dataset and Download": {
        "How can I download the dataset?": (
            "You can download the processed dataset by clicking the 'Download Dataset' button provided at the bottom of the page. "
            "The dataset will be in CSV format with all the processed and cleaned data."
        )
    },
    "Technical Details": {
        "What factors influence the edge weights between cities?": (
            "The edge weights are influenced by two factors: "
            "1. Distance (60%): The geographic distance between two cities. "
            "2. Electricity Consumption (40%): The average electricity consumption between two cities. This helps prioritize connections based on energy demand."
        )
    }
}

# Displaying the FAQ sections
for category, faqs in faq_data.items():
    with st.expander(f"🔍 {category}"):
        for question, answer in faqs.items():
            # Displaying each question and its answer under the category expander
            st.write(f"**{question}**")
            st.write(answer)

# Footer Section
st.markdown('<hr style="border: 2px solid orange;">', unsafe_allow_html=True)
st.subheader("📞 Contact Us")
st.write("""
📍 Address: Surabaya State University, Indonesia  
         ☎️ Phone: +62 83106471599
""")


st.markdown("""
<div style="text-align: center; color: gray;">
    <small>© 2024 EnerConnect. All rights reserved.</small>
</div>
""", unsafe_allow_html=True)