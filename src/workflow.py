import chromadb
from sentence_transformers import SentenceTransformer
from transformers import pipeline

print("Loading models...")
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

llm_pipeline = pipeline("text2text-generation", model="google/flan-t5-base")

client = chromadb.PersistentClient(path="./market_vector_store")
collection = client.get_or_create_collection(name="prediction_markets")

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
            
            # Chunking logic: Since each line is a question, we primarily chunk by line.
            # However, if a line is exceptionally long, we split it by word count.
            words = text.split()
            chunks = []
            if len(words) <= max_words_per_chunk:
                chunks.append(text)
            else:
                # Split long lines into smaller chunks
                for i in range(0, len(words), max_words_per_chunk):
                    chunks.append(" ".join(words[i:i+max_words_per_chunk]))
            
            for chunk_idx, chunk in enumerate(chunks):
                documents.append(chunk)
                # Metadata helps with traceability later
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
    
    # --- Source Traceability ---
    print("\n--- Source Traceability ---")
    context_parts = []
    for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances)):
        print(f"Source {i+1}: \"{doc}\"")
        print(f"  Metadata: {meta} | Distance: {dist:.4f} (Lower is better)\n")
        context_parts.append(doc)
        
    # Combine retrieved snippets into a single context string
    context = " | ".join(context_parts)
    
    # --- Answer Generation ---
    print("--- Generating Answer ---")
    
    # Format prompt for the LLM
    prompt = (
        f"Answer the question based strictly on the provided prediction market contexts. "
        f"If the context doesn't contain the answer, say 'I don't know based on the available markets.'\n\n"
        f"Context: {context}\n"
        f"Question: {query}\n"
        f"Answer:"
    )
    
    # Generate response using the local LLM
    response = llm_pipeline(prompt, max_length=200, do_sample=False)
    
    # Clean up the output
    answer = response[0]['generated_text'].replace("Answer:", "").strip()
    
    return answer

# Main Execution
def main():
    txt_file = "market_data.txt"
    
    # Step A: Load and Chunk
    print(f"Loading data from {txt_file}...")
    docs, metas, ids = load_and_chunk_txt(txt_file)
    
    # Step B: Index
    # (In a production app, you'd check if the file has changed before re-indexing)
    index_documents(docs, metas, ids)
    
    # Step C: Search & Retrieve
    search_query = "Will Bitcoin reach 100k this year?"
    print(f"Searching for: '{search_query}'")
    
    results = retrieve_relevant_snippets(search_query, n_results=3)
    
    # Step D: Trace & Generate
    if results and results['documents'][0]:
        final_answer = generate_answer_and_trace(search_query, results)
        print(f"\n🤖 FINAL ANSWER: {final_answer}")
    else:
        print("No relevant markets found in the database.")

if __name__ == "__main__":
    main()