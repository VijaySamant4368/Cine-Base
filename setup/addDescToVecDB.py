from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
import sqlite3

DB_PATH = "movies.db"
DB_PATH = "../" +DB_PATH

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

TOKENIZER_MAX_LENGTH = 384  # Max length for the tokenizer
api_key = "pcsk_5Z2G43_TGqbvtrGoeEMLCnRJCwK1eLMtih1Arb2bM9coQCEXWjbD33aPDdkYwYmC9ibq6Y"
pc = Pinecone(api_key=api_key)

index_name = "movie-base"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=TOKENIZER_MAX_LENGTH,  # (384 for 'all-MiniLM-L6-v2')
        metric="cosine",  # 'euclidean'
        spec=ServerlessSpec(cloud='aws', region='us-east-1') 
    )

index = pc.Index(index_name)
model = SentenceTransformer('all-MiniLM-L6-v2')

def upload_descriptions( cursor:sqlite3.Cursor):
    """
    The function retrieves movie data from the SQLite database, encodes the descriptions using a pre-trained model, and uploads the vectors to Pinecone.

    Args:
        cursor (sqlite3.Cursor): SQLite cursor object to execute SQL queries.
    """

    movie_data = cursor.execute("SELECT * FROM titles").fetchall()
    n = len(movie_data)

    for movie in movie_data:
        movie_id = movie[0]
        movie_title = movie[1]
        movie_description = movie[2]

        vector = model.encode(movie_description).tolist()
        metadata = {"title": movie_title, "description": movie_description}
        index.upsert(
            vectors=[(str(movie_id), vector, metadata)]
        )
        print(f"Uploaded movie {movie_id}/{n} to Pinecone")

if __name__ == "__main__":
    print(upload_descriptions(cursor))