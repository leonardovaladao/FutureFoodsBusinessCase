import streamlit as st
import pandas as pd
from datetime import timedelta
import numpy as np

from generalPage import general_page
from trendingsPage import trending_page
from cuisinesPage import cuisine_page

st.set_page_config(layout="wide")

with open ('style.css') as f:
			st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# ================ Sidebar ================ #
st.sidebar.image("data/logo.png")
st.sidebar.title("Restaurant Dashboard")
page_selection = st.sidebar.selectbox("Select page view:", ["General Metrics", "Trending Products", "Cuisines Page"])

if page_selection == "General Metrics":
    general_page()
elif page_selection == "Trending Products":
    trending_page()
elif page_selection == "Cuisines Page":
    cuisine_page()