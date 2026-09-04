EthereumHeist AML System

A professional blockchain forensic and AML-style analysis system for tracing suspicious Ethereum fund movement from known heist or suspicious wallet addresses. The system reads Ethereum transaction data, builds fund-flow evidence, runs TPP-style one-hop and multi-hop tracking, enriches outputs using service-provider mapping, calculates risk scores, and presents results through a web dashboard.

Important note: This project does not create a new blockchain. It analyzes existing Ethereum blockchain transaction data and converts it into structured investigative evidence.

Table of Contents

Project Overview

Key Features

System Architecture

Task Flow

Client-Server Flow

Dataset Flow

Backend Routing Flow

Algorithmic Workflow

Technology Stack

Project Structure

Backend Setup

Frontend Setup

Environment Variables

API Endpoints

Important Parameters

Example Test URLs

Output Files

How to Explain the Project

Limitations

Future Enhancements

Cloud Security Enhancement

Responsible Use

Project Overview

EthereumHeist AML System is designed to make Ethereum heist investigation more explainable and reproducible. Ethereum stores transaction records publicly, but heist fund movement can still be difficult to follow because funds may move through multiple wallets, ERC20 tokens, smart contracts, exchanges, bridges, mixers, and other services.

This project solves that problem by converting raw Ethereum transaction records into a clear investigation pipeline:

Known suspicious address
        ↓
Transaction collection
        ↓
Edge extraction
        ↓
One-hop / multi-hop tracking
        ↓
Service-provider matching
        ↓
Risk scoring
        ↓
CSV / JSON evidence
        ↓
Dashboard visualization

The system is useful for academic demonstration, AML-style research, blockchain forensic learning, and explainable transaction-flow analysis.

Key Features

Ethereum heist/suspicious address tracking

One-hop TPP-style transaction tracking

Multi-hop recursive fund-flow tracking

Normal ETH, internal ETH, and ERC20 transaction support

Service-provider address matching

Risk scoring for transaction edges

Graph-ready node-edge output

Batch experiment support for multiple addresses

CSV and JSON evidence generation

FastAPI backend with Swagger documentation

Next.js dashboard for charts, summary cards, and tables

Reproducible local execution flow

System Architecture

flowchart LR
    User[User / Analyst] --> UI[Next.js Frontend Dashboard]
    UI -->|HTTP Request| API[FastAPI Backend]

    API --> Dataset[Dataset Service]
    API --> Crawl[Etherscan Service]
    API --> Track[TPP Tracking Engine]
    API --> Match[Service Provider Matcher]
    API --> Risk[Risk Scoring Service]
    API --> Graph[Graph Service]
    API --> Result[Result Service]

    Dataset --> Raw[(data/raw)]
    Crawl --> Raw
    Track --> Tracking[(results/tracking)]
    Match --> Tracking
    Risk --> Tracking
    Graph --> Tracking
    Result --> UI

    UI --> Cards[Summary Cards]
    UI --> Charts[Charts]
    UI --> Tables[Evidence Tables]

Architecture Description

The frontend is the client side of the system. It collects the Ethereum address and tracking parameters from the user. The backend is the server side. It performs dataset loading, transaction processing, tracking, service matching, risk scoring, graph output generation, and file saving. The final results are returned to the frontend as JSON and displayed through charts, cards, and tables.

Task Flow

flowchart TD
    A[Start] --> B[Input Ethereum Address]
    B --> C[Set Parameters]
    C --> D[Send Request to Backend]
    D --> E[Load Local Dataset]
    E --> F{Missing Transaction Data?}
    F -->|Yes| G[Crawl Etherscan API]
    F -->|No| H[Use Existing Dataset]
    G --> I[Normalize Transactions]
    H --> I
    I --> J[Extract Source to Target Edges]
    J --> K[Apply beta, depth, and breadth filters]
    K --> L[Generate Multi-hop Edge File]
    L --> M[Match Service Providers]
    M --> N[Calculate Risk Score]
    N --> O[Generate Graph-ready Output]
    O --> P[Save CSV and JSON Evidence]
    P --> Q[Show Dashboard Result]
    Q --> R[End]

Client-Server Flow

