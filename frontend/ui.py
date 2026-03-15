import streamlit as st

def load_advanced_ui():

    st.markdown("""
    <script src="https://cdn.tailwindcss.com"></script>

    <style>
        body {
            background: #0f172a;
        }

        .glass {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(20px);
            border-radius: 25px;
            padding: 30px;
            border: 1px solid rgba(255,255,255,0.2);
        }

        .btn {
            background: linear-gradient(90deg,#6366f1,#8b5cf6);
            padding: 12px 25px;
            border-radius: 12px;
            color: white;
            font-weight: bold;
        }

        .btn:hover {
            transform: scale(1.05);
        }
    </style>
    """, unsafe_allow_html=True)