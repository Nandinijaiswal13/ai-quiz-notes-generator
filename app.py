import streamlit as st
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter

# -------- NLTK --------
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)

# -------- PAGE CONFIG --------
st.set_page_config(page_title="AI Notes & Quiz Generator", page_icon="📘")

# -------- SESSION --------
if "users" not in st.session_state:
    st.session_state.users = {"admin": "1234"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

# -------- LOGIN PAGE --------
def login():
    st.markdown("<h2 style='text-align:center;'>🔐 Login</h2>", unsafe_allow_html=True)

    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")

    if st.button("Go to Signup"):
        st.session_state.page = "signup"
        st.rerun()

# -------- SIGNUP PAGE --------
def signup():
    st.markdown("<h2 style='text-align:center;'>📝 Signup</h2>", unsafe_allow_html=True)

    new_user = st.text_input("👤 Create Username")
    new_pass = st.text_input("🔑 Create Password", type="password")

    if st.button("Create Account"):
        if new_user in st.session_state.users:
            st.warning("User already exists!")
        else:
            st.session_state.users[new_user] = new_pass
            st.success("Account created! Go to login.")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()

# -------- MAIN APP --------
def main_app():
    st.markdown(
        "<h1 style='text-align:center; color:#4CAF50;'>📘 AI Quiz & Study Notes Generator</h1>",
        unsafe_allow_html=True
    )

    text = st.text_area("📥 Enter Study Material", height=200)

    def preprocess(text):
        words = word_tokenize(text.lower())
        stop_words = set(stopwords.words("english"))
        return [word for word in words if word.isalnum() and word not in stop_words]

    def generate_summary(text):
        sentences = sent_tokenize(text)
        words = preprocess(text)
        word_freq = Counter(words)

        scores = {}
        for sentence in sentences:
            for word in word_tokenize(sentence.lower()):
                if word in word_freq:
                    scores[sentence] = scores.get(sentence, 0) + word_freq[word]

        summary = sorted(scores, key=scores.get, reverse=True)[:2]
        return " ".join(summary)

    def generate_quiz(text):
        sentences = sent_tokenize(text)
        questions = []
        for sentence in sentences:
            words = sentence.split()
            if len(words) > 5:
                questions.append("❓ What is " + " ".join(words[:5]) + "?")
        return questions[:3]

    if st.button("✨ Generate Notes & Quiz"):
        if text:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📘 Study Notes")
                st.success(generate_summary(text))

            with col2:
                st.subheader("📝 Quiz Questions")
                for q in generate_quiz(text):
                    st.info(q)
        else:
            st.warning("Please enter study material!")

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

# -------- FLOW CONTROL --------
if st.session_state.logged_in:
    main_app()
else:
    if st.session_state.page == "login":
        login()
    else:
        signup()