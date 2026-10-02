# 🏦 Corporate Financial Analyst & Decision Engine

> **An AI-powered financial analysis and decision-support engine for corporate financial statements.**

A backend-first financial analytics platform built with **FastAPI, PostgreSQL/SQLAlchemy, FAISS, Sentence Transformers, and Google Gemini**.

The system ingests corporate financial statements from Excel/PDF files, standardizes financial line items, calculates financial ratios and valuation metrics, performs capital budgeting and working-capital analysis, runs scenario/stress tests, generates financial recommendations, and provides an AI-powered financial Copilot grounded in the company's financial data.

---

## 🚀 What Does This Project Do?

The **Corporate Financial Analyst & Decision Engine** is designed to bring several corporate-finance workflows into a single analytical system.

### 📥 Financial Statement Ingestion

Upload financial statements and automatically:

* Parse Excel financial statements
* Extract relevant financial line items
* Parse PDF financial documents
* Standardize inconsistent financial terminology
* Validate financial data
* Store normalized financial information in the database

### 📊 Financial Analysis

The engine currently supports:

* Financial ratio analysis
* WACC calculation
* Capital budgeting
* Working-capital analysis
* Financial health scoring
* Scenario analysis
* Stress testing
* Financial recommendations

### 🤖 AI Financial Copilot

The project includes a Retrieval-Augmented Generation (RAG) based financial Copilot.

The Copilot:

1. Retrieves relevant financial information
2. Converts financial facts into embeddings
3. Performs vector similarity search using FAISS
4. Provides the retrieved context to Gemini
5. Generates a grounded financial response

The Copilot is explicitly instructed to avoid inventing information when the retrieved context is insufficient.

---

# ✨ Key Features

| Module                    | Description                                               |
| ------------------------- | --------------------------------------------------------- |
| 📥 Statement Ingestion    | Excel/PDF financial statement ingestion                   |
| 🧹 Data Standardization   | Maps inconsistent financial labels to standardized labels |
| 📊 Ratio Analysis         | Calculates key financial ratios                           |
| 💰 WACC                   | Weighted Average Cost of Capital analysis                 |
| 📈 Capital Budgeting      | NPV and related investment analysis                       |
| 🔄 Working Capital        | Working-capital and cash-conversion analysis              |
| 🧪 Stress Testing         | Financial scenario and stress testing                     |
| 🎲 Monte Carlo            | Probabilistic financial analysis                          |
| ❤️ Financial Health Score | Composite financial-health assessment                     |
| 💡 Recommendations        | Generates financial recommendations                       |
| 🤖 AI Copilot             | RAG-based financial question answering                    |
| 🔎 Disclosure Scanner     | Extracts narrative/disclosure information                 |
| 📝 AI Memo Generator      | Generates financial-analysis memos                        |
| 🧠 Embeddings             | Local Sentence Transformer embeddings                     |
| 🗂️ Vector Search         | FAISS-based similarity search                             |
| 🔐 Company Ownership      | Company-level access verification                         |

---

# 🧠 System Architecture

```text
                         ┌──────────────────────┐
                         │      User / API      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │      REST API        │
                         └──────────┬───────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
        ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
        │   Ingestion   │ │ Analysis Engine│ │  AI / GenAI    │
        │     Layer     │ │                │ │     Layer      │
        └───────┬────────┘ └───────┬────────┘ └───────┬────────┘
                │                  │                  │
                ▼                  ▼                  ▼
        ┌───────────────┐  ┌────────────────┐ ┌────────────────┐
        │ Excel / PDF   │  │ Financial      │ │ Gemini         │
        │ Parsers       │  │ Calculations   │ │ + RAG          │
        └───────┬───────┘  └───────┬────────┘ └───────┬────────┘
                │                  │                  │
                └──────────────────┼──────────────────┘
                                   ▼
                         ┌──────────────────────┐
                         │      Database        │
                         │ SQLAlchemy / DB      │
                         └──────────────────────┘

                         AI Retrieval Pipeline
                         
        Financial Facts
              │
              ▼
        Sentence Transformers
              │
              ▼
           Embeddings
              │
              ▼
             FAISS
              │
              ▼
       Relevant Financial Context
              │
              ▼
       Google Gemini 2.5 Flash
              │
              ▼
       Grounded AI Response
```

---

# 🏗️ Project Structure

