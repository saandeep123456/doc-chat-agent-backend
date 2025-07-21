import hashlib, chromadb, os
from pathlib import Path
from fastapi import UploadFile
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, ServiceContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import Settings
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core.embeddings import BaseEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "storage" / "uploads"
CHROMA_DIR = BASE_DIR / "storage" / "chromadb"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

client = chromadb.PersistentClient(path=CHROMA_DIR)

os.environ['OPENAI_API_KEY'] = ''
# Choose embeddings
USE_OPENAI = True  # Change to True to use OpenAI embeddings
if USE_OPENAI:
    embed_model = OpenAIEmbedding(model="text-embedding-ada-002")
else:
    embed_model = HuggingFaceEmbedding(model_name="hkunlp/instructor-large")

def get_vector_index(user_id: str) -> VectorStoreIndex:
    collection_name = f"documents_{user_id}"
    chroma_collection=client.get_or_create_collection(collection_name)
    vector_store = ChromaVectorStore(chroma_client=client, chroma_collection=chroma_collection,collection_name=collection_name)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    Settings.embed_model = embed_model
    return VectorStoreIndex([], storage_context=storage_context)

def compute_file_hash(file_path: Path) -> str:
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

async def process_document(file: UploadFile, user_id: str) -> None:
    """
    Upload, hash, parse, and index a document for a user.
    Skips re-indexing if file is already present.
    """
    file_path = UPLOAD_DIR / f"{user_id}_{file.filename}"
    with open(file_path, "wb") as f_out:
        f_out.write(await file.read())

    file_hash = compute_file_hash(file_path)

    collection = client.get_or_create_collection(f"documents_{user_id}")
    if collection.count() > 0:
        existing = collection.get(where={"hash": file_hash})
        if existing and existing.get("ids"):
            print(f"[SKIP] File '{file.filename}' already indexed for user '{user_id}'.")
            return

    reader = SimpleDirectoryReader(input_files=[str(file_path)])
    docs = reader.load_data()

    # Flatten docs if necessary
    if isinstance(docs[0], list):
        docs = [doc for sublist in docs for doc in sublist]

    for doc in docs:
        doc.metadata["hash"] = file_hash

    index = get_vector_index(user_id)
    parser = SimpleNodeParser()
    nodes = parser.get_nodes_from_documents(docs)
    index.insert_nodes(nodes)

    print(f"[INDEXED] {len(docs)} chunks from '{file.filename}' for user '{user_id}'.")
