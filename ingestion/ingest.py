import json
import collections
import pandas as pd
from typing import List

from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding, SparseTextEmbedding

with open('data/data.json', 'rt') as f_in:
    documents = json.load(f_in)


client = QdrantClient("http://localhost:6333")

def collection_exists(collection_name: str) -> bool:

    try:
        existing_collections = [col.name for col in client.get_collections().collections]
        return collection_name in existing_collections

    except:
        return False
    
def build_collection(name: str, vector_config: dict = None, sparse_vector_config: dict = None):

    try:
        vector_config = vector_config or {}
        sparse_vector_config = sparse_vector_config or {}

        exists = collection_exists(name)

        if exists:
            print(f"Collection '{name}' already exists.")
            return

        client.create_collection(
            collection_name = name,
            vectors_config = vector_config,
            sparse_vectors_config = sparse_vector_config
        )

        print(f"✅ Qdrant collection '{name}' created.")

    except Exception as e:
        print(f"Failed to create collection '{name}': {e}")

def populate_collection(name: str, models_names: dict, documents: List[dict]):

    try:
        exists = collection_exists(name)

        if not exists:
            print(f"Collection '{name}' does not exists.")
            return

        points = []

        for record in documents:

            text_embed = f"{record['term']}: {record['definition']} {record['extra']}"

            dict_vector = {}

            for vector_name, model_name in models_names.items():
                dict_vector[vector_name] = models.Document(
                    text = text_embed,
                    model = model_name
                )

            point = models.PointStruct(
                id = record['id'],
                vector = dict_vector,
                payload = {
                    'term': record['term'],
                    'description': f"{record['definition']} {record['extra']}",
                    'models_used': models_names
                }
            )

            points.append(point)

        client.upsert(
            collection_name = name,
            points=points
        )

        print(f"✅ Successfully populated collection '{name}' with {len(points)} records.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':

    build_collection(
    name = 'hybrid-search-collection',
    vector_config = {
        'dense_text': models.VectorParams(
            size = 512,
            distance = models.Distance.COSINE
        )
    },
    sparse_vector_config = {
        'sparse_text': models.SparseVectorParams(
            modifier = models.Modifier.IDF
        )
    }
    )
    
    populate_collection(
        name='hybrid-search-collection',
        models_names={
            'dense_text': 'jinaai/jina-embeddings-v2-small-en',
            'sparse_text': 'Qdrant/bm25'
        },
        documents=documents
    )