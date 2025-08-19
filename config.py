# Server Configuration
API_BASE = "https://ordermanagementsystem-production-dd4b.up.railway.app"
VENDOR_ID = "755562397636928"  # Andhra Ghuma Ghumalu

# UI Configuration
TIMEZONE = "Asia/Kolkata"
REQUEST_TIMEOUT = 15

# Streamlit Page Config
PAGE_CONFIG = {
    "page_title": "WhatsApp Admin Dashboard",
    "page_icon": "💬",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Custom CSS for better styling
CUSTOM_CSS = """
<style>
.stApp {
    background-color: #191919;
}

.stApp > header {
    background-color: #191919;
}

.stApp [data-testid="stHeader"] {
    background-color: #191919;
}

.stApp [data-testid="stSidebar"] {
    background-color: #202020;
}

.stApp .css-1d391kg {
    background-color: #202020;
}

.stMainBlockContainer {
    max-width: 900px;
    margin: auto auto;
    padding: 3rem 1rem;
}

.chat-wrapper {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 20px;
}

.message-left {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 10px;
}

.message-right {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 10px;
}

.user-message {
    background-color: #2A2A2A;
    color: #D9D9D9;
    padding: 12px 15px;
    border-radius: 15px;
    margin: 8px 0;
    max-width: 70%;
    box-shadow: 0 2px 5px rgba(0,0,0,0.3);
    font-size: 15px;
    line-height: 1.4;
}

.bot-message {
    background-color: #2A2A2A;
    color: #D9D9D9;
    padding: 12px 15px;
    border-radius: 15px;
    margin: 8px 0;
    max-width: 70%;
    box-shadow: 0 2px 5px rgba(0,0,0,0.3);
    font-size: 15px;
    line-height: 1.4;
}

.message-timestamp {
    font-size: 11px;
    color: #aaa;
    margin-top: 5px;
}

.message-sender {
    font-weight: bold;
    margin-bottom: 5px;
    font-size: 12px;
    color: #ACACAC;
}

.chat-container {
    height: calc(100vh - 250px);
    overflow-y: auto;
    padding: 20px;
    background-color: #191919;
    border-radius: 10px;
    margin: 10px 0;
    # border: 1px solid #333;
}

# .message-input-box {
#     position: fixed;
#     bottom: 20px;
#     left: 50%;
#     transform: translateX(-50%);
#     width: calc(100% - 400px);
#     max-width: 860px;
#     background-color: #191919;
#     padding: 15px;
#     border: 1px solid #333;
#     border-radius: 10px;
#     z-index: 1000;
# }
</style>
"""