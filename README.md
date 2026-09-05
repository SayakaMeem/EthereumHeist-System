<div align="center">

# 🛡️ EthereumHeist AML System

### Explainable Ethereum Fund-Flow Tracking, AML Forensics, Service Matching and Dashboard Evidence Generation

<p>
<img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
<img src="https://img.shields.io/badge/Frontend-Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white"/>
<img src="https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/UI-React-61DAFB?style=for-the-badge&logo=react&logoColor=black"/>
<img src="https://img.shields.io/badge/Database-DuckDB-orange?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Blockchain-Ethereum-3C3C3D?style=for-the-badge&logo=ethereum&logoColor=white"/>
</p>

<p>
<img src="https://img.shields.io/badge/AML-Tracking-red?style=flat-square"/>
<img src="https://img.shields.io/badge/Graph-Analysis-blueviolet?style=flat-square"/>
<img src="https://img.shields.io/badge/CSV%2FJSON-Evidence-orange?style=flat-square"/>
<img src="https://img.shields.io/badge/Service-Matching-brightgreen?style=flat-square"/>
<img src="https://img.shields.io/badge/Risk-Scoring-yellow?style=flat-square"/>
<img src="https://img.shields.io/badge/Testing-Manual%20QA-success?style=flat-square"/>
</p>

</div>


# 📌 Table of Contents