```text
corp-finance-decision-engine/
│
├── backend/
│   ├── .venv/
│   ├── .env
│   ├── requirements.txt
│   │
│   └── app/
│       ├── main.py
│       ├── config.py
│       │
│       ├── api/
│       │   ├── routes_upload.py
│       │   ├── routes_ratios.py
│       │   ├── routes_capital_budgeting.py
│       │   ├── routes_wacc.py
│       │   ├── routes_working_capital.py
│       │   ├── routes_scenarios.py
│       │   ├── routes_recommendation.py
│       │   └── routes_copilot.py
│       │
│       ├── ingestion/
│       │   ├── base_parser.py
│       │   ├── excel_parser.py
│       │   ├── pdf_parser.py
│       │   ├── column_mapper.py
│       │   └── validators.py
│       │
│       ├── engine/
│       │   ├── base_module.py
│       │   ├── ratios.py
│       │   ├── wacc.py
│       │   ├── capital_budgeting.py
│       │   ├── working_capital.py
│       │   ├── monte_carlo.py
│       │   ├── stress_testing.py
│       │   ├── health_score.py
│       │   └── recommendation.py
│       │
│       ├── genai/
│       │   ├── copilot_qa.py
│       │   ├── memo_generator.py
│       │   ├── disclosure_scanner.py
│       │   ├── mapping_assist.py
│       │   ├── embeddings.py
│       │   └── vector_store.py
│       │
│       ├── models/
│       │   ├── base.py
│       │   ├── company.py
│       │   ├── statement.py
│       │   ├── line_item.py
│       │   ├── ratio_snapshot.py
│       │   ├── scenario.py
│       │   ├── recommendation.py
│       │   ├── user.py
│       │   └── copilot_session.py
│       │
│       ├── schemas/
│       │   ├── copilot_schema.py
│       │   └── scenario_schema.py
│       │
│       ├── repositories/
│       │   ├── base_repository.py
│       │   ├── company_repository.py
│       │   ├── statement_repository.py
│       │   ├── line_item_repository.py
│       │   ├── recommendation_repository.py
│       │   ├── scenario_repository.py
│       │   └── user_repository.py
│       │
│       ├── services/
│       │   ├── ingestion_service.py
│       │   ├── analysis_service.py
│       │   ├── recommendation_service.py
│       │   └── copilot_service.py
│       │
│       └── db/
│           ├── session.py
│           ├── init_db.py
│           └── migrations/
│
├── frontend/
│   └── components/
│       ├── capital_budget.py
│       ├── copilot_workspace.py
│       ├── executive_pulse.py
│       ├── live_market.py
│       ├── ratio_analytics.py
│       ├── stress_monte_carlo.py
│       └── wacc_optimizer.py
│
│
├── data/
│   └── sample_statements/
│       ├── test_balance_sheet_FY2025.xlsx
│       ├── test_balance_sheet_FY2025.pdf
│       └── test_balance_sheet_complete_FY2025.xlsx
│

```

---

# ⚙️ Technology Stack

### Backend

* **Python 3.12**
* **FastAPI**
* **SQLAlchemy**
* **Pydantic**
* **Uvicorn**

### Financial Analytics

* Python numerical/data-analysis ecosystem
* Custom financial calculation engines
* Financial ratio analysis
* WACC
* NPV / capital budgeting
* Working capital
* Monte Carlo simulation
* Stress testing

### AI / GenAI

* **Google Gemini 2.5 Flash**
* **LangChain Google GenAI**
* **Sentence Transformers**
* **FAISS**
* Retrieval-Augmented Generation (RAG)

### Data

* Excel
* PDF
* SQL database
* SQLAlchemy ORM

---

# 🔌 API Endpoints

The backend currently exposes the following core routes.

### Statement Upload

```http
POST /statements/upload
```

Uploads and processes a financial statement.

---

### Ratio Analysis

```http
GET /statements/ratios/{id}
```

Runs financial-ratio analysis for a statement.

---

### Capital Budgeting

```http
GET /statements/capital_budgeting/{id}
```

Performs capital-budgeting analysis.

---

### WACC

```http
GET /statements/WACC/{id}
```

Calculates the company's Weighted Average Cost of Capital.

---

### Working Capital

```http
GET /statements/Working_Capital/{id}
```

Analyzes working-capital metrics.

---

### Stress Testing

```http
POST /statements/scenarios/stress-test
```

Runs a financial stress-test scenario.

---

### Recommendations

```http
GET /statements/recommendation/{id}
```

Retrieves financial recommendations generated by the analysis engine.

---

