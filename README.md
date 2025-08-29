# Lang Graph Customer Support Agent

A stage-based AI agent for customer support workflows, built using **Lang Graph** and MCP (Model Context Protocol) clients. This project demonstrates **deterministic and non-deterministic stage orchestration**, state persistence across nodes, and integration of multiple MCP modules for intelligent query handling.

---

## 🚀 Project Overview

This project implements a **stage-wise AI agent** that can:

* Accept and parse customer queries
* Extract relevant entities
* Search knowledge bases
* Evaluate solutions
* Escalate or resolve tickets
* Generate responses automatically

The agent uses **Lang Graph** to model the workflow as a **graph of stages**, where each stage is a node acting on a shared state. The agent demonstrates **deterministic stages** (nodes executed in sequence) and **non-deterministic stages** (nodes executed conditionally based on state).

The **MCP (Model Context Protocol)** modules (`CommonMCP` and `AtlasMCP`) act as mini-services handling parsing, entity extraction, scoring, KB search, and response generation. By calling MCPs inside nodes, we ensure modular, reusable, and testable logic for each stage.

---

## 🧩 Key Components

### 1. **State Definition**

The `State` TypedDict holds all shared variables such as `customer_name`, `email`, `query`, `parser`, `entities`, `messages`, `solution_score`, `ticket_status`, and more. This allows **persistent state across all stages**.

### 2. **MCP Modules**

* **CommonMCP**: Handles parsing, normalization, scoring, and response generation.
* **AtlasMCP**: Handles entity extraction, KB search, escalation, ticket updates, and notifications.

MCP calls are made inside nodes to keep logic **modular and reusable**.

### 3. **Stage Nodes**

The project has 11 stages, including:

1. **Accept Payload** – Entry stage to ingest the customer query.
2. **Understand** – Parse the query and extract entities.
3. **Prepare** – Normalize fields and calculate flags.
4. **Ask** – Ask for missing information if needed.
5. **Wait** – Wait for customer input and extract answers.
6. **Retrieve** – Search KB and store relevant information.
7. **Decide** – Evaluate solution score and decide on escalation.
8. **Update** – Update or close the ticket.
9. **Create** – Generate final response.
10. **Do Stage** – Execute APIs and notifications.
11. **Complete** – Print final structured payload.

> Deterministic stages run sequentially (like `accept_payload` → `understand`).
> Non-deterministic stages use conditional edges (like `decide` → `update` or back to `ask` depending on `solution_score`).

### 4. **Graph Orchestration**

* Nodes are connected using `add_edge` and `add_conditional_edges`.
* Entry point: `intake`
* Finish point: `complete`

The graph is compiled into a `CompiledStateGraph` object, which can be invoked with a sample payload.

---

## 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/niharnandala/LangGraph_Customer_Support_Agent.git
cd LangGraph_Customer_Support_Agent
```

2. Create virtual environment and install dependencies:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. Run the agent:

```bash
python langgrpah_customer_support_agent.py
```

---

## 💡 Sample Payload

```python
sample_state = State(
    customer_name="John Doe",
    email="john@example.com",
    query="My laptop screen flickers occasionally, and the warranty is about to expire. Please advise how to get it repaired.",
    priority="High",
    ticket_id="T12345",
    messages=[],
    solution_score=0,
    escalation=None,
    decision_record={},
    ticket_status="Open",
    last_updated="",
    response=""
)
```

---

## 🔧 Features

* Stage-based workflow modeling
* Deterministic & non-deterministic execution
* Persistent state across nodes
* MCP integration for modular logic
* Automatic ticket handling and response generation

---

## 📹 Demo Video

A short walkthrough explains:

* Stage modeling
* State persistence
* Sample query execution flow

📎 **Video link:** https://drive.google.com/file/d/1r5mhqHVEB0zQ_5iP61uRxSCjKYJy7iLd/view?usp=sharing

---

## ✉️ Submission

Send to: `santosh.thota@analytos.ai`
Cc: `shashwat.shlok@analytos.ai`, `sasidhar.sunkesula@analytos.ai`
Subject: `Lang Graph Agent Task – <Your Name>`

---

## ⚡ Notes

* The agent is **highly modular**, making it easy to extend with new stages or MCP services.
* Uses **first-principle thinking**: every stage focuses on a single responsibility and reuses logic through MCP calls.
* Built to handle **real-world support queries** and escalations intelligently.
