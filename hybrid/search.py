import ingestion.ingest
from ingestion.ingest import models

def rrf_search(question: str, collection_name: str, limit: int = 5):

    if not ingestion.ingest.collection_exists(collection_name):
        print(f"Collection '{collection_name}' does not exist.")
        return

    collection = ingestion.ingest.client.get_collection(collection_name)
    vector_config = collection.config.params.vectors
    sparse_vector_config = collection.config.params.sparse_vectors

    if len(vector_config) + len(sparse_vector_config) < 2:
        print("Both dense and sparse vectors are required for RRF search.")
        return

    sample_point = ingestion.ingest.client.scroll(collection_name=collection_name, limit=1)[0][0]
    used_models = sample_point.payload.get("models_used", {})

    dense = {}
    sparse = {}

    for vector_name, model_name in used_models.items():
        if vector_name in vector_config:
            dense = {"name": vector_name, "model": model_name}
        elif vector_name in sparse_vector_config:
            sparse = {"name": vector_name, "model": model_name}

    if not dense or not sparse:
        print("Dense and sparse vector fields not found in the collection.")
        return

    results = ingestion.ingest.client.query_points(
        collection_name=collection_name,
        query=models.FusionQuery(fusion=models.Fusion.RRF),
        prefetch=[
            models.Prefetch(
                query=models.Document(
                    text=question,
                    model=dense["model"]
                ),
                using=dense["name"],
                limit=2 * limit
            ),
            models.Prefetch(
                query=models.Document(
                    text=question,
                    model=sparse["model"]
                ),
                using=sparse["name"],
                limit=2 * limit
            )
        ],
        limit=limit,
        with_payload=True
    )

    context = {'question': question}

    for i, res in enumerate(results.points):
        context[f'context{i+1}'] = res.payload['description']

    return context