# Directors-cut-1.0
Essential film making techniques, from shots to editing, all in one place.

### Problem Description

<p>🎬 Filmmaking has tons of terms for shots, camera moves, editing, and lighting—but info is scattered everywhere!</p>

<p>✨ <strong>Directors-Cut-1.0</strong> brings it all together in one place. With type, term, definition, and extra, it’s easy to explore and learn filmmaking concepts without hunting through multiple sources. 📚</p>

<h2>📁 Project Structure</h2>
<pre>
Directors-cut-1.0/
├── data/
│     ├── data.json
│     ├── generate_ids.py
│     └── raw_data.json
├── evaluation/
│     ├── ground_truth.ipynb
│     ├── ground_truth.csv
│     ├── LLM_as_judge.ipynb
│     └── retrieval_evaluation.ipynb
├── retrieval/
│     ├── __init__.py
│     ├── response.py
│     └── search.py
├── ingestion/
│     ├── __init__.py
│     └── ingest.py
├── ui/
│     └── app.py
├── .gitignore
├── Dockerfile
├── environment.yml
└── README.md
</pre>


### Data

The dataset used in this project was collected through **web scraping** from multiple online sources, including articles from *StudioBinder*, *MetFilm School*, and *Art Department*.  

Since each source followed a different structure and formatting style, a single generic scraper could not be applied. Instead, custom scraping routines were written for each site to extract the relevant information.  

> **Note:** The scraping code itself is not included in this repository. The primary reason is that the scripts were highly tailored to the unique HTML structures of the individual websites, and therefore are not reusable in a general form. Moreover, the focus of this project is on the analysis and application of the curated dataset, not on the scraping process itself.  

All data used here is strictly for **academic and research purposes**, and care was taken to respect the **terms of service** and copyright of the original websites.
                                        
### 🚀 Getting Started

This guide provides two options for setting up and running this project.

-----

### Clone git repository

```bash
git clone https://github.com/user/project1.git
cd project1
```
----

### 💻 Option A: Local Setup with Conda

This is the recommended setup as the project was developed using **Conda**.

1.  **Install Miniconda** from this link: [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)

2.  **Create and activate the environment:**

    ```bash
    conda env create -f environment.yml
    conda activate project
    ```

3. **create Qdrant knowledge base:**
    ```bash
    python -m ingestion.ingest
    ```

4.  **Run the Streamlit app:**

    ```bash
    streamlit run ui/app.py
    ```

-----

### 🐳 Option B: Containerized Setup with Docker

You can also use **Docker** for a self-contained environment.

1.  **Build the Docker image:**

    ```bash
    docker build -t project .
    ```

2.  **Run the app in Docker:**

    ```bash
    docker run -p 8501:8501 project
    ```

3.  **Access the app** by navigating to:

    ```
    http://localhost:8501
    ```
---
### Evaluation

#### Retrieval evaluation
---
For retrieval evaluation, we experimented with several approaches:

- **Keyword Search:** Simple matching based on keywords.  
- **Semantic Search:** Uses embeddings to find semantically similar items.  
- **Multi-Stage Search:** Combines keyword and semantic search in multiple stages.  
- **Re-Ranking Fusion (RRF) Search:** Combines multiple retrieval strategies and re-ranks the results.

| Method               | MRR     | Hit Rate |
|----------------------|--------|----------|
| Keyword Search       | 0.7162 | 0.8347   |
| Semantic Search      | 0.8449 | 0.9288   |
| Multi-Stage Search   | 0.8013 | 0.9397   |
| RRF Search           | 0.8638 | 0.9421   |

For our use case, we selected **RRF Search** as it achieved the highest recall (Hit Rate) and precision (MRR).

#### RAG Evaluation
----

For the retrieval-augmented generation (RAG) evaluation, we used a large language model (LLM) as the judge. Specifically, we tested the generated responses from two models: **Gemini 2.5 Flash Lite** and **Gemini 2.0 Flash Lite**.  

Due to daily rate limits, we evaluated a subset of **1,000 queries** from the [ground_truth.csv](./Evaluation/ground_truth.csv) dataset. This allowed us to assess the performance of both models while staying within the API constraints.