sequenceDiagram
    participant User as User / Analyst
    participant Frontend as Next.js Frontend
    participant Backend as FastAPI Backend
    participant Dataset as Local Dataset
    participant Etherscan as Etherscan API
    participant Results as Results Folder

    User->>Frontend: Enter address and parameters
    Frontend->>Backend: GET /pipeline/full/{address}
    Backend->>Dataset: Load transaction and service data
    alt Data missing and crawl_missing=true
        Backend->>Etherscan: Fetch transaction data
        Etherscan-->>Backend: Return transaction records
    end
    Backend->>Backend: Run multi-hop tracking
    Backend->>Backend: Match service providers
    Backend->>Backend: Add risk scores
    Backend->>Results: Save CSV / JSON evidence
    Backend-->>Frontend: Return JSON response
    Frontend-->>User: Display dashboard charts and tables

Dataset Flow

flowchart LR
    A[Heist Labels] --> D[Dataset Loader]
    B[Transaction CSV Files] --> D
    C[Service Provider Map] --> D

    D --> E[Address Normalization]
    E --> F[Transaction Edge Extraction]
    F --> G[Tracking Edge File]
    G --> H[Service Enriched File]
    H --> I[Risk Scored File]
    I --> J[Graph-ready JSON / CSV]

Dataset Description

Dataset Component

Purpose

Heist labels

Stores known suspicious or heist root addresses

Transaction CSV files

Stores normal ETH, internal ETH, and ERC20 transfer records

Service-provider map

Stores known service addresses such as exchange, bridge, mixer, or DEX addresses

Tracking result files

Stores generated source-to-target edge evidence

Summary JSON

Stores final statistics and pipeline status

Backend Routing Flow

flowchart TD
    A[HTTP Request] --> B[main.py FastAPI Route]
    B --> C{Route Type}
    C -->|Dataset| D[dataset_service.py / incident_service.py]
    C -->|Crawling| E[etherscan_service.py]
    C -->|Tracking| F[tpp_tracking_service.py / multi_hop_tracking_service.py]
    C -->|Service Matching| G[service_provider_matching_service.py]
    C -->|Risk| H[risk_scoring_service.py]
    C -->|Graph| I[graph_service.py]
    C -->|Experiment| J[experiment_service.py]
    C -->|Full Pipeline| K[full_pipeline_service.py]

    D --> L[JSON Response]
    E --> L
    F --> L
    G --> L
    H --> L
    I --> L
    J --> L
    K --> L

Routing Description

The routing layer receives browser or frontend requests, validates path and query parameters, calls the correct backend service, and returns the result as JSON. The heavy logic is kept inside service files, while the route functions mainly connect URLs with backend functions.

Algorithmic Workflow

1. One-Hop Tracking

One-hop tracking analyzes only the direct outgoing transactions from a given suspicious address.

Root address → outgoing transactions → valid edges → evidence file

2. Multi-Hop Tracking

Multi-hop tracking expands the fund-flow path recursively up to a selected depth.

Root address
   ↓
Layer 1 target addresses
   ↓
Layer 2 target addresses
   ↓
Continue until max_depth is reached

3. Filtering Logic

The tracking process uses parameters to keep the graph controlled and readable.

if transaction_amount < beta:
    ignore_transaction()

if current_depth > max_depth:
    stop_expansion()

if expanded_addresses > max_addresses_per_layer:
    limit_expansion()

4. Service Matching

Each tracked target address is compared with a known service-provider map.

if target_address in service_provider_map:
    mark_as_service_provider()
else:
    mark_as_unresolved()

The system does not guess unknown services. This reduces false claims and keeps the output more defensible.

5. Risk Scoring

The risk score is calculated from interpretable features such as transaction amount, token type, layer depth, and service-provider matching.

Risk = amount factor + token factor + layer factor + service factor

Risk scoring is used for prioritization. It does not prove guilt.

Technology Stack

Backend

Tool

Use

Python

Core backend language

FastAPI

REST API backend

Pandas

CSV processing and transformation

Etherscan API

Ethereum transaction crawling

Uvicorn

Local backend server

python-dotenv

Environment variable loading

Frontend

Tool

Use

Next.js

Frontend framework

React

UI component development

TypeScript

Typed frontend development

Axios

HTTP request handling

Recharts

Charts and visual result presentation

Cytoscape

Graph visualization support

Tailwind CSS

Styling

Project Structure

EthereumHeist-System/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
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
│   │
│   ├── requirements.txt
│   └── .env
│
├── data/
│   └── raw/
│       ├── heist labels
│       ├── transaction files
│       └── service-provider maps
│
├── frontend/
│   ├── package.json
│   ├── app/
│   ├── components/
│   └── public/
│
├── results/
│   ├── tracking/
│   └── experiments/
│
└── README.md

Backend Setup

Open CMD or PowerShell:

cd /d D:\EthereumHeist_System\backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

Backend server:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs

Health check:

http://127.0.0.1:8000/health

