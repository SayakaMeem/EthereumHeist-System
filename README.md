<div align="center">

🛡️ EthereumHeist AML System

Explainable Ethereum Fund-Flow Tracking, AML Forensics, Service Matching and Dashboard Evidence Generation

<p>
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Frontend-Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white" />
  <img src="https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/UI-React-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/Data-Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/Blockchain-Ethereum-3C3C3D?style=for-the-badge&logo=ethereum&logoColor=white" />
</p>

<p>
  <img src="https://img.shields.io/badge/AML-Tracking-red?style=flat-square" />
  <img src="https://img.shields.io/badge/Graph-Analysis-blueviolet?style=flat-square" />
  <img src="https://img.shields.io/badge/CSV%2FJSON-Evidence-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/Service-Matching-brightgreen?style=flat-square" />
  <img src="https://img.shields.io/badge/Risk-Scoring-yellow?style=flat-square" />
  <img src="https://img.shields.io/badge/Status-Research%20Prototype-informational?style=flat-square" />
</p>

EthereumHeist AML System is a full-stack research prototype that tracks suspicious Ethereum fund movement from known heist or placement addresses and converts raw blockchain activity into structured, reviewable AML evidence.

</div>

📌 Table of Contents

Project Summary

Why This Project Matters

Key Features

Technology Stack

Dependencies

System Architecture

Working Flow

Backend Routing Flow

Client-Server Sequence

Tracking Algorithm Flow

Dataset and Evidence Flow

Logical Relational Data Model

Folder Structure

Backend API Routes

Important Parameters

Dashboard Overview

Installation and Setup

Run the Software

Example API Calls

Generated Output Files

Algorithmic Contribution

Security and Cloud Enhancement

Limitations

Future Enhancements

Troubleshooting

Responsible Use

🧠 Project Summary

EthereumHeist AML System analyzes Ethereum transaction behavior from a suspicious or known heist address. It collects or loads blockchain transaction records, performs TPP-style one-hop and multi-hop fund-flow tracking, identifies possible layering paths, matches addresses with known service-provider records, generates AML risk scores, and visualizes results through a web dashboard.

The system does not build a new blockchain. Instead, it builds an investigative graph on top of existing Ethereum blockchain data.

Simple idea: Ethereum is the source blockchain. EthereumHeist builds the forensic tracking layer above it.

🎯 Why This Project Matters

Ethereum transaction data is public, but public data is not always easy to investigate. Suspicious funds can move through many wallets, ERC20 tokens, smart contracts, exchanges, bridges, DEXs, and mixers. Manual checking through block explorers is slow, repetitive, and difficult to reproduce.

EthereumHeist solves this problem by converting raw Ethereum transaction data into:

📁 CSV evidence files

📄 JSON summaries

🔗 Graph-ready node-edge outputs

📊 Dashboard charts

🧾 Transaction-level investigation tables

🛡️ AML risk-priority outputs

✨ Key Features

Feature

Description

Benefit

🔍 One-hop tracking

Tracks direct outgoing transfers from one address

Fast initial investigation

🧭 Multi-hop tracking

Recursively expands candidate addresses

Finds possible laundering layers

🪙 ETH + ERC20 support

Handles normal ETH, internal ETH and ERC20 token flow

More complete Ethereum view

🧹 Beta filtering

Removes tiny/noisy transactions using a threshold

Cleaner graph and faster runtime

🏦 Service-provider matching

Checks targets against known service maps

Finds possible integration endpoints

⚠️ Risk scoring

Adds AML risk score and risk level

Prioritizes suspicious edges

🕸️ Graph output

Converts source-target records into nodes and edges

Supports fund-flow visualization

📊 Dashboard

Shows summary cards, charts and tables

Easy presentation and review

🧪 Batch experiment

Runs the pipeline on multiple heist records

Evaluation and comparison support

📦 Evidence export

Saves CSV and JSON files

Reproducible forensic output