- [Project Summary](#-project-summary)
- [Why This Project Matters](#-why-this-project-matters)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Dependencies](#-dependencies)
- [System Architecture](#-system-architecture)
- [Working Flow](#-working-flow)
- [Backend Routing Flow](#-backend-routing-flow)
- [Client-Server Sequence](#-client-server-sequence)
- [Tracking Algorithm Flow](#-tracking-algorithm-flow)
- [Dataset and Evidence Flow](#-dataset-and-evidence-flow)
- [Logical Relational Data Model](#-logical-relational-data-model)
- [Folder Structure](#-folder-structure)
- [Backend API Routes](#-backend-api-routes)
- [Important Parameters](#-important-parameters)
- [Dashboard Overview](#-dashboard-overview)
- [Software Testing and Quality Assurance](#-software-testing-and-quality-assurance)
- [Installation and Setup](#-installation-and-setup)
- [Run the Software](#-run-the-software)
- [Example API Calls](#-example-api-calls)
- [Generated Output Files](#-generated-output-files)
- [Algorithmic Contribution](#-algorithmic-contribution)
- [Security and Cloud Enhancement](#-security-and-cloud-enhancement)
- [Limitations](#-limitations)
- [Future Enhancements](#-future-enhancements)
- [Troubleshooting](#-troubleshooting)
- [Responsible Use](#-responsible-use)


# 🧠 Project Summary

EthereumHeist AML System is a full-stack blockchain forensic investigation platform designed for tracking suspicious Ethereum fund movement.

The system analyzes Ethereum transaction behavior from known heist or suspicious addresses and converts raw blockchain activity into structured AML investigation evidence.

It performs:

- One-hop transaction tracking
- Multi-hop fund-flow analysis
- Candidate layering detection
- Service-provider matching
- AML risk scoring
- Graph-based visualization
- Automated evidence generation


The system does not create a new blockchain.

Instead:


The main objective is to transform complex blockchain transaction trails into readable forensic information for researchers, analysts, and investigators.



# 🎯 Why This Project Matters

Ethereum transactions are publicly available, but investigating suspicious fund movement manually is difficult.

Criminal activities may involve:

- Multiple wallet transfers
- Token swaps
- Smart contracts
- Exchanges
- Bridges
- Layering through intermediate addresses


Traditional blockchain explorers provide transaction history, but they do not automatically provide:

- Investigation paths
- Suspicious movement patterns
- Risk prioritization
- Evidence generation


EthereumHeist solves this problem by converting raw blockchain data into:

📁 CSV evidence files

📄 JSON investigation summaries

🔗 Graph-ready transaction networks

📊 Interactive dashboard visualization

🧾 Transaction-level investigation tables

🛡️ AML risk-priority outputs



# ✨ Key Features


| Feature | Description | Benefit |
|---|---|---|
| 🔍 One-hop Tracking | Tracks direct outgoing transfers from suspicious addresses | Fast initial investigation |
| 🧭 Multi-hop Tracking | Recursively follows transaction paths | Detects possible layering |
| 🪙 ETH + ERC20 Support | Handles multiple Ethereum transaction types | More complete fund analysis |
| 🧹 Beta Filtering | Removes tiny/noisy transfers | Cleaner graph generation |
| 🏦 Service Matching | Matches addresses with known services | Identifies possible endpoints |
| ⚠️ Risk Scoring | Assigns AML risk levels | Helps prioritize investigation |
| 🕸️ Graph Generation | Creates node-edge transaction networks | Enables visualization |
| 📊 Dashboard | Displays charts and evidence tables | Easier analysis |
| 🧪 Batch Experiment | Runs multiple investigation cases | Supports evaluation |
| 📦 Evidence Export | Generates CSV and JSON outputs | Reproducible analysis |



# 🧰 Technology Stack


| Layer | Technology | Purpose |
|---|---|---|
| Frontend | Next.js, React, TypeScript | Interactive dashboard |
| Backend | FastAPI, Uvicorn | REST API services |
| Data Processing | Pandas, NumPy | Transaction processing |
| Graph Processing | NetworkX, igraph | Fund-flow graph analysis |
| Database | DuckDB | Local analytical storage |
| API Communication | Axios / Fetch | Frontend-backend communication |
| Visualization | Recharts, Cytoscape | Charts and graph visualization |
| Blockchain Data | Ethereum CSV Data, Etherscan API | Transaction source |
| Testing | Postman, SQL, Browser DevTools, Jira | QA validation |

# 📦 Dependencies


## Backend Dependencies

Backend packages are available in:


| Package | Purpose |
|---|---|
| FastAPI | Backend API framework |
| Uvicorn | ASGI server |
| Pandas | CSV and transaction processing |
| NumPy | Numerical operations |
| Requests | External API communication |
| Python-dotenv | Environment configuration |
| NetworkX | Graph analysis |
| igraph | Graph processing |
| DuckDB | Local analytical database |
| PyArrow | Data processing support |
| Pydantic | Data validation |



## Frontend Dependencies


Frontend packages are available in:
# 🚀 Backend API Routes


The backend exposes REST APIs for blockchain analysis,
transaction tracking, risk evaluation, and evidence generation.


| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Check backend health |
| `/dataset/status` | GET | Check dataset availability |
| `/crawl/address/{address}` | GET | Crawl Ethereum address data |
| `/track/one-hop/{address}` | GET | Execute direct transaction tracking |
| `/track/multi-hop/{address}` | GET | Execute multi-hop fund tracking |
| `/graph/tracking/{file}` | GET | Generate graph visualization data |
| `/risk/edges/{file}` | GET | Calculate risk scores |
| `/pipeline/full/{address}` | POST | Execute complete AML pipeline |
| `/experiment/run` | POST | Run batch experiments |



# ⚙️ Important Parameters


The tracking engine uses configurable parameters
to control investigation depth and filtering.


| Parameter | Description |
|---|---|
| `max_depth` | Maximum transaction exploration depth |
| `beta` | Minimum transfer amount threshold |
| `max_edges` | Maximum number of generated edges |
| `time_window` | Transaction filtering period |
| `risk_threshold` | Suspicious activity threshold |
| `service_matching` | Enable/disable provider matching |



Example:

```json
{
 "address":"0x123456789",
 "max_depth":3,
 "beta":0.1,
 "max_edges":500
}

# ⚙️ Important Parameters

...

Example:

```json
{
 "address":"0x123456789",
 "max_depth":3,
 "beta":0.1,
 "max_edges":500
}

continue with the **Dashboard Overview** section.

Paste this next:

```markdown
# 📊 Dashboard Overview


The EthereumHeist dashboard provides an interactive investigation
environment for analyzing suspicious Ethereum transactions.


The dashboard allows analysts to:

- Submit Ethereum addresses for investigation
- Configure tracking parameters
- Monitor transaction flow
- Visualize multi-hop fund movement
- Analyze risk scores
- Review service-provider matches
- Export investigation evidence


<div align="center">

<img src="docs/dashboard.png" width="850"/>

</div>



## Dashboard Components


| Component | Description |
|---|---|
| Address Input | Accepts suspicious Ethereum wallet addresses |
| Tracking Configuration | Controls depth, threshold, and filtering parameters |
| Transaction Graph | Displays fund movement relationships |
| Risk Panel | Shows AML risk classification |
| Evidence Table | Displays analyzed transaction records |
| Export Module | Generates investigation files |



# 🧪 Software Testing and Quality Assurance


The EthereumHeist AML System was validated through manual QA practices
to ensure functional correctness, API reliability, database consistency,
and stable frontend-backend communication.


## Testing Activities


| Testing Type | Description |
|---|---|
| Functional Testing | Verified wallet analysis, transaction tracking, risk scoring, graph generation, and evidence generation workflows |
| Regression Testing | Ensured existing features remained stable after updates |
| API Testing | Tested REST API endpoints, request validation, response formats, and error handling |
| Database Testing | Verified transaction storage, retrieval accuracy, and data consistency |
| Error Handling Testing | Tested invalid inputs, missing parameters, and unexpected scenarios |



## Testing Tools


| Tool | Purpose |
|---|---|
| Postman | REST API testing and response validation |
| SQL | Database verification and data validation |
| Browser Developer Tools | Frontend debugging and network inspection |
| Jira | Bug tracking and defect management |



## QA Documentation


Detailed testing documentation is available in:

testing/

├── Test_Plan.md

├── Functional_Test_Cases.xlsx

├── API_Testing.md

├── Database_Testing.md

├── Bug_Report.md

├── Regression_Test_Report.md

├── Test_Data.md

└── Test_Summary.md




## Defect Reporting Process


All identified software issues were documented using a
standard defect management workflow.


Each bug report contains:


- Bug ID
- Issue description
- Environment details
- Steps to reproduce
- Expected result
- Actual result
- Severity level
- Priority level
- Resolution status



# 📦 Installation and Setup


## Clone Repository


```bash
git clone https://github.com/SayakaMeem/EthereumHeist-System.git

cd EthereumHeist-System
