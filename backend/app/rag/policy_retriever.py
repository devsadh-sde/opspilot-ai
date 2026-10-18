
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_DIR = BASE_DIR / "data" / "chroma_db"

COLLECTION_NAME = "northstar_policies"


def retrieve_policies(query: str, top_k: int = 3) -> list[dict]:
    if not query.strip():
        raise ValueError("Query cannot be empty")

    if top_k <= 0:
        raise ValueError("top_k must be positive")

    # Step 1: Load the same embedding model used during ingestion.
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Step 2: Convert the question into an embedding.
    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    # Step 3: Connect to our existing ChromaDB collection.
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_collection(name=COLLECTION_NAME)

    # Step 4: Search for relevant policy sections.
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"]
    )

    # Step 5: Return structured retrieval results.
    return [
        {
            "document": document,
            "metadata": metadata,
            "distance": distance
        }
        for document, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        )
    ]
