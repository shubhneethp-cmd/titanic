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

# Sidebar Navigation
st.sidebar.title("📄 Navigation")
selected_page = st.sidebar.radio("Go to", ["Sheet 1: Overview", "Sheet 2: Survival Analysis"])

# Sidebar Filters
st.sidebar.header("🎛 Filter Options")
gender_options = ["All"] + df["Sex"].unique().tolist()
selected_gender = st.sidebar.selectbox("Select Gender", gender_options)

pclass_options = ["All"] + sorted(df["Pclass"].unique().tolist())
selected_pclass = st.sidebar.selectbox("Select Passenger Class", pclass_options)

# Apply Filters
filtered_df = df.copy()
if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["Sex"] == selected_gender]
if selected_pclass != "All":
    filtered_df = filtered_df[filtered_df["Pclass"] == selected_pclass]

# ---------------- SHEET 1 -------------------
if selected_page == "Sheet 1: Overview":
    st.subheader("🔍 Filtered Data Preview")
    with st.expander("Show Filtered Data"):
        st.dataframe(filtered_df.head())

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Survival Count by Gender")
        filtered_df["Survival Status"] = filtered_df["Survived"].map({0: "Did Not Survive", 1: "Survived"})
        fig1, ax1 = plt.subplots(figsize=(5, 4))
        sns.countplot(data=filtered_df, x="Survival Status", hue="Sex", ax=ax1)
        ax1.set_title("Survival Count by Gender")
        st.pyplot(fig1)

    with col2:
        st.subheader("🎂 Age Distribution")
        fig2, ax2 = plt.subplots(figsize=(5, 4))
        sns.histplot(filtered_df["Age"].dropna(), kde=True, bins=30, ax=ax2)
        ax2.set_title("Age Distribution of Passengers")
        st.pyplot(fig2)

# ---------------- SHEET 2 -------------------
elif selected_page == "Sheet 2: Survival Analysis":
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("🏷 Survival Rate by Passenger Class")
        survival_by_class = filtered_df.groupby("Pclass")["Survived"].mean().reset_index()
