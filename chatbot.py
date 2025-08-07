# import pandas as pd
# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity
# import streamlit as st
# import time

# # === Page setup ===
# st.set_page_config(
#     page_title="💼 Employee Help Center", 
#     page_icon="💼", 
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # === Enhanced Professional Styling ===
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
#     .stApp {
#         background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 50%, #f1f3f4 100%);
#         font-family: 'Poppins', sans-serif;
#         min-height: 100vh;
#     }
    
#     /* Remove default spacing */
#     .css-1d391kg, .css-18e3th9 {
#         padding: 0 !important;
#     }
    
#     .main .block-container {
#         max-width: 1200px;
#         padding: 2rem 1rem;
#         margin: 0 auto;
#     }
    
#     /* Header Section */
#     .header-section {
#         background: linear-gradient(135deg, #2c3e50, #34495e);
#         color: white;
#         padding: 3rem 2rem;
#         border-radius: 16px;
#         margin-bottom: 2rem;
#         box-shadow: 0 10px 30px rgba(44, 62, 80, 0.15);
#         position: relative;
#         overflow: hidden;
#     }
    
#     .header-section::before {
#         content: '';
#         position: absolute;
#         top: 0;
#         right: 0;
#         width: 200px;
#         height: 200px;
#         background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
#         border-radius: 50%;
#         transform: translate(50%, -50%);
#     }
    
#     .header-title {
#         font-size: 2.8rem;
#         font-weight: 700;
#         margin-bottom: 0.5rem;
#         position: relative;
#         z-index: 2;
#     }
    
#     .header-subtitle {
#         font-size: 1.2rem;
#         opacity: 0.9;
#         font-weight: 400;
#         position: relative;
#         z-index: 2;
#     }
    
#     /* Main Content Grid */
#     .content-grid {
#         display: grid;
#         grid-template-columns: 1fr 350px;
#         gap: 2rem;
#         margin-bottom: 2rem;
#     }
    
#     @media (max-width: 968px) {
#         .content-grid {
#             grid-template-columns: 1fr;
#         }
#     }
    
#     /* Chat Section */
#     .chat-section {
#         background: white;
#         border-radius: 16px;
#         padding: 2rem;
#         box-shadow: 0 8px 32px rgba(0,0,0,0.08);
#         border: 1px solid rgba(0,0,0,0.05);
#         animation: slideInLeft 0.6s ease-out;
#     }
    
#     @keyframes slideInLeft {
#         from { opacity: 0; transform: translateX(-30px); }
#         to { opacity: 1; transform: translateX(0); }
#     }
    
#     .chat-header {
#         display: flex;
#         align-items: center;
#         margin-bottom: 2rem;
#         padding-bottom: 1rem;
#         border-bottom: 2px solid #f8f9fa;
#     }
    
#     .chat-icon {
#         width: 60px;
#         height: 60px;
#         background: linear-gradient(135deg, #667eea, #764ba2);
#         border-radius: 50%;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         font-size: 1.5rem;
#         margin-right: 1rem;
#         box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
#     }
    
#     .chat-title {
#         font-size: 1.5rem;
#         font-weight: 600;
#         color: #2c3e50;
#         margin: 0;
#     }
    
#     .input-section {
#         margin-bottom: 2rem;
#     }
    
#     .stTextInput > div > div > input {
#         background: linear-gradient(135deg, #ffffff, #f8f9fa) !important;
#         border: 2px solid #e9ecef !important;
#         border-radius: 12px !important;
#         padding: 1.2rem 1.5rem !important;
#         font-size: 1rem !important;
#         font-weight: 500 !important;
#         color: #495057 !important;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
#         transition: all 0.3s ease !important;
#     }
    
#     .stTextInput > div > div > input:focus {
#         border: 2px solid #667eea !important;
#         box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1), 0 8px 25px rgba(0,0,0,0.1) !important;
#         transform: translateY(-2px) !important;
#         background: #ffffff !important;
#     }
    
#     /* Message Bubbles */
#     .message-container {
#         animation: slideInUp 0.5s ease-out;
#         margin: 1.5rem 0;
#     }
    
