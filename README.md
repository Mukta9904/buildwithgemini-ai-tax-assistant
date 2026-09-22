# AI Tax Filing Assistant

An agentic AI assistant built with Google Agent Development Kit (ADK) that helps Indian salaried employees analyze their tax position, identify deductions, and generate filing guidance. It grounds its advice using official Indian tax rules via Vertex AI RAG Engine.

## How it works
1. **Document Parsing**: Upload your Form 16 or rent receipts. The agent parses it (using mock extraction in this prototype).
2. **Knowledge Retrieval**: It queries a Vertex AI Serverless RAG corpus containing Indian tax rules (Section 10(13A), Section 80C, etc.) to fetch the exact legal context.
3. **Filing Checklist**: The agent tracks missing information (like rent receipts if HRA is claimed) and provides a dynamic checklist of what's completed and what's pending.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) installed.
- [agents-cli](https://adk.dev/) installed (`uv tool install google-agents-cli`).
- Google Cloud Project with Billing enabled (Required for Vertex AI Vector Search).
- Enable APIs:
  ```bash
  gcloud services enable aiplatform.googleapis.com vectorsearch.googleapis.com
  ```

## Setup & Installation

1. **Install dependencies**:
   ```bash
   agents-cli install
   ```

2. **Authenticate with Google Cloud**:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Populate the RAG Knowledge Base**:
   This project uses a serverless RAG Engine corpus to ground the tax rules.
   - Ensure you have a Google Cloud Storage bucket with your tax documents (like the sample `data/tax_rules.txt`).
   - Edit `scripts/create_rag_corpus.py` to point to your GCP project and GCS bucket URL.
   - Run the script to ingest the tax data:
     ```bash
     uv run python scripts/create_rag_corpus.py
     ```
   - *Note: Serverless RAG mode currently operates in `us-central1`.*
   - Copy the generated `corpus_name` output (e.g. `projects/.../ragCorpora/...`) and paste it into the `CORPUS_NAME` variable inside `app/tools.py`.

## Running the Agent

You can interact with the agent directly from the terminal or using a local web playground.

**Terminal**:
```bash
agents-cli run "I uploaded my Form 16, can you check it?"
```

**Web Playground**:
```bash
agents-cli playground
```
This opens a local chat UI in your browser where you can have a continuous conversation with the Tax Assistant.

## Project Structure
- `app/agent.py`: Contains the system instructions, checklist rules, and agent orchestration.
- `app/tools.py`: Contains the `extract_document_data` (mock parsing) and `retrieve_tax_rules` (RAG search) functions.
- `scripts/create_rag_corpus.py`: Script to initialize and populate the Vertex AI RAG database.
- `data/tax_rules.txt`: Sample tax rules ingested into the knowledge base.
