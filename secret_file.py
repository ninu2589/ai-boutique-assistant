
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Prefer Streamlit Cloud Secrets; fall back to local .env
try:
    API_KEY = st.secrets["API_KEY"]
except (KeyError, FileNotFoundError):
    API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError(
        "API_KEY is missing. Configure it in Streamlit Cloud Secrets "
        "or your local .env file."
    )
