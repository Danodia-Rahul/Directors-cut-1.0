#!/bin/bash
set -e

echo "Waiting for Qdrant to start..."
until curl -s http://qdrant:6333/collections | grep -q 'collections'; do
    sleep 10
done
echo "Qdrant is up!"

cd /app

conda run -n project python -m ingestion.ingest || true

exec conda run -n project streamlit run ui/app.py --server.port=8501 --server.address=0.0.0.0
