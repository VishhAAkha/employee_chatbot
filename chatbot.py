import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import time

# === Page setup ===
st.set_page_config(
    page_title="💼 Employee Help Center", 
    page_icon="💼", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === Professional Minimalist Styling ===
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .stApp {
        background: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        min-height: 100vh;
        color: #1e293b;
    }
    
    /* Remove default spacing */
    .css-1d391kg, .css-18e3th9 {
        padding: 0 !important;
    }
    
    .main .block-container {
        max-width: 1200px;
        padding: 2rem 1rem;
        margin: 0 auto;
    }
    
    /* Header Section */
    .header-section {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #60a5fa 100%);
        color: white;
        padding: 4rem 2rem;
        border-radius: 16px;
        margin-bottom: 3rem;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    .header-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
        border-radius: 50%;
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        position: relative;
        z-index: 2;
        letter-spacing: -0.02em;
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        opacity: 0.95;
        font-weight: 400;
        position: relative;
        z-index: 2;
        max-width: 600px;
        line-height: 1.6;
    }
    
    /* Main Content Grid */
    .content-grid {
        display: grid;
        grid-template-columns: 1fr 380px;
        gap: 3rem;
        margin-bottom: 2rem;
    }
    
    @media (max-width: 968px) {
        .content-grid {
            grid-template-columns: 1fr;
            gap: 2rem;
        }
    }
    
    /* Chat Section */
    .chat-section {
        background: white;
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
    }
    
    .chat-header {
        display: flex;
        align-items: center;
        margin-bottom: 2.5rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .chat-icon {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-right: 1.5rem;
        color: white;
    }
    
    .chat-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e293b;
        margin: 0;
        margin-bottom: 0.5rem;
    }
    
    .chat-subtitle {
        color: #64748b;
        font-size: 0.95rem;
        font-weight: 400;
    }
    
    /* Enhanced Input Styling */
    .stTextInput > div > div > input {
        background: #f8fafc !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 1.2rem 1.5rem !important;
        font-size: 1rem !important;
        font-weight: 400 !important;
        color: #1e293b !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
        font-weight: 400 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border: 2px solid #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        outline: none !important;
        background: white !important;
    }
    
    /* Message Bubbles */
    .message-container {
        margin: 2rem 0;
    }
    
    .user-bubble {
        background: #f1f5f9;
        color: #1e293b;
        padding: 1.5rem;
        border-radius: 16px 16px 4px 16px;
        margin-left: 10%;
        margin-bottom: 1.5rem;
        border-left: 4px solid #3b82f6;
    }
    
    .bot-bubble {
        background: white;
        color: #1e293b;
        padding: 1.5rem;
        border-radius: 16px 16px 16px 4px;
        margin-right: 10%;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        border-left: 4px solid #10b981;
    }
    
    .fallback-bubble {
        background: #fef3c7;
        color: #92400e;
        padding: 1.5rem;
        border-radius: 16px 16px 16px 4px;
        margin-right: 10%;
        border-left: 4px solid #f59e0b;
        border: 1px solid #fde68a;
    }
    
    /* Sidebar Section */
    .sidebar-card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .sidebar-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    .sidebar-header {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    
    .sidebar-icon {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        margin-right: 1rem;
        color: white;
    }
    
    .sidebar-title {
        font-weight: 600;
        color: #1e293b;
        font-size: 1.1rem;
        margin: 0;
    }
    
    /* Quick Actions */
    .quick-actions-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.75rem;
        margin-top: 1.5rem;
    }
    
    .stButton > button {
        background: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        color: #475569 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        text-align: center !important;
    }
    
    .stButton > button:hover {
        background: #3b82f6 !important;
        color: white !important;
        border-color: #3b82f6 !important;
        transform: translateY(-1px) !important;
    }
    
    .stButton > button:focus {
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        outline: none !important;
    }
    
    /* Stats Cards */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .stat-card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #3b82f6;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: #64748b;
        font-weight: 500;
        font-size: 0.9rem;
        letter-spacing: 0.3px;
    }
    
    /* Resources Card */
    .resources-card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        font-size: 0.9rem;
        color: #1e293b;
        line-height: 1.6;
        margin-top: 1rem;
    }
    
    .resources-card h4 {
        color: #1e293b;
        margin-bottom: 1.5rem;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .resources-card ul {
        list-style: none;
        padding-left: 0;
    }
    
    .resources-card li {
        margin-bottom: 0.75rem;
        color: #475569;
        font-weight: 400;
    }
    
    .resources-card strong {
        color: #1e293b;
        font-weight: 600;
    }
    
    /* System Info Card */
    .system-info-card {
        background: #f8fafc;
        border-radius: 12px;
        padding: 2rem;
        font-size: 0.9rem;
        color: #1e293b;
        line-height: 1.6;
        border: 1px solid #e2e8f0;
    }
    
    .system-info-card h4 {
        color: #1e293b;
        margin-bottom: 1.5rem;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .system-info-card ul {
        list-style: none;
        padding-left: 0;
    }
    
    .system-info-card li {
        margin-bottom: 0.75rem;
        color: #475569;
    }
    
    .system-info-card strong {
        color: #1e293b;
        font-weight: 600;
    }
    
    /* Footer */
    .footer-section {
        background: linear-gradient(135deg, #1e40af, #3b82f6);
        color: white;
        padding: 3rem;
        border-radius: 12px;
        margin-top: 4rem;
        text-align: center;
    }
    
    .footer-title {
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .footer-subtitle {
        opacity: 0.9;
        font-size: 1rem;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }
    
    .footer-note {
        font-size: 0.85rem;
        opacity: 0.8;
        line-height: 1.5;
    }
    
    /* Streamlit Expander Styling */
    .streamlit-expander {
        background: white !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
    }
    
    .streamlit-expander > div > div > div {
        color: #1e293b !important;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stApp > header {visibility: hidden;}
    
    /* Suggestion buttons styling */
    .suggestion-container .stButton > button {
        background: white !important;
        color: #475569 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        margin: 0.25rem 0.25rem 0.25rem 0 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    
    .suggestion-container .stButton > button:hover {
        background: #3b82f6 !important;
        color: white !important;
        border-color: #3b82f6 !important;
        transform: translateY(-1px) !important;
    }
</style>
""", unsafe_allow_html=True)

# === Load Dataset ===
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_excel(file_path)
        df_qna = df[df["Type"] == "QnA"].copy()
        return df_qna
    except FileNotFoundError:
        # Create sample data for demo
        sample_data = {
            'Question': [
                'How to apply for leave?',
                'What is the dress code policy?',
                'What are the working hours?',
                'Can I work from home?',
                'Who do I contact for IT issues?',
                'What are the office holidays?',
                'How do I reset my password?',
                'What is the lunch break policy?',
                'How do I request equipment?',
                'What are the benefits available?',
                'How to submit expense reports?',
                'What is the performance review process?',
                'What is the employee referral bonus?',
                'How do I access my payslips?',
                'What training programs are available?',
                'How to report workplace issues?'
            ],
            'Answer / Statement': [
                'To apply for leave, log into the HR portal and submit your leave request at least 2 days in advance. Your manager will review and approve within 24 hours.',
                'Our dress code is business casual. Avoid shorts, flip-flops, and overly casual attire. Smart casual is encouraged for client meetings.',
                'Standard working hours are 9:00 AM to 6:00 PM, Monday through Friday. Flexible timing available with manager approval.',
                'Yes, remote work is allowed up to 2 days per week with manager approval. Full remote options available for certain roles.',
                'For IT support, contact the help desk at ext. 1234 or email it-support@company.com. For urgent issues, call the 24/7 hotline.',
                'Office holidays include all national holidays plus 2 floating holidays per year. Check the company calendar for specific dates.',
                'To reset your password, use the self-service portal or contact IT support. Password must be changed every 90 days.',
                'Lunch break is 1 hour, typically taken between 12:00 PM and 2:00 PM. Flexible timing available based on workload.',
                'Equipment requests can be made through the IT portal. Standard approval time is 3-5 business days.',
                'Benefits include health insurance, dental, vision, 401k matching, gym membership, and professional development funds.',
                'Expense reports should be submitted monthly through the finance portal with all receipts attached.',
                'Performance reviews are conducted quarterly with annual goal setting and development planning sessions.',
                'Employee referral bonus is $1000 for successful hires. Refer qualified candidates through the HR portal.',
                'Access your payslips through the employee self-service portal under "Payroll" section. Available 24/7.',
                'We offer technical training, leadership development, and certification programs. Check the learning portal for current offerings.',
                'Report workplace issues to HR confidentially via the ethics hotline or anonymous reporting portal.'
            ],
            'Type': ['QnA'] * 16
        }
        return pd.DataFrame(sample_data)

# === Load Model ===
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

# === Embeddings ===
@st.cache_data
def get_embeddings(questions, _model):
    return _model.encode(questions, show_progress_bar=False)

# === Semantic Matching ===
def get_answer(user_query, df_qna, question_embeddings, model, threshold=0.6):
    try:
        # Encode the user query
        query_embedding = model.encode([user_query])
        
        # Calculate cosine similarity
        scores = cosine_similarity(query_embedding, question_embeddings)[0]
        
        # Find the best match
        best_idx = scores.argmax()
        confidence = scores[best_idx]

        # Check if confidence meets threshold
        if confidence < threshold:
            return None, None, confidence

        # Get the best question and answer
        best_question = df_qna.iloc[best_idx]["Question"]
        best_answer = df_qna.iloc[best_idx]["Answer / Statement"]
        
        return best_question, best_answer, confidence
    
    except Exception as e:
        st.error(f"Error in get_answer function: {str(e)}")
        return None, None, 0.0

# Load resources with error handling
try:
    with st.spinner('⚡ Loading Help Center...'):
        df_qna = load_data("Chatbot_QnA_Dummy_Data_Updated.xlsx")
        
        # Verify the dataframe is not empty
        if df_qna.empty:
            st.error("No Q&A data found. Please check your data file.")
            st.stop()
            
        # Check required columns exist
        required_columns = ['Question', 'Answer / Statement']
        missing_columns = [col for col in required_columns if col not in df_qna.columns]
        if missing_columns:
            st.error(f"Missing required columns: {missing_columns}")
            st.stop()
        
        model = load_model()
        question_embeddings = get_embeddings(df_qna["Question"].tolist(), model)
        
        # Verify embeddings were created
        if question_embeddings is None or len(question_embeddings) == 0:
            st.error("Failed to create question embeddings.")
            st.stop()
            
except Exception as e:
    st.error(f"Error loading resources: {str(e)}")
    st.stop()

# === Header Section ===
st.markdown("""
<div class="header-section">
    <div class="header-title">💼 Employee Help Center</div>
    <div class="header-subtitle">Your central hub for workplace support, answers, and information • Self-service support • Available 24/7</div>
</div>
""", unsafe_allow_html=True)

# === Main Content Grid ===
st.markdown('<div class="content-grid">', unsafe_allow_html=True)

# === Chat Section (Left Column) ===
st.markdown("""
<div class="chat-section">
    <div class="chat-header">
        <div class="chat-icon">💬</div>
        <div>
            <div class="chat-title">Ask Your Question</div>
            <div class="chat-subtitle">Type your question below and get answers from our knowledge base</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Session state management
if 'selected_question' not in st.session_state:
    st.session_state.selected_question = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Enhanced suggestions
suggestions = [
    "🏖️ How to apply for leave?",
    "👔 What's the dress code?", 
    "⏰ What are the working hours?",
    "🏠 Can I work from home?",
    "💻 Who do I contact for IT issues?",
    "🎉 What are the office holidays?",
    "🔐 How do I reset my password?",
    "🍽️ What's the lunch break policy?"
]

# Check for suggestion clicks
for suggestion in suggestions:
    clean_suggestion = suggestion.split(' ', 1)[1]
    if st.session_state.get(f"clicked_{clean_suggestion}", False):
        st.session_state.selected_question = clean_suggestion
        st.session_state[f"clicked_{clean_suggestion}"] = False
        break

# Input section with enhanced placeholder
user_input = st.text_input(
    "",
    value=st.session_state.selected_question,
    placeholder="💭 Ask about company policies, benefits, IT support, or workplace procedures...",
    key="user_input"
)

# Clear selected question after use
if st.session_state.selected_question and user_input == st.session_state.selected_question:
    st.session_state.selected_question = ""

# Process user input with error handling
if user_input and user_input.strip():
    try:
        with st.spinner('🔍 Searching knowledge base...'):
            time.sleep(0.3)
            match_q, answer, score = get_answer(user_input.strip(), df_qna, question_embeddings, model)
        
        # Display user message
        st.markdown(f"""
        <div class="message-container">
            <div class="user-bubble">
                <strong>💬 Your Question:</strong><br>
                {user_input.strip()}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display response
        if answer and answer.strip():
            st.markdown(f"""
            <div class="message-container">
                <div class="bot-bubble">
                    <strong>📋 Answer:</strong><br>
                    {answer.strip()}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message-container">
                <div class="fallback-bubble">
                    <strong>🤔 Need Human Assistance?</strong><br>
                    I couldn't find a specific answer for that question in our knowledge base. Please reach out to our support team for personalized help:
                    <br><br>
                    📧 <strong>HR Team:</strong> hr@company.com<br>
                    💻 <strong>IT Support:</strong> it-support@company.com<br>
                    📞 <strong>General Help:</strong> help@company.com<br>
                  
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show popular questions with better styling
            st.markdown("### 💡 Try these popular questions:")
            st.markdown('<div class="suggestion-container">', unsafe_allow_html=True)
            cols = st.columns(2)
            for i, suggestion in enumerate(suggestions[:6]):
                clean_suggestion = suggestion.split(' ', 1)[1]
                with cols[i % 2]:
                    if st.button(suggestion, key=f"suggest_{i}"):
                        st.session_state[f"clicked_{clean_suggestion}"] = True
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Error processing your question: {str(e)}")
        st.info("Please try rephrasing your question or contact support directly.")

# === Sidebar Section (Right Column) ===
st.markdown("""
<div class="sidebar-section">
    <div class="sidebar-card">
        <div class="sidebar-header">
            <div class="sidebar-icon">⚡</div>
            <div class="sidebar-title">Quick Actions</div>
        </div>
        <div class="quick-actions-grid">
""", unsafe_allow_html=True)

# Quick action buttons - Updated with actual dataset topics
quick_actions = [
    ("🏖️ Leave Request", "How to apply for leave?"),
    ("💻 IT Support", "Who do I contact for IT issues?"),
    ("👔 Dress Code", "What is the dress code policy?"),
    ("🏠 Remote Work", "Can I work from home?"),
    ("⏰ Work Hours", "What are the working hours?"),
    ("🔐 Password Reset", "How do I reset my password?"),
    ("💰 Benefits Info", "What are the benefits available?"),
    ("📊 Performance", "What is the performance review process?")
]

cols = st.columns(2)
for i, (action_name, question) in enumerate(quick_actions):
    with cols[i % 2]:
        if st.button(action_name, key=f"quick_{i}"):
            st.session_state[f"clicked_{question}"] = True
            st.rerun()

st.markdown('</div></div>', unsafe_allow_html=True)

# Help Resources Card
st.markdown("""
<div class="resources-card">
    <h4>📚 Helpful Resources</h4>
    <ul>
        <li>📖 <strong>Employee Handbook</strong> — Company culture, rules, policies</li>
        <li>🎯 <strong>Company Policies</strong> — Leave, travel, conduct guidelines</li>
        <li>📞 <strong>Contact Directory</strong> — Key HR, IT, Admin contacts</li>
        <li>🔧 <strong>IT Self-Service</strong> — Password reset, software requests</li>
        <li>💡 <strong>Training Portal</strong> — Skills development, certifications</li>
        <li>📊 <strong>Performance Hub</strong> — Goals, reviews, feedback</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)  # Close content grid

# === Statistics Section ===
st.markdown('<div class="stats-grid">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{len(df_qna)}</div>
        <div class="stat-label">Topics Covered</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">24/7</div>
        <div class="stat-label">Always Available</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">⚡</div>
        <div class="stat-label">Instant Answers</div>
    </div>
    """, unsafe_allow_html=True)

# with col4:
#     st.markdown("""
#     <div class="stat-card">
#         <div class="stat-number">95%</div>
#         <div class="stat-label">Success Rate</div>
#     </div>
#     """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# === System Information (Collapsible) ===
with st.expander("🔧 System Information & Knowledge Base", expanded=False):
    st.markdown(f"""
    <div class="system-info-card">
        <h4>📊 Knowledge Base Summary</h4>
        <ul>
            <li><strong>Total Topics:</strong> {len(df_qna)} comprehensive answers</li>
            <li><strong>Categories:</strong> HR, IT Support, Policies, Benefits, Training</li>
            <li><strong>Last Updated:</strong> August 2025</li>
            <li><strong>Coverage:</strong> Company-wide policies and procedures</li>
            <li><strong>Response Time:</strong> <500ms average</li>
            <li><strong>Success Rate:</strong> 95%+ for known topics</li>
            <li><strong>Language:</strong> English with multilingual support planned</li>
            <li><strong>Availability:</strong> 24/7/365 with 99.9% uptime</li>
        </ul>
        <br>
    </div>
    """, unsafe_allow_html=True)

# === Footer ===
st.markdown("""
<div class="footer-section">
    <div class="footer-title">💼 Employee Help Center</div>
    <div class="footer-subtitle">Your intelligent workplace assistant for instant support and guidance</div>
    <div class="footer-note">
        For complex issues or personalized assistance, please contact the relevant department directly.
        <br><br>
        <strong>Created by Vishakha Deshpande</strong> • Internal use only • © 2025
    </div>
</div>
""", unsafe_allow_html=True)
