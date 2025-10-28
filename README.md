# DataDetox - AC215 Project

**Team Members**: Kushal Chattopadhyay, Terry Zhou, Keyu Wang

**Group Name**: DataDetox

## Project Description

DataDetox is an AI-powered application designed to help users understand model lineages and their associated data. The current system leverages Retrieval-Augmented Generation (RAG) to provide enriched information about foundation models by retrieving relevant details from comprehensive model documentation from HuggingFace.

## Project Wireframe & Workflow (Missing from Milestone 1)
- Landing Page:

    ![](img/ms1/wireframe_1.png)
    ![](img/ms1/wireframe_2.png)
    ![](img/ms1/wireframe_3.png)

- Chatbot Page:

    ![](img/ms1/wireframe_4.png)

- Agentic Workflow (included in Milestone 1):
    ![](img/ms1/workflow.svg)

Screenshots of landing and chatbot pages also are added to previous submitted MS1 pdf, see Figure 3, 4, 5 in [report/AC215_MileStone_1.pdf](report/AC215_MileStone_1.pdf).

## Project Organization

```
├── README.md
├── docker-compose.yml
├── uv.lock
│
├── backend
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── README.md
│   ├── uv.lock
│   ├── ... # details omitted as it's not perfectly structured yet
│
├── frontend
│   ├── Dockerfile
│   ├── README.md
│   ├── ... # details omitted as it's not perfectly structured yet
│
├── data ⭐️   # downloaded data should be stored here
│
├── rag ⭐️
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── rag_cli.py
│   ├── README.md
│   ├── uv.lock
│   └── data/
│
├── mcp
│   ├── ... # details omitted as it's not perfectly structured yet
│
├── img
│   ├── ... # images used for README
│
└── report
    └── AC215_Milestone_1.pdf



```

## Getting Started

Clone the repository:
```bash
git clone https://github.com/kushal-chat/AC215_datadetox.git
cd AC215_datadetox
```

## Milestone 3 - Midterm Presentation
See [midterm_presentation/DataDetox_Milestone3.pdf](midterm_presentation/DataDetox_Milestone3.pdf).
