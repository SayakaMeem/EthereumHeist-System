EthereumHeist AML System

A full-stack blockchain forensic system for tracing suspicious Ethereum fund movement from known heist or placement addresses. The system converts raw Ethereum transactions into explainable AML evidence using multi-hop tracking, service-provider matching, risk scoring, graph-ready output, and an interactive dashboard.

Overview

EthereumHeist AML System is designed to support blockchain-based anti-money laundering analysis. It starts from a suspicious Ethereum address, collects or loads transaction data, tracks outgoing fund-flow paths, identifies candidate layering addresses, checks known service-provider mappings, assigns risk scores, and presents the results through CSV/JSON files and a Next.js dashboard.

This project does not create a new blockchain. It analyzes existing Ethereum blockchain transaction records and converts them into a forensic investigation graph.

Key Features

Multi-hop Ethereum fund-flow tracking

One-hop TPP-style transaction tracing

Normal ETH, internal ETH, and ERC20 token transfer support

Etherscan API based missing-data crawling

Service-provider matching using a curated address map

AML risk scoring with interpretable reasons

Graph-ready node-edge output

Batch experiment mode for multiple heist addresses

CSV and JSON evidence generation

Interactive dashboard with cards, charts, graph view, and tables

FastAPI Swagger documentation for backend testing

System Architecture

flowchart LR
    A[User / Analyst] --> B[Next.js Frontend Dashboard]
    B -->|HTTP Request| C[FastAPI Backend]
    C --> D[Dataset Service]
    C --> E[Etherscan Crawling Service]
    C --> F[TPP Tracking Service]
    F --> G[Multi-Hop Tracking Service]
    G --> H[Service Provider Matching]
    H --> I[Risk Scoring Service]
    I --> J[Graph Service]
    J --> K[CSV / JSON Evidence]
    K --> B

Task Flow

flowchart TD
    A[Input suspicious Ethereum address] --> B[Check local transaction dataset]
    B --> C{Data available?}
    C -- Yes --> D[Load normal, internal, and ERC20 CSV files]
    C -- No --> E[Crawl missing data from Etherscan API]
    E --> D
    D --> F[Run one-hop TPP tracking]
    F --> G[Expand candidate layering addresses]
    G --> H[Run multi-hop tracking with depth and address limits]
    H --> I[Save multihop edge and layer files]
    I --> J[Match service-provider addresses]
    J --> K[Calculate AML risk score]
    K --> L[Build graph-ready node-edge output]
    L --> M[Show dashboard charts, tables, and summaries]

AML Investigation Flow

flowchart LR
    A[Placement: Known Heist Address] --> B[Layering: Intermediate Wallets]
    B --> C[Integration: Exchange / Mixer / Bridge / DEX]
    C --> D[Evidence: CSV, JSON, Graph, Dashboard]

Project Structure

EthereumHeist-System/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── routes/
│   │   └── services/
│   │       ├── dataset_service.py
│   │       ├── etherscan_service.py
│   │       ├── experiment_service.py
│   │       ├── full_pipeline_service.py
│   │       ├── graph_service.py
│   │       ├── incident_service.py
│   │       ├── multi_hop_tracking_service.py
│   │       ├── result_stats_service.py
│   │       ├── risk_scoring_service.py
│   │       ├── service_provider_matching_service.py
│   │       ├── tpp_tracking_service.py
│   │       ├── tracking_result_service.py
│   │       └── transaction_service.py
│   └── requirements.txt
│
├── data/
│   └── raw/
│       ├── EthereumHeist-main/
│       └── transactions/
│
├── frontend/
│   ├── app/
│   ├── public/
│   ├── package.json
│   ├── next.config.ts
│   └── tsconfig.json
│
└── results/
    ├── tracking/
    └── experiments/

Technology Stack

Layer

Tools / Libraries

Backend

Python, FastAPI, Uvicorn

Data Processing

Pandas, NumPy, PyArrow, DuckDB

Blockchain Data

Etherscan API

Graph Processing

NetworkX, igraph

Frontend

Next.js, React, TypeScript

UI / Visualization

Tailwind CSS, Recharts, Cytoscape, Lucide React

Output Format

CSV, JSON

API Testing

Swagger UI, Postman, Browser

