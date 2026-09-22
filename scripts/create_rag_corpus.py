from vertexai.preview import rag
from vertexai.preview.rag.utils import resources as rr
import vertexai

PROJECT_ID = "qwiklabs-gcp-02-06f72f9742c5"
LOCATION   = "us-central1"
GCS_PATH   = "gs://qwiklabs-gcp-02-06f72f9742c5-rag-bucket/rag/"

PARSING_PROMPT = (
    "Extract the individual useful facts, tax rules, and definitions described in this text. "
    "Ignore and omit all metadata, boilerplate, and image captions. "
    "Output clean, self-contained prose focused on Indian tax laws, deductions, and forms."
)

vertexai.init(project=PROJECT_ID, location=LOCATION)

# 1. Switch the region's RAG managed DB to serverless mode (project-level, once).
cfg = f"projects/{PROJECT_ID}/locations/{LOCATION}/ragEngineConfig"
print(f"Setting RAG managed DB mode to serverless for {cfg}")
rag.update_rag_engine_config(rag_engine_config=rag.RagEngineConfig(
    name=cfg,
    rag_managed_db_config=rag.RagManagedDbConfig(mode=rr.Serverless()),
))

# 2. Create the corpus
print("Creating RAG corpus...")
corpus = rag.create_corpus(
    display_name="tax-rules-corpus",
    embedding_model_config=rag.EmbeddingModelConfig(
        publisher_model="publishers/google/models/text-embedding-005"),
)
print("corpus:", corpus.name)

# 3. Import + parse + chunk + embed.
print("Importing files from GCS...")
resp = rag.import_files(
    corpus_name=corpus.name,
    paths=[GCS_PATH],
    transformation_config=rag.TransformationConfig(
        chunking_config=rag.ChunkingConfig(chunk_size=512, chunk_overlap=100)),
    llm_parser=rag.LlmParserConfig(
        model_name="gemini-3.6-flash",
        custom_parsing_prompt=PARSING_PROMPT),
)
print("imported:", resp.imported_rag_files_count)
