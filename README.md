# OpsPilot AI

**Multi-Agent AI-Powered Business Operations & Order Fulfillment Platform**

OpsPilot AI is a full-stack portfolio project that demonstrates how AI agents, deterministic business logic, retrieval-augmented generation (RAG), and human approvals can work together to analyze customer orders and propose fulfillment plans.

The application operates in a fictional business environment called **Northstar Electronics**.

## Key Features

- **Natural Language Order Processing:** Extract product, quantity, budget, and deadline information from customer requests using Claude.
- **Multi-Step AI Orchestration:** Coordinate request extraction, product identification, inventory checking, supplier lookup, fulfillment planning, and policy evaluation using LangGraph.
- **Warehouse-First Fulfillment:** Allocate available warehouse stock before using external supplier inventory.
- **Pricing & Budget Evaluation:** Calculate order subtotals and compare them against customer budgets.
- **RAG Policy Retrieval:** Retrieve relevant business policy excerpts using ChromaDB and SentenceTransformer embeddings.
- **Policy Enforcement:** Apply deterministic rules for inventory sufficiency, manager authorization, customer confirmation, and human review.
- **Human-in-the-Loop Approval:** Save eligible order proposals in SQLite and approve or reject them through the React dashboard.
- **MCP Integration:** Expose an inventory lookup through an MCP server and client for use by the LangGraph inventory node.
- **Inventory Management:** View warehouse stock and supplier availability.
- **Policy Search:** Search business policies using natural-language questions.

## Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React, TypeScript, Vite, Tailwind CSS |
| Backend | Python, FastAPI, Pydantic |
| AI | Anthropic Claude API |
| Workflow Orchestration | LangGraph |
| Tool Integration | Model Context Protocol (MCP) |
| RAG | ChromaDB, SentenceTransformers |
| Database | SQLite, SQLAlchemy |
| Testing | pytest, TypeScript, ESLint |

## Architecture

```text
React + TypeScript
        |
        v
     FastAPI
        |
        v
 LangGraph Workflow
        |
        +-- Request Extraction (Claude)
        |
        +-- Product Lookup (SQLite)
        |
        +-- Inventory Node
        |        |
        |        v
        |    MCP Client
        |        |
        |        v
        |    MCP Server
        |        |
        |        v
        |    Inventory Tool (SQLite)
        |
        +-- Supplier Lookup (SQLite)
        |
        +-- Fulfillment Planning
        |
        +-- Pricing and Budget Evaluation
        |
        +-- RAG Policy Retrieval (ChromaDB)
        |
        +-- Deterministic Policy Enforcement
        |
        v
   Order Proposal
        |
        v
 Human Approval / Rejection
        |
        v
 SQLite Persistence
```

## Example Workflow

A customer submits:

> I need 25 High-End Laptop units with a budget of $40,000.

Using the seeded demonstration database, OpsPilot AI can produce:

| Detail | Example Result |
|---|---|
| Requested units | 25 |
| Houston warehouse allocation | 12 |
| Dallas warehouse allocation | 8 |
| Supplier allocation | 5 |
| Unit selling price | $1,500 |
| Order subtotal | $37,500 |
| Customer budget | $40,000 |
| Budget evaluation | Within budget |
| Supplier procurement cost | $3,100 |
| Manager approval required | No |
| Human approval required | Yes |

These are proposed allocations, not inventory reservations or confirmed deliveries.

## Project Structure

```text
opspilot-ai/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── ai/
│   │   ├── api/
│   │   ├── database/
│   │   ├── mcp/
│   │   ├── rag/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── tools/
│   │   ├── workflows/
│   │   └── main.py
│   ├── data/
│   │   └── policies/
│   │       └── fulfillment_policy.md
│   ├── scripts/
│   ├── requirements.txt
│   └── requirements-lock.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── types/
│   │   └── App.tsx
│   └── package.json
├── .gitignore
└── README.md
```

## Local Setup

### Prerequisites

- Python (developed with Python 3.14)
- Node.js and npm
- Anthropic API key

### 1. Clone the repository

```bash
git clone https://github.com/devsadh-sde/opspilot-ai.git
cd opspilot-ai
```

### 2. Configure the backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Create a `backend/.env` file and add:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

Do not commit actual API keys.

### 3. Initialize the database

From the `backend` directory:

```bash
python -m app.database.seed
```

This populates the local demonstration database with product, warehouse, inventory, supplier, and supplier-offer records.

### 4. Build the policy knowledge base

From the `backend` directory:

```bash
python -m app.rag.policy_ingestion
```

This generates embeddings for the policy document and stores them in the local ChromaDB collection.

### 5. Start FastAPI

```bash
uvicorn app.main:app --reload
```

Backend API documentation:

http://127.0.0.1:8000/docs

### 6. Start React

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

http://localhost:5173

## API Overview

| Method | Endpoint | Description |
|---|---|---|
| POST | `/requests/analyze` | Analyze a natural-language customer request |
| POST | `/orders/proposals` | Analyze and save an eligible proposal |
| GET | `/orders/proposals` | List saved proposals |
| GET | `/orders/proposals/{id}` | Retrieve saved proposal details |
| POST | `/orders/proposals/{id}/review` | Approve or reject a pending proposal |
| GET | `/inventory/{product_id}` | Retrieve warehouse inventory |
| GET | `/suppliers/{product_id}` | Retrieve supplier availability |
| POST | `/policies/search` | Retrieve relevant policy excerpts |
| GET | `/health` | Health check |

## Testing

Backend:

```bash
cd backend
python -m pytest -q
python -m scripts.test_mcp
```

Frontend:

```bash
cd frontend
npm run lint
npm run build
```

Some manually executed backend scripts may call the Claude API and incur usage charges.

## Limitations

OpsPilot AI is a demonstration application and is not production-ready.

- Approving a proposal changes its status but does not reserve inventory, charge customers, or execute supplier purchases.
- Delivery feasibility is not fully verified against carrier transit estimates.
- The demonstration database contains limited seeded business data.
- Proposal review does not currently include production-grade authentication and authorization.
- The current implementation may rerun AI analysis when saving a proposal.
- MCP communication uses a local subprocess-based implementation.

## Future Improvements

- Role-based access control and approval audit trails
- Delivery-date feasibility validation
- Persistent MCP sessions and more MCP tools
- Additional products and suppliers
- Stronger automated integration testing
- Asynchronous processing and workflow monitoring
- Deployment using containers and cloud infrastructure

## Project Purpose

OpsPilot AI demonstrates practical integration of full-stack software development, AI-assisted request understanding, workflow orchestration, database-backed business logic, retrieval-augmented generation, and human-in-the-loop decision-making.

**Built as a software engineering and AI engineering portfolio project.**
