"""Tools for the AI Tax Filing Assistant."""

from typing import Dict, Any, List
import json
import os

def retrieve_tax_rules(query: str) -> str:
    """Search the official tax rules knowledge base and return relevant passages.

    Call this tool whenever you need to cite a tax section, rule, deduction, or form.
    Do NOT invent tax rules. Always ground your tax advice in the passages returned by this tool.

    Args:
        query: What to look up (e.g., 'HRA exemption rules', 'Section 80C limits', 'Form 16').
    Returns:
        The matched passages from the official tax documents, or a note that none was found.
    """
    # Fallback local search over the text file to avoid GCP costs
    # In a real app with large data, use an in-memory vector DB like Chroma or FAISS.
    # Here, we just return the full contents of the knowledge base to the model, 
    # since it easily fits in Gemini's context window.
    
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'tax_rules.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return f"Official Tax Rules Context:\n\n{content}\n\nSearch Query Context: Focus your answer on elements related to '{query}'."
    except Exception as e:
        return f"Retrieval failed: {e}"


def extract_document_data(document_name: str) -> str:
    """Extract and structure data from an uploaded Form 16, Form 12BB, or other tax document.
    
    In a real app, this would use an OCR/Extraction service.
    For this prototype, it returns mock data based on the document name.
    
    Args:
        document_name: The name or type of document uploaded (e.g., 'Form 16', 'Rent Receipts').
    Returns:
        A JSON string containing the extracted data.
    """
    doc_name_lower = document_name.lower()
    
    if "form 16" in doc_name_lower:
        return json.dumps({
            "document_type": "Form 16",
            "extracted_data": {
                "Gross Salary": 1240000,
                "HRA Received": 240000,
                "Basic Salary": 600000,
                "TDS Deducted": 85000,
                "80C Investments Declared": 0, # They haven't declared 80C to employer
                "Employer NPS Contribution": 0
            }
        }, indent=2)
        
    if "rent" in doc_name_lower:
        return json.dumps({
            "document_type": "Rent Receipts",
            "extracted_data": {
                "Monthly Rent Paid": 18000,
                "Total Rent Paid": 216000,
                "Landlord PAN": "Provided"
            }
        }, indent=2)
        
    return json.dumps({"error": f"No mock data available for {document_name}. Ask the user for the details directly."})