#     @keyframes slideInUp {
#         from { opacity: 0; transform: translateY(20px); }
#         to { opacity: 1; transform: translateY(0); }
#     }
    
#     .user-bubble {
#         background: linear-gradient(135deg, #667eea, #764ba2);
#         color: white;
#         padding: 1.5rem;
#         border-radius: 20px 20px 5px 20px;
#         margin-left: 15%;
#         margin-bottom: 1rem;
#         box-shadow: 0 8px 25px rgba(102, 126, 234, 0.25);
#         position: relative;
#     }
    
#     .bot-bubble {
#         background: linear-gradient(135deg, #f8f9fa, #e9ecef);
#         color: #495057;
#         padding: 1.5rem;
#         border-radius: 20px 20px 20px 5px;
#         margin-right: 15%;
#         box-shadow: 0 8px 25px rgba(0,0,0,0.08);
#         border-left: 4px solid #667eea;
#     }
    
#     .fallback-bubble {
#         background: linear-gradient(135deg, #fff3cd, #ffeeba);
#         color: #856404;
#         padding: 1.5rem;
#         border-radius: 20px 20px 20px 5px;
#         margin-right: 15%;
#         box-shadow: 0 8px 25px rgba(255, 193, 7, 0.15);
#         border-left: 4px solid #ffc107;
#     }
    
#     .confidence-pill {
#         display: inline-block;
#         background: rgba(255, 255, 255, 0.2);
#         color: white;
#         padding: 0.4rem 0.8rem;
#         border-radius: 20px;
#         font-size: 0.8rem;
#         font-weight: 600;
#         margin-top: 0.8rem;
#     }
    
#     /* Sidebar Section */
#     .sidebar-section {
#         animation: slideInRight 0.6s ease-out;
#     }
    
#     @keyframes slideInRight {
#         from { opacity: 0; transform: translateX(30px); }
#         to { opacity: 1; transform: translateX(0); }
#     }
    
#     .sidebar-card {
#         background: white;
#         border-radius: 16px;
#         padding: 1.5rem;
#         margin-bottom: 1.5rem;
#         box-shadow: 0 8px 32px rgba(0,0,0,0.08);
#         border: 1px solid rgba(0,0,0,0.05);
#         transition: transform 0.3s ease, box-shadow 0.3s ease;
#     }
    
#     .sidebar-card:hover {
#         transform: translateY(-4px);
#         box-shadow: 0 12px 40px rgba(0,0,0,0.15);
#     }
    
#     .sidebar-header {
#         display: flex;
#         align-items: center;
#         margin-bottom: 1rem;
#     }
    
#     .sidebar-icon {
#         width: 40px;
#         height: 40px;
#         background: linear-gradient(135deg, #667eea, #764ba2);
#         border-radius: 8px;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         font-size: 1.2rem;
#         margin-right: 0.8rem;
#         color: white;
#     }
    
#     .sidebar-title {
#         font-weight: 600;
#         color: #2c3e50;
#         font-size: 1.1rem;
#         margin: 0;
#     }
    
#     /* Quick Actions */
#     .quick-actions-grid {
#         display: grid;
#         grid-template-columns: 1fr 1fr;
#         gap: 0.8rem;
#         margin-top: 1rem;
#     }
    
#     .quick-action-btn {
#         background: linear-gradient(135deg, #f8f9fa, #e9ecef);
#         border: 1px solid #dee2e6;
#         border-radius: 8px;
#         padding: 0.8rem;
#         font-size: 0.85rem;
#         font-weight: 500;
#         color: #495057;
#         cursor: pointer;
#         transition: all 0.3s ease;
#         text-align: left;
#     }
    
#     .quick-action-btn:hover {
#         background: linear-gradient(135deg, #667eea, #764ba2);
#         color: white;
#         transform: translateY(-2px);
#         box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
#     }
    
#     /* Stats Cards */
#     .stats-grid {
#         display: grid;
#         grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
#         gap: 1.5rem;
#         margin: 2rem 0;
#     }
    
