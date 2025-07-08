from pinecone import Pinecone
from huggingface_hub import InferenceClient
import os

# Set up Pinecone instance using the new API
api_key = os.getenv("PINECONE_TOKEN")
pc = Pinecone(api_key=api_key)

# Check if the index exists; if not, create it
index_name = "movie-base"
index = pc.Index(index_name)
# model = SentenceTransformer('all-MiniLM-L6-v2')
# tokenizer = model.tokenizer  # This is the tokenizer used by the model
model = None        #Lazy loading to save build time
tokenizer = None

def getMoviesByDescText(desc_text, top_k=10):
    """
    Retrieve movie IDs based on a description text using Pinecone.

    Args:
        desc_text (str): The description text to search for.
        top_k (int): The number of top results to return.

    Returns:
        list: A list of movie IDs that match the description text.
    """
    client = InferenceClient(provider="hf-inference", api_key=os.getenv("HF_TOKEN"))
    vector = client.feature_extraction(model="sentence-transformers/all-MiniLM-L6-v2", text=desc_text).tolist() #Needs numpy to perform .toList()
    query_response = index.query(vector=[vector], top_k=top_k, include_metadata=True)
    movie_ids = [int(match['id']) for match in query_response['matches']]
    print(movie_ids)
    
    return movie_ids