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

# Sidebar Filters Box
with st.sidebar:
    st.header("🔍 Filter Options")
    # Instead of selectbox, use slider
    gender_choice = st.slider(
        "Select Gender View",
        min_value=0,
        max_value=2,
        value=0,
        step=1,
        format_func=lambda x: ["Both", "Male", "Female"][x]
    )
    pclass = st.selectbox("Select Passenger Class", options=df["Pclass"].unique())

# Apply filters
if gender_choice == 0:   # Both
    filtered_df = df[df["Pclass"] == pclass]
elif gender_choice == 1: # Male
    filtered_df = df[(df["Sex"] == "male") & (df["Pclass"] == pclass)]
else:                    # Female
    filtered_df = df[(df["Sex"] == "female") & (df["Pclass"] == pclass)]

# --- Layout in 2 Boxes (Columns) ---
col1, col2 = st.columns(2)

# Left Column (Raw Data + Filtered Preview)
with col1:
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("📂 Raw Data")
    if st.checkbox("Show Raw Data"):
        st.dataframe(df)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("📊 Filtered Data Preview")
    st.write(filtered_df.head())
    st.markdown("</div>", unsafe_allow_html=True)

# Right Column (Visualization)
with col2:
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("📦 Survival Count")

    if gender_choice == 0:   # Both (side by side male + female)
        gcol1, gcol2 = st.columns(2)

        with gcol1:
            male_df = filtered_df[filtered_df["Sex"] == "male"]
            fig, ax = plt.subplots()
            sns.countplot(data=male_df, x="Survived", ax=ax, palette="Blues")
            ax.set_title("Male Survival")
            st.pyplot(fig)

        with gcol2:
            female_df = filtered_df[filtered_df["Sex"] == "female"]
            fig, ax = plt.subplots()
            sns.countplot(data=female_df, x="Survived", ax=ax, palette="Reds")
            ax.set_title("Female Survival")
            st.pyplot(fig)

    elif gender_choice == 1: # Male only
        fig, ax = plt.subplots()
        sns.countplot(data=filtered_df, x="Survived", ax=ax, palette="Blues")
        ax.set_title("Male Survival")
        st.pyplot(fig)

    else:  # Female only
        fig, ax = plt.subplots()
        sns.countplot(data=filtered_df, x="Survived", ax=ax, palette="Reds")
        ax.set_title("Female Survival")
        st.pyplot(fig)

    st.markdown("</div>", unsafe_allow_html=True)
