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

# Show Raw Data
if st.checkbox("Show Raw Data"):
    st.dataframe(df)

# Sidebar Filters
st.sidebar.header("Filter Options")

# Gender filter
gender_options = ["All"] + df["Sex"].unique().tolist()
gender = st.sidebar.selectbox("Select Gender", options=gender_options)

# Pclass filter
pclass_options = ["All"] + sorted(df["Pclass"].unique().tolist())
pclass = st.sidebar.selectbox("Select Passenger Class", options=pclass_options)

# Age Range Slicer
min_age = int(df["Age"].min())
max_age = int(df["Age"].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

# Fare Range Slicer
min_fare = float(df["Fare"].min())
max_fare = float(df["Fare"].max())
fare_range = st.sidebar.slider("Select Fare Range", min_value=float(min_fare), max_value=float(max_fare), value=(min_fare, max_fare))

# Apply Filters
filtered_df = df.copy()

if gender != "All":
    filtered_df = filtered_df[filtered_df["Sex"] == gender]
if pclass != "All":
    filtered_df = filtered_df[filtered_df["Pclass"] == pclass]

filtered_df = filtered_df[
    (filtered_df["Age"].between(age_range[0], age_range[1], inclusive="both")) &
    (filtered_df["Fare"].between(fare_range[0], fare_range[1], inclusive="both"))
]

# Preview Filtered Data
st.subheader("🔍 Filtered Data Preview")
st.write(filtered_df.head())

# Map Survival
filtered_df["Survival Status"] = filtered_df["Survived"].map({0: "Did Not Survive", 1: "Survived"})

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Distribution", "📌 Correlations"])

# TAB 1: Overview
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Survival Count")
        fig1, ax1 = plt.subplots(figsize=(5, 3.5))
        sns.countplot(data=filtered_df, x="Survival Status", hue="Sex", ax=ax1, width=0.5)
        ax1.set_title("Survival Count by Gender")
        fig1.tight_layout()
        st.pyplot(fig1)

    with col2:
        st.subheader("Embarked Port Count")
        fig2, ax2 = plt.subplots(figsize=(5, 3.5))
        sns.countplot(data=filtered_df, x="Embarked", ax=ax2, width=0.5)
        ax2.set_title("Embarkation Port Count")
        fig2.tight_layout()
        st.pyplot(fig2)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Survival Rate by Class")
        survival_by_class = filtered_df.groupby("Pclass")["Survived"].mean().reset_index()
        fig3, ax3 = plt.subplots(figsize=(5, 3.5))
        sns.barplot(data=survival_by_class, x="Pclass", y="Survived", ax=ax3, width=0.5)
        ax3.set_ylim(0, 1)
        ax3.set_ylabel("Survival Rate")
        ax3.set_title("Survival Rate by Class")
        fig3.tight_layout()
        st.pyplot(fig3)

    with col4:
        st.subheader("Average Fare by Class")
        fare_by_class = filtered_df.groupby("Pclass")["Fare"].mean().reset_index()
        fig4, ax4 = plt.subplots(figsize=(5, 3.5))
        sns.barplot(data=fare_by_class, x="Pclass", y="Fare", ax=ax4, width=0.5)
        ax4.set_title("Average Fare by Class")
        fig4.tight_layout()
        st.pyplot(fig4)

# TAB 2: Distribution
with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Age Distribution")
        fig5, ax5 = plt.subplots(figsize=(5, 3.5))
        sns.histplot(filtered_df["Age"].dropna(), kde=True, bins=30, ax=ax5)
        ax5.set_title("Age Distribution of Passengers")
        fig5.tight_layout()
        st.pyplot(fig5)

    with col2:
        st.subheader("Boxplot: Age by Survival")
        fig6, ax6 = plt.subplots(figsize=(5, 3.5))
        sns.boxplot(data=filtered_df, x="Survival Status", y="Age", ax=ax6, width=0.5)
        ax6.set_title("Boxplot of Age by Survival")
        fig6.tight_layout()
        st.pyplot(fig6)

# TAB 3: Correlation
with tab3:
    st.subheader("Correlation Heatmap")
    numeric_df = filtered_df.select_dtypes(include=["number"])
    fig7, ax7 = plt.subplots(figsize=(6, 3))
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax7, cbar=False, square=True)
    ax7.set_title("Feature Correlation", fontsize=12)
    fig7.tight_layout(pad=0.5)
    st.pyplot(fig7)
