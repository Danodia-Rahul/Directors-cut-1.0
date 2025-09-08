FROM continuumio/miniconda3:main

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY environment.yaml .
RUN conda env create -f environment.yaml

COPY data /app/data
COPY ingestion /app/ingestion
COPY retrieval /app/retrieval
COPY ui /app/ui

COPY setup.sh /app/
RUN chmod +x /app/setup.sh

ENTRYPOINT [ "/app/setup.sh" ]

