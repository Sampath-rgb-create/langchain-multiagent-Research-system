import os
import streamlit as st
from dotenv import load_dotenv

# Load local environment defaults (if any exist)
load_dotenv()

from src.pipeline.pipeline import run_research_pipeline

# Page Configuration
st.set_page_config(
    page_title="AI Multi-Agent Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #2E76CF 0%, #15B8A6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .key-status-box {
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "openrouter_key" not in st.session_state:
    st.session_state.openrouter_key = os.getenv("OPENROUTER_API_KEY", "")
if "tavily_key" not in st.session_state:
    st.session_state.tavily_key = os.getenv("TAVILY_API_KEY", "")
if "pipeline_results" not in st.session_state:
    st.session_state.pipeline_results = None
if "current_topic" not in st.session_state:
    st.session_state.current_topic = None

# Sidebar: Visitor API Key Configuration
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/artificial-intelligence.png", width=65)
    st.title("Settings & Keys")
    st.caption("Bring Your Own API Keys (BYOK)")

    st.divider()

    st.subheader("🔑 Enter Your API Keys")
    st.markdown(
        "To run the research pipeline, please provide your own API keys. "
        "Your keys are kept securely in memory for this session and never stored permanently."
    )

    # OpenRouter API Key Input
    or_key_input = st.text_input(
        "OpenRouter API Key",
        value=st.session_state.openrouter_key,
        type="password",
        placeholder="sk-or-v1-...",
        help="Used to power the AI reasoning and writing models."
    )
    if or_key_input != st.session_state.openrouter_key:
        st.session_state.openrouter_key = or_key_input.strip()

    st.caption("👉 [Get a free OpenRouter Key](https://openrouter.ai/keys)")

    st.write("")

    # Tavily API Key Input
    tavily_key_input = st.text_input(
        "Tavily Search API Key",
        value=st.session_state.tavily_key,
        type="password",
        placeholder="tvly-...",
        help="Used by the Search Agent for real-time web research."
    )
    if tavily_key_input != st.session_state.tavily_key:
        st.session_state.tavily_key = tavily_key_input.strip()

    st.caption("👉 [Get a free Tavily Key](https://tavily.com)")

    # Key Status Badges
    has_or = bool(st.session_state.openrouter_key)
    has_tavily = bool(st.session_state.tavily_key)

    st.divider()
    st.markdown("**API Status:**")
    if has_or and has_tavily:
        st.success("All API Keys Ready ✅", icon="🟢")
    else:
        if not has_or:
            st.warning("OpenRouter Key Missing ⚠️")
        if not has_tavily:
            st.warning("Tavily Key Missing ⚠️")

    # Clear Keys Option
    if has_or or has_tavily:
        if st.button("🗑️ Clear Keys from Session", use_container_width=True):
            st.session_state.openrouter_key = ""
            st.session_state.tavily_key = ""
            st.rerun()

    st.divider()

    # Agent Pipeline Workflow
    st.subheader("🤖 How Agents Work")
    with st.expander("View 4-Agent Pipeline", expanded=False):
        st.markdown("""
        1. **🔍 Search Agent**: Queries web sources via Tavily API.
        2. **🌐 Reader Agent**: Scrapes deep text from the best article.
        3. **✍️ Writer Agent**: Drafts a comprehensive structured report.
        4. **🧐 Critic Agent**: Evaluates clarity, coherence & recommends enhancements.
        """)

# Main Content Area
st.markdown('<div class="main-header">🔬 AI Multi-Agent Research System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Collaborative multi-agent research team powered by LangChain, OpenRouter, and Tavily.</div>', unsafe_allow_html=True)

# Prompt banner if keys are not entered
if not (st.session_state.openrouter_key and st.session_state.tavily_key):
    st.info(
        "👋 **Welcome!** To get started, please paste your **OpenRouter** and **Tavily** API keys in the sidebar on the left.",
        icon="🔑"
    )

# Quick Sample Topic Buttons
st.write("**💡 Quick Example Topics:**")
col1, col2, col3, col4 = st.columns(4)
sample_topic = None

if col1.button("🤖 AI in Healthcare", use_container_width=True):
    sample_topic = "The impact of generative AI in modern healthcare diagnostics"
if col2.button("🔋 Solid-State Batteries", use_container_width=True):
    sample_topic = "Latest breakthroughs and commercialization timeline of solid-state batteries"
if col3.button("🧠 Quantum Computing", use_container_width=True):
    sample_topic = "Recent milestones in quantum computing and post-quantum cryptography"
if col4.button("💼 Future of Work", use_container_width=True):
    sample_topic = "The impact of artificial intelligence on the job market and workforce transition"

# Research Topic Input
default_topic = sample_topic if sample_topic else ""
topic_input = st.text_input(
    "Enter research topic or question:",
    value=default_topic,
    placeholder="e.g. Next-generation nuclear energy and small modular reactors (SMRs) in 2026",
)

start_research = st.button("🚀 Start Multi-Agent Research", type="primary", use_container_width=True)

# Pipeline Execution Logic
if start_research:
    active_or_key = st.session_state.openrouter_key.strip()
    active_tavily_key = st.session_state.tavily_key.strip()

    if not active_or_key:
        st.error("Please paste your **OpenRouter API Key** in the sidebar to proceed.", icon="🔑")
    elif not active_tavily_key:
        st.error("Please paste your **Tavily API Key** in the sidebar to proceed.", icon="🔍")
    elif not topic_input.strip():
        st.warning("Please enter a research topic.", icon="✍️")
    else:
        # Dynamically inject visitor keys into the runtime environment
        os.environ["OPENROUTER_API_KEY"] = active_or_key
        os.environ["TAVILY_API_KEY"] = active_tavily_key

        st.session_state.current_topic = topic_input.strip()
        progress_bar = st.progress(0, text="Initializing agents...")
        status_container = st.status("🚀 Multi-Agent Team Conducting Research...", expanded=True)

        def streamlit_callback(step: int, title: str, status: str, content: str = ""):
            step_progress = {1: 25, 2: 50, 3: 75, 4: 100}
            percent = step_progress.get(step, 0)
            
            if status == "running":
                status_container.write(f"🔄 **Step {step}: {title}** — *in progress...*")
                progress_bar.progress(max(percent - 15, 5), text=f"Step {step}/4: {title} is working...")
            elif status == "completed":
                status_container.write(f"✅ **Step {step}: {title}** — *completed!*")
                progress_bar.progress(percent, text=f"Step {step}/4: {title} completed.")

        try:
            with st.spinner("Agents are researching, scraping, and writing..."):
                results = run_research_pipeline(topic_input.strip(), step_callback=streamlit_callback)
                st.session_state.pipeline_results = results
                status_container.update(label="🎉 Research Pipeline Completed Successfully!", state="complete", expanded=False)
                progress_bar.progress(100, text="Research Completed!")
        except Exception as e:
            status_container.update(label="❌ Pipeline encountered an error", state="error", expanded=True)
            st.error(f"Execution Error: {str(e)}")

# Display Results Section
if st.session_state.pipeline_results:
    results = st.session_state.pipeline_results
    topic = st.session_state.current_topic

    st.divider()
    st.subheader(f"📊 Research Dossier: *{topic}*")

    report_text = results.get("report", "")
    feedback_text = results.get("feedback", "")
    scraped_text = results.get("scraped_content", "")
    search_text = results.get("search_results", "")

    # Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Report Word Count", f"{len(report_text.split()):,} words")
    m2.metric("Scraped Article Text", f"{len(scraped_text):,} chars")
    m3.metric("Search Snippets", f"{len(search_text):,} chars")
    m4.metric("Review Status", "Peer-Reviewed ✅")

    # Output Tabs
    tab_report, tab_critic, tab_scraped, tab_search = st.tabs([
        "📄 Synthesized Report",
        "🧐 Critic Review",
        "🌐 Scraped Web Content",
        "🔍 Search Results"
    ])

    with tab_report:
        st.download_button(
            label="📥 Download Report (.md)",
            data=report_text,
            file_name=f"research_report_{topic[:30].replace(' ', '_').lower()}.md",
            mime="text/markdown"
        )
        st.markdown("### Final Research Report")
        st.markdown(report_text)

    with tab_critic:
        st.markdown("### Critic Review & Analysis")
        st.info("The Critic Agent evaluated the report for structural coherence, clarity, tone, and depth.")
        st.markdown(feedback_text)

    with tab_scraped:
        st.markdown("### Deep Scraped Web Content")
        st.caption("Full content extracted from the primary URL selected by the Reader Agent:")
        st.text_area("Extracted Web Text", scraped_text, height=350)

    with tab_search:
        st.markdown("### Raw Tavily Search Findings")
        st.caption("Top search hits discovered by Search Agent:")
        st.text_area("Search Results", search_text, height=350)
