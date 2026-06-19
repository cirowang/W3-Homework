import sqlite3
import spacy
import json

nlp = spacy.load("en_core_web_trf")
#nlp.add_pipe("merge_noun_chunks")

BASE_URL = "https://gamma-api.polymarket.com/markets"

BASE_EVENT_URL = "https://gamma-api.polymarket.com/events/"


def get_market_questions_from_db(CAP = None):
    conn = sqlite3.connect('polymarket_markets.db')
    cursor = conn.cursor()
    query = """
        SELECT 
            s.market_name AS market_question,
            s.days_left AS days_left,
            s.event_title AS event_title,
            s.tags AS tags,
            s.entities AS entities
        FROM runs r
        JOIN snapshots s ON s.run_id = r.id
        WHERE r.id = (SELECT MAX(id) FROM runs WHERE status = 'COMPLETED');
        """
    cursor.execute(query)
    rows = cursor.fetchall()
    market_data = []
    for row in rows:
        market_question, days_left, event_title, tags, entities = row
        market_data.append({
            "market_question": market_question,
            "days_left": days_left,
            "event_title": event_title,
            "tags": json.loads(tags) if tags else [],
            "entities": json.loads(entities) if entities else []  # parse JSON string to list
        })
    
    conn.close()
    if CAP is not None:
        market_data = market_data[:CAP]
    return market_data




def db_to_market_data(CAP=None):
    conn = sqlite3.connect('polymarket_markets.db')
    cursor = conn.cursor()
    query = """
        SELECT 
            s.market_name AS market_question,
            s.days_left AS days_left,
            s.event_title AS event_title,
            s.tags AS tags,
            s.entities AS entities
        FROM runs r
        JOIN snapshots s ON s.run_id = r.id
        WHERE r.id = (SELECT MAX(id) FROM runs WHERE status = 'COMPLETED');
        """
    cursor.execute(query)
    rows = cursor.fetchall()
    
    # Write market questions to file
    with open('market_data.txt', 'w', encoding='utf-8') as f:
        for i, row in enumerate(rows):
            if CAP is not None and i >= CAP:
                break
            market_question = row[0]
            f.write(f"{market_question}\n")
    
    conn.close()