### Financial Copilot

```http
POST /companies/{id}/copilot
```

Allows users to ask questions about the company's available financial information.

Example request:

```json
{
    "statement_id": "statement-id",
    "question": "What are the company's total assets?"
}
```

Example response:

```json
{
    "company_id": "company-id",
    "question": "What are the company's total assets?",
    "answer": "The total assets are 2,792,249."
}
```

---

# 🤖 How the Financial Copilot Works

The Copilot uses a lightweight RAG pipeline.

```text
User Question
      │
      ▼
Question Embedding
      │
      ▼
FAISS Similarity Search
      │
      ▼
Relevant Financial Facts
      │
      ▼
Context Construction
      │
      ▼
Gemini 2.5 Flash
      │
      ▼
Grounded Financial Answer
```

Financial statement line items are converted into text facts such as:

```text
Total Assets: 2792249
Current Liabilities: 849488
Cash And Equivalents: 270518
Total Equity: 831923
```

These facts are embedded locally and indexed using FAISS.

The retrieved context is then provided to Gemini.

The Copilot is instructed to **use only the supplied financial context and explicitly acknowledge insufficient information rather than fabricate values.**

---

# 📥 Data Ingestion Pipeline

```text
Excel / PDF
     │
     ▼
Parser
     │
     ▼
Raw Financial Data
     │
     ▼
Column Mapping
     │
     ▼
Standardized Financial Labels
     │
     ▼
Validation
     │
     ▼
Database
     │
     ▼
Analysis Engine
```

The column-mapping system handles multiple representations of common financial concepts.

For example:

```text
"Cash"
"Cash in Hand"
"Cash and Cash Equivalents"
        ↓
cash_and_equivalents
```

Similarly:

```text
"Trade Payables"
"Accounts Payable"
"Creditors"
        ↓
accounts_payable
```

---

# 🧮 Financial Analysis Engine

The engine is organized into independent modules.

### Ratio Analysis

Calculates relevant liquidity, profitability, leverage, efficiency, and other financial ratios.

### WACC

Calculates:

* Cost of equity
* Cost of debt
* Capital structure
* Weighted Average Cost of Capital

### Capital Budgeting

Supports investment-analysis calculations such as:

* NPV
* Cash-flow based project analysis

### Working Capital

Analyzes:

* Current assets
* Current liabilities
* Working capital
* Cash conversion cycle
* Related operating metrics

### Stress Testing

Allows financial assumptions to be modified and tested against the company's financial position.

### Monte Carlo Simulation

Provides probabilistic analysis for uncertain financial inputs.

### Financial Health Score

Produces a consolidated financial-health indicator based on available financial metrics.

### Recommendation Engine

Acts as an orchestration layer that combines financial-analysis outputs into actionable financial recommendations.

---

# 🧪 Testing

Formal `pytest` coverage is currently **not yet implemented**.

During development, modules have been tested using:

* Python inline test scripts
* FastAPI `/docs`
* Live API requests
* Sample financial statements
* End-to-end ingestion and analysis workflows

Formal automated testing is part of the roadmap.

---

# 🗄️ Database

The project currently uses SQLAlchemy for database interaction.

The data model contains entities for:

```text
User
Company
Statement
LineItem
RatioSnapshot
Scenario
Recommendation
CopilotSession
```

Database schema migrations are **not yet configured**.

The current development workflow uses SQLAlchemy table creation/reset functionality.

> ⚠️ Production deployments should use a proper migration system such as Alembic rather than relying on `create_all()` / `drop_all()`.

---

# 🔐 Environment Variables

Create a `.env` file inside the `backend/` directory.

```env
DATABASE_URL=your_database_url
GOOGLE_API_KEY=your_google_api_key

APP_NAME=Corporate Financial Analyst
DEBUG=True
ENV=development
```

**Never commit your `.env` file or API keys to GitHub.**

Make sure `.gitignore` contains:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

---

# 🛠️ Installation & Setup

> The exact setup commands will be added here based on the project's current `requirements.txt` and environment configuration.

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd corp-finance-decision-engine
```

### 2. Create the virtual environment

```bash
cd backend

