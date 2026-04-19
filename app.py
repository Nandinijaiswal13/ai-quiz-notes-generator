import streamlit as st
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter

nltk.download('punkt')
nltk.download('stopwords')

st.title("📘 AI Quiz & Study Notes Generator")

text = st.text_area("Enter your study material:")

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
            questions.append("What is " + " ".join(words[:5]) + "?")
    return questions[:3]

if st.button("Generate"):
    if text:
        st.subheader("📘 Study Notes")
        st.write(generate_summary(text))

        st.subheader("📝 Quiz Questions")
        for i, q in enumerate(generate_quiz(text), 1):
            st.write(f"{i}. {q}")
    else:
        st.warning("Please enter text!")