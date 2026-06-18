from neighborhood_builder import build_neighborhood
from fetch import get_market_questions_from_db
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="./market_vector_store")

collection = client.get_or_create_collection(name="prediction_markets")

def store_market_data(market_data):
    """Generates embeddings and saves them to disk."""
    
    documents = [item['market_question'] for item in market_data]
    ids = [str(item.get('id', i)) for i, item in enumerate(market_data)]
    
    metadatas = [{"category": item.get("category", "unknown")} for item in market_data]
    
    embeddings = model.encode(documents).tolist()
    
    collection.upsert(
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print(f"Successfully stored {len(documents)} questions into the vector database.\n")


def search_markets(query_text, n_results=3):
    """Searches the database for the closest semantic matches."""
    
    query_embedding = model.encode(query_text).tolist()
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    return results


def main():

    market_data = get_market_questions_from_db(CAP = 100)
    print(len(market_data))
    
    #store_market_data(market_data)

    search_query = "bitcoin is good"
    print(f"Searching for: '{search_query}'\n")
    
    results = search_markets(search_query, n_results=2)

    for i in range(len(results['documents'][0])):
        question = results['documents'][0][i]
        metadata = results['metadatas'][0][i]
        distance = results['distances'][0][i] # Lower distance = closer semantic match
        
        print(f"Match {i+1}: {question}")
        print(f"Category: {metadata['category']} | Distance: {distance}\n")
    


if __name__ == "__main__":
    main()
