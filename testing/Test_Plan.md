# EthereumHeist AML System
# Software Test Plan


## 1. Introduction

EthereumHeist is an AML investigation platform designed to analyze
Ethereum transactions, detect suspicious activity, perform multi-hop
transaction tracing, and generate investigation evidence.


## 2. Testing Objective

The objective of testing is to ensure:

- Correct transaction analysis
- Accurate risk scoring
- Reliable API responses
- Database consistency
- Proper error handling
- Stable frontend-backend communication


## 3. Testing Scope


### Included

- User interface testing
- API testing
- Database testing
- Functional testing
- Regression testing
- Error handling testing


### Excluded

- Blockchain network security audit
- Performance stress testing


## 4. Testing Types


### Functional Testing

Verify that all system features work according to requirements.


### Regression Testing

Verify that new changes do not break existing functionality.


### API Testing

Validate REST API endpoints and responses.


### Database Testing

Verify data storage and retrieval accuracy.


## 5. Testing Environment


Operating System:
Windows 10


Backend:
FastAPI


Frontend:
Next.js


Database:
DuckDB / SQL


Tools:

- Postman
- Browser Developer Tools
- SQL Client
- Jira (Bug Tracking)