"""Tools for the AI Tax Filing Assistant."""

from typing import Dict, Any, List
import json
# We will populate this dynamically or via an environment variable / replacement
CORPUS_NAME = "projects/606861713769/locations/us-central1/ragCorpora/4385336156686909440"

def retrieve_tax_rules(query: str) -> str:
    """Search the official tax rules corpus and return matched passages.

    Call this tool whenever you need to cite a tax section, rule, deduction, or form.
    Do NOT invent tax rules. Always ground your tax advice in the passages returned by this tool.

    Args:
        query: What to look up (e.g., 'HRA exemption rules', 'Section 80C limits', 'Form 16').
    Returns:
        The matched passages from the official tax documents, or a note that none was found.
    """
    from vertexai.preview import rag
    import vertexai
    
    # RAG Engine Serverless is us-central1 only
    vertexai.init(project="qwiklabs-gcp-02-06f72f9742c5", location="us-central1")
    
    try:
        resp = rag.retrieval_query(
            text=query,
            rag_resources=[rag.RagResource(rag_corpus=CORPUS_NAME)],
            rag_retrieval_config=rag.RagRetrievalConfig(top_k=3),
        )
    except Exception as e:
        return f"Retrieval failed: {e}"
        
    contexts = getattr(resp.contexts, "contexts", [])
    passages = [c.text.strip() for c in contexts if getattr(c, "text", "").strip()]
    return "\n\n---\n\n".join(passages) or "No relevant passage found."


def extract_document_data(document_name: str) -> str:
    """Extract and structure data from an uploaded Form 16, Form 12BB, or other tax document.
    
    In a real app, this would use Document AI to parse the uploaded file.
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
