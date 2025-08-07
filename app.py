import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Assume df already loaded and contains a "Date" column
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Day"] = df["Date"].dt.day

st.title("Date-based Visuals")

# 📅 Monthly Distribution
monthly_counts = df["Month"].value_counts().sort_index()
fig1, ax1 = plt.subplots()
ax1.bar(monthly_counts.index, monthly_counts.values)
ax1.set_title("Records per Month")
ax1.set_xlabel("Month")
ax1.set_ylabel("Count")
st.pyplot(fig1)

# 📆 Yearly Distribution
yearly_counts = df["Year"].value_counts().sort_index()
fig2, ax2 = plt.subplots()
ax2.plot(yearly_counts.index, yearly_counts.values, marker='o')
ax2.set_title("Records per Year")
ax2.set_xlabel("Year")
ax2.set_ylabel("Count")
st.pyplot(fig2)
