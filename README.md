# DataDetox - AC215 Project

**Team Members**: Kushal Chauhan, Pavlos Mosho, Rohit Kundu, Ruisen Liu

**Group Name**: DataDetox

## Project Description

DataDetox is an AI-powered application designed to help users understand and analyze foundation models and their associated data. The system leverages Retrieval-Augmented Generation (RAG) to provide enriched information about foundation models by retrieving relevant details from comprehensive model documentation.

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

## Components

### 1. RAG System

The RAG (Retrieval-Augmented Generation) system serves as a **prompt refining tool** that retrieves information about foundation models and enriches user prompts. When a user mentions something about a foundation model, the RAG system:
- Retrieves relevant information from the foundation model documentation
- Enriches the user's prompt with detailed context about the model
- Provides comprehensive answers based on retrieved information

**Data Preservation Note**: We intentionally did not preprocess the `.md` files downloaded from Hugging Face in order to preserve all the details of the foundation model data. This ensures that the RAG system has access to complete and accurate information about each foundation model.

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

### 2. Data Pipeline

The data pipeline component handles:
- Loading data from various sources
- Data preprocessing and cleaning
- Preparing data for model training and RAG indexing

**Key Files**:
- `dataloader.py`: Handles data loading from multiple sources
- `preprocess.py`: Data preprocessing utilities
- `docker-shell.sh`: Script to run the data pipeline in Docker

### 3. Models

The models component includes:
- Model training scripts
- Inference pipelines
- Model evaluation utilities

**Key Files**:
- `train_model.py`: Training pipeline for models
- `infer_model.py`: Inference and prediction scripts
- `docker-shell.sh`: Script to run model training/inference in Docker

### 4. Notebooks

Exploratory Data Analysis (EDA) notebooks for:
- Understanding data distributions
- Visualizing data patterns
- Testing preprocessing approaches

## Setup and Installation

### Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Google Cloud Platform account (for deployment)

### Getting Started

1. Clone the repository:
```bash
git clone https://github.com/kushal-chat/AC215_datadetox.git
cd AC215_datadetox
```

2. Set up each component by navigating to its directory and following the respective README:
   - For RAG system: `cd rag` and see `rag/README.md`
   - For data pipeline: `cd src/datapipeline`
   - For models: `cd src/models`

3. Each component uses Docker for containerization. Use the provided `docker-shell.sh` scripts to build and run containers.

## Usage

### RAG System for Foundation Model Queries

The RAG system is designed to help users get detailed information about foundation models:

```bash
cd rag
./docker-shell.sh
python cli.py --query "Tell me about GPT-3 architecture"
```

The system will retrieve relevant information from the indexed Hugging Face documentation and provide enriched responses.

## Development

Each component is containerized using Docker for consistency across development and production environments. Use the provided `docker-shell.sh` scripts in each directory to:

- Build Docker images
- Run containers with appropriate volume mounts
- Execute component-specific commands

## Contributing

This is an academic project for Harvard AC215. For questions or contributions, please contact the team members.

## License

This project is developed for educational purposes as part of AC215 coursework.
