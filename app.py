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

# Preview Filtered Data
st.subheader("🔍 Filtered Data Preview")
st.write(filtered_df.head())

# 1. Survival Count by Gender
st.subheader("📊 Survival Count by Gender")
filtered_df["Survival Status"] = filtered_df["Survived"].map({0: "Did Not Survive", 1: "Survived"})
fig1, ax1 = plt.subplots()
sns.countplot(data=filtered_df, x="Survival Status", hue="Sex", ax=ax1)
ax1.set_title("Survival Count by Gender")
st.pyplot(fig1)

# 2. Age Distribution
st.subheader("🎂 Age Distribution")
fig2, ax2 = plt.subplots()
sns.histplot(filtered_df["Age"].dropna(), kde=True, bins=30, ax=ax2)
ax2.set_title("Age Distribution of Passengers")
st.pyplot(fig2)

# 3. Survival Rate by Class
st.subheader("🏷 Survival Rate by Passenger Class")
survival_by_class = filtered_df.groupby("Pclass")["Survived"].mean().reset_index()
fig3, ax3 = plt.subplots()
sns.barplot(data=survival_by_class, x="Pclass", y="Survived", ax=ax3)
ax3.set_ylabel("Survival Rate")
ax3.set_ylim(0, 1)
ax3.set_title("Survival Rate by Passenger Class")
st.pyplot(fig3)

# 4. Correlation Heatmap
st.subheader("📌 Feature Correlation Heatmap")
numeric_df = filtered_df.select_dtypes(include=["number"])
fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax4)
ax4.set_title("Correlation Heatmap")
st.pyplot(fig4)
