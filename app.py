import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Config
warnings.simplefilter(action='ignore', category=FutureWarning)
st.set_page_config(page_title="Titanic EDA Dashboard", layout="wide")

# Title
st.title("🚢 Titanic Data Analytics Dashboard")

# Load Data
try:
    df = pd.read_csv("cleaned_titanic.csv")
except FileNotFoundError:
    st.error("Data file not found. Please ensure 'cleaned_titanic.csv' exists.")
    st.stop()

# Sidebar Page Navigation
st.sidebar.title("📄 Navigation")
page = st.sidebar.radio("Go to", ["Sheet 1: Passenger Overview", "Sheet 2: Survival Analysis"])

# Sidebar Filters
st.sidebar.header("🎛 Filter Options")
gender_options = ["All"] + df["Sex"].unique().tolist()
gender = st.sidebar.selectbox("Select Gender", options=gender_options)

pclass_options = ["All"] + sorted(df["Pclass"].unique().tolist())
pclass = st.sidebar.selectbox("Select Passenger Class", options=pclass_options)

# Apply Filters
filtered_df = df.copy()
if gender != "All":
    filtered_df = filtered_df[filtered_df["Sex"] == gender]
if pclass != "All":
    filtered_df = filtered_df[filtered_df["Pclass"] == pclass]

# ---------------- SHEET 1 -------------------
if page == "Sheet 1: Passenger Overview":
    with st.expander("🧾 Show Raw Data"):
        st.dataframe(filtered_df.head())

    col1, col2 = st.columns(2)

    with col1:
        with st.container():
            st.subheader("📊 Survival Count by Gender")
            filtered_df["Survival Status"] = filtered_df["Survived"].map({0: "Did Not Survive", 1: "Survived"})
            fig1, ax1 = plt.subplots(figsize=(5, 4))
            sns.countplot(data=filtered_df,_