#     .stat-card {
#         background: white;
#         border-radius: 12px;
#         padding: 2rem;
#         text-align: center;
#         box-shadow: 0 8px 32px rgba(0,0,0,0.08);
#         border: 1px solid rgba(0,0,0,0.05);
#         transition: transform 0.3s ease;
#     }
    
#     .stat-card:hover {
#         transform: translateY(-4px);
#     }
    
#     .stat-number {
#         font-size: 2.5rem;
#         font-weight: 700;
#         background: linear-gradient(135deg, #667eea, #764ba2);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         background-clip: text;
#         margin-bottom: 0.5rem;
#     }
    
#     .stat-label {
#         color: #6c757d;
#         font-weight: 500;
#         font-size: 0.9rem;
#     }
    
#     /* Footer */
#     .footer-section {
#         background: linear-gradient(135deg, #2c3e50, #34495e);
#         color: white;
#         padding: 2rem;
#         border-radius: 16px;
#         margin-top: 3rem;
#         text-align: center;
#     }
    
#     .footer-title {
#         font-size: 1.3rem;
#         font-weight: 600;
#         margin-bottom: 0.5rem;
#     }
    
#     .footer-subtitle {
#         opacity: 0.8;
#         font-size: 0.9rem;
#         margin-bottom: 1rem;
#     }
    
#     .footer-note {
#         font-size: 0.8rem;
#         opacity: 0.6;
#     }
    
#     /* Hide Streamlit elements */
#     #MainMenu {visibility: hidden;}
#     .stDeployButton {display:none;}
#     footer {visibility: hidden;}
#     .stApp > header {visibility: hidden;}
#     .css-1rs6os {visibility: hidden;}
#     .css-17eq0hr {visibility: hidden;}
    
#     /* Loading states */
#     .loading-pulse {
#         animation: pulse 2s infinite;
#     }
    
#     @keyframes pulse {
#         0% { opacity: 1; }
#         50% { opacity: 0.5; }
#         100% { opacity: 1; }
#     }
# </style>
# """, unsafe_allow_html=True)

# # === Load Dataset ===
# @st.cache_data
# def load_data(file_path):
#     try:
#         df = pd.read_excel(file_path)
#         df_qna = df[df["Type"] == "QnA"].copy()
#         return df_qna
#     except FileNotFoundError:
#         # Create sample data for demo
#         sample_data = {
#             'Question': [
#                 'How to apply for leave?',
#                 'What is the dress code policy?',
#                 'What are the working hours?',
#                 'Can I work from home?',
#                 'Who do I contact for IT issues?',
#                 'What are the office holidays?',
#                 'How do I reset my password?',
#                 'What is the lunch break policy?',
#                 'How do I request equipment?',
#                 'What are the benefits available?',
#                 'How to submit expense reports?',
#                 'What is the performance review process?'
#             ],
#             'Answer / Statement': [
#                 'To apply for leave, log into the HR portal and submit your leave request at least 2 days in advance. Your manager will review and approve within 24 hours.',
#                 'Our dress code is business casual. Avoid shorts, flip-flops, and overly casual attire. Smart casual is encouraged for client meetings.',
#                 'Standard working hours are 9:00 AM to 6:00 PM, Monday through Friday. Flexible timing available with manager approval.',
#                 'Yes, remote work is allowed up to 2 days per week with manager approval. Full remote options available for certain roles.',
#                 'For IT support, contact the help desk at ext. 1234 or email it-support@company.com. For urgent issues, call the 24/7 hotline.',
#                 'Office holidays include all national holidays plus 2 floating holidays per year. Check the company calendar for specific dates.',
#                 'To reset your password, use the self-service portal or contact IT support. Password must be changed every 90 days.',
#                 'Lunch break is 1 hour, typically taken between 12:00 PM and 2:00 PM. Flexible timing available based on workload.',
#                 'Equipment requests can be made through the IT portal. Standard approval time is 3-5 business days.',
#                 'Benefits include health insurance, dental, vision, 401k matching, gym membership, and professional development funds.',
#                 'Expense reports should be submitted monthly through the finance portal with all receipts attached.',
#                 'Performance reviews are conducted quarterly with annual goal setting and development planning sessions.'
#             ],
#             'Type': ['QnA'] * 12
#         }
#         return pd.DataFrame(sample_data)

