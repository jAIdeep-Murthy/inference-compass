import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

from models import load_catalog
from recommender import get_recommendations
from utils import get_api_key, generate_api_snippet, run_live_inference

# Configure Streamlit page layout and title
st.set_page_config(
    page_title="Inference Compass",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling for badges and layout
st.markdown("""
<style>
.family-badge {
    background-color: #2E1065;
    color: #C4B5FD;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 600;
    display: inline-block;
    margin-bottom: 8px;
}
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
    margin: 2px;
    background-color: #7C3AED;
    color: white;
}
.tag-fast { background-color: #059669; color: white; }
.tag-medium { background-color: #D97706; color: white; }
.tag-slow { background-color: #DC2626; color: white; }
.tag-cheap { background-color: #0284C7; color: white; }
.tag-moderate { background-color: #7C3AED; color: white; }
.tag-expensive { background-color: #9D174D; color: white; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------------
st.title("🧭 Inference Compass")
st.subheader("Find your open-source model. Fast.")
st.caption("Powered by Featherless AI — 30,000+ models, serverless inference")
st.markdown("---")

# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("How it works")
    st.markdown("""
    * **Context length filtering**: Immediately prunes models that cannot support your required token window.
    * **Semantic matching**: Maps your use case keywords and task types against curated model strengths using an offline synonym graph.
    * **Priority boosting**: Heavily weights recommendations toward speed, cost-efficiency, or frontier reasoning quality based on your primary objective.
    """)
    st.markdown("---")
    st.markdown("[Featherless AI Docs](https://featherless.ai/docs)")
    st.markdown("[GitHub Repository](#)")

# Load catalog
try:
    catalog = load_catalog()
except Exception as e:
    st.error(f"Failed to load model catalog: {e}")
    catalog = []

# -----------------------------------------------------------------------------
# SECTION 1 — Describe your use case
# -----------------------------------------------------------------------------
st.header("1. Describe your use case")

col1, col2 = st.columns([2, 1])

with col1:
    use_case_text = st.text_area(
        "What are you building?",
        placeholder="e.g. a RAG chatbot for legal documents, a coding assistant, a multilingual summarizer",
        height=130
    )

with col2:
    priority_raw = st.selectbox(
        "What matters most?",
        options=["Speed", "Cost", "Quality"]
    )
    priority = priority_raw.lower()

    context_need_raw = st.selectbox(
        "How much context do you need?",
        options=["Short (<4k)", "Medium (4k–32k)", "Long (>32k)"]
    )
    if "Short" in context_need_raw:
        context_need = "short"
    elif "Medium" in context_need_raw:
        context_need = "medium"
    else:
        context_need = "long"

task_types = st.multiselect(
    "Task types",
    options=["chat", "coding", "rag", "reasoning", "summarization", "multilingual", "agents"],
    default=["chat"]
)

submit_button = st.button("Find My Model →", type="primary")

# -----------------------------------------------------------------------------
# SECTION 2 — Results
# -----------------------------------------------------------------------------
st.markdown("---")
st.header("2. Results")

if not submit_button and not use_case_text:
    st.info("💡 Describe your use case above or select options to get personalized model recommendations. Displaying featured defaults below:")
    recommendations = get_recommendations("general chat assistant", "speed", "short", ["chat"], catalog=catalog)
else:
    recommendations = get_recommendations(use_case_text, priority, context_need, task_types, catalog=catalog)

if not recommendations:
    st.warning("No models matched your criteria.")
else:
    # Normalize score for progress bar
    max_score = max([r.score for r in recommendations] + [10])
    
    cards = st.columns(3)
    for i, rec in enumerate(recommendations):
        with cards[i]:
            model = rec.model
            st.markdown(f"<div class='family-badge'>{model.family}</div>", unsafe_allow_html=True)
            st.markdown(f"### {model.name}")
            
            # Score bar
            norm_score = min(rec.score / float(max_score), 1.0)
            st.progress(norm_score, text=f"Match Score: {rec.score}")
            
            # Tags
            lat_chip = f"<span class='badge tag-{model.latency_tier}'>⚡ {model.latency_tier}</span>"
            cost_chip = f"<span class='badge tag-{model.cost_tier}'>💰 {model.cost_tier}</span>"
            size_chip = f"<span class='badge'>📦 {model.size}</span>"
            st.markdown(f"{lat_chip} {cost_chip} {size_chip}", unsafe_allow_html=True)
            
            # Reason
            st.markdown(f"*{rec.reason}*")
            
            # Expander for API snippet
            with st.expander("Copy API snippet"):
                snippet = generate_api_snippet(model.id)
                st.code(snippet, language="python")

# -----------------------------------------------------------------------------
# SECTION 3 — Try it live
# -----------------------------------------------------------------------------
st.markdown("---")
st.header("3. Try it live")

api_key = get_api_key()

if not api_key:
    st.info("⚠️ No API key configured — live testing disabled. Set `FEATHERLESS_API_KEY` in `.env` or Streamlit secrets to enable serverless inference.")
else:
    top_model_ids = [r.model.id for r in recommendations] if recommendations else [catalog[0].id]
    top_model_names = {r.model.id: r.model.name for r in recommendations} if recommendations else {catalog[0].id: catalog[0].name}
    
    selected_model_id = st.selectbox(
        "Select recommended model to test",
        options=top_model_ids,
        format_func=lambda x: top_model_names.get(x, x)
    )
    
    test_prompt = st.text_input("Enter test prompt", value="Hello! Who are you and what are your core strengths?")
    
    if st.button("Send →"):
        with st.spinner(f"Querying {selected_model_id} via Featherless AI..."):
            response_text, latency_ms = run_live_inference(selected_model_id, test_prompt, api_key)
        
        st.success(f"⚡ Inference completed in **{latency_ms:.1f} ms**")
        st.markdown("#### Model Output:")
        st.write(response_text)

# -----------------------------------------------------------------------------
# SECTION 4 — What I learned building this
# -----------------------------------------------------------------------------
st.markdown("---")
st.header("4. What I learned building this")

st.markdown("""
> **A Reflection on Open Source DX & Model Curation**
>
> Building Inference Compass forced me to confront a reality that every developer in AI faces today: **analysis paralysis**. When a platform like Featherless hosts over 30,000 open-source models, the paradox of choice becomes a massive bottleneck. Standard model catalogs provide dense benchmark tables, but builders don't want raw numbers—they want opinionated answers.
>
> **Why Opinionated Defaults Matter**  
> Developers building real-world applications usually balance three practical constraints: context depth, latency budget, and unit economics. By abstracting 30,000 models into 20 hand-curated archetypes categorized by practical tiers (`fast`/`cheap`, `reasoning-heavy`), we drastically reduce the friction from ideation to prototype.
>
> **The Serverless Inference Shift**  
> Integrating Featherless AI via an OpenAI-compatible API highlighted how commoditized model execution has become. Switching between a lightweight 7B model and a massive 405B frontier model is literally just changing a string in the SDK. Zero provisioning, zero cold starts, and seamless scaling.
>
> **Honest Limitations of v1**  
> While our keyword and synonym matching engine is incredibly fast and works 100% offline, static heuristics have limits. They don't account for nuanced prompt formatting sensitivity or multi-turn agentic reliability. In v2, pairing this static compass with an automated, real-time LLM evaluator would bridge the gap between static curation and dynamic performance.
""")