Frontend Setup

Open another CMD or PowerShell window:

cd /d D:\EthereumHeist_System\frontend
npm install
npm run dev

Frontend server:

http://localhost:3000

Environment Variables

Create a .env file inside the backend folder.

APP_ENV=development
LOG_LEVEL=INFO
ETHERSCAN_API_KEY=your_etherscan_api_key_here
FRONTEND_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
ALLOWED_HOSTS=*

Environment Variable Description

Variable

Meaning

APP_ENV

Application environment, for example development or production

LOG_LEVEL

Logging level such as INFO, DEBUG, WARNING

ETHERSCAN_API_KEY

API key for fetching Ethereum transaction data

FRONTEND_ORIGINS

Allowed frontend URLs for CORS

ALLOWED_HOSTS

Hosts allowed by backend trusted-host middleware

API Endpoints

System Routes

Method

Endpoint

Description

GET

/

Backend home route

GET

/health

Backend health check

GET

/api/health

API health check

Dataset Routes

Method

Endpoint

Description

GET

/dataset/status

Check dataset availability

GET

/dataset/overview

Show dataset overview

GET

/incidents

Show heist incident records

GET

/heist-labels

Show known heist labels

GET

/service-providers

Show service-provider mappings

Crawling Routes

Method

Endpoint

Description

GET

/crawl/address/{address}

Fetch Ethereum transactions for an address

Transaction Routes

Method

Endpoint

Description

GET

/transactions/files

List transaction files

GET

/transactions/preview/{file_name}

Preview a transaction file

Tracking Routes

Method

Endpoint

Description

GET

/track/one-hop/{address}

Run one-hop TPP tracking

GET

/track/multi-hop/{address}

Run multi-hop TPP tracking

Tracking Result Routes

Method

Endpoint

Description

GET

/tracking/files

List tracking result files

GET

/tracking/preview/{file_name}

Preview tracking result file

GET

/tracking/csv/{file_name}

Preview tracking CSV file

GET

/tracking/summary/{file_name}

Read tracking summary JSON

GET

/tracking/download/{file_name}

Download tracking output file

GET

/tracking/enrich-service/{edges_file_name}

Match edges with service-provider map

GET

/tracking/stats/{edges_file_name}

Get tracking statistics

Graph Routes

Method

Endpoint

Description

GET

/graph/tracking/{file_name}

Build graph-ready output from edge file

Experiment Routes

Method

Endpoint

Description

GET

/experiment/run

Run batch experiment

GET

/experiment/files

List experiment files

GET

/experiment/csv/{file_name}

Preview experiment CSV

Risk Routes

Method

Endpoint

Description

GET

/risk/edges/{file_name}

Add AML risk scores to edge file

Full Pipeline Route

Method

Endpoint

Description

GET

/pipeline/full/{address}

Run tracking, service matching, risk scoring, graph output, and summary generation together

Important Parameters

Parameter

Used In

Default

Range / Type

Meaning

address

Tracking / pipeline / crawling

Required

Ethereum address string

Suspicious root address used to start tracking

beta

One-hop, multi-hop, experiment, pipeline

0.01

float, >= 0.0

Minimum proportional-value threshold used to filter tiny/noisy transfers

omega

One-hop, multi-hop, experiment, pipeline

1000

integer, >= 1

Maximum transaction/time constraint used by the tracking logic

max_depth

Multi-hop, experiment, pipeline

2 or route-specific default

integer, 1-10

Maximum recursive depth for fund-flow expansion

max_addresses_per_layer

Multi-hop, experiment, pipeline

10, 3, or route-specific default

integer, 1-1000

Maximum number of addresses expanded at each layer

crawl_missing

Multi-hop, experiment, pipeline

true or route-specific default

boolean

Whether the backend should fetch missing transaction data from Etherscan

limit

Graph / experiment

Route-specific default

integer

Limits number of graph records or experiment addresses

file_name

Preview / graph / download / risk

Required

CSV/JSON file name

Name of the result file to preview, graph, download, or score

edges_file_name

Service enrichment / stats

Required

CSV file name

Name of generated edge CSV file used for enrichment or statistics

Example Test URLs

Full Pipeline Test

http://127.0.0.1:8000/pipeline/full/0xeb31973e0febf3e3d7058234a5ebbae1ab4b8c23?max_depth=1&max_addresses_per_layer=1&beta=0.01&omega=1000&crawl_missing=false

Multi-Hop Tracking Only

