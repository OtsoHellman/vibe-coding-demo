import streamlit as st
import pandas as pd
from pathlib import Path

# Define the file where feedback will be saved
FEEDBACK_FILE = "feedback.csv"

# Load existing feedback (if any)
def load_feedback(file_path):
    if Path(file_path).is_file():
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame(columns=["Name", "Email", "Rating", "Feedback"])

# Save feedback to CSV
def save_feedback(name, email, rating, feedback):
    feedback_data = pd.DataFrame([{ "Name": name, "Email": email, "Rating": rating, "Feedback": feedback}])
    if Path(FEEDBACK_FILE).is_file():
        feedback_data.to_csv(FEEDBACK_FILE, mode='a', header=False, index=False)
    else:
        feedback_data.to_csv(FEEDBACK_FILE, index=False)

# Load existing feedback
existing_feedback = load_feedback(FEEDBACK_FILE)

# Apply CSS styling
CSS = """
<style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f9f9f9;
        margin: 0;
        padding: 0;
    }

    .main {
        max-width: 800px;
        margin: 50px auto;
        background: #fff;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 20px;
    }

    h1, h2, h3, h4 {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #333;
    }

    input, textarea, select {
        width: 100%;
        padding: 12px;
        margin: 8px 0;
        display: inline-block;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-sizing: border-box;
    }

    input[type=submit] {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 14px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
    }

    input[type=submit]:hover {
        background-color: #45a049;
    }
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# Streamlit app layout
st.markdown('<div class="main">', unsafe_allow_html=True)
st.header("🌟 Event Feedback")
st.markdown("We value your feedback! Please take a moment to share your thoughts about the event.")

# Input fields
with st.form("feedback_form"):
    name = st.text_input("Name", max_chars=50)
    email = st.text_input("Email")
    rating = st.slider("Rating (1-5 Stars)", min_value=1, max_value=5, step=1)
    feedback = st.text_area("Your Feedback")

    # Submit button
    submitted = st.form_submit_button("Submit")

    if submitted:
        if name and email and rating and feedback:
            save_feedback(name, email, rating, feedback)
            st.success("Thank you for your feedback!")
        else:
            st.error("Please fill in all the required fields.")

st.markdown("</div>", unsafe_allow_html=True)