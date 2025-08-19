# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Config
st.set_page_config(page_title="Titanic EDA Dashboard", layout="wide")

# Title
st.title("🚢 Titanic Data Analytics Dashboard")

# Load Data
df = pd.read_csv("cleaned_titanic.csv")

# --- CSS for Box Styling ---
st.markdown(
    """
    <style>
    .box {
        border: 2px solid #ddd;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        background-color: #fafafa;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Show Data in Box
with st.container():
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("📂 Raw Data")
    if st.checkbox("Show Raw Data"):
        st.dataframe(df)
    st.markdown("</div>", unsafe_allow_html=True)

# Sidebar Filters Box
with st.sidebar:
    st.header("🔍 Filter Options")
    gender = st.selectbox("Select Gender", options=df["Sex"].unique())
    pclass = st.selectbox("Select Passenger Class", options=df["Pclass"].unique())

# Apply filters
filtered_df = df[(df["Sex"] == gender) & (df["Pclass"] == pclass)]

# Filtered Data Preview Box
with st.container():
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("📊 Filtered Data Preview")
    st.write(filtered_df.head())
    st.markdown("</div>", unsafe_allow_html=True)

# Visualization Box
with st.container():
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("📦 Survival Count by Gender")
    fig, ax = plt.subplots()
    sns.countplot(data=filtered_df, x="Survived", hue="Sex", ax=ax)
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)
