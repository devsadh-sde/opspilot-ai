
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parents[2]
POLICY_FILE = BASE_DIR / "data" / "policies" / "fulfillment_policy.md"
CHROMA_DIR = BASE_DIR / "data" / "chroma_db"

COLLECTION_NAME = "northstar_policies"


def ingest_policies() -> int:
    # Step 1: Read the policy document.
    content = POLICY_FILE.read_text(encoding="utf-8")

    # Step 2: Split the document into sections.
    sections = [
        section.strip()
        for section in content.split("\n## ")
        if section.strip()
    ]

    # Step 3: Load the embedding model.
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Step 4: Generate embeddings for each section.
    embeddings = model.encode(
        sections,
        normalize_embeddings=True
    ).tolist()

    # Step 5: Open a persistent ChromaDB database.
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    # Step 6: Store document sections and embeddings.
    collection.upsert(
        ids=[f"policy-section-{i}" for i in range(len(sections))],
        documents=sections,
        embeddings=embeddings,
        metadatas=[
            {
                "source": POLICY_FILE.name,
                "section": i
            }
            for i in range(len(sections))
        ]
    )

    return len(sections)


if __name__ == "__main__":
    count = ingest_policies()
    print(f"Successfully indexed {count} policy sections.")
