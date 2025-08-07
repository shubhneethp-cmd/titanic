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

# Apply Filters
filtered_df = df.copy()
if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["Sex"] == selected_gender]
if selected_pclass != "All":
    filtered_df = filtered_df[filtered_df["Pclass"] == selected_pclass]

filtered_df = filtered_df[
    (filtered_df["Age"].between(age_range[0], age_range[1], inclusive="both")) &
    (filtered_df["Fare"].between(fare_range[0], fare_range[1], inclusive="both"))
]

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
        sns.countplot(data=filtered_df, x="Survival Status", hue="Sex", ax=ax1, palette=bar_palette)
        ax1.set_title("Survival Count by Gender")
        st.pyplot(fig1)

    with col2:
        st.subheader("🎂 Age Distribution")
        fig2, ax2 = plt.subplots(figsize=(5, 4))
        sns.histplot(filtered_df["Age"].dropna(), kde=True, bins=30, ax=ax2, color=bar_color)
        ax2.set_title("Age Distribution of Passengers")
        st.pyplot(fig2)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("🏷 Survival Rate by Passenger Class")
        survival_by_class = filtered_df.groupby("Pclass")["Survived"].mean().reset_index()
        fig3, ax3 = plt.subplots(figsize=(5, 4))
        sns.barplot(data=survival_by_class, x="Pclass", y="Survived", ax=ax3, color=bar_color)
        ax3.set_ylabel("Survival Rate")
        ax3.set_ylim(0, 1)
        ax3.set_title("Survival Rate by Class")
        st.pyplot(fig3)

    with col4:
        st.subheader("📌 Feature Correlation Heatmap")
        numeric_df = filtered_df.select_dtypes(include=["number"])
        fig4, ax4 = plt.subplots(figsize=(6, 4))
        sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm_
