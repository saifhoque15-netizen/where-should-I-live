import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from components.background import add_bg

from components.matching import find_matching

favicon = Image.open("data-science-in-action\images\house.png")
st.set_page_config(page_title="City Recommendation", layout="wide", page_icon=favicon)

st.markdown(
    """
    <h1 style='
        background-color: lightblue;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    '>European City Recommendation System</h1>
    """, 
    unsafe_allow_html=True
)

# --- Load data ---
@st.cache_data
def load_data():
    return pd.read_csv("data\city_data_clean.csv")

df = load_data()

# --- Sidebar ---

languages_available = ["Any"] + list(df['Main Spoken Languages'].str.split(',').explode().str.strip().unique())
lang_pref = st.sidebar.selectbox(
        'Prefered Main Spoken Language',
        languages_available)

w_salary = st.sidebar.number_input(
        "Your Monthly Salary (€)",
        min_value=0,
        max_value=20000,
        value=3000,
        step = 500)
    
w_unemployment = st.sidebar.slider("Unemployment Rate", min(df['Unemployment Rate']), max(df['Unemployment Rate']), np.mean(df['Unemployment Rate']))

w_gdp = st.sidebar.slider("GDP per Capita", 0, 10, 5)

w_rent = st.sidebar.slider(
    "Average Rent Price",
    min_value=int(df['Average Rent Price'].min()),
    max_value=int(df['Average Rent Price'].max()),
    value=int(df['Average Rent Price'].mean()),
    step=50
)

w_cost = st.sidebar.slider(
    "Average Cost of Living",
    min_value=int(df['Average Cost of Living'].min()),
    max_value=int(df['Average Cost of Living'].max()),
    value=int(df['Average Cost of Living'].mean()),
    step=50
)

run_button = st.sidebar.button("Find Matching Cities", type="primary")
results_placeholder = st.empty()

# --- Page ---
if run_button:
    weights = {
        "Unemployment Rate": w_unemployment,
        "GDP per Capita": w_gdp,
        "Average Monthly Salary": w_salary,
        "Average Rent Price": w_rent,
        "Average Cost of Living": w_cost
    }

    matching_cities = find_matching(df, user_language=lang_pref, weights=weights)

    if matching_cities.empty:
        st.toast("No match found! Try changing your preferences", icon="😪")
    else:
        st.balloons()
        st.markdown(f"<h2 style='text-align:center'>We suggest you:", unsafe_allow_html=True)

        st.markdown(
            f"<h1 style='text-align:center; background-color:lightgreen;'>{matching_cities['City'].iloc[0]}</h1>",
            unsafe_allow_html=True
        )

        st.divider()
        st.markdown(f"<h3 style='text-align:center'>All the matching cities based on your preferences:", unsafe_allow_html=True)
        st.dataframe(matching_cities)



    