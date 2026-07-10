import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from rag_engine import extract_text_from_pdf
from database import get_db_connection

# Load secure environment keys
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# Initialize official Google GenAI Client wrapper 
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def look_up_past_audit_logs(vendor_name: str) -> str:
    """
    AGENT TOOL: Allows Gemini to cross-reference historical logs inside our 
    SQLite database to catch double-billing attempts automatically.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT total_amount, status, processed_at FROM audit_logs WHERE vendor_name = ?", 
        (vendor_name,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return f"Database Query Result: No prior invoice logs found for vendor '{vendor_name}'."
    
    summary = f"Database Query Result: Found {len(rows)} past historical transactions for {vendor_name}:\n"
    for row in rows:
        summary += f"- Amount: ${row['total_amount']}, Status: {row['status']}, Date: {row['processed_at']}\n"
    return summary


def run_audit_agent(file_path: str, filename: str, **kwargs) -> dict:
    """
    The agent supervisor. Sends invoice text to Gemini, manages tools routing,
    and returns a normalized dict containing structured data fields.
    """
    # 1. Safely extract custom_query if app.py sent it, otherwise default to None
    custom_query = kwargs.get('custom_query', None)

    # Extract the invoice body characters
    invoice_text = extract_text_from_pdf(file_path)
    
    system_instruction = (
        "You are an elite AI Corporate Compliance Auditor.\n"
        "Your task is to analyze the text layout of the provided invoice against policy constraints.\n"
        "CRITICAL REQUIREMENT: You MUST look up historical logs for the vendor using the provided tool "
        "'look_up_past_audit_logs' before issuing a final status.\n\n"
        "CORPORATE COMPLIANCE CONSTRAINTS:\n"
        "1. Flag an invoice immediately if any line item representing single meals exceeds $50.\n"
        "2. Flag an invoice if the history tool reveals that an invoice with the identical total dollar amount "
        "has been logged previously for this same vendor (Double Billing Protection).\n\n"
        "Provide your clear findings and conclude with a definitive verdict of 'Approved' or 'Flagged'."
    )
    
    # Base user message
    user_message = f"Please evaluate newly received file context: {filename}\n\nInvoice Raw Content:\n{invoice_text}"
    
    # If a custom query is present, attach it
    if custom_query:
        user_message += f"\n\nUser Custom Question/Constraint: {custom_query}"
        
    # ... your remaining code goes here ...
    
    # Send execution context to the free tier model with tool configuration enabled
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[look_up_past_audit_logs],
            temperature=0.1
        )
    )
    
    analysis_text = response.text
    
    # Routing classification step based on structural keywords inside response text
    status = "Flagged" if "flag" in analysis_text.lower() or "violation" in analysis_text.lower() else "Approved"
    
    # Fallback keyword extraction strategy for our database record filing fields
    extracted_vendor = "Unclassified Vendor"
    if "vendor" in analysis_text.lower():
        extracted_vendor = "Identified Vendor"
        
    return {
        "status": status,
        "reason": analysis_text,
        "vendor": extracted_vendor,
        "amount": 0.0
    }