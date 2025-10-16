# DataDetox - AC215 Project

**Team Members**: Kushal Chattopadhyay, Terry Zhou, Keyu Wang

**Group Name**: DataDetox

## Project Description

DataDetox is an AI-powered application designed to help users understand model lineages and their associated data. The current system leverages Retrieval-Augmented Generation (RAG) to provide enriched information about foundation models by retrieving relevant details from comprehensive model documentation from HuggingFace.

## Project Wireframe (Missing from Milestone 1)
Screenshots of landing and chatbot pages are added to previous submitted MS1 pdf, see `report/AC215_MileStone_1.pdf`.

## Project Organization

```
├── README.md
├── data                    # Data storage (not uploaded to GitHub)
├── notebooks
│   └── eda.ipynb          # Exploratory Data Analysis
├── rag                     # RAG system for foundation model information
│   ├── Dockerfile
│   ├── Pipfile
│   ├── Pipfile.lock
│   ├── README.md
│   ├── cli.py
│   ├── docker-shell.sh
│   └── rag_pipeline.py
├── references              # Reference materials
├── reports                 # Project reports and documentation
│   └── Statement of Work.pdf
└── src                     # Source code
    ├── datapipeline       # Data pipeline components
    │   ├── Dockerfile
    │   ├── Pipfile
    │   ├── Pipfile.lock
    │   ├── dataloader.py
    │   ├── docker-shell.sh
    │   └── preprocess.py
    └── models             # Model training and inference
        ├── Dockerfile
        ├── docker-shell.sh
        ├── infer_model.py
        └── train_model.py
```

## Milestone 2 Components

### 1. Data Source

Our data source for RAG comes from the HuggingFace Transformers library. https://github.com/huggingface/transformers/tree/main/src/transformers/models


### 2. RAG System

The RAG (Retrieval-Augmented Generation) system serves as a **prompt refining tool** that retrieves information about foundation models and enriches user prompts. When a user mentions something about a foundation model, the RAG system:
- Retrieves relevant information from the foundation model documentation
- Enriches the user's prompt with detailed context about the model

**Data Preservation Note**: We intentionally did not preprocess the `.md` files downloaded from HuggingFace in order to preserve all the details of the foundation model data. This ensures that the RAG system has access to complete and accurate information about each foundation model.

#### Running the RAG System

To run the RAG system, navigate to the `rag` directory and use the following commands:

```bash
# Build and run the Docker container
./docker-shell.sh

# Index documents (first time setup)
python cli.py --index

# Query the RAG system
python cli.py --query "What are the details about BERT model?"
```

For more detailed instructions, see [rag/README.md](rag/README.md).


### Getting Started

1. Clone the repository:
```bash
git clone https://github.com/kushal-chat/AC215_datadetox.git
cd AC215_datadetox
```
2. Build the docker images:

```bash
docker compose up -d rag_cli
```

3. Navigating to a directory and following the respective README for each component:
   - For RAG system: `cd rag` and see `rag/README.md`

## Usage

### RAG System for Foundation Model Queries

The RAG system acts as a prompt enrichment tool when welll-known foundation models are mentioned in uer query:

```bash
cd rag
./docker-shell.sh
python cli.py --query "Tell me about GPT-3 architecture"
```

The system will retrieve relevant information from the indexed Hugging Face documentation and provide enriched responses.


## License

This project is developed for educational purposes as part of AC215 coursework.
