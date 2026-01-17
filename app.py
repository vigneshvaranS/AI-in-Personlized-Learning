import streamlit as st
import requests
import json
import re
import numpy as np
import joblib

# --------------------------------------------------
# PAGE CONFIGURATION & STYLES
# --------------------------------------------------
st.set_page_config(
    page_title="Personalized Learning Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .resource-card {
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #41444C;
        margin-bottom: 15px;
    }
    h1 { color: #FF4B4B; }
    .box {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #41444C;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# API KEYS
# --------------------------------------------------
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
PEXELS_API_KEY = st.secrets["PEXELS_API_KEY"]
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]

MODEL_NAME = "meta-llama/llama-3.3-70b-instruct:free"

# --------------------------------------------------
# LOAD ML MODEL
# --------------------------------------------------
rf_model = joblib.load("saved_models/random_forest_model.pkl")
scaler = joblib.load("saved_models/scaler.pkl")
label_encoder = joblib.load("saved_models/label_encoder.pkl")

def predict_difficulty(score, time_spent, attempts):
    x = scaler.transform([[score, time_spent, attempts]])
    pred = rf_model.predict(x)
    return label_encoder.inverse_transform(pred)[0]

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "current_plan" not in st.session_state:
    st.session_state.current_plan = None
if "history" not in st.session_state:
    st.session_state.history = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "quiz" not in st.session_state:
    st.session_state.quiz = None

# --------------------------------------------------
# HELPERS
# --------------------------------------------------
def search_serper(query, num_results=5):
    try:
        r = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
            json={"q": query, "num": num_results},
            timeout=20
        )
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

def fetch_topic_image(topic):
    try:
        r = requests.get(
            "https://api.pexels.com/v1/search",
            headers={"Authorization": PEXELS_API_KEY},
            params={"query": topic, "per_page": 1}
        )
        if r.json().get("photos"):
            return r.json()["photos"][0]["src"]["large"]
    except:
        pass
    return None

def query_llm(messages):
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
        json={"model": MODEL_NAME, "messages": messages},
        timeout=40
    )
    data = r.json()
    if "choices" in data:
        return data["choices"][0]["message"]["content"]
    return "⚠️ AI unavailable."

def extract_resources(ai_text, search_results):
    try:
        match = re.search(r"\{[\s\S]*\}", ai_text)
        if match:
            j = json.loads(match.group(0))
            if "resources" in j:
                return j["resources"]
    except:
        pass

    resources = []
    if search_results and "organic" in search_results:
        for r in search_results["organic"]:
            resources.append({
                "title": r.get("title"),
                "description": "Recommended learning resource",
                "link": r.get("link")
            })
    return resources

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.title("⚙ Preferences")

    with st.form("preferences_form"):
        topic = st.text_input("I want to learn...")

        col1, col2 = st.columns(2)
        with col1:
            style = st.selectbox("Learning Style", ["Visual", "Text-Based", "Hands-on", "Academic"])
        with col2:
            depth = st.selectbox("Explanation Depth", ["Overview", "Core Concepts", "Deep Dive"])

        st.markdown("### 🧠 Quick Learning Assessment")
        st.markdown('<div class="box">', unsafe_allow_html=True)
        quiz_score = st.slider("Expected quiz score (%)", 0, 100, 60)
        time_spent = st.slider("Time spent learning (minutes)", 5, 120, 30)
        attempts = st.slider("Attempts to understand topic", 1, 5, 2)
        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("🚀 Start Learning Journey")

    st.markdown("---")
    st.subheader("📜 History")

    for i, p in enumerate(reversed(st.session_state.history)):
        if st.button(f"{p['topic']} ({p['level']})", key=f"h{i}"):
            st.session_state.current_plan = p
            st.session_state.chat_history = []
            st.session_state.quiz = None
            st.rerun()

# --------------------------------------------------
# HERO
# --------------------------------------------------
if not st.session_state.current_plan:
    st.markdown("""
    <div style="text-align:center; padding:50px">
        <h1>🎓 Personalized Learning Assistant</h1>
        <p style="font-size:18px">
            Personalized learning powered by Machine Learning and Generative AI.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# GENERATE PLAN
# --------------------------------------------------
if submitted and topic:
    with st.status("🚀 Building your personalized learning plan...", expanded=True) as status:

        status.write("🧠 Predicting learner difficulty...")
        level = predict_difficulty(quiz_score, time_spent, attempts)

        status.write("🔍 Searching learning resources...")
        search_results = search_serper(f"{topic} learning resources")

        status.write("🖼️ Fetching topic image...")
        image = fetch_topic_image(topic)

        status.write("✍️ Generating study guide...")
        ai_text = query_llm([
            {"role": "system", "content": "You are an expert educational consultant."},
            {"role": "user", "content": f"""
            Topic: {topic}
            Difficulty: {level}
            Style: {style}
            Depth: {depth}
            """}
        ])

        resources = extract_resources(ai_text, search_results)

        plan = {
            "topic": topic,
            "level": level,
            "image": image,
            "text": ai_text,
            "resources": resources
        }

        st.session_state.current_plan = plan
        st.session_state.history.append(plan)
        st.session_state.chat_history = []
        st.session_state.quiz = None

        status.update(label="✅ Learning Plan Ready!", state="complete")

# --------------------------------------------------
# DISPLAY
# --------------------------------------------------
if st.session_state.current_plan:
    p = st.session_state.current_plan

    if p["image"]:
        st.image(p["image"], use_container_width=True)

    st.title(f"📘 Mastery Guide: {p['topic']}")
    st.caption(f"🧠 AI-Predicted Difficulty: {p['level']}")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📖 Study Guide", "🔗 Resources", "💬 AI Tutor", "🧠 Quiz"]
    )

    with tab1:
        st.markdown(p["text"])

    with tab2:
        for r in p["resources"]:
            st.markdown(
                f"<div class='resource-card'><b>{r['title']}</b><br>"
                f"{r['description']}<br>"
                f"<a href='{r['link']}' target='_blank'>Open</a></div>",
                unsafe_allow_html=True
            )

    with tab3:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if q := st.chat_input("Ask a question about this topic"):
            st.session_state.chat_history.append({"role": "user", "content": q})
            ans = query_llm([
                {"role": "system", "content": f"You are a tutor for {p['topic']}"},
                {"role": "user", "content": q}
            ])
            st.session_state.chat_history.append({"role": "assistant", "content": ans})
            with st.chat_message("assistant"):
                st.markdown(ans)

    with tab4:
        if st.button("Generate Quiz"):
            quiz = query_llm([
                {"role": "user", "content": f"Create a short quiz for {p['topic']} with answers hidden."}
            ])
            st.session_state.quiz = quiz

        if st.session_state.quiz:
            st.markdown(st.session_state.quiz)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")
st.caption("Developed by Vignesh S | AI-Powered Personalized Learning Assistant")
