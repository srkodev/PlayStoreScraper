import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        .stTextInput > div > div > input {
            border-radius: 10px;
        }
        .stButton > button {
            border-radius: 10px;
            background-color: #FF4B4B;
            color: white;
            font-weight: bold;
        }
        .success-message {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #D4EDDA;
            color: #155724;
            margin: 1rem 0;
        }
        .error-message {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #F8D7DA;
            color: #721C24;
            margin: 1rem 0;
        }
        .app-header {
            text-align: center;
            padding: 1rem;
            background-color: #F8F9FA;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)
