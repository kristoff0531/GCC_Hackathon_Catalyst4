from pathlib import Path
import re


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCUMENTS_DIR = PROJECT_ROOT / "documents"


def parse_front_matter(text: str) -> tuple[dict, str]:
    """
    Extract YAML-style front matter from the beginning of a document.

    Example:

    ---
    mnemonic: WTXN
    application_name: Wire Transfer Processing Engine
    issue_id: WTXN-4041
    ---

    Returns:
        metadata, document_content
    """

    if not text.startswith("---"):
        return {}, text.strip()

    parts = text.split("---", 2)

    if len(parts) != 3:
        return {}, text.strip()

    metadata_text = parts[1].strip()
    content = parts[2].strip()

    metadata = {}

    for line in metadata_text.splitlines():
        line = line.strip()

        if not line or ":" not in line:
            continue

        key, value = line.split(":", 1)

        metadata[key.strip()] = value.strip()

    return metadata, content


def load_documents():
    """
    Read all Markdown knowledge documents from:

        documents/<MNEMONIC>/*.md
    """

    documents = []

    for file_path in DOCUMENTS_DIR.rglob("*.md"):

        text = file_path.read_text(
            encoding="utf-8"
        )

        metadata, content = parse_front_matter(text)

        document = {
            "source": str(
                file_path.relative_to(PROJECT_ROOT)
            ),
            "metadata": metadata,
            "content": content,
        }

        documents.append(document)

    return documents

def chunk_document(document: dict) -> list[dict]:
    """
    Split a document into chunks while preserving metadata and source.
    """

    content = document["content"]

    # Split whenever a Markdown heading appears
    sections = re.split(r"(?=^#{1,3}\s)", content, flags=re.MULTILINE)

    chunks = []

    for section in sections:
        section = section.strip()

        if not section:
            continue

        # Ignore extremely small fragments
        if len(section) < 50:
            continue

        chunk = {
            "source": document["source"],
            "metadata": document["metadata"].copy(),
            "content": section,
        }

        chunks.append(chunk)

    return chunks

if __name__ == "__main__":

    documents = load_documents()

    print(f"Found {len(documents)} document(s)\n")

    all_chunks = []

    for document in documents:

        chunks = chunk_document(document)

        all_chunks.extend(chunks)

        print("=" * 60)
        print(f"Source: {document['source']}")
        print(f"Chunks created: {len(chunks)}")

        for index, chunk in enumerate(chunks, start=1):

            print(f"\n--- Chunk {index} ---")
            print(chunk["content"])

    print("\n" + "=" * 60)
    print(f"Total chunks: {len(all_chunks)}")