Backend Services

File

Purpose

main.py

Main FastAPI application, middleware, and API endpoint definitions

config.py

Project path, data path, result path, and runtime directory configuration

dataset_service.py

Checks available raw, processed, and parquet dataset files

etherscan_service.py

Fetches normal ETH, internal ETH, and ERC20 transaction data from Etherscan

tpp_tracking_service.py

Runs one-hop TPP-style transaction tracking

multi_hop_tracking_service.py

Expands fund-flow tracking across multiple layers

service_provider_matching_service.py

Matches source/target addresses with known service-provider map

risk_scoring_service.py

Adds AML risk score, risk level, and risk reasons to tracked edges

graph_service.py

Converts tracking edge CSV into graph-ready nodes and edges

full_pipeline_service.py

Runs tracking, matching, risk scoring, and graph generation together

experiment_service.py

Runs batch experiments over multiple heist addresses

tracking_result_service.py

Lists, previews, and reads generated tracking result files

transaction_service.py

Lists and previews transaction files

incident_service.py

Reads heist labels, incident data, and service-provider maps

Important API Routes

Method

Endpoint

Description

GET

/

Backend home route

GET

/health

Checks backend health

GET

/api/health

API health check

GET

/dataset/status

Shows dataset availability

GET

/dataset/overview

Shows dataset overview

GET

/incidents

Reads heist incident records

GET

/heist-labels

Reads known heist address labels

GET

/service-providers

Reads known service-provider address map

GET

/crawl/address/{address}

Crawls normal, internal, and ERC20 transaction data from Etherscan

GET

/transactions/files

Lists transaction files

GET

/transactions/preview/{file_name}

Previews a transaction file

GET

/track/one-hop/{address}

Runs one-hop TPP tracking

GET

/track/multi-hop/{address}

Runs multi-hop TPP tracking

GET

/tracking/files

Lists generated tracking files

GET

/tracking/csv/{file_name}

Previews a tracking CSV file

GET

/tracking/summary/{file_name}

Reads a tracking summary JSON file

GET

/tracking/download/{file_name}

Downloads a tracking result file

GET

/tracking/enrich-service/{edges_file_name}

Adds service-provider matching to an edge file

GET

/tracking/stats/{edges_file_name}

Shows tracking statistics

GET

/graph/tracking/{file_name}

Builds graph-ready output

GET

/risk/edges/{file_name}

Adds AML risk scores to an edge file

GET

/pipeline/full/{address}

Runs the complete AML pipeline

GET

/experiment/run

Runs batch experiment on multiple heist addresses

GET

/experiment/files

Lists experiment result files

GET

/experiment/csv/{file_name}

Previews experiment CSV output

Installation and Setup

1. Clone the Repository

git clone https://github.com/SayakaMeem/EthereumHeist-System.git
cd EthereumHeist-System

2. Backend Setup

cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

For Windows local execution, the current backend services are designed around this project path:

D:\EthereumHeist_System

So the easiest setup is to keep the project at:

D:\EthereumHeist_System

or update the base directory/path configuration in the backend service files.

3. Configure Environment Variables

Create a .env file inside the backend/ folder:

ETHERSCAN_API_KEY=your_etherscan_api_key_here
ETHERSCAN_CHAIN_ID=1
APP_ENV=development
FRONTEND_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
ALLOWED_HOSTS=*

4. Run Backend Server

uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

Backend will run at:

http://127.0.0.1:8000

Swagger API documentation:

http://127.0.0.1:8000/docs

5. Frontend Setup

Open another terminal:

cd frontend
npm install
npm run dev

Frontend dashboard will run at:

http://localhost:3000

Quick Test Commands

Backend Health Check

http://127.0.0.1:8000/health

Dataset Status

http://127.0.0.1:8000/dataset/status

Run Multi-Hop Tracking

http://127.0.0.1:8000/track/multi-hop/0xeb31973e0febf3e3d7058234a5ebbae1ab4b8c23?max_depth=1&max_addresses_per_layer=1&beta=0.01&omega=1000&crawl_missing=false

Run Full AML Pipeline

http://127.0.0.1:8000/pipeline/full/0xeb31973e0febf3e3d7058234a5ebbae1ab4b8c23?max_depth=1&max_addresses_per_layer=1&beta=0.01&omega=1000&crawl_missing=false

