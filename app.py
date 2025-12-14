import streamlit as st
import requests
import json
import re

# --------------------------------------------------
# 1. PAGE CONFIGURATION & CUSTOM STYLES
# --------------------------------------------------
st.set_page_config(
    page_title="Personalized Learning Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI cards and typography
st.markdown("""
<style>
    /* Card Style for Resources */
    .resource-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #41444C;
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .resource-card:hover {
        transform: translateY(-5px);
        border-color: #FF4B4B;
    }
    .resource-title {
        font-size: 18px;
        font-weight: bold;
        color: #FFFFFF;
        margin-bottom: 5px;
    }
    .resource-type {
        font-size: 12px;
        background-color: #FF4B4B;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        display: inline-block;
        margin-bottom: 10px;
    }
    .resource-desc {
        font-size: 14px;
        color: #D3D3D3;
        margin-bottom: 15px;
    }
    /* Sidebar History Buttons */
    .stButton button {
        width: 100%;
        text-align: left;
    }
    /* Headers */
    h1 { color: #FF4B4B; }
    h2, h3 { color: #FAFAFA; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 2. API KEYS
# --------------------------------------------------
try:
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
    PEXELS_API_KEY = st.secrets["PEXELS_API_KEY"]
    SERPER_API_KEY = st.secrets["SERPER_API_KEY"]
except FileNotFoundError:
    st.error("Secrets file not found. Please add your API keys to .streamlit/secrets.toml")
    st.stop()

MODEL_NAME = "meta-llama/llama-3.3-70b-instruct:free"

# --------------------------------------------------
# 3. SESSION STATE INITIALIZATION
# --------------------------------------------------
if "current_plan" not in st.session_state:
    st.session_state.current_plan = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "history" not in st.session_state:
    st.session_state.history = []  # List to store past plans

# --------------------------------------------------
# 4. HELPER FUNCTIONS
# --------------------------------------------------

def search_serper(query, num_results=5):
    """Fetches real search results from Google via Serper."""
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": query, "num": num_results}
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"Search Error: {e}")
        return None

def fetch_topic_image(topic):
    """Fetches a relevant image from Pexels."""
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": topic, "per_page": 1, "orientation": "landscape"}
    try:
        response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params, timeout=5)
        data = response.json()
        if data.get("photos"):
            return data["photos"][0]["src"]["large2x"]
    except Exception:
        pass
    return None

def query_llm(messages):
    """Generic function to query OpenRouter LLM."""
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8501",
                "X-Title": "Personalized Learning Assistant",
            },
            data=json.dumps({
                "model": MODEL_NAME,
                "messages": messages,
                "temperature": 0.7
            }),
            timeout=45
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            st.error(f"LLM Error: {response.text}")
            return None
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

def extract_json_from_text(text):
    """Extracts JSON block from LLM response for structured data."""
    try:
        # Robust regex to capture JSON object
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            return json.loads(match.group(0))
    except:
        pass
    return None

# --------------------------------------------------
# 5. SIDEBAR CONFIGURATION
# --------------------------------------------------
with st.sidebar:
    st.title("⚙ Preferences")
    
    # --- INPUT FORM ---
    with st.form("preferences_form"):
        topic = st.text_input("I want to learn...", placeholder="e.g., Astrophysics, Python, Piano")
        
        col1, col2 = st.columns(2)
        with col1:
            level = st.selectbox("Current Level", ["Beginner", "Intermediate", "Expert"])
        with col2:
            style = st.selectbox("Style", ["Visual", "Text-Based", "Hands-on", "Academic"])
            
        depth = st.select_slider("Depth", options=["Overview", "Core Concepts", "Deep Dive"])
        
        resources_types = st.multiselect(
            "Preferred Resources", 
            ["Video Courses", "Books", "Articles", "Interactive Tutorials"],
            default=["Video Courses", "Articles"]
        )
        
        submitted = st.form_submit_button("🚀 Start Learning Journey")

    # --- HISTORY SECTION ---
    st.markdown("---")
    st.subheader("📜 Your History")

    if st.session_state.history:
        # Display history items as buttons
        for i, past_plan in enumerate(reversed(st.session_state.history)):
            # Use specific key to identify each button
            if st.button(f"📄 {past_plan['topic']} ({past_plan['level']})", key=f"hist_{i}"):
                # Load the selected plan into current_plan
                st.session_state.current_plan = past_plan
                # Clear chat history for the new context
                st.session_state.chat_history = []
                st.session_state.quiz_data = None
                st.rerun()
        
        if st.button("🗑️ Clear History", type="primary"):
            st.session_state.history = []
            st.rerun()
    else:
        st.caption("No plans generated yet.")

# --------------------------------------------------
# 6. MAIN LOGIC
# --------------------------------------------------

# HEADER (Show only if no plan is active)
if not st.session_state.current_plan:
    st.markdown(
        """
        <div style="text-align: center; padding: 50px;">
            <h1>🎓 Personalized Learning Assistant</h1>
            <p style="font-size: 1.2rem;">
                Your AI-powered tutor that creates custom roadmaps, curates real-world resources, 
                and tests your knowledge.
            </p>
        </div>
        """, unsafe_allow_html=True
    )

# GENERATE NEW PLAN
if submitted and topic:
    # Reset State for new generation
    st.session_state.chat_history = []
    st.session_state.quiz_data = None
    
    with st.status("🏗 Building your personalized curriculum...", expanded=True) as status:
        
        # 1. Search Web
        status.write("🔍 Scouring the web for top-rated resources...")
        search_results = search_serper(f"best {topic} learning resources {', '.join(resources_types)}")
        
        formatted_search = ""
        if search_results and "organic" in search_results:
            for r in search_results["organic"][:5]:
                formatted_search += f"- {r.get('title')} ({r.get('link')})\n"
        
        # 2. Fetch Image
        status.write("🎨 Designing your dashboard...")
        image_url = fetch_topic_image(topic)
        
        # 3. Generate Content (Prompt Engineering)
        status.write("🤖 Drafting the study guide...")
        
        system_prompt = (
            "You are an elite educational consultant. Create a learning plan. "
            "CRITICAL: At the very end of your response, include a JSON block with key 'resources' "
            "containing a list of 4 best resources found in the search results. "
            "Structure: { 'resources': [ { 'title': '...', 'type': '...', 'link': '...', 'description': '...' } ] }"
        )
        
        user_prompt = f"""
        Topic: {topic}
        Level: {level}
        Style: {style}
        Depth: {depth}
        Web Context: {formatted_search}
        
        1. Write a clear, engaging introduction.
        2. Create a Step-by-Step Learning Path (Week by Week or Module by Module).
        3. Explain the 3 most critical core concepts.
        4. Provide a "Practical Exercise" idea.
        """
        
        response_text = query_llm([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])
        
        if response_text:
            # Extract JSON for cards
            json_data = extract_json_from_text(response_text)
            
            # Remove JSON from display text if present
            display_text = re.sub(r"\{[\s\S]*\}", "", response_text).strip()
            
            # Create the plan dictionary
            new_plan = {
                "topic": topic,
                "level": level,
                "image": image_url,
                "text": display_text,
                "resources_json": json_data,
                "raw_search": formatted_search
            }
            
            # Save to Session State (Current)
            st.session_state.current_plan = new_plan
            
            # Save to History (Append to list)
            # We check if it already exists to avoid duplicates on rerun
            if not st.session_state.history or st.session_state.history[-1]['topic'] != topic:
                st.session_state.history.append(new_plan)
                
            status.update(label="✅ Learning Plan Ready!", state="complete", expanded=False)

# DISPLAY CONTENT
if st.session_state.current_plan:
    plan = st.session_state.current_plan
    
    # Hero Section
    if plan["image"]:
        st.image(plan["image"], use_container_width=True)
    
    st.title(f"📘 Mastery Guide: {plan['topic']}")
    
    # TABS INTERFACE
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Study Guide", "🔗 Curated Resources", "💬 AI Tutor", "🧠 Quiz"])
    
    # --- TAB 1: STUDY GUIDE ---
    with tab1:
        st.markdown(plan["text"])
        st.markdown("---")
        st.caption("Content generated by AI based on real-time web search.")

    # --- TAB 2: RESOURCE CARDS ---
    with tab2:
        st.subheader("📚 Top Recommended Materials")
        
        # Robust JSON retrieval
        json_data = plan.get("resources_json")
        if json_data is None:
            json_data = {}
            
        resources = json_data.get("resources", [])
        
        if resources:
            cols = st.columns(2)
            for idx, res in enumerate(resources):
                with cols[idx % 2]:
                    st.markdown(f"""
                    <div class="resource-card">
                        <div class="resource-title">{res.get('title', 'Resource')}</div>
                        <div class="resource-type">{res.get('type', 'External Link')}</div>
                        <div class="resource-desc">{res.get('description', 'No description available.')}</div>
                        <a href="{res.get('link', '#')}" target="_blank" style="text-decoration:none; color:#4DA6FF; font-weight:bold;">
                            🔗 Open Resource &rarr;
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("Could not extract structured cards. Here are the search results:")
            st.text(plan.get("raw_search", "No results found."))

    # --- TAB 3: AI TUTOR (CHAT) ---
    with tab3:
        st.subheader(f"💬 Chat with your {plan['topic']} Tutor")
        st.info("Ask specific questions about the modules, concepts, or code examples.")
        
        # Display chat history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        # Chat Input
        if user_input := st.chat_input("Ask a follow-up question..."):
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)
            
            # Generate Answer
            with st.spinner("Thinking..."):
                context_messages = [
                    {"role": "system", "content": f"You are a helpful tutor for the topic: {plan['topic']}. Keep answers concise and educational."},
                    {"role": "assistant", "content": plan["text"]}
                ] + st.session_state.chat_history
                
                answer = query_llm(context_messages)
            
            # Add assistant message
            if answer:
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                with st.chat_message("assistant"):
                    st.markdown(answer)

    # --- TAB 4: QUIZ ---
    with tab4:
        st.subheader("🧠 Test Your Knowledge")
        
        if st.button("Generate a Quiz based on this plan"):
            with st.spinner("Creating questions..."):
                quiz_prompt = f"""
                Create a quiz for: {plan['topic']} based on this text:
                {plan['text'][:1000]}...
                
                Generate 3 multiple choice questions.
                Format clearly with Question, Options, and Correct Answer hidden or at the bottom.
                """
                quiz_content = query_llm([{"role": "user", "content": quiz_prompt}])
                st.session_state.quiz_data = quiz_content
        
        if st.session_state.quiz_data:
            st.markdown(st.session_state.quiz_data)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: grey;">
        Built with Streamlit, OpenRouter, and Serper Dev | 
        <a href="https://streamlit.io" target="_blank">Streamlit Docs</a>
    </div>
    """, unsafe_allow_html=True
)