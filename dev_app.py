# dev_app.py
import streamlit as st
import json
import requests
import random
import string
import re
from bs4 import BeautifulSoup
from google import genai
from google.genai import types

# Page Configuration
st.set_page_config(
    page_title="DevSuite // Ultra Clean Developer Tools",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Cyberpunk / Dark Minimalist CSS Style
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    h1 { color: #00ffcc; font-family: 'Courier New', Courier, monospace; }
    .stTextArea textarea, .stTextInput input { background-color: #1a1c23 !important; color: #00ffcc !important; font-family: monospace !important; }
    </style>
""", unsafe_allow_html=True)

# Sidebar Menu
st.sidebar.title("⚡ DevSuite v4.0")
st.sidebar.write("Integrated Developer Tools")
menu = st.sidebar.radio("Select a tool:", [
    "🛠️ JSON Formatter", 
    "🤖 AI Python Assistant",
    "🔍 SEO Analyzer Bot",
    "🔐 Password Shield Generator"
])

# API Configuration Section
st.sidebar.write("---")
st.sidebar.subheader("🔑 API Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

st.title("⚡ DevSuite // Black Edition")
st.write("---")

# TOOL 1: JSON FORMATTER
if menu == "🛠️ JSON Formatter":
    st.subheader("🛠️ JSON Formatter & Cleaner")
    json_input = st.text_area("Raw JSON:", height=200, placeholder='{"name":"ricky","status":"coding"}')
    if st.button("Format JSON ✨"):
        try:
            st.code(json.dumps(json.loads(json_input), indent=4), language="json")
        except Exception as e:
            st.error(f"Error: {e}")

# TOOL 2: AI ASSISTANT
elif menu == "🤖 AI Python Assistant":
    st.subheader("🤖 AI Python Script Generator")
    user_prompt = st.text_area("What do you want to automate?", height=150, placeholder="Describe your python script here...")
    if st.button("Generate Code 🚀"):
        if not api_key:
            st.error("Please add your Gemini API Key in the sidebar!")
        else:
            with st.spinner("AI is coding..."):
                try:
                    client = genai.Client(api_key=api_key)
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=user_prompt,
                        config=types.GenerateContentConfig(
                            system_instruction="You are an expert Python developer. Return ONLY the requested python code in markdown blocks.",
                            temperature=0.2,
                        )
                    )
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"AI Error: {e}")

# TOOL 3: SEO BOT
elif menu == "🔍 SEO Analyzer Bot":
    st.subheader("🔍 Express Website SEO Analyzer")
    st.write("Enter a URL below to instantly extract and analyze its primary SEO data tags.")
    
    target_url = st.text_input("Website URL to analyze:", value="https://backlinko.com/blog")
    
    if st.button("Launch Analysis 🎯"):
        with st.spinner("Scraping target website..."):
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                res = requests.get(target_url, headers=headers, timeout=10)
                
                if res.status_code != 200:
                    st.error(f"Could not connect to website (Error Code: {res.status_code})")
                else:
                    soup = BeautifulSoup(res.text, 'html.parser')
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("### 📋 General Overview")
                        title = soup.title.string if soup.title else "No title tag found"
                        st.info(f"**Page Title:** {title} ({len(title)} characters)")
                        meta_desc = soup.find('meta', attrs={'name': 'description'})
                        desc_text = meta_desc['content'] if meta_desc and 'content' in meta_desc.attrs else "No meta description found."
                        st.warning(f"**Meta Description:** {desc_text}")
                    with col2:
                        st.markdown("### 📊 Headings Structure")
                        for tag in ['h1', 'h2', 'h3']:
                            headings = soup.find_all(tag)
                            st.write(f"**<{tag.upper()}> Tags ({len(headings)} found):**")
                            for h in headings[:5]:
                                st.code(h.text.strip())
            except Exception as e:
                st.error(f"Scraping error: {e}")

# TOOL 4: PASSWORD GENERATOR (NEW !)
elif menu == "🔐 Password Shield Generator":
    st.subheader("🔐 Password Shield & Strength Analyzer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⚙️ Custom Settings")
        length = st.slider("Password Length:", min_value=8, max_value=32, value=16)
        use_upper = st.checkbox("Include Uppercase Letters (A-Z)", value=True)
        use_digits = st.checkbox("Include Digits (0-9)", value=True)
        use_specials = st.checkbox("Include Special Characters (!@#$%^&*)", value=True)
        
        # Generation Logic
        characters = string.ascii_lowercase
        if use_upper: characters += string.ascii_uppercase
        if use_digits: characters += string.digits
        if use_specials: characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if st.button("Generate Secure Password ⚡"):
            pwd = "".join(random.choice(characters) for _ in range(length))
            st.session_state['generated_password'] = pwd

    with col2:
        st.markdown("### 🔑 Generated Output")
        current_pwd = st.session_state.get('generated_password', '')
        
        if current_pwd:
            st.code(current_pwd, language="text")
            
            # Strength Checker Logic
            score = 0
            if len(current_pwd) >= 12: score += 1
            if len(current_pwd) >= 16: score += 1
            if re.search(r"[A-Z]", current_pwd): score += 1
            if re.search(r"[0-9]", current_pwd): score += 1
            if re.search(r"[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]", current_pwd): score += 1
            
            # Display Strength Meter
            st.write("**Security Level:**")
            if score <= 2:
                st.error("🔴 WEAK (Easy to crack)")
            elif score == 3 or score == 4:
                st.warning("🟡 MEDIUM (Good security)")
            else:
                st.success("🟢 ULTRA STRONG (Military grade)")
        else:
            st.info("Click the generate button to build a secured shield password.")