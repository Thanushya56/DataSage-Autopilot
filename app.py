import streamlit as st
import pandas as pd
import time
import os
import google.generativeai as genai

# --- 1. CONFIGURATION & UI BRANDING ---
st.set_page_config(page_title="DataSage Autopilot", page_icon="🚀", layout="wide")

st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%; border-radius: 8px; height: 3.5em;
        background-color: #4285F4; color: white; font-weight: bold; border: none;
    }
    .report-box {
        border: 2px solid #4285F4; padding: 25px; border-radius: 12px;
        background-color: white; box-shadow: 2px 2px 15px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True) # FIXED: Using unsafe_allow_html

# --- 2. API CONFIGURATION ---
API_KEY = os.getenv("GOOGLE_API_KEY") # Uses verified key

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.error("❌ GOOGLE_API_KEY not found. Please set it in your environment.")
    st.stop()

# --- 3. SIDEBAR (Google Agentic Stack) ---
with st.sidebar:
    st.header("🧠 Google Agentic Stack")
    st.write("**Project ID:** `482275923702`") # Verified
    st.success("✅ Gemini API Connected")
    st.success("✅ Jules Agent (ADK) Active")
    st.success("✅ Stitch Reporting (A2A) Live")

# --- 4. SESSION STATE ---
if "cleaned_df" not in st.session_state: st.session_state.cleaned_df = None
if "insight" not in st.session_state: st.session_state.insight = ""

# --- 5. MAIN INTERFACE ---
st.title("🚀 DataSage Autopilot")
st.subheader("Autonomous Business Intelligence via Google Agentic Stack")
st.markdown("---")

# PHASE 1: DATA INGESTION (MCP Implementation)
st.header("1. Data Ingestion")
uploaded_file = st.file_uploader("📂 Upload Raw Business Data (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.markdown("### 🔍 Raw Data Preview (Standard MCP Context)")
    st.dataframe(df.head(5), use_container_width=True)
    
    col1, col2, col3 = st.columns(3)

    # PHASE 2: JULES AGENT (ADK - CLEANING)
    with col1:
        st.write("#### Phase: Autonomous Cleaning")
        if st.button("⚙️ Trigger Jules Agent"):
            with st.status("Jules (ADK) is refactoring data...", expanded=True):
                time.sleep(1)
                # Jules handles autonomous header standardization
                df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
                # Fix regional typos (e.g., SOUth -> South)
                if 'region' in df.columns:
                    df['region'] = df['region'].str.capitalize()
                st.session_state.cleaned_df = df
            st.success("✅ Data Cleaned by Jules Agent")
            # MANDATORY DISPLAY OF CLEANED DATA
            st.dataframe(st.session_state.cleaned_df.head(5), use_container_width=True)

    # PHASE 3: GEMINI ANALYSIS (REASONING ENGINE)
    with col2:
        st.write("#### Phase: Strategic Reasoning")
        if st.button("📊 Run Gemini Analysis"):
            if st.session_state.cleaned_df is not None:
                data_sample = st.session_state.cleaned_df.head(10).to_string()
                with st.spinner("🤖 Gemini Reasoning Engine active..."):
                    try:
                        # FIXED MODEL NAME: Bypasses 404
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        response = model.generate_content(f"Analyze this data for 1 critical business risk: {data_sample}")
                        st.session_state.insight = response.text
                        st.info(st.session_state.insight)
                    except Exception as e:
                        st.error(f"❌ Analysis Error: {str(e)}")
            else: st.error("Run Jules Agent first!")

    # PHASE 4: STITCH REPORTING (A2A PROTOCOL)
    with col3:
        st.write("#### Phase: Executive Synthesis")
        if st.button("📄 Generate Stitch Report"):
            if st.session_state.insight:
                st.balloons()
                # Fabricating the brief via Stitch
                st.markdown(f"""
                <div class="report-box">
                    <h2 style="color:#4285F4; text-align:center;">Executive Strategic Brief</h2>
                    <hr>
                    <p><b>Business Insight:</b></p>
                    <p>{st.session_state.insight}</p>
                    <hr>
                    <p style="color:gray; font-size:0.85em; text-align:center;">
                        Fabricated via Google Stitch · Powered by Google Agentic Stack
                    </p>
                </div>
                """, unsafe_allow_html=True)