import os
import json
import logging
from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

INDEX_DIR = "indexdir"
DATA_FILE = "cdp_docs.json"


def create_index():
    """
    Create or rebuild the Whoosh index from `cdp_docs.json` data.
    """
    if not os.path.exists(DATA_FILE):
        logging.error(f"Missing data file: {DATA_FILE}")
        return

    # Load JSON data
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    # Prepare index directory
    if not os.path.exists(INDEX_DIR):
        os.mkdir(INDEX_DIR)

    # Define schema
    schema = Schema(
        platform=TEXT(stored=True),
        url=TEXT(stored=True),
        content=TEXT(stored=True)  # Combined question + answer
    )

    # Create index
    ix = create_in(INDEX_DIR, schema)
    writer = ix.writer()

    for entry in data:
        platform = entry["platform"]
        url = entry["url"]
        for faq in entry["content"]:
            question = faq.get("question", "").strip()
            answer = faq.get("answer", "").strip()
            full_content = f"{question} {answer}".lower()

            writer.add_document(platform=platform, url=url, content=full_content)

    writer.commit()
    logging.info("Index successfully created.")


def search_index(platform, search_query):
    """
    Searches the index for matching documents based on platform and query.
    """
    if not os.path.exists(INDEX_DIR) or not exists_in(INDEX_DIR):
        logging.warning("Index directory missing. Creating index...")
        create_index()

    try:
        ix = open_dir(INDEX_DIR)
        with ix.searcher() as searcher:
            query_parser = QueryParser("content", schema=ix.schema)
            parsed_query = query_parser.parse(search_query.lower())
            results = searcher.search(parsed_query, limit=5)

            filtered_results = [
                dict(result) for result in results if result.get("platform") == platform
            ]

            logging.info(f"Search results for '{search_query}' on {platform}: {filtered_results}")
            return filtered_results

    except Exception as e:
        logging.error(f"Error during search: {e}")
        return []