🧰 Technology Stack

Layer

Tools / Technologies

Purpose

Frontend

Next.js, React, TypeScript

Client-side dashboard and UI

Charts

Recharts

Transaction and experiment visualization

Graph UI

Cytoscape

Graph-oriented visualization support

API Client

Axios / Fetch API

HTTP communication with backend

Backend

FastAPI, Uvicorn, Starlette

REST API server

Data Processing

Pandas, NumPy, PyArrow

CSV loading, cleaning and transformation

Graph Processing

NetworkX, igraph

Graph-ready analysis support

Data Source

Ethereum transaction CSV, Etherscan API

Blockchain transaction input

Runtime Storage

CSV, JSON, local result folders

Evidence storage and reproducibility

Security Middleware

CORS, TrustedHost, GZip

Safer API access and response handling

Development Tools

Git, GitHub, VS Code, Postman

Development and testing

📦 Dependencies

Backend Dependencies

Important backend packages are listed in backend/requirements.txt.

Package

Version

Use

fastapi

0.138.1

Backend API framework

uvicorn

0.49.0

ASGI server

pandas

2.3.3

CSV and tabular processing

numpy

2.2.6

Numeric processing

requests

2.34.2

API calls, including Etherscan-style requests

python-dotenv

1.2.2

Environment variable loading

networkx

3.4.2

Graph analysis support

igraph

1.0.0

Graph processing support

duckdb

1.5.4

Local analytical data processing support

pyarrow

24.0.0

Columnar data support

pydantic

2.13.4

Data validation

python-multipart

0.0.32

File/form handling support

Frontend Dependencies

Important frontend packages are listed in frontend/package.json.

Package

Version

Use

next

16.2.9

Frontend framework

react

19.2.4

UI components

react-dom

19.2.4

DOM rendering

axios

^1.18.1

HTTP API requests

recharts

^3.9.0

Charts and dashboard visualization

cytoscape

^3.34.0

Graph visualization support

lucide-react

^1.22.0

Icons

tailwindcss

^4

Styling

typescript

^5

Type safety

eslint

^9

Code quality

🏗️ System Architecture

flowchart LR
    User((User / Analyst)) --> Frontend[Next.js Dashboard]
    Frontend -->|HTTP Requests| API[FastAPI Backend]

    API --> Dataset[Dataset Service]
    API --> Crawl[Etherscan Crawler]
    API --> Tracking[TPP Tracking Engine]
    API --> Matching[Service Provider Matcher]
    API --> Risk[Risk Scoring Service]
    API --> Graph[Graph Service]
    API --> Experiment[Batch Experiment Service]

    Dataset --> Raw[(data/raw)]
    Crawl --> Tx[(data/raw/transactions)]
    Tracking --> Results[(results/tracking)]
    Matching --> Results
    Risk --> Results
    Graph --> Results
    Experiment --> Exp[(results/experiments)]

    Results --> Frontend
    Exp --> Frontend

🔄 Working Flow

flowchart TD
    A[Start] --> B[Open Dashboard]
    B --> C[Enter Ethereum Heist Address]
    C --> D[Set Parameters: depth, layer limit, beta, crawl]
    D --> E[Click Run Tracking]
    E --> F[Frontend Sends HTTP Request]
    F --> G[FastAPI Route Receives Request]
    G --> H[Load Local Dataset / Crawl Missing Data]
    H --> I[Run TPP Multi-hop Tracking]
    I --> J[Generate Edge and Layer CSV]
    J --> K[Match Service Providers]
    K --> L[Apply Risk Scoring]
    L --> M[Build Graph-ready Output]
    M --> N[Return JSON Response]
    N --> O[Dashboard Shows Cards, Charts, Tables]
    O --> P[Download / Reuse Evidence Files]

🧭 Backend Routing Flow

