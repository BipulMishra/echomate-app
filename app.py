import streamlit as st
import google.generativeai as genai
import pandas as pd
import re
import random

# --- CONFIGURATION & PAGE SETUP ---
st.set_page_config(
    page_title="EchoMate ❤️",
    page_icon="🤖",
    layout="centered"
)

# --- GEMINI API CONFIGURATION ---
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except (KeyError, FileNotFoundError):
    st.error("⚠️ Gemini API Key not found!")
    st.info("For the app to work, the developer needs to set the API Key in the deployment secrets.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- SESSION STATE INITIALIZATION ---
if "processing_done" not in st.session_state:
    st.session_state.processing_done = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "person_messages" not in st.session_state:
    st.session_state.person_messages = []
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "target_name" not in st.session_state:
    st.session_state.target_name = ""


# --- PARSING FUNCTION (NOW UNIVERSAL FOR iOS & ANDROID) ---
def parse_chat_and_prepare(uploaded_file, user_name, target_name):
    """Reads the uploaded file and extracts messages from the target person."""
    try:
        chat_content = uploaded_file.read().decode('utf-8')
        lines = chat_content.splitlines()
        
        # --- THIS IS THE UNIVERSAL FIX ---
        # Define patterns for both platforms
        ios_pattern = re.compile(r'\[.*?\] ([^:]+): (.*)')
        android_pattern = re.compile(r'.*? - ([^:]+): (.*)')
        
        messages = []
        sanitized_target_name = re.sub(r'[^\w]', '', target_name).lower()

        for line in lines:
            # Check which pattern matches the line
            ios_match = ios_pattern.match(line)
            android_match = android_pattern.match(line)
            
            match = None
            if ios_match:
                match = ios_match
            elif android_match:
                match = android_match
            
            if match:
                sender_name_from_file = match.group(1)
                sanitized_file_name = re.sub(r'[^\w]', '', sender_name_from_file).lower()
                
                if sanitized_file_name == sanitized_target_name:
                    messages.append(match.group(2).strip())
        
        if not messages:
            st.error(f"Couldn't find any messages from '{target_name}'. Please double-check the spelling and ensure the file is a valid WhatsApp chat export.")
            return False
        
        st.session_state.person_messages = messages
        st.session_state.user_name = user_name
        st.session_state.target_name = target_name
        st.session_state.processing_done = True
        st.session_state.chat_history = [] 
        st.success(f"Great! I've learned the chat style of {target_name}. Let's talk!")
        return True

    except Exception as e:
        st.error(f"Oops! Something went wrong while reading the file: {e}")
        return False

# --- UI SETUP ---
st.title("EchoMate ❤️")
st.caption("Upload a WhatsApp chat and talk to a digital reflection of your loved one.")

st.info("📱 **Mobile User?** Click the `>` icon in the top-left corner to open the setup panel.", icon="💡")

with st.sidebar:
    st.header("Setup Your Chat Persona")
    uploaded_file = st.file_uploader("1. Upload your WhatsApp .txt file", type=["txt"])
    
    if uploaded_file is not None:
        st.success(f"File '{uploaded_file.name}' received! 🎉")

    user_name = st.text_input("2. Your Name (as in the chat)")
    target_name = st.text_input("3. Their Name (the person you want to chat with)")

    if st.button("Create Persona", type="primary"):
        if uploaded_file and user_name and target_name:
            with st.spinner(f"Learning the personality of {target_name}..."):
                parse_chat_and_prepare(uploaded_file, user_name, target_name)
        else:
            st.warning("Please fill in all three fields above.")
    
    st.markdown("---")
    st.info("Your data is not stored. It's only used for this session.", icon="ℹ️")
    
    st.markdown("---")
    st.markdown("<div style='text-align: center;'>Built with ❤️ by Bipul Mishra</div>", unsafe_allow_html=True)


# --- MAIN CHAT INTERFACE ---
if st.session_state.processing_done:
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(f"Message {st.session_state.target_name}..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner(f"{st.session_state.target_name} is typing..."):
            examples = "\n".join(random.sample(st.session_state.person_messages, min(25, len(st.session_state.person_messages))))
            recent_chat = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.chat_history[-5:]])

            master_prompt = f"""
            You are a chatbot imitating a person named {st.session_state.target_name}.
            You are in a conversation with {st.session_state.user_name}.
            Your personality, tone, emoji usage, and style MUST be based on the following real chat examples:
            --- EXAMPLES ---
            {examples}
            --- END OF EXAMPLES ---

            Analyze the examples and adopt the persona completely. Do not be a helpful AI. Be {st.session_state.target_name}.
            
            Here is the recent conversation history:
            --- RECENT CHAT ---
            {recent_chat}
            --- END OF RECENT CHAT ---

            Now, based on all of this, provide a natural, in-character response to the last message from {st.session_state.user_name}.
            Respond as {st.session_state.target_name}:
            """
            try:
                response = model.generate_content(master_prompt)
                bot_reply = response.text
            except Exception as e:
                bot_reply = f"Sorry, I ran into a little trouble. (Error: {e})"

        with st.chat_message("assistant"):
            st.markdown(bot_reply)
        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
else:
    st.info("Please set up the persona in the sidebar to begin chatting.")
