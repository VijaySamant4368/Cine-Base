from pinecone import Pinecone
from sentence_transformers import SentenceTransformer


# Set up Pinecone instance using the new API
api_key = "pcsk_5Z2G43_TGqbvtrGoeEMLCnRJCwK1eLMtih1Arb2bM9coQCEXWjbD33aPDdkYwYmC9ibq6Y"
pc = Pinecone(api_key=api_key)

# Check if the index exists; if not, create it
index_name = "movie-base"
index = pc.Index(index_name)
model = SentenceTransformer('all-MiniLM-L6-v2')
tokenizer = model.tokenizer  # This is the tokenizer used by the model

def getMoviesByDescText(desc_text, top_k=10):
    """
    Retrieve movie IDs based on a description text using Pinecone.

    Args:
        desc_text (str): The description text to search for.
        top_k (int): The number of top results to return.

    Returns:
        list: A list of movie IDs that match the description text.
    """
    vector = model.encode(desc_text).tolist()

    query_response = index.query(vector=[vector], top_k=top_k, include_metadata=True)

    movie_ids = [int(match['id']) for match in query_response['matches']]
    print(movie_ids)
    
    return movie_ids