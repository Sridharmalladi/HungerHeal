import streamlit as st
import folium
from streamlit_folium import folium_static
import time
from datetime import datetime, timedelta
import os
from PIL import Image
from folium.plugins import LocateControl
import math

# Import our custom modules
from firebase_config import (
    initialize_firebase,
    save_food_post,
    get_all_food_posts,
    delete_expired_posts,
    verify_user
)
from geo_utils import geocode_address

# Page configuration
st.set_page_config(
    page_title="HungerHeal - Surplus is Support",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    /* Base theme */
    .stApp {
        background-color: #121212;
    }
    
    /* Typography */
    * {
        color: #E0E0E0;
    }
    
    .main-title {
        font-size: 48px !important;
        font-weight: 700 !important;
        color: #4CAF50 !important;
        text-align: center !important;
        margin-bottom: 0 !important;
        padding: 20px 0 !important;
    }
    
    .sub-title {
        font-size: 24px !important;
        color: #81C784 !important;
        text-align: center !important;
        margin-bottom: 40px !important;
        font-style: italic !important;
    }

    /* Stats Cards */
    .stat-card {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin-bottom: 20px;
    }
    
    .stat-number {
        font-size: 36px !important;
        font-weight: 700 !important;
        color: #4CAF50 !important;
        margin-bottom: 10px !important;
    }
    
    .stat-label {
        font-size: 16px !important;
        color: #E0E0E0 !important;
    }

    /* Mission Section */
    .mission-text {
        font-size: 18px !important;
        line-height: 1.6 !important;
        color: #E0E0E0 !important;
    }

    /* Form Elements */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
        border: 1px solid #333333 !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #4CAF50 !important;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2) !important;
    }

    /* Labels */
    .stTextInput > label,
    .stNumberInput > label,
    .stTextArea > label {
        color: #E0E0E0 !important;
        font-weight: 500 !important;
        font-size: 16px !important;
        margin-bottom: 8px !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #4CAF50 !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        background-color: #388E3C !important;
        transform: translateY(-2px) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1E1E1E !important;
        padding: 10px !important;
        border-radius: 8px !important;
        gap: 10px !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: #E0E0E0 !important;
        background-color: #333333 !important;
        border-radius: 6px !important;
        padding: 8px 16px !important;
        font-weight: 500 !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #4CAF50 !important;
        color: white !important;
    }

    /* Form Container */
    .stForm > div {
        background-color: #1E1E1E !important;
        padding: 20px !important;
        border-radius: 12px !important;
        border: 1px solid #333333 !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: #1E1E1E !important;
        color: #E0E0E0 !important;
        border-radius: 8px !important;
    }

    .streamlit-expanderContent {
        background-color: #1E1E1E !important;
        color: #E0E0E0 !important;
        border: 1px solid #333333 !important;
        border-radius: 0 0 8px 8px !important;
    }

    /* Text and Content */
    p, li, h1, h2, h3, h4, h5, h6 {
        color: #E0E0E0 !important;
    }

    .stMarkdown a {
        color: #81C784 !important;
    }

    /* Slider */
    .stSlider > div > div > div > div {
        background-color: #4CAF50 !important;
    }

    /* Select Box */
    .stSelectbox > div > div {
        background-color: #1E1E1E !important;
    }

    .stSelectbox > div > div > div {
        color: #E0E0E0 !important;
    }

    /* Impact Stats */
    .impact-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }
    
    .impact-card {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        border-top: 4px solid #4CAF50;
    }
    
    .impact-number {
        font-size: 32px;
        font-weight: bold;
        color: #4CAF50;
        margin-bottom: 10px;
    }
    
    .impact-label {
        color: #E0E0E0;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Firebase
initialize_firebase()

# App Header
st.markdown("<h1 class='main-title'>HungerHeal</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Food That Finds a Home</p>", unsafe_allow_html=True)

# Create tabs
tab0, tab1, tab2 = st.tabs(["🌍 Our Mission", "📦 Post Surplus Food", "📍 Find Available Food"])

with tab0:
    st.markdown("""
    ## 🌍 A Global Crisis Hidden in Plain Sight
    
    Every single day, over 1.3 billion tons of food is wasted globally. That's nearly one-third of all food produced—gone. 
    Discarded. Dumped. Often, this food is still perfectly edible but ends up in landfills due to overproduction, 
    aesthetic standards, expiry confusion, or logistical inefficiencies.
    
    At the same time, 828 million people worldwide—1 in every 10 humans—go to bed hungry. Millions of families struggle 
    to put a basic meal on the table, while children suffer the lifelong consequences of malnutrition.
    """)
    
    # Impact Statistics
    st.markdown("""
    <div class="impact-grid">
        <div class="impact-card">
            <div class="impact-number">24.7%</div>
            <div class="impact-label">Global freshwater used for wasted food</div>
        </div>
        <div class="impact-card">
            <div class="impact-number">8-10%</div>
            <div class="impact-label">Greenhouse gas emissions from food waste</div>
        </div>
        <div class="impact-card">
            <div class="impact-number">44.3%</div>
            <div class="impact-label">Municipal waste from food in some cities</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ## 💡 Our Solution: Turn Surplus Into Support
    
    HungerHeal is born from a simple belief: **"No one should go hungry while good food is thrown away."**
    
    We connect:
    - 🏪 Food donors (restaurants, grocery stores, bakeries, caterers)
    - 👥 Receivers (NGOs, shelters, volunteers, families in need)
    
    Through our real-time, location-based system, surplus food can be posted and claimed in minutes. 
    No bureaucracy. No red tape. Just fast, efficient redistribution of what's already available.
    
    ## ❤️ Together, We Can Make a Difference
    
    HungerHeal is more than an app. It's a movement—a call to action for businesses, communities, and individuals 
    to come together and turn waste into hope.
    
    - Let's stop the waste
    - Let's feed the need
    - Let's build a world where no meal goes to waste, and no person goes hungry
    """)

with tab1:
    st.markdown("### Share Your Surplus Food")
    
    # Safety Guidelines
    with st.expander("📋 Safety Guidelines"):
        st.markdown("""
        ### For Food Donors:
        1. Ensure food is properly stored and handled
        2. Clearly label any allergens or special storage requirements
        3. Provide accurate expiry information
        4. Maintain food safety standards
        
        ### For Food Recipients:
        1. Verify food quality before accepting
        2. Check expiry dates
        3. Follow proper food handling procedures
        4. Report any issues immediately
        
        ### General Safety Tips:
        - Meet in public places
        - Verify identity when possible
        - Trust your instincts
        - Report suspicious activity
        """)
    
    # Form for posting food
    with st.form("food_post_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name or Business Name", placeholder="e.g., Green Plate Cafe")
            food_type = st.text_input("Food Type", placeholder="e.g., Biryani, Bread Loaf")
            business_type = st.selectbox("Business Type", 
                ["Restaurant", "Bakery", "Catering", "Grocery Store", "Individual", "Other"])
            
        with col2:
            contact = st.text_input("Contact Number", placeholder="+1234567890")
            quantity = st.number_input("Quantity Available", min_value=1, value=5)
            expiry_hours = st.number_input("Hours until expiry", min_value=1, max_value=48, value=24)
        
        address = st.text_input("Pickup Address", placeholder="Full address for pickup location")
        additional_info = st.text_area("Additional Information", 
            placeholder="Storage conditions, allergens, preparation details, etc.")
        
        # ID Verification
        st.markdown("### ID Verification (Optional but Recommended)")
        st.markdown("Uploading an ID increases your trust score and credibility")
        id_file = st.file_uploader("Upload ID (Business License, Government ID, etc.)", type=['jpg', 'jpeg', 'png', 'pdf'])
        
        submit_button = st.form_submit_button("Post Food Availability")
        
        if submit_button:
            if not (name and contact and food_type and address):
                st.error("Please fill out all required fields.")
            else:
                lat, lng, geocode_status = geocode_address(address)
                
                if geocode_status:
                    post_data = {
                        "name": name,
                        "contact": contact,
                        "food_type": food_type,
                        "quantity": quantity,
                        "address": address,
                        "latitude": lat,
                        "longitude": lng,
                        "timestamp": datetime.now().isoformat(),
                        "verified": id_file is not None,  # Set verified based on ID upload
                        "business_type": business_type,
                        "additional_info": additional_info,
                        "expiry_hours": expiry_hours
                    }
                    
                    success = save_food_post(post_data)
                    
                    if success:
                        st.success("Thank you for sharing! Your food post is now live on the map.")
                        if id_file:
                            st.success("Your ID has been uploaded and your post is marked as verified!")
                        st.balloons()
                    else:
                        st.error("There was an issue saving your post. Please try again.")
                else:
                    st.error("Could not find coordinates for this address. Please check and try again.")

with tab2:
    st.markdown("### Find Available Food Near You")
    
    # Add address search
    search_address = st.text_input("🔍 Search by address", placeholder="Enter an address to search")
    
    # Delete expired posts
    delete_expired_posts()
    
    # Get all food posts
    food_posts = get_all_food_posts()
    
    # Set default map center
    map_center = [40.7128, -74.0060]  # Default to New York City
    
    # Update map center if search address is provided
    if search_address:
        lat, lng, geocode_status = geocode_address(search_address)
        if geocode_status:
            map_center = [lat, lng]
            st.success("Map centered on your search location!")
        else:
            st.error("Could not find this address. Please check and try again.")
    elif food_posts:  # If no search address but we have posts, center on average location
        avg_lat = sum(post.get('latitude', 0) for post in food_posts) / len(food_posts)
        avg_lng = sum(post.get('longitude', 0) for post in food_posts) / len(food_posts)
        map_center = [avg_lat, avg_lng]
    
    m = folium.Map(location=map_center, zoom_start=12)
    LocateControl().add_to(m)
    
    # Add markers
    for post in food_posts:
        # Calculate trust score
        trust_score = 0
        if post.get('quantity', 0) > 0:
            trust_score += 1
        if post.get('business_type'):
            trust_score += 1
        if post.get('name'):
            trust_score += 1
        if post.get('contact'):
            trust_score += 2
        if post.get('address'):
            trust_score += 2
        if post.get('additional_info'):
            trust_score += 1
        if post.get('verified'):
            trust_score += 2

        # Calculate time left
        expiry_hours = post.get('expiry_hours', 24)
        try:
            post_time = datetime.fromisoformat(post.get('timestamp'))
        except Exception:
            post_time = datetime.now()
        expiry_time = post_time + timedelta(hours=expiry_hours)
        now = datetime.now()
        time_left = expiry_time - now
        if time_left.total_seconds() > 0:
            hours, remainder = divmod(int(time_left.total_seconds()), 3600)
            minutes = (remainder // 60)
            # Round minutes to nearest 15
            minutes = int(round(minutes / 15.0) * 15)
            if minutes == 60:
                hours += 1
                minutes = 0
            time_left_str = f"Time left to grab: {hours}h {minutes}m (approx.)"
        else:
            time_left_str = "Expired"

        popup_html = f"""
        <div style="width: 250px; font-family: system-ui;">
            <h3 style="color: #4CAF50; margin-bottom: 10px;">{post.get('food_type')}</h3>
            <p><strong>Quantity:</strong> {post.get('quantity')} units</p>
            <p><strong>Business:</strong> {post.get('business_type')}</p>
            <p><strong>Posted by:</strong> {post.get('name')}</p>
            <p><strong>Contact:</strong> {post.get('contact')}</p>
            <p><strong>Address:</strong> {post.get('address')}</p>
            <p><strong>Additional Info:</strong> {post.get('additional_info', 'N/A')}</p>
            <p><strong>Trust Score:</strong> {trust_score}/10</p>
            <p><em style="color: #666;">{time_left_str}</em></p>
        </div>
        """
        
        folium.Marker(
            location=[post.get('latitude'), post.get('longitude')],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{post.get('food_type')} - {post.get('quantity')} units",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
    
    # Display map
    folium_static(m, width=1000, height=600)
    
    st.info(f"Showing {len(food_posts)} available food posts")