flowchart LR
    Root[/ /] --> Home[Backend Status]
    Health[/health/] --> HealthFn[Health Check]
    Dataset[/dataset/status/] --> DatasetFn[Dataset Status]
    Incidents[/incidents/] --> IncidentsFn[Heist Incidents]
    Labels[/heist-labels/] --> LabelsFn[Heist Labels]
    Services[/service-providers/] --> ServicesFn[Service Map]
    Crawl[/crawl/address/{address}/] --> CrawlFn[Fetch Transactions]
    OneHop[/track/one-hop/{address}/] --> OneHopFn[One-hop TPP]
    MultiHop[/track/multi-hop/{address}/] --> MultiHopFn[Multi-hop TPP]
    Enrich[/tracking/enrich-service/{file}/] --> EnrichFn[Service Matching]
    Stats[/tracking/stats/{file}/] --> StatsFn[Tracking Statistics]
    Graph[/graph/tracking/{file}/] --> GraphFn[Node-edge Graph]
    Risk[/risk/edges/{file}/] --> RiskFn[Risk Score]
    Pipeline[/pipeline/full/{address}/] --> PipelineFn[Full AML Pipeline]
    Experiment[/experiment/run/] --> ExperimentFn[Batch Experiment]

🔁 Client-Server Sequence

sequenceDiagram
    participant U as User
    participant FE as Next.js Dashboard
    participant BE as FastAPI Backend
    participant DS as Dataset / CSV Files
    participant ES as Etherscan API
    participant RS as Results Folder

    U->>FE: Enter address and parameters
    FE->>BE: GET /track/multi-hop/{address}
    BE->>DS: Check local transaction files
    alt Missing data and crawl_missing=true
        BE->>ES: Fetch normal, internal and ERC20 transactions
        ES-->>BE: Return transaction records
        BE->>DS: Save newly crawled data
    end
    BE->>BE: Run multi-hop tracking
    BE->>RS: Save edges, layers and summary files
    BE-->>FE: Return tracking JSON
    FE->>BE: GET /tracking/enrich-service/{edges_file}
    BE->>RS: Save service-enriched CSV
    BE-->>FE: Return matching summary
    FE->>BE: GET /graph/tracking/{edges_file}
    BE-->>FE: Return graph nodes and edges
    FE->>U: Show dashboard cards, charts and tables

🧬 Tracking Algorithm Flow

flowchart TD
    A[Root Heist Address] --> B[Initialize Layer 0]
    B --> C{Depth <= max_depth?}
    C -- No --> Z[Stop]
    C -- Yes --> D[Take limited addresses from current layer]
    D --> E{Transaction files exist?}
    E -- Yes --> F[Load local normal/internal/ERC20 CSV]
    E -- No and crawl enabled --> G[Crawl missing transaction data]
    E -- No and crawl disabled --> X[Skip / return warning]
    G --> F
    F --> H[Run one-hop TPP tracking]
    H --> I{Amount >= beta?}
    I -- No --> J[Ignore tiny/noisy edge]
    I -- Yes --> K[Save source → target edge]
    K --> L{Label = candidate_layering?}
    L -- Yes --> M[Add target to next layer]
    L -- No --> N[Mark as integration/other evidence]
    M --> O[Write layer records]
    N --> O
    O --> P[Save multihop_edges.csv]
    P --> Q[Save multihop_layers.csv]
    Q --> R[Save multihop_summary.json]
    R --> C

🗂️ Dataset and Evidence Flow

flowchart LR
    A[Heist Labels] --> D[Dataset Service]
    B[Normal ETH CSV] --> D
    C[Internal ETH CSV] --> D
    E[ERC20 Transfer CSV] --> D
    F[Service Provider Map] --> D

    D --> G[Tracking Engine]
    G --> H[Multihop Edge File]
    G --> I[Layer File]
    H --> J[Service Enrichment]
    J --> K[Risk Scoring]
    K --> L[Graph Builder]

    H --> R[(results/tracking)]
    I --> R
    J --> R
    K --> R
    L --> R
    R --> M[Dashboard + Downloadable Evidence]