http://127.0.0.1:8000/track/multi-hop/0xeb31973e0febf3e3d7058234a5ebbae1ab4b8c23?max_depth=1&max_addresses_per_layer=1&beta=0.01&omega=1000&crawl_missing=false

Run Batch Experiment

http://127.0.0.1:8000/experiment/run?limit=3&max_depth=1&max_addresses_per_layer=1&beta=0.01&omega=1000&crawl_missing=false

List Tracking Files

http://127.0.0.1:8000/tracking/files

Service Enrichment Example

http://127.0.0.1:8000/tracking/enrich-service/EXACT_EDGE_FILE_NAME.csv

Risk Scoring Example

http://127.0.0.1:8000/risk/edges/EXACT_EDGE_FILE_NAME.csv

Graph Output Example

http://127.0.0.1:8000/graph/tracking/EXACT_EDGE_FILE_NAME.csv?limit=30

Output Files

The system generates files mainly inside:

results/tracking/
results/experiments/

Common outputs:

Output File Type

Description

multihop_edges_*.csv

Source-to-target tracking edges

multihop_layers_*.csv

Layer-wise address expansion details

service_enriched_*.csv

Tracking edges enriched with service-provider labels

risk_scored_*.csv

Edges with AML-style risk score

summary_*.json

Pipeline summary, counts, and status

graph_*.json

Graph-ready nodes and edges

experiment_*.csv

Batch experiment result summary

How to Explain the Project

Simple Explanation

EthereumHeist is a blockchain forensic system that starts from a suspicious Ethereum address, tracks where funds move, checks whether target addresses are known services, assigns risk priority, and presents all evidence using CSV/JSON files and a web dashboard.

Technical Explanation

The system uses a FastAPI backend to expose AML tracking routes. The backend loads Ethereum transaction files, optionally crawls missing data through Etherscan, extracts source-to-target transaction edges, applies TPP-style one-hop and multi-hop tracking, enriches edges with service-provider labels, calculates risk scores, and generates graph-ready output. The Next.js frontend sends HTTP requests to the backend and visualizes the results using summary cards, charts, and evidence tables.

Contribution Explanation

The main contribution is the implementation of a complete runnable AML pipeline. Instead of only discussing Ethereum heist tracking conceptually, this project provides backend routing, dataset processing, multi-hop tracking, service matching, risk scoring, evidence generation, dashboard visualization, and batch experiment support.

Limitations

The system depends on the completeness of transaction CSV files and Etherscan API availability.

Etherscan API rate limits may affect large crawling tasks.

Ethereum's account-based model mixes funds inside account balances, so exact coin identity cannot always be proven.

Service matching depends on the available service-provider map; unknown services remain unresolved.

Deep multi-hop tracking can increase runtime and produce very large graphs.

Cross-chain movement through bridges is not fully tracked in the current version.

Mixer-specific behavior needs more advanced heuristics.

The system supports investigation but does not provide final legal proof.

Future Enhancements

Add larger verified service-provider database

Add cross-chain bridge tracking

Add mixer-specific behavior detection

Add real-time transaction monitoring

Add interactive graph filtering and path highlighting

Add automated PDF forensic report generation

Add user authentication and role-based access control

Add PostgreSQL or MongoDB for persistent investigation storage

Add cloud deployment with secure backend and dashboard hosting

Add background task queue for long-running analysis

Add Docker and Docker Compose support

Add CI/CD workflow for testing and deployment

Add unit tests and API integration tests

Add analyst feedback loop for improving risk scoring

Cloud Security Enhancement

The project can be made more secure by deploying it in a cloud environment with proper configuration.

Recommended cloud security improvements:

Use HTTPS/TLS for frontend-backend communication

Store API keys in a cloud secret manager

Use encrypted storage for CSV/JSON evidence files

Add login system with JWT or OAuth

Add role-based access control for admin and analyst users

Use cloud IAM policies for access restriction

Add WAF and firewall rules

Add rate limiting to protect API endpoints

Enable centralized logging and monitoring

Enable automatic backup and disaster recovery

Use private storage buckets for evidence files

Use Docker containers for reproducible deployment

Cloud does not automatically make the project secure. Security improves only when encryption, access control, monitoring, and secret management are configured correctly.

Responsible Use

This project is intended for academic, forensic-learning, and AML-style research purposes. The system analyzes public blockchain data, but the output should be interpreted carefully. A service match or risk score should be treated as investigative support, not as final proof of criminal activity.

License

Add your selected license here, such as MIT License, academic-only license, or university project license.

Author

Sayaka Alam
Department of Computer Science and Engineering
Khulna University of Engineering & Technology
GitHub: SayakaMeem
