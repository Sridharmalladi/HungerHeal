from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import streamlit as st
import time

# Cache for geocoded addresses to avoid repeated API calls
geocode_cache = {}

def geocode_address(address):
    """
    Convert an address to latitude and longitude coordinates
    
    Args:
        address (str): The address to geocode
        
    Returns:
        tuple: (latitude, longitude, status)
            latitude (float): The latitude coordinate
            longitude (float): The longitude coordinate
            status (bool): True if geocoding was successful, False otherwise
    """
    # Check cache first
    if address in geocode_cache:
        return geocode_cache[address]
    
    # Use a try-except block to handle potential geocoding errors
    try:
        # Create a geocoder with a custom user-agent (important for API usage policies)
        geolocator = Nominatim(user_agent="foodflow-app")
        
        # Geocode the address with a timeout
        location = geolocator.geocode(address, timeout=10)
        
        # If we got a result, return the coordinates and cache them
        if location:
            result = (location.latitude, location.longitude, True)
            geocode_cache[address] = result
            return result
        else:
            # No result found
            return (0, 0, False)
            
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        # Handle timeout or service unavailability
        st.error(f"Geocoding service error: {str(e)}. Please try again.")
        return (0, 0, False)
        
    except Exception as e:
        # Handle other exceptions
        st.error(f"Geocoding error: {str(e)}")
        return (0, 0, False)

def reverse_geocode(latitude, longitude):
    """
    Convert coordinates to an address
    
    Args:
        latitude (float): The latitude coordinate
        longitude (float): The longitude coordinate
        
    Returns:
        str: The address corresponding to the coordinates, or empty string if unsuccessful
    """
    try:
        # Create a geocoder with a custom user-agent
        geolocator = Nominatim(user_agent="foodflow-app")
        
        # Reverse geocode the coordinates
        location = geolocator.reverse((latitude, longitude), timeout=10)
        
        if location:
            return location.address
        else:
            return ""
            
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        # Handle timeout or service unavailability
        st.error(f"Reverse geocoding service error: {str(e)}")
        return ""
        
    except Exception as e:
        # Handle other exceptions
        st.error(f"Reverse geocoding error: {str(e)}")
        return ""