import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Config
warnings.simplefilter(action='ignore', category=FutureWarning)
st.set_page_config(page_title="Titanic EDA Dashboard", layout="wide")

# Theme Colors
bar_color = "#007acc"
bar_palette = {"male": "#007acc", "female": "#ff7f0e"}

# Title
st.title("🚢 Titanic Data Analytics Dashboard")

# Load Data
try:
    df = pd.read_csv("cleaned_titanic.csv")
except FileNotFoundError:
    st.error("Data file not found. Please ensure 'cleaned_titanic.csv' exists.")
    st.stop()

# Sidebar Navigation
st.sidebar.title("📄 Navigation")
selected_page = st.sidebar.radio("Go to", ["Sheet 1: Overview", "Sheet 2: Passenger Insights"])

# Sidebar Filters
st.sidebar.header("🎛 Filter Options")
gender_options = ["All"] + df["Sex"].unique().tolist()
selected_gender = st.sidebar.selectbox("Select Gender", gender_options)

pclass_options = ["All"] + sorted(df["Pclass"].unique().tolist())
selected_pclass = st.sidebar.selectbox("Select Passenger Class", pclass_options)

# Age and Fare sliders
min_age, max_age = int(df["Age"].min()), int(df["Age"].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

min_fare, max_fare = int(df["Fare"].min()), int(df["Fare"].max())
fare_range = st.sidebar.slider("Select Fare Range", min_value=min_fare, max_value=max_fare, value=(min_fare, max_fare))

# Apply
