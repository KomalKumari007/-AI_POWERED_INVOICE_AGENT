
import streamlit as st
import os
import agent
from database import initialize_database, get_db_connection
from agent import run_audit_agent

#st.write("Target Agent File Path:", agent.__file__)

# Initialize standard multi-column wide UI display state
st.set_page_config(page_title="AI Invoice Audit Platform", layout="wide")

# Trigger relational system tables boot automation sequence
initialize_database()

st.title("🛡️ AI Corporate Invoice Audit Platform")
st.caption("Enterprise Agentic RAG core engine designed for automated vendor compliance testing.")

# Split interface into a pristine 50/50 dashboard grid layout
col1, col2 = st.columns(2)

with col1:
    st.header("Audit Workstation")
    uploaded_file = st.file_uploader("Upload incoming vendor invoice file", type=["pdf"])
    
    user_query = st.text_input(
        "Ask a specific question about this invoice (Optional)", 
        placeholder="e.g., Are there any hidden service fees or incorrect tax rates listed?"
    )
    
    # ─── UPDATE THIS BLOCK BELOW ───
    if st.button("Execute Agent Analysis Loop", type="primary"):
        # 1. Guardrail Check: If no file is uploaded, stop immediately and warn the user
        if uploaded_file is None:
            st.warning("⚠️ Operational Error: You must upload a valid PDF invoice before executing the agent loop.")
        
        # 2. Safe Execution Path: Only runs if a file actually exists
        else:
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
                
            with st.spinner("Gemini core mapping invoice attributes against SQLite ledger constraints..."):
                try:
                    # Run our agent loop
                    result = run_audit_agent(temp_path, uploaded_file.name, custom_query=user_query)
                    
                    # Store output properties cleanly into the local database
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO audit_logs (filename, vendor_name, total_amount, status, audit_reason) VALUES (?, ?, ?, ?, ?)",
                        (uploaded_file.name, result["vendor"], result["amount"], result["status"], result["reason"])
                    )
                    conn.commit()
                    conn.close()
                    
                    # Visual feedback execution
                    st.success("Automated evaluation sequence finalized.")
                    if result["status"] == "Approved":
                        st.markdown(f"### Audit Ruling: **🟢 COMPLIANT / APPROVED**")
                    else:
                        st.markdown(f"### Audit Ruling: **🔴 NON-COMPLIANT / FLAGGED**")
                        
                    st.markdown("#### Auditor Report & Reason Tree Log:")
                    st.write(result["reason"])
                    
                except Exception as e:
                    st.error(f"Execution Exception encountered: {str(e)}")
                    
                finally:
                    # Cleanup staging data block cache safely
                    if os.path.exists(temp_path):
                        os.remove(temp_path)