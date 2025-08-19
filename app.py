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

# Right Column (Gender-wise Plots Only)
with col2:
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("📦 Survival Count (Gender-wise)")

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

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FULL-WIDTH PLOTS ----------------
st.markdown("<div class='box'>", unsafe_allow_html=True)
st.subheader("📊 Age Distribution by Survival")
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(data=filtered_df, x="Age", hue="Survived", multiple="stack", bins=20, ax=ax)
st.pyplot(fig)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='box'>", unsafe_allow_html=True)
st.subheader("💰 Fare Distribution by Survival")
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(data=filtered_df, x="Fare", hue="Survived", multiple="stack", bins=20, ax=ax)
st.pyplot(fig)
st.markdown("</div>", unsafe_allow_html=True)
