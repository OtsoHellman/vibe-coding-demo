import streamlit as st
import pandas as pd
from pathlib import Path
import sqlite3

# Define SQLite database connection
DB_NAME = "feedback.db"

def initialize_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS feedback (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT,
                      rating INTEGER,
                      feedback TEXT)''')
    conn.commit()
    conn.close()

def save_feedback(name, rating, feedback):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO feedback (name, rating, feedback)
                      VALUES (?, ?, ?)''', (name, rating, feedback))
    conn.commit()
    conn.close()

# Load existing feedback (if any)
def load_feedback():
    conn = sqlite3.connect(DB_NAME)
    try:
        return pd.read_sql_query("SELECT * FROM feedback", conn)
    except:
        return pd.DataFrame(columns=["Name", "Rating", "Feedback"])
    finally:
        conn.close()

def fetch_feedback():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, rating, feedback FROM feedback")
    feedback_data = cursor.fetchall()
    conn.close()
    return feedback_data

# Initialize SQLite database at app startup
initialize_db()
# Load existing feedback
existing_feedback = load_feedback()

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

# Navigation for separate pages
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Give Feedback", "View Feedback Results"])

if page == "Give Feedback":
    st.header("🌟 Event Feedback")
    st.markdown("We value your feedback! Please take a moment to share your thoughts about the event.")

    with st.form("feedback_form"):
        name = st.text_input("Name", max_chars=50)
        rating = st.slider("Rating (1-5 Stars)", min_value=1, max_value=5, step=1)
        feedback = st.text_area("Your Feedback")

        submitted = st.form_submit_button("Submit")

        if submitted:
            if name and rating and feedback:
                save_feedback(name, rating, feedback)
                st.success("Thank you for your feedback!")
            else:
                st.error("Please fill in all the required fields.")

elif page == "View Feedback Results":
    st.header("Feedback Results")

    feedback_data = fetch_feedback()

    if feedback_data:
        # Extract ratings and count frequencies
        ratings = [row[1] for row in feedback_data]

        # Display Average Rating
        average_rating = sum(ratings) / len(ratings)
        st.metric(label="Average Rating", value=f"{average_rating:.2f}")

        # Visualize Ratings
        st.subheader("Ratings Breakdown")
        ratings_data = pd.DataFrame({'Rating': ratings})
        ratings_count = ratings_data['Rating'].value_counts().sort_index()
        st.bar_chart(ratings_count)
 
        # Display individual feedback
        for name, rating, feedback in feedback_data:
            st.subheader(f"{name}")
            st.write(f"**Rating:** {rating}")
            st.write(f"**Feedback:** {feedback}")
            st.markdown("---")
    else:
        st.write("No feedback available yet.")
