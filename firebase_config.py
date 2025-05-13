import firebase_admin
from firebase_admin import credentials, firestore
import json
import os
from datetime import datetime, timedelta
import streamlit as st

def initialize_firebase():
    """Initialize Firebase if not already initialized"""
    if not firebase_admin._apps:
        try:
            cred_path = "service_account.json"
            
            if not os.path.exists(cred_path):
                cred_data = {
                    "type": "service_account",
                    "project_id": "your-project-id",
                    "private_key_id": "your-private-key-id",
                    "private_key": "your-private-key",
                    "client_email": "your-client-email",
                    "client_id": "your-client-id",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": "your-cert-url"
                }
                
                with open(cred_path, "w") as f:
                    json.dump(cred_data, f, indent=2)
                
                st.warning("""
                ### Firebase Setup Required
                
                This app requires Firebase to store and retrieve food posts. Please follow these steps:
                
                1. Create a Firebase project at [firebase.google.com](https://firebase.google.com)
                2. Set up Firestore database
                3. Generate a service account key (Project Settings → Service accounts → Generate new private key)
                4. Replace the contents of `service_account.json` with your actual credentials
                
                Once configured, restart the app to connect to your Firebase project.
                """)
                
                cred = credentials.Certificate(cred_path)
            else:
                cred = credentials.Certificate(cred_path)
            
            firebase_admin.initialize_app(cred)
            
        except Exception as e:
            st.error(f"Firebase initialization error: {str(e)}")
            st.info("The app is running in demo mode with mock data.")

def verify_user(id_file):
    """Verify user with uploaded ID
    
    Args:
        id_file: The uploaded ID file
        
    Returns:
        bool: True if verification successful, False otherwise
    """
    try:
        # In a real implementation, this would include:
        # 1. OCR to extract information from ID
        # 2. Verification against official databases
        # 3. Manual review process
        # For demo purposes, we'll just simulate success
        st.session_state.verified = True
        return True
    except Exception as e:
        st.error(f"Verification error: {str(e)}")
        return False

def save_food_post(post_data):
    """Save food post data to Firestore
    
    Args:
        post_data (dict): The food post data to save
        
    Returns:
        bool: True if save was successful, False otherwise
    """
    try:
        if not firebase_admin._apps:
            return mock_save_food_post(post_data)
            
        db = firestore.client()
        db.collection('food_posts').add(post_data)
        return True
    except Exception as e:
        st.error(f"Error saving to Firestore: {str(e)}")
        return False

def get_all_food_posts():
    """Get all food posts from Firestore
    
    Returns:
        list: List of food post dictionaries
    """
    try:
        if not firebase_admin._apps:
            return mock_get_all_food_posts()
            
        db = firestore.client()
        posts_ref = db.collection('food_posts').order_by('timestamp', direction=firestore.Query.DESCENDING)
        posts = posts_ref.stream()
        
        return [post.to_dict() for post in posts]
    except Exception as e:
        st.error(f"Error retrieving from Firestore: {str(e)}")
        return []

def delete_expired_posts():
    """Delete posts that are past their expiry time"""
    try:
        if not firebase_admin._apps:
            return
            
        db = firestore.client()
        posts = db.collection('food_posts').stream()
        
        for post in posts:
            post_data = post.to_dict()
            post_time = datetime.fromisoformat(post_data['timestamp'])
            expiry_hours = post_data.get('expiry_hours', 24)
            if datetime.now() > post_time + timedelta(hours=expiry_hours):
                post.reference.delete()
            
    except Exception as e:
        st.error(f"Error deleting expired posts: {str(e)}")

def mock_save_food_post(post_data):
    """Mock function to save food post data when Firebase isn't configured"""
    mock_data = st.session_state.get('mock_food_posts', [])
    mock_data.append(post_data)
    st.session_state['mock_food_posts'] = mock_data
    return True

def mock_get_all_food_posts():
    """Mock function to get food posts when Firebase isn't configured"""
    if 'mock_food_posts' not in st.session_state:
        st.session_state['mock_food_posts'] = [
            {
                "name": "Green Plate Cafe",
                "contact": "+1-555-123-4567",
                "food_type": "Vegetable Curry",
                "quantity": 12,
                "address": "123 Main St, New York, NY",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "timestamp": datetime.now().isoformat(),
                "verified": True,
                "trust_score": 10,
                "business_type": "Restaurant",
                "additional_info": "Freshly made, contains dairy",
                "expiry_hours": 6
            },
            {
                "name": "Fresh Bakery",
                "contact": "+1-555-987-6543",
                "food_type": "Bread Loaves",
                "quantity": 25,
                "address": "456 Park Ave, New York, NY",
                "latitude": 40.7580,
                "longitude": -73.9855,
                "timestamp": datetime.now().isoformat(),
                "verified": False,
                "trust_score": 5,
                "business_type": "Bakery",
                "additional_info": "Assorted breads",
                "expiry_hours": 12
            },
            {
                "name": "Spice House Restaurant",
                "contact": "+1-555-444-5555",
                "food_type": "Chicken Biryani",
                "quantity": 18,
                "address": "789 Broadway, New York, NY",
                "latitude": 40.7484,
                "longitude": -73.9857,
                "timestamp": datetime.now().isoformat(),
                "verified": True,
                "trust_score": 8,
                "business_type": "Restaurant",
                "additional_info": "Contains nuts, dairy",
                "expiry_hours": 4
            }
        ]
    
    return st.session_state['mock_food_posts']