python -m venv .venv
```

### 3. Activate the virtual environment

#### Windows

```bash
.venv\Scripts\activate
```

#### macOS / Linux

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create:

```text
backend/.env
```

and add the required database and Gemini API configuration.

### 6. Initialize the database

```bash
<DB INITIALIZATION COMMAND>
```

### 7. Start the FastAPI server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 📊 Sample Data

The repository includes sample financial statements under:

```text
data/sample_statements/
```

These datasets are intended for:

* Testing ingestion
* Validating financial calculations
* Testing API endpoints
* Testing the AI Copilot
* End-to-end development

---

# 🧭 Current Status

### Backend

| Component                     | Status |
| ----------------------------- | ------ |
| FastAPI application           | ✅      |
| Financial statement ingestion | ✅      |
| Excel parser                  | ✅      |
| PDF parser                    | ✅      |
| Column standardization        | ✅      |
| Data validation               | ✅      |
| Ratio engine                  | ✅      |
| WACC engine                   | ✅      |
| Capital budgeting             | ✅      |
| Working capital               | ✅      |
| Stress testing                | ✅      |
| Recommendation engine         | ✅      |
| AI Copilot                    | ✅      |
| FAISS retrieval               | ✅      |
| Gemini integration            | ✅      |
| Formal pytest suite           | 🚧     |
| Database migrations           | 🚧     |
| Frontend                      | 🚧     |

---

# 🚧 Roadmap

The project is actively being developed.

### Phase 1 — Backend Foundation

* [x] FastAPI architecture
* [x] Database models
* [x] Repository layer
* [x] Financial statement ingestion
* [x] Financial analysis engine
* [x] Recommendation engine

### Phase 2 — AI Layer

* [x] Local embeddings
* [x] FAISS vector search
* [x] Financial Copilot
* [x] Disclosure scanner
* [x] Memo generator
* [x] Mapping assistance

### Phase 3 — Reliability

* [ ] Formal pytest test suite
* [ ] Database migrations with Alembic
* [ ] Improved error handling
* [ ] Better financial-data validation
* [ ] Improved RAG retrieval
* [ ] Structured financial-data retrieval
* [ ] Better multi-period analysis

### Phase 4 — Frontend

* [ ] Financial dashboard
* [ ] Interactive charts
* [ ] Ratio visualization
* [ ] WACC / valuation dashboard
* [ ] Scenario analysis interface
* [ ] AI Copilot interface
* [ ] Financial recommendation dashboard

### Phase 5 — Production

* [ ] Authentication and authorization hardening
* [ ] Production database configuration
* [ ] Dockerization
* [ ] CI/CD
* [ ] Automated testing pipeline
* [ ] Cloud deployment
* [ ] Observability / logging

---

# 🎯 Project Objective

The long-term objective is to build a system that can take a company's financial information and provide a unified analytical workflow:

```text
Financial Statements
        ↓
Data Extraction
        ↓
Standardization
        ↓
Financial Analysis
        ↓
Valuation / Risk / Scenario Analysis
        ↓
Recommendations
        ↓
AI Financial Copilot
        ↓
Decision Support
```

The goal is not simply to build a financial chatbot, but to combine **deterministic financial calculations with AI-assisted interpretation**.

---

# ⚠️ Current Limitations

This project is currently in active development.

Known limitations include:

* Formal automated test coverage is not yet implemented.
* Database migrations are not yet configured.
* Frontend development is still pending.
* Some GenAI modules are built but not fully integrated into the ingestion workflow.
* Copilot retrieval is currently based on semantic similarity and can be improved for complex multi-line financial questions.
* Some engine modules still require additional `None`/missing-data hardening.
* The system is currently intended primarily for development and experimentation rather than production financial decision-making.

---

# 👨‍💻 Development Philosophy

The system follows a layered architecture:

```text
API
 │
 ▼
Services
 │
 ▼
Repositories
 │
 ▼
Database

         +

Ingestion
 │
 ▼
Financial Engine
 │
 ▼
Recommendations

         +

GenAI
 │
 ▼
Embeddings
 │
 ▼
Vector Retrieval
 │
 ▼
LLM
```

This separation makes individual components easier to test, replace, and extend.

---

# 📌 Disclaimer

This project is intended for **educational, research, and software-engineering experimentation**.

Financial calculations and AI-generated analysis should be independently verified before being used for real investment, lending, valuation, or corporate-finance decisions.

---

## ⭐ Future Vision

The eventual goal is to evolve this into a complete **AI-assisted corporate-finance analytics platform** combining:

**Financial Data → Quantitative Analysis → Scenario Modeling → AI Interpretation → Decision Support**

If you find the project interesting, feel free to explore the codebase, experiment with the sample statements, and contribute ideas for improving the financial-analysis and AI layers.
