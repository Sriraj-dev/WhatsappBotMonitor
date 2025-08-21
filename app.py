import streamlit as st
from streamlit_autorefresh import st_autorefresh
from streamlit.components.v1 import html as st_html
import streamlit.components.v1 as components
import random

import time
import html
from config import PAGE_CONFIG, CUSTOM_CSS
from utils import (
    format_timestamp, get_active_users, get_messages, 
    send_message, test_connection, get_display_name
)

st.set_page_config(**PAGE_CONFIG)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)



# Initialize session state
if 'selected_user' not in st.session_state:
    st.session_state.selected_user = None

# Main App
def main():
    # Only show title when no user is selected
    if not st.session_state.selected_user:
        st.title("💬 WhatsApp Admin Dashboard")
    
    # Connection status
    if test_connection():
        if not st.session_state.selected_user:
            st.success("🟢 Connected to OMS Server")
    else:
        st.error("🔴 Cannot connect to OMS Server")
        st.stop()
    
    # Sidebar - User List
    with st.sidebar:
        # Controls
        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button("🔄 Refresh", use_container_width=True):
                st.rerun()
        with col2:
            # Auto-refresh toggle
            auto_refresh = st.toggle("⏱ Auto (10s)", key="auto_refresh")

        st.header("🔥 Active Conversations")
        
        # Search bar
        search_query = st.text_input("🔍 Search contacts", placeholder="Search by name or phone...", label_visibility="collapsed")

        if auto_refresh:
            st_autorefresh(interval=10 * 1000, key="refresh")
        
        # Fetch users
        users = get_active_users()
        
        # Filter users based on search
        if search_query:
            filtered_users = []
            for user in users:
                user_name = get_display_name(user['userName'], user['userId']).lower()
                user_phone = user['userId'][2:]
                if search_query.lower() in user_name or search_query in user_phone:
                    filtered_users.append(user)
            users = filtered_users
        
        if users:
            st.write(f"**{len(users)} active users**")
            
            for user in users:
                user_id = user['userId']
                user_name = get_display_name(user['userName'], user_id)
                last_msg : str = user['lastMessage']
                last_time = format_timestamp(user['lastMessageTime'])
                direction_icon = "" if user['direction'] == 'out' else ""
                phone = f"{user_id[2:]}"
                
                # User card
                if st.button(
                    f"{direction_icon} **{user_name}** ({phone})  \n{last_msg[:25]} *{last_time}*",
                    key=f"user_{user_id}",
                    use_container_width=True
                ):
                    st.session_state.selected_user = user
                    st.rerun()
        else:
            st.info("No active conversations")
    
    # Main Chat Area
    if st.session_state.selected_user:
        user = st.session_state.selected_user
        user_id = user['userId']
        user_name = get_display_name(user['userName'], user_id)
        
        st.markdown(f"#### 💬 {user_name} ({user_id})")
        # chatScreen_html = '<div class="chat-screen" id="chat-screen">'
        # chatScreen_html += f'<h3>💬 {user_name} ({user_id})</h3>'
        
        # Messages Container
        messages = get_messages(user_id)

        # Build all messages HTML in one block
        messages_html = '<div class="chat-container" id="chat-container">'
        
        if messages:
            for msg in messages:
                timestamp = format_timestamp(msg['timestamp'])
                escaped_message = html.escape(msg['message'])
                
                if msg['direction'] == 'in':
                    messages_html += f'<div class="message-left"><div class="user-message"><div class="message-sender">{html.escape(user_name)}</div><div>{escaped_message}</div><div class="message-timestamp">{timestamp}</div></div></div>'
                else:
                    messages_html += f'<div class="message-right"><div class="bot-message"><div class="message-sender">You (Bot)</div><div>{escaped_message}</div><div class="message-timestamp">{timestamp}</div></div></div>'
            messages_html += '<div id="end-of-chat"></div>'

        # st.markdown(messages_html, unsafe_allow_html=True)
        messages_html += '</div>'
        # chatScreen_html += messages_html
        # chatScreen_html += '</div>'
        st.markdown(messages_html, unsafe_allow_html=True)
        # components.html(chatScreen_html)


        # Message Input
        form_key = f"send_message_form_{user_id}"
        with st.form(form_key, clear_on_submit=True):
            col1, col2 = st.columns([9, 1])
            
            with col1:
                message_input = st.text_input(
                    "",
                    placeholder="Type your message...",
                    label_visibility="collapsed"
                )
            
            with col2:
                send_button = st.form_submit_button("➤", use_container_width=True)
            
            if send_button and message_input and message_input.strip():
                with st.spinner("Sending..."):
                    success = send_message(user_id, message_input.strip())
                
                if success:
                    st.success("✅ Message sent!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("❌ Failed to send")
        
    
    else:
        # Welcome screen
        st.markdown("""
        ### 🚀 Welcome to WhatsApp Admin Dashboard
        
        Select a conversation from the sidebar to start monitoring messages and sending custom responses.
        
        #### Features:
        - 📱 Monitor all WhatsApp conversations
        - 💬 View message history
        - 📤 Send custom messages to users
        - 🔄 Manual refresh available
        
        #### Getting Started:
        1. Check the connection status above
        2. Select a user from the sidebar
        3. View their conversation history
        4. Send custom messages as needed
        """)



# Run the main app
main()