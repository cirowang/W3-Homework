import os
import chromadb
import sys
import re
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
print("Loading models...")
# 1. Initialize Models
embed_model = SentenceTransformer('all-MiniLM-L6-v2')
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
llm_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

client = chromadb.PersistentClient(path="./market_vector_store")
collection = client.get_or_create_collection(name="prediction_markets")

# --- ADDED: Auto-generate sample data if missing ---
def ensure_sample_data(file_path):
    if not os.path.exists(file_path):
        print(f"Creating sample '{file_path}' since it was not found...")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("Bitcoin is currently trading high, and prediction markets show a 40% chance for Bitcoin to reach 100k this year based on recent ETF approvals.\n")
            f.write("Ethereum prediction markets suggest it might hit 5k by the end of Q3.\n")
            f.write("Polymarket odds show a 20% chance of Solana flipping Ethereum in market cap.\n")

# 2. Document Loading & Chunking
def load_and_chunk_txt(file_path, max_words_per_chunk=100):
    """Reads the TXT file and segments text into manageable chunks."""
    documents = []
    metadatas = []
    ids = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f):
            text = line.strip()
            if not text:
                continue
            
            words = text.split()
            chunks = []
            if len(words) <= max_words_per_chunk:
                chunks.append(text)
            else:
                for i in range(0, len(words), max_words_per_chunk):
                    chunks.append(" ".join(words[i:i+max_words_per_chunk]))
            
            for chunk_idx, chunk in enumerate(chunks):
                documents.append(chunk)
                metadatas.append({
                    "source": file_path,
                    "line_number": line_num + 1,
                    "chunk_index": chunk_idx
                })
                ids.append(f"doc_{line_num}_chunk_{chunk_idx}")
                
    return documents, metadatas, ids

# 3. Embedding Generation & Indexing
def index_documents(documents, metadatas, ids):
    """Generates embeddings and saves them to the vector database."""
    if not documents:
        print("No documents to index.")
        return
        
    print(f"Generating embeddings for {len(documents)} chunks...")
    embeddings = embed_model.encode(documents).tolist()
    
    print("Upserting to ChromaDB...")
    collection.upsert(
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print(f"Successfully indexed {len(documents)} chunks into the vector store.\n")

# 4. Retrieval of Relevant Snippets
def retrieve_relevant_snippets(query_text, n_results=3):
    """Searches the database for the closest semantic matches."""
    query_embedding = embed_model.encode(query_text).tolist()
    
    # Check if database has enough documents to fulfill n_results
    count = collection.count()
    if count < n_results:
        n_results = count
        
    if n_results == 0:
        return None
        
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results

# 5. Answer Generation & Source Traceability
def generate_answer_and_trace(query, retrieved_results):
    """Prints sources and generates an answer using the retrieved context."""
    documents = retrieved_results['documents'][0]
    metadatas = retrieved_results['metadatas'][0]
    distances = retrieved_results['distances'][0]
    
    print("\n--- Source Traceability ---")
    context_parts = []
    for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances)):
        print(f"Source {i+1}: \"{doc}\"")
        print(f"  Metadata: {meta} | Distance: {dist:.4f} (Lower is better)\n")
        context_parts.append(doc)
        
    context = " | ".join(context_parts)

    # Compose a deterministic, retrieval-backed answer that cites sources
    print("--- Composing retrieval-backed answer (RAG) ---")

    composed_lines = [f"Based on {len(context_parts)} retrieved market snippets for the question: {query}"]
    numbers_found = []
    for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances)):
        src = meta.get('source', 'unknown')
        line = meta.get('line_number', '?')
        composed_lines.append(f"Source {i+1} ({src}#L{line}, distance={dist:.4f}): {doc}")

        # extract simple numeric mentions (percent, $ amounts)
        numbers = re.findall(r"\d+[\d,.]*%?|\$\d+[\d,]*", doc)
        if numbers:
            numbers_found.extend(numbers)

    if numbers_found:
        composed_lines.append("Observed explicit numeric mentions in sources: " + ", ".join(numbers_found))
        composed_lines.append("Conclusion: The retrieved markets include explicit numeric indications; answer should be formed from these sources and cited above.")
    else:
        composed_lines.append("No explicit odds or percentages were found in the retrieved snippets. These are market questions or headlines; consult the original market pages for odds.")

    # Final short recommendation phrasing
    composed_lines.append("Answer (retrieval-backed): See the cited sources above; they are the basis for any probabilistic estimate.")

    answer = "\n".join(composed_lines)
    return answer

# Main Execution
def main():
    txt_file = "market_data.txt"
    ensure_sample_data(txt_file)
    
    print(f"Loading data from {txt_file}...")
    docs, metas, ids = load_and_chunk_txt(txt_file)
    
    index_documents(docs, metas, ids)
    
    # Allow passing a custom query as the first command-line argument
    if len(sys.argv) > 1:
        search_query = sys.argv[1]
    else:
        search_query = "What do prediction markets say about Bitcoin reaching $100,000 by December 31, 2026?"
    print(f"Searching for: '{search_query}'")
    
    results = retrieve_relevant_snippets(search_query, n_results=3)
    
    if results and results['documents'] and results['documents'][0]:
        final_answer = generate_answer_and_trace(search_query, results)
        print(f"\n🤖 FINAL ANSWER:\n{final_answer}")
        # append results to results.txt for record
        try:
            with open('results.txt', 'a', encoding='utf-8') as rf:
                rf.write('\n--- RAG RUN ---\n')
                rf.write(f"Query: {search_query}\n\n")
                rf.write(final_answer + "\n")
        except Exception as e:
            print(f"Failed to append to results.txt: {e}")
    else:
        print("No relevant markets found in the database.")

if __name__ == "__main__":
    main()