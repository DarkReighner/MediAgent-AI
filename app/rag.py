import chromadb

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="policies"
)

def add_policy(text):

    collection.add(
        documents=[text],
        ids=["policy1"]
    )

def search_policy(query):

    results = collection.query(
        query_texts=[query],
        n_results=1
    )

    return results["documents"][0][0]