🧩 Logical Relational Data Model

The current implementation is primarily CSV/JSON based, but the following logical relational design can be used if the system is migrated to SQLite, PostgreSQL, MySQL, or a cloud database.

erDiagram
    HEIST_LABEL ||--o{ TRANSACTION : starts_from
    ADDRESS ||--o{ TRANSACTION : sends
    ADDRESS ||--o{ TRANSACTION : receives
    TRANSACTION ||--o{ TRACKING_EDGE : becomes
    TRACKING_EDGE ||--o| SERVICE_MATCH : checks
    TRACKING_EDGE ||--o| RISK_SCORE : scores
    TRACKING_EDGE ||--o{ GRAPH_EDGE : visualizes
    ADDRESS ||--o{ GRAPH_NODE : visualizes

    HEIST_LABEL {
        int id PK
        string heist_name
        string root_address
        string incident_type
        string source_reference
    }

    ADDRESS {
        int id PK
        string address_hash
        string address_role
        string label_status
    }

    TRANSACTION {
        int id PK
        string tx_hash
        string source_address FK
        string target_address FK
        string transaction_type
        decimal amount
        string token_symbol
        datetime block_time
    }

    TRACKING_EDGE {
        int id PK
        string source_address
        string target_address
        decimal amount
        string transaction_type
        string label
        int source_layer
    }

    SERVICE_MATCH {
        int id PK
        int edge_id FK
        string service_name
        string service_category
        boolean is_service_provider
    }

    RISK_SCORE {
        int id PK
        int edge_id FK
        int risk_score
        string risk_level
        string risk_reasons
    }

    GRAPH_NODE {
        int id PK
        string address_hash
        int layer
        string role
    }

    GRAPH_EDGE {
        int id PK
        string source
        string target
        string transaction_type
        decimal amount
    }

📁 Folder Structure

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
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx
│   │   ├── layout.tsx
│   │   └── globals.css
│   ├── package.json
│   └── tsconfig.json
│
├── data/
│   └── raw/
│       ├── EthereumHeist-main/
│       └── transactions/
│
├── results/
│   ├── tracking/
│   └── experiments/
│
└── README.md

🛣️ Backend API Routes

Method

Route

Purpose

Main Output

GET

/

Backend home

Status message

GET

/health

Check backend health

Health JSON

GET

/api/health

API health check

API status

GET

/dataset/status

Check dataset availability

Dataset status

GET

/dataset/overview

Get dataset summary

Dataset overview

GET

/incidents

List heist incidents

Incident records

GET

/heist-labels

Load heist/placement labels

Heist labels

GET

/service-providers

Load service-provider map

Service labels

GET

/crawl/address/{address}

Fetch transactions for address

Crawled data summary

GET

/transactions/files

List transaction files

File list

GET

/transactions/preview/{file_name}

Preview transaction file

CSV preview

GET

/track/one-hop/{address}

Run one-hop TPP tracking

One-hop edge result

GET

/track/multi-hop/{address}

Run multi-hop tracking

Edge/layer/summary files

GET

/tracking/files

List tracking outputs

File list

GET

/tracking/preview/{file_name}

Preview tracking file

Preview rows

GET

/tracking/csv/{file_name}

Preview tracking CSV

CSV preview

GET

/tracking/summary/{file_name}

Read tracking summary JSON

Summary JSON

GET

/tracking/download/{file_name}

Download output file

CSV/JSON download

GET

/tracking/enrich-service/{edges_file_name}

Match services with edge file

Service-enriched CSV

GET

/tracking/stats/{edges_file_name}

Generate tracking statistics

Counts and summaries

GET

/graph/tracking/{file_name}

Build graph nodes and edges

Graph JSON

GET

/experiment/run

Run batch experiment

Experiment summary

GET

/experiment/files

List experiment outputs

File list

GET

/experiment/csv/{file_name}

Preview experiment CSV

Experiment table

GET

/risk/edges/{file_name}

Add AML risk scores

Risk-scored CSV

GET

/pipeline/full/{address}

Run complete AML pipeline

Tracking + service + risk + graph

⚙️ Important Parameters

Parameter

Example

Used In

Meaning

address

0xeb31973e...b8c23

Tracking, crawling, pipeline

Root heist or suspicious Ethereum address

max_depth

1 or 2

Multi-hop tracking, pipeline, experiment

Maximum number of layers to expand

max_addresses_per_layer

1 or 10

Multi-hop tracking

Controls how many addresses are expanded per layer

beta

0.01

One-hop and multi-hop TPP tracking

Minimum value threshold for filtering tiny/noisy transfers

omega

1000

TPP tracking

Maximum transaction/time constraint used by tracking logic

crawl_missing

false

Tracking, pipeline, experiment

If true, missing transaction data is fetched using the crawler

limit

3

Batch experiment

Number of heist records to process

file_name

abc_multihop_edges.csv

Preview, graph, download, risk

Existing output file name

edges_file_name

abc_multihop_edges.csv

Service matching, stats

Edge CSV file generated by tracking

🖥️ Dashboard Overview

The frontend dashboard is designed for analysts, researchers and thesis demonstration. It provides a clear interface for both single-address tracking and batch experiment execution.

flowchart TD
    Dashboard[Dashboard Home] --> A[Run Multihop Tracking Panel]
    Dashboard --> B[Batch Experiment Mode]
    Dashboard --> C[Summary Cards]
    Dashboard --> D[Charts]
    Dashboard --> E[Evidence Tables]
    Dashboard --> F[Graph Preview]

    A --> A1[Address Input]
    A --> A2[Max Depth]
    A --> A3[Max Addresses Per Layer]
    A --> A4[Crawl Missing Checkbox]
    A --> A5[Run Tracking Button]

    B --> B1[Experiment Limit]
    B --> B2[Experiment Max Depth]
    B --> B3[Run Batch Experiment Button]

    C --> C1[Total Edges]
    C --> C2[Visited Addresses]
    C --> C3[Service Matches]
    C --> C4[Risk Summary]

    D --> D1[Transaction Type Chart]
    D --> D2[Service Matching Chart]
    D --> D3[Experiment Comparison Chart]

Dashboard Sections

Section

Description

Run Multihop Tracking

Input one Ethereum address and run address-level investigation

Batch Experiment Mode

Run multiple heist addresses for evaluation and comparison

Summary Cards

Shows total edges, service matches, layer counts and run status

Charts

Shows transaction-type distribution and experiment comparisons

Evidence Tables

Shows CSV rows from tracking and experiment outputs

Graph Output

Shows graph-ready nodes and edges for blockchain fund-flow visualization

🧪 Installation and Setup

1. Clone the Repository

https://github.com/SayakaMeem/EthereumHeist-System.git
cd EthereumHeist-System

2. Backend Setup

cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

3. Optional .env File

Create a .env file inside the backend folder:

APP_ENV=development
LOG_LEVEL=INFO
FRONTEND_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
ALLOWED_HOSTS=*
ETHERSCAN_API_KEY=your_etherscan_api_key_here
PROJECT_BASE_DIR=D:\EthereumHeist_System
DATA_DIR=D:\EthereumHeist_System\data
RESULTS_DIR=D:\EthereumHeist_System\results
TRACKING_DIR=D:\EthereumHeist_System\results\tracking
EXPERIMENT_DIR=D:\EthereumHeist_System\results\experiments
TRANSACTION_DIR=D:\EthereumHeist_System\data\raw\transactions

4. Frontend Setup

cd frontend
npm install

▶️ Run the Software

Run Backend Server

Open Terminal 1:

cd /d D:\EthereumHeist_System\backend
.venv\Scripts\activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

Backend URL:

http://127.0.0.1:8000

Swagger API Docs:

http://127.0.0.1:8000/docs

Run Frontend Server

Open Terminal 2:

cd /d D:\EthereumHeist_System\frontend
npm run dev

Frontend URL:

http://localhost:3000

🌐 Example API Calls

Health Check

http://127.0.0.1:8000/health

Dataset Status

http://127.0.0.1:8000/dataset/status

Run Multi-hop Tracking

http://127.0.0.1:8000/track/multi-hop/0xeb31973e0febf3e3d7058234a5ebbae1ab4b8c23?max_depth=1&max_addresses_per_layer=1&beta=0.01&omega=1000&crawl_missing=false

Run Full AML Pipeline

http://127.0.0.1:8000/pipeline/full/0xeb31973e0febf3e3d7058234a5ebbae1ab4b8c23?max_depth=1&max_addresses_per_layer=1&beta=0.01&omega=1000&crawl_missing=false

Enrich Edge File with Service Providers

http://127.0.0.1:8000/tracking/enrich-service/PASTE_EXACT_EDGE_FILE_NAME.csv

Add Risk Scores

http://127.0.0.1:8000/risk/edges/PASTE_EXACT_EDGE_FILE_NAME.csv

Build Graph Output

http://127.0.0.1:8000/graph/tracking/PASTE_EXACT_EDGE_FILE_NAME.csv?limit=30

Run Batch Experiment

http://127.0.0.1:8000/experiment/run?limit=3&max_depth=1&max_addresses_per_layer=1&beta=0.01&omega=1000&crawl_missing=false

📤 Generated Output Files

Output File

Folder

Description

{address}_multihop_edges.csv

results/tracking

Source-to-target tracked transaction edges

{address}_multihop_layers.csv

results/tracking

Layer-wise placement/layering records

{address}_multihop_summary.json

results/tracking

Tracking summary, parameters, error preview and file paths

{edge_file}_service_enriched.csv

results/tracking

Edge file with service-provider match columns

{edge_file}_risk_scored.csv

results/tracking

Edge file with risk score, risk level and reasons

experiment_result.csv

results/experiments

Batch experiment comparison table

Graph JSON response

API response

Node-edge output for visualization

🧠 Algorithmic Contribution

The project extends Ethereum heist-tracking research into a complete runnable software pipeline.

Main Additions

Contribution

Explanation

Unified transaction handling

Normal ETH, internal ETH and ERC20 transfers are handled together

Configurable multi-hop expansion

max_depth controls tracking layers

Breadth control

max_addresses_per_layer prevents path explosion

Value filtering

beta removes tiny/noisy transfers

API-based crawling

Missing address data can be fetched when needed

Service matching

Addresses are matched with known service-provider records

Conservative labeling

Unknown addresses are marked unresolved, not guessed

Risk scoring

AML-style risk score and level are added to edges

Evidence generation

CSV and JSON outputs make analysis reproducible

Dashboard visualization

Investigation results become readable for non-technical reviewers

Short Pseudocode

current_layer = {root_address}
visited = set()
all_edges = []

for depth in range(max_depth + 1):
    limited_layer = list(current_layer)[:max_addresses_per_layer]
    next_layer = set()

    for address in limited_layer:
        if address in visited:
            continue

        visited.add(address)

        if crawl_missing:
            ensure_address_crawled(address)

        one_hop_edges = run_one_hop_tpp_tracking(
            address=address,
            beta=beta,
            omega=omega
        )

        for edge in one_hop_edges:
            all_edges.append(edge)

            if edge.label == "candidate_layering":
                next_layer.add(edge.target)

    current_layer = next_layer

🔐 Security and Cloud Enhancement

The current version can run locally. For production or institutional deployment, cloud security can make the system safer and more reliable.

Cloud Security Feature

How It Helps

HTTPS/TLS

Encrypts frontend-backend communication

Secret Manager

Stores Etherscan/API keys outside source code

IAM / RBAC

Controls who can access admin, analyst and viewer functions

WAF

Blocks common web attacks before reaching the backend

Rate Limiting

Prevents API abuse and expensive repeated crawling

Encrypted Storage

Protects CSV/JSON evidence files at rest

Audit Logging

Records who ran which investigation and when

Backup and Versioning

Protects evidence files from deletion or corruption

Cloud Database

Enables reliable structured storage instead of only local CSV

Container Deployment

Improves portability using Docker/Kubernetes

Cloud Deployment Concept

flowchart LR
    User[Analyst Browser] -->|HTTPS| CDN[Cloud CDN / Frontend Hosting]
    CDN -->|HTTPS API Call| WAF[WAF + Rate Limiter]
    WAF --> API[FastAPI Container]
    API --> Secrets[Secret Manager]
    API --> DB[(Cloud SQL / PostgreSQL)]
    API --> Storage[(Encrypted Object Storage)]
    API --> Logs[Monitoring + Audit Logs]
    API --> Etherscan[Etherscan API]

Cloud itself does not automatically make a system secure. Correct configuration, access control, encryption and monitoring make it secure.

⚠️ Limitations

Limitation

Explanation

Account-based mixing

Ethereum merges funds inside one balance, so exact coin identity cannot always be proven

API dependency

Crawling depends on Etherscan/API availability and rate limits

Service label coverage

Matching quality depends on the completeness of the service-provider map

Local file storage

CSV/JSON files are simple and reproducible but less scalable than a database

Large graph size

Deep tracking can create many edges and increase runtime

Cross-chain limitation

Bridge and non-Ethereum chain tracking require more modules

Mixer complexity

Privacy mixers need specialized heuristics beyond basic service matching

No legal accusation

Output is investigation support, not final legal proof

🚀 Future Enhancements

Enhancement

Benefit

PostgreSQL / SQLite database

Better relational storage and query performance

User authentication

Secure analyst login and role control

Cloud deployment

Safer access, backups and monitored production use

Larger service-provider map

Better exchange, DEX, mixer and bridge detection

Cross-chain support

Track funds across bridge transfers and other chains

Advanced graph visualization

Node filtering, path highlighting and community detection

Mixer-specific detection

Better handling of Tornado-like privacy movement

Report generation

Auto-generate PDF investigation reports

Scheduled monitoring

Watch selected addresses over time

Docker support

Easier installation and deployment

Unit and integration testing

Higher reliability for backend and frontend

CI/CD pipeline

Automated checks before deployment

🧯 Troubleshooting

Problem

Meaning

Fix

Backend not opening

Server is not running

Run uvicorn app.main:app --reload --port 8000

Frontend cannot fetch data

Backend URL unavailable

Check http://127.0.0.1:8000/health

edges_file_name not found

Wrong file name used

Copy exact edge CSV name from results/tracking

HTTPValidationError

Required parameter missing or wrong

Check URL path and query parameters

Empty graph

No edge data found

Run tracking first or increase parameters

Etherscan crawl failed

API key/rate issue

Check .env and API limit

Port already used

Another server is running

Kill process or change port

Kill Used Backend Port on Windows

netstat -ano | findstr :8000
taskkill /PID PID_NUMBER /F

Kill Used Frontend Port on Windows

netstat -ano | findstr :3000
taskkill /PID PID_NUMBER /F

🧾 Responsible Use

This system is intended for academic research, AML analysis, blockchain forensics education and responsible investigation support.

It should not be used to accuse any real person or organization without verified external evidence. A service match, risk score or transaction path is an investigative signal, not a final legal conclusion.

👩‍💻 Project Author

Sayaka Alam
Department of Computer Science and Engineering
Khulna University of Engineering & Technology
GitHub: SayakaMeem

<div align="center">

⭐ If this project helps, consider starring the repository.

EthereumHeist AML System — turning complex blockchain trails into readable forensic evidence.

</div>
