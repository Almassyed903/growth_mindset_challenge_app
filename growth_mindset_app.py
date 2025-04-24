

import streamlit as st
import random
import datetime
import json
import os
from io import StringIO

# Difficulty-wise challenges
challenges = {
    "Easy": [
        "Write down one thing you're grateful for today.",
        "Name one mistake you learned from recently.",
        "Watch a 3-min motivational video.",
        "Write a short compliment to yourself.",
        "Take 5 deep breaths and reset your focus."
    ],
    "Medium": [
        "Identify a weakness and plan how to improve it.",
        "Teach someone something you learned this week.",
        "Do something uncomfortable on purpose today.",
        "Give yourself constructive feedback on something.",
        "Write a paragraph about a recent growth experience."
    ],
    "Hard": [
        "List 3 major fears and how you can face them.",
        "Start a small 7-day personal challenge (describe it).",
        "Reflect deeply on a failure and its hidden lesson.",
        "Have a tough conversation you've been avoiding.",
        "Spend 30 minutes learning something brand new."
    ]
}

DATA_FILE = "user_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- Streamlit UI Config ---
st.set_page_config(page_title="Growth Mindset Challenge", layout="centered")

st.markdown("""
    <style>
        .card {padding:20px; background:#f0f8ff; border-radius:12px; margin-bottom:15px;}
        .challenge-box {
            background: linear-gradient(to right, #e0f7fa, #e8f5e9);
            padding:15px;
            border-left: 5px solid #26a69a;
            border-radius:10px;
            font-size: 18px;
        }
        .note {color:#d32f2f; font-weight:bold;}
    </style>
""", unsafe_allow_html=True)

st.title("🌱 Growth Mindset Challenge")

# --- Sidebar Login & Difficulty ---
st.sidebar.header("Login")
username = st.sidebar.text_input("Username")
difficulty = st.sidebar.selectbox("Choose Difficulty", ["Easy", "Medium", "Hard"])
login_btn = st.sidebar.button("Login / Start")

# --- Export / Import ---
st.sidebar.markdown("### Export / Import Progress")
data = load_data()

# Export
if st.sidebar.download_button("📤 Export My Data", data=json.dumps(data.get(username, {}), indent=4),
                              file_name=f"{username}_growth_data.json"):
    st.sidebar.success("Your data has been exported!")

# Import
uploaded = st.sidebar.file_uploader("📥 Import JSON", type=["json"])
if uploaded and username:
    try:
        imported_data = json.load(uploaded)
        data[username] = imported_data
        save_data(data)
        st.sidebar.success("Data imported successfully!")
        st.rerun()
    except:
        st.sidebar.error("Invalid JSON file!")

# --- Login Logic ---
if login_btn and username:
    st.session_state.logged_in = True
    st.session_state.username = username
    st.session_state.difficulty = difficulty
    st.rerun()

if st.session_state.get("logged_in", False):
    username = st.session_state["username"]
    difficulty = st.session_state.get("difficulty", "Medium")

    st.success(f"Welcome, {username}!")
    st.info(f"Current Difficulty: *{difficulty}*")

    user_data = data.get(username, {"history": {}, "challenges": {}})
    today = str(datetime.date.today())

    if today not in user_data["challenges"]:
        challenge = random.choice(challenges[difficulty])
        user_data["challenges"][today] = {"text": challenge, "difficulty": difficulty}
        data[username] = user_data
        save_data(data)

    daily = user_data["challenges"][today]

    # --- Reminder Banner if Not Completed ---
    if today not in user_data["history"]:
        st.markdown('<div class="note">⚠ Don’t forget to complete your challenge today!</div>', unsafe_allow_html=True)

    # --- Show Challenge ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader(f"🧠 Today's Challenge ({today})")
    st.markdown(f'<div class="challenge-box">{daily["text"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Completion Check ---
    completed = st.checkbox("✅ I completed today's challenge")
    if completed and today not in user_data["history"]:
        user_data["history"][today] = daily
        st.balloons()
        save_data(data)

    # --- Progress Bar ---
    total = len(user_data["history"])
    st.progress(min(total / 10, 1.0))
    st.success(f"Total Challenges Completed: {total}")

    # --- History View ---
    if user_data["history"]:
        st.subheader("📅 Completed Challenges")
        for date, chal in sorted(user_data["history"].items(), reverse=True):
            st.markdown(f"- *{date}* ({chal['difficulty']}): {chal['text']}")

    st.markdown("---")
    st.caption("Made with love to grow your mindset.")
else:
    st.warning("Please log in from the sidebar to continue.")