# # === Load Model ===
# @st.cache_resource
# def load_model():
#     return SentenceTransformer('all-MiniLM-L6-v2')

# # === Embeddings ===
# @st.cache_data
# def get_embeddings(questions, _model):
#     return _model.encode(questions, show_progress_bar=False)

# # === Semantic Matching ===
# def get_answer(user_query, df_qna, question_embeddings, model, threshold=0.6):
#     query_embedding = model.encode([user_query])
#     scores = cosine_similarity(query_embedding, question_embeddings)[0]
#     best_idx = scores.argmax()
#     confidence = scores[best_idx]

#     if confidence < threshold:
#         return None, None, confidence

#     best_question = df_qna.iloc[best_idx]["Question"]
#     best_answer = df_qna.iloc[best_idx]["Answer / Statement"]
#     return best_question, best_answer, confidence

# # Load resources
# with st.spinner('⚡ Loading Help Center...'):
#     df_qna = load_data("Chatbot_QnA_Dummy_Data_Updated.xlsx")
#     model = load_model()
#     question_embeddings = get_embeddings(df_qna["Question"].tolist(), model)

# # === Header Section ===
# st.markdown("""
# <div class="header-section">
#     <div class="header-title">💼 Employee Help Center</div>
#     <div class="header-subtitle">Get instant answers to your workplace questions • Self-service support • Available 24/7</div>
# </div>
# """, unsafe_allow_html=True)

# # === Main Content Grid ===
# st.markdown('<div class="content-grid">', unsafe_allow_html=True)

# # === Chat Section (Left Column) ===
# st.markdown("""
# <div class="chat-section">
#     <div class="chat-header">
#         <div class="chat-icon">💬</div>
#         <div>
#             <div class="chat-title">Ask Your Question</div>
#             <div style="color: #6c757d; font-size: 0.9rem;">Type your question below and get instant answers</div>
#         </div>
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # Session state management
# if 'selected_question' not in st.session_state:
#     st.session_state.selected_question = ""
# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []

# # Enhanced suggestions
# suggestions = [
#     "🏖️ How to apply for leave?",
#     "👔 What's the dress code?", 
#     "⏰ What are the working hours?",
#     "🏠 Can I work from home?",
#     "💻 Who do I contact for IT issues?",
#     "🎉 What are the office holidays?",
#     "🔐 How do I reset my password?",
#     "🍽️ What's the lunch break policy?"
# ]

# # Check for suggestion clicks
# for suggestion in suggestions:
#     clean_suggestion = suggestion.split(' ', 1)[1]
#     if st.session_state.get(f"clicked_{clean_suggestion}", False):
#         st.session_state.selected_question = clean_suggestion
#         st.session_state[f"clicked_{clean_suggestion}"] = False
#         break

# # Input section
# user_input = st.text_input(
#     "",
#     value=st.session_state.selected_question,
#     placeholder="💭 Ask me anything... (e.g., How do I submit an expense report?)",
#     key="user_input"
# )

# # Clear selected question after use
# if st.session_state.selected_question and user_input == st.session_state.selected_question:
#     st.session_state.selected_question = ""

# # Process user input
# if user_input:
#     with st.spinner('🔍 Finding your answer...'):
#         time.sleep(0.3)
#         match_q, answer, score = get_answer(user_input, df_qna, question_embeddings, model)
    
#     # Display user message
#     st.markdown(f"""
#     <div class="message-container">
#         <div class="user-bubble">
#             <strong>Your Question:</strong><br>
#             {user_input}
#         </div>
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Display response
#     if answer:
#         st.markdown(f"""
#         <div class="message-container">
#             <div class="bot-bubble">
#                 <strong>📋 Answer:</strong><br>
#                 {answer}
#                 <div class="confidence-pill">
#                     ✓ Match: {score:.0%}
#                 </div>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
#     else:
#         st.markdown(f"""
#         <div class="message-container">
#             <div class="fallback-bubble">
#                 <strong>🤔 Need More Help?</strong><br>
#                 I couldn't find a specific answer for that question. Please contact our support team:
#                 <br>• HR Team: hr@company.com
#                 <br>• IT Support: it-support@company.com
#                 <br>• General Help: help@company.com
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
        
