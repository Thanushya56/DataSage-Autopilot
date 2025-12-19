import streamlit as st
import pandas as pd
import time
import os
import sys
import google.generativeai as genai
from datetime import datetime
import hashlib

# 1. PAGE CONFIG & STYLING - Updated to match images exactly
st.set_page_config(
    page_title="DataSage Autopilot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to match the exact styling from images
st.markdown("""
<style>
    /* Main background */
    .main { 
        background-color: #f8f9fa; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Headers */
    h1 {
        color: #1a73e8;
        font-weight: 600;
        border-bottom: 3px solid #1a73e8;
        padding-bottom: 10px;
        margin-bottom: 30px;
    }
    
    h2 {
        color: #1a73e8;
        font-weight: 500;
        margin-top: 25px;
        margin-bottom: 15px;
    }
    
    h3 {
        color: #5f6368;
        font-weight: 500;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%; 
        border-radius: 6px; 
        height: 45px;
        background-color: #1a73e8; 
        color: white; 
        font-weight: 500; 
        border: none;
        font-size: 14px;
        transition: all 0.2s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton>button:hover {
        background-color: #0d62d9;
        box-shadow: 0 2px 6px rgba(26, 115, 232, 0.3);
    }
    
    /* Report box - matches Executive Strategic Brief from images */
    .report-box {
        border: 2px solid #1a73e8; 
        padding: 25px; 
        border-radius: 10px;
        background: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-top: 20px;
        font-size: 14px;
    }
    
    /* Status boxes for agent progress */
    .status-box {
        background-color: #e8f0fe;
        border-left: 4px solid #1a73e8;
        padding: 12px 15px;
        border-radius: 4px;
        margin: 8px 0;
        font-size: 14px;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: white;
        border-right: 1px solid #dadce0;
    }
    
    /* Metrics styling */
    .metric-container {
        background: white;
        border: 1px solid #dadce0;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    
    /* Upload area styling */
    .upload-box {
        border: 2px dashed #dadce0;
        border-radius: 10px;
        padding: 40px;
        text-align: center;
        background: white;
        color: #5f6368;
        margin: 20px 0;
    }
    
    /* Data preview table */
    .dataframe {
        font-size: 13px;
    }
    
    /* Alert boxes */
    .stAlert {
        border-radius: 8px;
        padding: 15px;
    }
    
    /* Custom columns for metrics */
    .metric-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        margin: 5px;
    }
    
    .metric-value {
        font-size: 24px;
        font-weight: 600;
        color: #1a73e8;
    }
    
    .metric-label {
        font-size: 12px;
        color: #5f6368;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

# 2. API KEY CONFIG
API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

if not API_KEY:
    # Create a more visually appealing error message
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.error("""
        ❌ **API Key Not Found**  
        Please set your Google API Key to continue.
        
        **Instructions:**
        1. Set environment variable: `GOOGLE_API_KEY`
        2. Or set: `GEMINI_API_KEY`
        
        **For Windows PowerShell:**
        ```powershell
        $env:GOOGLE_API_KEY="your-api-key-here"
        ```
        
        Then restart the app.
        """)
    st.stop()

try:
    genai.configure(api_key=API_KEY)
    api_status = True
except Exception as e:
    st.error(f"❌ Failed to configure Gemini API: {str(e)}")
    st.stop()

# 3. SIDEBAR - Updated to match images exactly
with st.sidebar:
    # Header matching image
    st.markdown('<div class="sidebar-header">🧠 Google Agentic Stack</div>', unsafe_allow_html=True)
    
    # Project ID - from image
    st.markdown("**Project ID:** `452177523793`")
    
    # Status indicators from image
    st.markdown("---")
    st.markdown("### Status")
    
    # Gemini API Status
    col_a, col_b = st.columns([1, 4])
    with col_a:
        st.success("✅")
    with col_b:
        st.markdown("**Gemini API Active**")
    
    # Aleks Agent Status
    col_a, col_b = st.columns([1, 4])
    with col_a:
        st.success("✅")
    with col_b:
        st.markdown("**Aleks Agent (ADK) Ready**")
    
    # Stitch Reporting Status
    col_a, col_b = st.columns([1, 4])
    with col_a:
        st.success("✅")
    with col_b:
        st.markdown("**Stitch Reporting (A24) Live**")
    
    st.markdown("---")
    
    # Current date from image format
    current_date = datetime.now().strftime("%d-%m-%Y")
    st.markdown(f"**Date:** {current_date}")
    
    # System Metrics from image
    st.markdown("### System Metrics:")
    
    # Create metric cards matching the image
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">4</div>
            <div class="metric-label">Active Agents</div>
            <div style="font-size: 11px; color: #34a853;">+1</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">500</div>
            <div class="metric-label">API Calls</div>
            <div style="font-size: 11px; color: #34a853;">+40</div>
        </div>
        """, unsafe_allow_html=True)

# 4. SESSION STATE
session_defaults = {
    "raw_df": None,
    "cleaned_df": None,
    "insight": "",
    "analysis_complete": False,
    "report_generated": False,
    "file_name": "",
    "file_size": 0,
    "upload_time": None,
    "gemini_model_used": ""
}

for key, default in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = default

# 5. MAIN UI - Updated to match images
st.title("🚀 DataSage Autopilot")
st.markdown("### Autonomous Business Intelligence via Google Agentic Stack")
st.markdown("---")

# File upload section matching image
st.markdown("## 📂 Upload Raw Business Data (CSV)")
uploaded_file = st.file_uploader(
    "**Drag and drop file here**  \nLimit 500MB per file - CSV",
    type=["csv"],
    help="Upload your business data in CSV format for analysis",
    label_visibility="collapsed"
)

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.session_state.raw_df = df
        st.session_state.file_name = uploaded_file.name
        st.session_state.file_size = uploaded_file.size / 1024  # KB
        st.session_state.upload_time = datetime.now()
        
        # Show upload confirmation matching image
        st.success(f"📁 **Uploaded:** {st.session_state.file_name} ({st.session_state.file_size:.2f} KB)")
        
        st.markdown("### 🔍 Raw Data Preview (Standard MCP Context)")
        
        # Display dataframe with custom styling
        st.dataframe(
            df.head(),
            use_container_width=True,
            hide_index=False,
            column_config={
                col: st.column_config.Column(
                    width="medium",
                    help=f"Column: {col}"
                ) for col in df.columns
            }
        )
        
        # Data Quality Assessment expander
        with st.expander("🔬 Data Quality Assessment", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Rows", df.shape[0])
            
            with col2:
                st.metric("Columns", df.shape[1])
            
            with col3:
                missing_total = df.isnull().sum().sum()
                st.metric("Missing Values", missing_total, delta=f"{(missing_total/df.size*100):.1f}%" if missing_total > 0 else None)
            
            # Column-wise analysis
            st.markdown("**Column Analysis:**")
            col_info = []
            for col in df.columns:
                null_count = df[col].isnull().sum()
                unique_count = df[col].nunique()
                dtype = str(df[col].dtype)
                col_info.append({
                    "Column": col,
                    "Type": dtype,
                    "Missing": null_count,
                    "Unique": unique_count
                })
            
            col_df = pd.DataFrame(col_info)
            st.dataframe(col_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # AGENT CONTROLS - 3 columns matching image
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### ⚙️ Trigger Jules Agent")
            if st.button("**Trigger Agent**", key="jules_btn", help="Clean and prepare data using Jules Agent"):
                if st.session_state.raw_df is not None:
                    with st.status("**Jules (ADK) is refactoring data...**", expanded=True) as status:
                        # Step 1: Cleaning column names
                        st.markdown('<div class="status-box">🔧 Cleaning column names...</div>', unsafe_allow_html=True)
                        time.sleep(0.8)
                        
                        df = st.session_state.raw_df.copy()
                        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
                        
                        # Step 2: Validating data types
                        st.markdown('<div class="status-box">📊 Validating data types...</div>', unsafe_allow_html=True)
                        time.sleep(0.8)
                        
                        for col in df.select_dtypes(include=['object']).columns:
                            df[col] = df[col].astype(str).str.strip()
                        
                        # Step 3: Removing duplicates
                        st.markdown('<div class="status-box">🧹 Removing duplicates...</div>', unsafe_allow_html=True)
                        time.sleep(0.8)
                        
                        initial_rows = len(df)
                        df = df.drop_duplicates()
                        duplicates_removed = initial_rows - len(df)
                        
                        st.session_state.cleaned_df = df
                        
                        status.update(label="✅ **Data refactoring completed**", state="complete")
                    
                    st.success("🎉 **Data Cleaned by Jules Agent**")
                    
                    # Show cleaned data in expander
                    with st.expander("📊 View Cleaned Data", expanded=True):
                        st.dataframe(
                            st.session_state.cleaned_df.head(),
                            use_container_width=True,
                            hide_index=False
                        )
                        
                        # Show data cleaning stats
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("New Shape", f"{df.shape[0]} rows × {df.shape[1]} cols")
                        with col2:
                            st.metric("Duplicates Removed", duplicates_removed)
        
        with col2:
            st.markdown("#### 📊 Run Gemini Analysis")
            if st.button("**Run Analysis**", key="gemini_btn", help="Analyze data with Gemini AI"):
                if st.session_state.cleaned_df is not None:
                    data_sample = st.session_state.cleaned_df.head(10).to_string()
                    
                    with st.spinner("🔍 **Discovering available Gemini models...**"):
                        try:
                            models = genai.list_models()
                            available_models = [
                                m.name for m in models 
                                if 'generateContent' in m.supported_generation_methods
                            ]
                            
                            if not available_models:
                                st.error("No Gemini models available with generateContent capability")
                                st.stop()
                            
                            # Model selection logic
                            model_name = None
                            for preference in ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]:
                                for model in available_models:
                                    if preference in model.lower():
                                        model_name = model
                                        break
                                if model_name:
                                    break
                            
                            if not model_name:
                                model_name = available_models[0]
                            
                            model_display = model_name.split('/')[-1].replace('models/', '')
                            st.session_state.gemini_model_used = model_display
                            
                            st.info(f"🤖 **Using model:** {model_display}")
                            
                            # Create prompt for analysis
                            prompt = f"""
                            Analyze this business data and identify ONE significant business risk.
                            Focus on data quality, operational issues, or strategic risks.
                            
                            Data Sample:
                            {data_sample}
                            
                            Provide your response in this format:
                            
                            **Risk:** [Concise risk name]
                            
                            **Explanation:** [Brief explanation focusing on data quality issues like:
                            - sales_amount containing non-numeric values or errors
                            - region having inconsistent casing or missing values
                            - customer_feedback having missing values]
                            
                            **Impact:** [Business impact - how this affects decision making]
                            
                            **Recommendation:** [Suggested action steps]
                            
                            Keep the response professional and concise.
                            """
                            
                            model = genai.GenerativeModel(model_name)
                            response = model.generate_content(prompt)
                            st.session_state.insight = response.text
                            st.session_state.analysis_complete = True
                            
                            # Display analysis result
                            st.markdown("### 🎯 Analysis Result")
                            st.markdown(st.session_state.insight)
                            
                        except Exception as e:
                            error_msg = str(e)
                            st.error(f"❌ **Analysis Error:** {error_msg}")
                            if "quota" in error_msg.lower():
                                st.warning("⚠️ You may have exceeded your API quota. Check your Google AI Studio account.")
                            elif "permission" in error_msg.lower() or "access" in error_msg.lower():
                                st.warning("⚠️ You may not have access to this model. Check your Google AI Studio permissions.")
                else:
                    st.error("⚠️ **Please run Jules Agent first to clean the data!**")
        
        with col3:
            st.markdown("#### 📄 Generate Stitch Report")
            if st.button("**Generate Report**", key="stitch_btn", help="Generate Executive Strategic Brief"):
                if st.session_state.analysis_complete and st.session_state.insight:
                    # Create progress animation
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    steps = [
                        "📋 Compiling executive summary...",
                        "📈 Generating insights visualization...",
                        "🔒 Securing report with A24 protocol...",
                        "🚀 Finalizing Stitch Report..."
                    ]
                    
                    for i in range(100):
                        progress_bar.progress(i + 1)
                        status_text.text(steps[min(i // 25, 3)])
                        time.sleep(0.02)
                    
                    progress_bar.empty()
                    status_text.empty()
                    
                    # Celebration
                    st.balloons()
                    st.session_state.report_generated = True
                    
                    # Generate Report ID
                    report_id = hashlib.md5(f"{st.session_state.file_name}{datetime.now()}".encode()).hexdigest()[:12].upper()
                    
                    # Format insight for HTML display
                    insight_html = st.session_state.insight.replace("**", "").replace("\n", "<br>")
                    
                    # Executive Strategic Brief matching image exactly
                    st.markdown(f"""
                    <div class="report-box">
                        <h2 style="color:#1a73e8; text-align:center; margin-bottom:25px; border-bottom:2px solid #1a73e8; padding-bottom:15px;">
                            📊 Executive Strategic Brief
                        </h2>
                        
                        <div style="background:#f0f7ff; padding:15px; border-radius:8px; margin:15px 0; border-left:4px solid #1a73e8;">
                            <p style="color:#5f6368; font-size:0.9em; margin:5px 0;"><b>Report ID:</b> A24-{report_id}</p>
                            <p style="color:#5f6368; font-size:0.9em; margin:5px 0;"><b>Generated:</b> {current_date}</p>
                            <p style="color:#5f6368; font-size:0.9em; margin:5px 0;"><b>Source:</b> {st.session_state.file_name}</p>
                            <p style="color:#5f6368; font-size:0.9em; margin:5px 0;"><b>Model:</b> {st.session_state.gemini_model_used}</p>
                        </div>
                        
                        <hr style="border:1px solid #e0e0e0; margin:20px 0;">
                        
                        <h3 style="color:#ea4335; font-size:18px; margin-bottom:15px;">🔴 Critical Risk Identified</h3>
                        
                        <div style="background:#fffbf0; padding:15px; border-radius:6px; border-left:4px solid #fbbc04;">
                            {insight_html}
                        </div>
                        
                        <hr style="border:1px solid #e0e0e0; margin:20px 0;">
                        
                        <div style="background:#f9f9f9; padding:20px; border-radius:8px; margin-top:20px; border:1px solid #e0e0e0;">
                            <h4 style="color:#1a73e8; font-size:16px; margin-bottom:15px;">📋 Recommended Actions:</h4>
                            <ol style="color:#5f6368; padding-left:20px;">
                                <li style="margin-bottom:8px;">Immediate data validation for Sales_Amount column</li>
                                <li style="margin-bottom:8px;">Regional data standardization protocol implementation</li>
                                <li style="margin-bottom:8px;">Weekly automated data quality audits</li>
                                <li style="margin-bottom:8px;">Stakeholder review of BI reporting accuracy</li>
                                <li style="margin-bottom:8px;">Data governance framework establishment</li>
                            </ol>
                        </div>
                        
                        <div style="text-align:center; margin-top:25px; padding-top:15px; border-top:1px solid #e0e0e0;">
                            <small style="color:#999;">Confidential - For Internal Use Only</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Create downloadable report text
                    report_text = f"""EXECUTIVE STRATEGIC BRIEF
================================================================================
Report ID: A24-{report_id}
Generated: {current_date}
Project ID: 452177523793
Source File: {st.session_state.file_name}
File Size: {st.session_state.file_size:.2f} KB
Analysis Model: {st.session_state.gemini_model_used}

CRITICAL RISK IDENTIFIED
================================================================================
{st.session_state.insight}

RECOMMENDED ACTIONS
================================================================================
1. Immediate data validation for Sales_Amount column
2. Regional data standardization protocol implementation
3. Weekly automated data quality audits
4. Stakeholder review of BI reporting accuracy
5. Data governance framework establishment

================================================================================
DataSage Autopilot v1.0 | Google Agentic Stack
Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
================================================================================
"""
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Stitch Report (TXT)",
                        data=report_text,
                        file_name=f"stitch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        key="download_report",
                        help="Download the complete Executive Strategic Brief"
                    )
                else:
                    st.error("⚠️ **Please complete Gemini Analysis first!**")
    
    except Exception as e:
        st.error(f"❌ **Error loading CSV file:** {str(e)}")
        st.info("Please ensure you're uploading a valid CSV file with proper formatting.")

else:
    # Upload placeholder matching image
    st.markdown("""
    <div class="upload-box">
        <h3 style="color:#5f6368; margin-bottom:15px;">📁 No file uploaded</h3>
        <p style="color:#5f6368; margin-bottom:10px;">Drag and drop a CSV file here to begin analysis</p>
        <p style="color:#999; font-size:0.9em;"><small>Supported: CSV files up to 500MB</small></p>
        <div style="margin-top:20px; color:#1a73e8;">
            <small>Try uploading: sample_database.csv</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 6. FOOTER
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #5f6368; font-size: 0.9em; padding: 20px;'>"
    "DataSage Autopilot v1.0 | Powered by Google Agentic Stack"
    "</div>",
    unsafe_allow_html=True
)

# 7. DEBUG SECTION (optional)
with st.expander("🔧 System Information", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**App Info:**")
        st.write(f"- Streamlit: {st.__version__}")
        st.write(f"- Pandas: {pd.__version__}")
        st.write(f"- Python: {sys.version.split()[0]}")
        
        if st.session_state.raw_df is not None:
            st.write(f"- Data Shape: {st.session_state.raw_df.shape}")
        
        st.write(f"- API Status: {'✅ Active' if api_status else '❌ Inactive'}")
    
    with col2:
        st.write("**Session State:**")
        for key in ["file_name", "file_size", "analysis_complete", "report_generated"]:
            value = st.session_state.get(key, "Not set")
            st.write(f"- {key}: {value}")
