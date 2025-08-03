import streamlit as st
import pandas as pd

# Load the data
df = pd.read_csv("eduaccess_courses_100.csv")

# Convert 'Cost' column to numeric (handle 'Free' or invalid values)
df['Cost'] = df['Cost'].replace("Free", "0")  # Optional: Convert 'Free' to 0
df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')  # Coerce invalid values to NaN

# Optional: Define a ranking for education levels for proper comparison
education_levels = {
    "10th Pass": 1,
    "12th Pass": 2,
    "Graduate": 3,
    "Other": 0  # You can adjust this value based on your logic
}

st.title("🎓 EduAccess Bot")
st.write("Helping you find affordable, quality education by 2030 🌱")

# Step 1: Basic user info
name = st.text_input("What's your name?")
age = st.number_input("Your age", min_value=10, max_value=100)
location = st.selectbox("Your location", df['Location'].unique())
education = st.selectbox("Your highest completed education", list(education_levels.keys()))
interest = st.text_input("Field of interest (e.g., electronics, computers)")
income_level = st.radio("Your family's income level", ["Low", "Medium", "High"])

if st.button("Find Courses"):
    st.subheader(f"Hi {name}, here are your matched courses:")

    # Apply education level filtering using numeric mapping
    user_education_level = education_levels[education]

    # Also map course eligibility if it's in the same format
    df['Eligibility_Level'] = df['Eligibility'].map(education_levels).fillna(0)

    filtered = df[
        (df['Location'] == location) &
        (df['Eligibility_Level'] <= user_education_level)
    ]

    # Filter for low-cost if applicable
    if income_level == "Low":
        filtered = filtered[filtered['Cost'] <= 500]

    if not filtered.empty:
        for _, row in filtered.iterrows():
            cost_display = "Free" if row['Cost'] == 0 else f"₹{int(row['Cost'])}"
            st.markdown(f"""
            **{row['Course Name']}** 
            📘 Type: {row['Type']}  
            📍 Location: {row['Location']}  
            💰 Cost: {cost_display}  
            🔗 [Apply Here]({row['Link']})
            """)
    else:
        st.error("Sorry, no matching courses found. Try changing location or eligibility.")