#         # Show popular questions
#         st.markdown("**💡 Try these popular questions:**")
#         cols = st.columns(2)
#         for i, suggestion in enumerate(suggestions[:6]):
#             clean_suggestion = suggestion.split(' ', 1)[1]
#             with cols[i % 2]:
#                 if st.button(suggestion, key=f"suggest_{i}"):
#                     st.session_state[f"clicked_{clean_suggestion}"] = True
#                     st.rerun()

# # === Sidebar Section (Right Column) ===
# st.markdown("""
# <div class="sidebar-section">
#     <div class="sidebar-card">
#         <div class="sidebar-header">
#             <div class="sidebar-icon">⚡</div>
#             <div class="sidebar-title">Quick Actions</div>
#         </div>
#         <div class="quick-actions-grid">
# """, unsafe_allow_html=True)

# # Quick action buttons
# quick_actions = [
#     "Leave Request", "IT Support", "HR Portal", "Benefits",
#     "Expense Report", "Equipment", "Payroll", "Directory"
# ]

# cols = st.columns(2)
# for i, action in enumerate(quick_actions):
#     with cols[i % 2]:
#         if st.button(action, key=f"quick_{i}"):
#             if action == "Leave Request":
#                 st.session_state["clicked_How to apply for leave?"] = True
#                 st.rerun()
#             elif action == "IT Support":
#                 st.session_state["clicked_Who do I contact for IT issues?"] = True
#                 st.rerun()

# st.markdown('</div></div>', unsafe_allow_html=True)

# # # System Status Card
# # st.markdown("""
# # <div class="sidebar-card">
# #     <div class="sidebar-header">
# #         <div class="sidebar-icon">📊</div>
# #         <div class="sidebar-title">System Status</div>
# #     </div>
# #     <div style="color: #28a745; font-weight: 500;">🟢 All systems operational</div>
# #     <div style="color: #6c757d; font-size: 0.85rem; margin-top: 0.5rem;">
# #         Last updated: Just now<br>
# #         Response time: <500ms<br>
# #         Uptime: 99.9%
# #     </div>
# # </div>
# # """, unsafe_allow_html=True)

# # Help Resources Card
# # Improved Resources Card
# st.markdown("""
# <div style="background: linear-gradient(135deg, #ffffff, #f8f9fa);
#             border-radius: 12px;
#             padding: 1.5rem 2rem;
#             box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
#             font-size: 0.95rem;
#             color: #2c3e50;
#             line-height: 1.6;
#             margin-top: 1rem;">
#     <h4 style="margin-bottom: 1rem;">📚 Helpful Resources</h4>
#     <ul style="list-style: none; padding-left: 0;">
#         <li style="margin-bottom: 0.5rem;">📖 <strong>Employee Handbook</strong> — Company culture, rules, policies</li>
#         <li style="margin-bottom: 0.5rem;">🎯 <strong>Company Policies</strong> — Leave, travel, conduct guidelines</li>
#         <li style="margin-bottom: 0.5rem;">📞 <strong>Contact Directory</strong> — Key HR, IT, Admin emails</li>
#         <li style="margin-bottom: 0.5rem;">🔧 <strong>IT Self-Service</strong> — Password reset, laptop requests</li>
#     </ul>
# </div>
# """, unsafe_allow_html=True)

# st.markdown('</div></div>', unsafe_allow_html=True)  # Close content grid

# # === Statistics Section ===
# st.markdown('<div class="stats-grid">', unsafe_allow_html=True)

# col1, col2, col3, col4 = st.columns(4)

# with col1:
#     st.markdown(f"""
#     <div class="stat-card">
#         <div class="stat-number">{len(df_qna)}</div>
#         <div class="stat-label">Topics Covered</div>
#     </div>
#     """, unsafe_allow_html=True)

