import requests
import streamlit as st
from datetime import datetime
import pytz
from config import API_BASE, VENDOR_ID, TIMEZONE, REQUEST_TIMEOUT

def format_timestamp(timestamp_str):
    """Format timestamp to readable format in IST"""
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        ist = pytz.timezone(TIMEZONE)
        dt_ist = dt.astimezone(ist)
        return dt_ist.strftime("%H:%M")
    except:
        return "00:00"

def get_active_users():
    """Fetch active users from API"""
    try:
        response = requests.get(f"{API_BASE}/admin/users/{VENDOR_ID}", timeout=5)
        if response.status_code == 200:
            return response.json().get('users', [])
    except Exception as e:
        st.error(f"Error fetching users: {e}")
    return []

def get_messages(user_id):
    """Fetch messages for a specific user"""
    try:
        response = requests.get(f"{API_BASE}/admin/messages/{VENDOR_ID}/{user_id}", timeout=5)
        if response.status_code == 200:
            return response.json().get('messages', [])
    except Exception as e:
        st.error(f"Error fetching messages: {e}")
    return []

def send_message(user_id, message):
    """Send message to user"""
    try:
        print(f"Sending message to user {user_id}: {message}")
        response = requests.post(
            f"{API_BASE}/admin/send-message",
            json={
                "vendorId": VENDOR_ID,
                "userId": user_id,
                "message": message
            },
            timeout=REQUEST_TIMEOUT
        )
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            return result.get('success', False)
        else:
            st.error(f"Server returned status {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        st.error("Request timeout - message sending took too long")
        return False
    except requests.exceptions.ConnectionError:
        st.error("Connection error - check if OMS server is running")
        return False
    except Exception as e:
        st.error(f"Error sending message: {str(e)}")
        print(f"Exception details: {e}")
        return False

def test_connection():
    """Test server connection"""
    try:
        response = requests.get(f"{API_BASE}/admin/test-redis", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_display_name(user_name, user_id):
    """Get display name for user"""
    if user_name and user_name != "Unknown":
        return user_name
    return f"User {user_id[-4:]}"