# Directors-cut-1.0
Essential film making techniques, from shots to editing, all in one place.

### Problem Description

<p>🎬 Filmmaking has tons of terms for shots, camera moves, editing, and lighting—but info is scattered everywhere!</p>

<p>✨ <strong>Directors-Cut-1.0</strong> brings it all together in one place. With type, term, definition, and extra, it’s easy to explore and learn filmmaking concepts without hunting through multiple sources. 📚</p>

<h2>📁 Project Structure</h2>
<pre>
Directors-cut-1.0/
├── Data/
│   ├── data.json
│   ├── generate_ids.py
│   └── raw_data.json
├── Evaluation/
│   └── ground_truth.ipynb
│   └── ground_truth.csv
├── .gitignore
└── README.md
</pre>

├──, └──, │


### 🚀 Getting Started

This guide provides two options for setting up and running this project.

-----

### 💻 Option A: Local Setup with Conda

This is the recommended setup as the project was developed using **Conda**.

1.  **Install Miniconda** from this link: [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)

2.  **Create and activate the environment:**

    ```bash
    conda env create -f environment.yml
    conda activate project
    ```

3.  **Run the Streamlit app:**

    ```bash
    streamlit run app.py
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