# with col2:
#     st.markdown("""
#     <div class="stat-card">
#         <div class="stat-number">24/7</div>
#         <div class="stat-label">Always Available</div>
#     </div>
#     """, unsafe_allow_html=True)

# with col3:
#     st.markdown("""
#     <div class="stat-card">
#         <div class="stat-number">⚡</div>
#         <div class="stat-label">Instant Answers</div>
#     </div>
#     """, unsafe_allow_html=True)

# with col4:
#     st.markdown("""
#     <div class="stat-card">
#         <div class="stat-number">95%</div>
#         <div class="stat-label">Accuracy Rate</div>
#     </div>
#     """, unsafe_allow_html=True)

# st.markdown('</div>', unsafe_allow_html=True)

# # === System Information (Collapsible) ===
# with st.expander("🔧 System Information", expanded=False):
#     st.markdown(f"""
#     <div style="background: linear-gradient(135deg, #e9ecef, #f8f9fa);
#                 border-radius: 12px;
#                 padding: 1.5rem 2rem;
#                 box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
#                 font-size: 0.95rem;
#                 color: #2c3e50;
#                 line-height: 1.6;">
#         <h4 style="margin-bottom: 1rem;">📊 Knowledge Base Summary</h4>
#         <ul style="list-style: none; padding-left: 0;">
#             <li><strong>Total Topics:</strong> {len(df_qna)}</li>
#             <li><strong>Categories:</strong> HR, IT, Policies, Benefits</li>
#             <li><strong>Last Updated:</strong> August 2025</li>
#             <li><strong>Coverage:</strong> Company-wide policies</li>
#         </ul>
#     </div>
#     """, unsafe_allow_html=True)

# # === Footer ===
# st.markdown("""
# <div class="footer-section">
#     <div class="footer-title">💼 Employee Help Center</div>
#     <div class="footer-subtitle">Your go-to resource for workplace questions and support</div>
#     <div class="footer-note">
#         For complex issues or personalized assistance, please contact the relevant department directly.
#         <br> By Vishakha Deshpande . Internal use only
#     </div>
# </div>
# """, unsafe_allow_html=True)



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

