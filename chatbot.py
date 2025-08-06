
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# === Page setup ===
st.set_page_config(page_title="💬 Employee Help Chatbot", page_icon="🧠", layout="centered")

# === Custom Styling ===
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #e0f2f1, #fce4ec);
        padding: 2rem;
        font-family: 'Segoe UI', sans-serif;
    }
    .chat-bubble {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.05);
        margin-top: 1rem;
    }
    .user-question {
        background-color: #e3f2fd;
        border-left: 5px solid #42a5f5;
        padding: 0.8rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    .bot-answer {
        background-color: #ede7f6;
        border-left: 5px solid #7e57c2;
        padding: 0.8rem;
        border-radius: 10px;
        margin-top: 0.5rem;
    }
    .fallback {
        background-color: #fff3e0;
        border-left: 5px solid #ffb74d;
        padding: 0.8rem;
        border-radius: 10px;
        margin-top: 0.5rem;
    }
    .footer {
        text-align: center;
        font-size: 13px;
        color: #888;
        margin-top: 2rem;
    }
    .suggest-btn {
        background-color: #f3e5f5;
        color: #4a148c;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# === Title / Welcome ===
st.markdown("<h2 style='color:#1a237e;'>👋 Welcome to the Employee Help Chatbot</h2>", unsafe_allow_html=True)
st.markdown("Ask me anything about company policies, HR, IT, or work culture.")

# === Load Dataset ===
@st.cache_data
def load_data(file_path):
    df = pd.read_excel(file_path)
    df_qna = df[df["Type"] == "QnA"].copy()
    return df_qna

# === Load Model ===
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

# === Embeddings ===
@st.cache_data
def get_embeddings(questions, _model):
    return _model.encode(questions, show_progress_bar=True)

# === Semantic Matching ===
def get_answer(user_query, df_qna, question_embeddings, model, threshold=0.6):
    query_embedding = model.encode([user_query])
    scores = cosine_similarity(query_embedding, question_embeddings)[0]
    best_idx = scores.argmax()
    confidence = scores[best_idx]

    if confidence < threshold:
        return None, None, confidence

    best_question = df_qna.iloc[best_idx]["Question"]
    best_answer = df_qna.iloc[best_idx]["Answer / Statement"]
    return best_question, best_answer, confidence

# Load all
df_qna = load_data("Chatbot_QnA_Dummy_Data_Updated.xlsx")
model = load_model()
question_embeddings = get_embeddings(df_qna["Question"].tolist(), model)

# Fallback suggestions
suggestions = [
    "How to apply for leave?",
    "What's the dress code?",
    "What are the working hours?",
    "Can I work from home?",
    "Who do I contact for IT issues?",
    "What are the office holidays?",
    "How do I reset my password?",
    "What's the lunch break policy?"
]

# Session state
if 'selected_question' not in st.session_state:
    st.session_state.selected_question = ""

# Check if fallback button clicked
selected_suggestion = None
for suggestion in suggestions:
    if st.session_state.get(f"clicked_{suggestion}", False):
        selected_suggestion = suggestion
        st.session_state.selected_question = suggestion
        st.session_state[f"clicked_{suggestion}"] = False
        break

# Input box
user_input = st.text_input(
    "You:", 
    value=st.session_state.selected_question,
    placeholder="e.g., How many days do I have to work?",
    key="user_input"
)

# Clear after use
if st.session_state.selected_question and user_input == st.session_state.selected_question:
    st.session_state.selected_question = ""

# Process input
if user_input:
    match_q, answer, score = get_answer(user_input, df_qna, question_embeddings, model)

    st.markdown(f"<div class='user-question'>🧑‍💼 <strong>You:</strong> {user_input}</div>", unsafe_allow_html=True)

    if answer:
        st.markdown(f"<div class='bot-answer'>🤖 <strong>Answer:</strong> {answer}</div>", unsafe_allow_html=True)
        st.caption(f"Confidence: {score:.2f}")
    else:
        st.markdown(f"<div class='fallback'>🤖 I'm not sure how to answer that yet. Please contact HR or IT support.</div>", unsafe_allow_html=True)
        st.caption(f"Confidence: {score:.2f}")
        st.markdown("### 💡 Try asking about:")
        col1, col2 = st.columns(2)
        for i, suggestion in enumerate(suggestions):
            if i % 2 == 0:
                with col1:
                    if st.button(suggestion, key=f"suggest_{i}"):
                        st.session_state[f"clicked_{suggestion}"] = True
                        st.rerun()
            else:
                with col2:
                    if st.button(suggestion, key=f"suggest_{i}"):
                        st.session_state[f"clicked_{suggestion}"] = True
                        st.rerun()

# Footer
st.markdown("<div class='footer'>Made with 💬 by Vishakha Deshpande · Internal Demo Only</div>", unsafe_allow_html=True)

# Dataset stats
with st.expander("📊 Dataset Info"):
    st.write(f"**Total Q&A pairs loaded:** {len(df_qna)}")
    st.write(f"**Confidence threshold:** 60%")
    st.write("**Model:** all-MiniLM-L6-v2")
    st.write("**UX:** Gradient + Bubble UI + Safe fallback")