Run Batch Experiment

http://127.0.0.1:8000/experiment/run?limit=3&max_depth=1&max_addresses_per_layer=1&beta=0.01&omega=1000&crawl_missing=false

How the Algorithm Works

One-Hop TPP Tracking

The one-hop tracker reads three transaction files for a selected address:

{address}_normal.csv

{address}_internal.csv

{address}_erc20.csv

It normalizes transaction values, filters small transactions using beta, and stores valid outgoing transfers as source-to-target edges.

Multi-Hop Tracking

The multi-hop tracker starts from the root heist address and expands candidate layering addresses layer by layer. It uses:

max_depth to control how many layers are tracked

max_addresses_per_layer to control how many addresses are expanded at each layer

beta to remove tiny/noisy transactions

omega to detect high-volume unknown-service behavior

crawl_missing to decide whether missing address files should be fetched from Etherscan

Service Matching

After edge generation, the service-provider matcher checks whether source or target addresses exist in the service-provider map. Matched addresses receive service name, category, source, and note. Unmatched addresses remain unresolved instead of being guessed.

Risk Scoring

Risk scoring adds a numeric score and level for every tracked edge. The score considers:

Large transfer amount

ERC20 or ETH transaction type

Candidate layering behavior

Stablecoin transfers

Zero/burn address interaction

Matched service provider

Mixer, exchange, bridge, or DEX category

Full Pipeline

The full pipeline runs the major stages in sequence:

Multi-hop tracking
→ Service-provider enrichment
→ Risk scoring
→ Graph generation
→ JSON response + CSV output

Output Files

Tracking Output

Generated inside:

results/tracking/

Common files:

{address}_multihop_edges.csv
{address}_multihop_layers.csv
{address}_multihop_summary.json
{address}_multihop_edges_service_enriched.csv
{address}_multihop_edges_service_enriched_risk_scored.csv

Experiment Output

Generated inside:

results/experiments/

Common files:

experiment_result.csv
experiment_result.json

Frontend Dashboard Modules

The dashboard supports:

Manual suspicious address input

Heist-label dropdown selection

Max depth selection

Max addresses per layer selection

Auto-crawl missing address option

Run Tracking button

Batch Experiment mode

Summary metric cards

Transaction type charts

Service-provider matching summary

Layering address table

Transaction edge table

Graph view

CSV export option

Example Use Case

An investigator enters a known heist address.

The frontend sends a request to the backend.

The backend loads local transaction files or crawls missing data.

The TPP tracker extracts suspicious outgoing transfers.

Multi-hop tracking expands candidate layering wallets.

Service matching checks known exchanges, mixers, bridges, or DEX addresses.

Risk scoring ranks the tracked edges.

The dashboard displays charts, tables, graph output, and downloadable evidence files.

Security Notes

Keep ETHERSCAN_API_KEY inside .env; do not commit it to GitHub.

Use HTTPS when deploying the backend online.

Restrict FRONTEND_ORIGINS in production.

Avoid ALLOWED_HOSTS=* in production.

Add authentication before exposing investigation endpoints publicly.

Store generated evidence files in encrypted storage for production use.

Add logging and audit trails for sensitive investigation activity.

Future Enhancements

Add user authentication and role-based access control

Deploy backend on cloud with HTTPS and protected secrets

Replace hardcoded local paths with full environment-based configuration

Add database storage for investigation history

Add advanced graph visualization with path highlighting

Add mixer-specific and bridge-specific heuristic detection

Add cross-chain tracking support

Add automated PDF investigation report generation

Add unit tests and API integration tests

Add Docker and Docker Compose setup

Add CI/CD pipeline using GitHub Actions

Add caching and rate-limit handling for Etherscan API

Improve service-provider database coverage

Add analyst feedback loop for improving risk scoring

Responsible Use

This system is intended for academic research, blockchain forensic learning, and AML-style investigation support. It does not prove criminal activity by itself. All results should be interpreted carefully by a human analyst and verified with additional evidence.

Author

Sayaka Alam
Department of Computer Science and Engineering
Khulna University of Engineering & Technology

License

This repository is currently shared as an academic project. Add a license file before using it for public or commercial distribution.