# === Enhanced Professional Styling ===
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        min-height: 100vh;
        color: #f8fafc;
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
        background: linear-gradient(135deg, #3b82f6, #1d4ed8, #1e40af);
        color: white;
        padding: 4rem 2rem;
        border-radius: 20px;
        margin-bottom: 2.5rem;
        box-shadow: 0 20px 40px rgba(59, 130, 246, 0.3);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .header-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 60%);
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        50% { transform: translate(-20px, -10px) rotate(180deg); }
    }
    
    .header-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        position: relative;
        z-index: 2;
        background: linear-gradient(135deg, #ffffff, #e2e8f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.02em;
    }
    
    .header-subtitle {
        font-size: 1.3rem;
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
        gap: 2.5rem;
        margin-bottom: 2rem;
    }
    
    @media (max-width: 968px) {
        .content-grid {
            grid-template-columns: 1fr;
        }
    }
    
    /* Chat Section */
    .chat-section {
        background: linear-gradient(135deg, #1e293b, #334155);
        border-radius: 24px;
        padding: 2.5rem;
        box-shadow: 0 20px 50px rgba(0,0,0,0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        animation: slideInLeft 0.8s ease-out;
        backdrop-filter: blur(10px);
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-40px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .chat-header {
        display: flex;
        align-items: center;
        margin-bottom: 2.5rem;
        padding-bottom: 1.5rem;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    .chat-icon {
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        margin-right: 1.5rem;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .chat-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 0;
        margin-bottom: 0.5rem;
    }
    
    .chat-subtitle {
        color: #cbd5e1;
        font-size: 1rem;
        font-weight: 400;
    }
    
    /* Enhanced Input Styling */
    .stTextInput > div > div > input {
        background: linear-gradient(135deg, #475569, #64748b) !important;
        border: 2px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 16px !important;
        padding: 1.5rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        color: #f8fafc !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2) !important;
        transition: all 0.4s ease !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #cbd5e1 !important;
        opacity: 0.8 !important;
        font-weight: 400 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border: 2px solid #3b82f6 !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2), 0 20px 40px rgba(0,0,0,0.3) !important;
        transform: translateY(-3px) !important;
        background: linear-gradient(135deg, #64748b, #475569) !important;
        outline: none !important;
    }
    
    /* Message Bubbles */
    .message-container {
        animation: slideInUp 0.6s ease-out;
        margin: 2rem 0;
    }
    
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        padding: 2rem;
        border-radius: 24px 24px 8px 24px;
        margin-left: 10%;
        margin-bottom: 1.5rem;
        box-shadow: 0 15px 35px rgba(59, 130, 246, 0.4);
        position: relative;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .bot-bubble {
        background: linear-gradient(135deg, #374151, #4b5563);
        color: #f8fafc;
        padding: 2rem;
        border-radius: 24px 24px 24px 8px;
        margin-right: 10%;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        border-left: 4px solid #3b82f6;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .fallback-bubble {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        padding: 2rem;
        border-radius: 24px 24px 24px 8px;
        margin-right: 10%;
        box-shadow: 0 15px 35px rgba(245, 158, 11, 0.4);
        border-left: 4px solid #fbbf24;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .confidence-pill {
        display: inline-block;
        background: rgba(255, 255, 255, 0.25);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(5px);
    }
    
    /* Sidebar Section */
    .sidebar-section {
        animation: slideInRight 0.8s ease-out;
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(40px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .sidebar-card {
        background: linear-gradient(135deg, #1e293b, #334155);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.4s ease;
        backdrop-filter: blur(10px);
    }
    
    .sidebar-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 25px 50px rgba(0,0,0,0.4);
        border-color: rgba(59, 130, 246, 0.3);
    }
    
    .sidebar-header {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    
    .sidebar-icon {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-right: 1rem;
        color: white;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .sidebar-title {
        font-weight: 700;
        color: #f8fafc;
        font-size: 1.3rem;
        margin: 0;
    }
    
    /* Quick Actions - Enhanced */
    .quick-actions-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-top: 1.5rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #475569, #64748b) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 12px !important;
        padding: 1rem 1.5rem !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        color: #f8fafc !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        text-align: left !important;
        width: 100% !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
        transform: translateY(-2px) scale(1.05) !important;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.4) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
    }
    
    .stButton > button:focus {
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3) !important;
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
        background: linear-gradient(135deg, #1e293b, #334155);
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.4s ease;
        backdrop-filter: blur(10px);
    }
    
    .stat-card:hover {
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 25px 50px rgba(0,0,0,0.4);
        border-color: rgba(59, 130, 246, 0.3);
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        text-shadow: 0 2px 10px rgba(59, 130, 246, 0.3);
    }
    
    .stat-label {
        color: #cbd5e1;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.5px;
    }
    
    /* Footer */
    .footer-section {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        color: #f8fafc;
        padding: 3rem;
        border-radius: 20px;
        margin-top: 4rem;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .footer-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .footer-subtitle {
        opacity: 0.9;
        font-size: 1rem;
        margin-bottom: 1.5rem;
        color: #cbd5e1;
    }
    
    .footer-note {
        font-size: 0.85rem;
        opacity: 0.7;
        color: #94a3b8;
    }
    
    /* Resources Card Enhanced */
    .resources-card {
        background: linear-gradient(135deg, #1e293b, #334155);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        font-size: 0.95rem;
        color: #f8fafc;
        line-height: 1.7;
        margin-top: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .resources-card h4 {
        color: #f8fafc;
        margin-bottom: 1.5rem;
        font-weight: 700;
        font-size: 1.2rem;
    }
    
    .resources-card ul {
        list-style: none;
        padding-left: 0;
    }
    
    .resources-card li {
        margin-bottom: 0.8rem;
        color: #cbd5e1;
        font-weight: 500;
    }
    
    .resources-card strong {
        color: #f8fafc;
    }
    
    /* System Info Enhanced */
    .system-info-card {
        background: linear-gradient(135deg, #374151, #4b5563);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        font-size: 0.95rem;
        color: #f8fafc;
        line-height: 1.7;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .system-info-card h4 {
        color: #f8fafc;
        margin-bottom: 1.5rem;
        font-weight: 700;
        font-size: 1.2rem;
    }
    
    .system-info-card ul {
        list-style: none;
        padding-left: 0;
    }
    
    .system-info-card li {
        margin-bottom: 0.8rem;
        color: #cbd5e1;
    }
    
    .system-info-card strong {
        color: #f8fafc;
        font-weight: 600;
    }
    
    /* Streamlit Expander Styling */
    .streamlit-expander {
        background: linear-gradient(135deg, #1e293b, #334155) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .streamlit-expander > div > div > div {
        color: #f8fafc !important;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stApp > header {visibility: hidden;}
    .css-1rs6os {visibility: hidden;}
    .css-17eq0hr {visibility: hidden;}
    
    /* Loading states */
    .loading-pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    /* Suggestion buttons styling */
    .suggestion-container .stButton > button {
        background: linear-gradient(135deg, #374151, #4b5563) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 12px !important;
        padding: 0.8rem 1.2rem !important;
        margin: 0.5rem 0.5rem 0.5rem 0 !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
    }
    
    .suggestion-container .stButton > button:hover {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4) !important;
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
    query_embedding = model.encode([user_query])
    scores = cosine_similarity(query_embedding, question_embeddings)[0]
    best_idx = scores.argmax()
    confidence = scores[best_idx]

    if confidence < threshold:
        return None, None, confidence

    best_question = df_qna.iloc[best_idx]["Question"]
    best_answer = df_qna.iloc[best_idx]["Answer / Statement"]
    return best_question, best_answer, confidence

# Load resources
with st.spinner('⚡ Loading Help Center...'):
    df_qna = load_data("Chatbot_QnA_Dummy_Data_Updated.xlsx")
    model = load_model()
    question_embeddings = get_embeddings(df_qna["Question"].tolist(), model)

# === Header Section ===
st.markdown("""
<div class="header-section">
    <div class="header-title">💼 Employee Help Center</div>
    <div class="header-subtitle">Get instant answers to your workplace questions • Self-service support • Available 24/7 • AI-powered assistance</div>
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
            <div class="chat-subtitle">Type your question below and get instant AI-powered answers</div>
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
    placeholder="💭 Ask me anything about company policies, benefits, IT support, or workplace procedures...",
    key="user_input"
)

# Clear selected question after use
if st.session_state.selected_question and user_input == st.session_state.selected_question:
    st.session_state.selected_question = ""

# Process user input
if user_input:
    with st.spinner('🔍 Searching knowledge base...'):
        time.sleep(0.5)
        match_q, answer, score = get_answer(user_input, df_qna, question_embeddings, model)
    
    # Display user message
    st.markdown(f"""
    <div class="message-container">
        <div class="user-bubble">
            <strong>💬 Your Question:</strong><br>
            {user_input}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display response
    if answer:
        st.markdown(f"""
        <div class="message-container">
            <div class="bot-bubble">
                <strong>🤖 AI Assistant:</strong><br>
                {answer}
                <div class="confidence-pill">
                    ✨ Confidence: {score:.0%}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="message-container">
            <div class="fallback-bubble">
                <strong>🤔 Need Human Assistance?</strong><br>
                I couldn't find a specific answer for that question in my knowledge base. Please reach out to our support team for personalized help:
                <br><br>
                📧 <strong>HR Team:</strong> hr@company.com<br>
                💻 <strong>IT Support:</strong> it-support@company.com<br>
                📞 <strong>General Help:</strong> help@company.com<br>
                🆘 <strong>Emergency:</strong> Call extension 911
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

# === Sidebar Section (Right Column) ===
st.markdown("""
<div class="sidebar-section">
    <div class="sidebar-card">
        <div class="sidebar-header">
            <div class="sidebar-icon">⚡

