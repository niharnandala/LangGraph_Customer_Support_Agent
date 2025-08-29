# langgraph_customer_support_agent.py

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# -------------------------
# State definition
# -------------------------
class State(TypedDict):
    customer_name: str
    email: str
    query: str
    priority: str
    ticket_id: str
    parser: dict
    entities: dict
    messages: Annotated[list, add_messages]
    kb_info: str
    solution_score: int
    escalation: str
    decision_record: dict
    ticket_status: str
    last_updated: str
    response: str

# -------------------------
# Mock MCPs
# -------------------------
class CommonMCP:
    @staticmethod
    def solution_evaluation(state: State) -> int:
        # mock scoring: always 95 for demo
        return 95

    @staticmethod
    def parse_request_text(state: State) -> dict:
        # mock parse: return structured dict from query
        return {"intent": "product_issue", "details": "repair" }

    @staticmethod
    def normalize_fields(state: State):
        # mock normalization
        return {"query": state["query"].strip()}

    @staticmethod
    def add_flags_calculations(state: State):
        # mock flags
        return {"priority_flag": state["priority"]}

    @staticmethod
    def response_generation(state: State):
        return f"Dear {state['customer_name']}, your ticket {state['ticket_id']} has been processed."

common_mcp = CommonMCP()

class AtlasMCP:
    @staticmethod
    def extract_entities(state: State) -> dict:
        # mock entity extraction
        return {"account_id": "A123", "product_id": "P456"}

    @staticmethod
    def clarify_question(state: State) -> str:
        return "Please provide missing info."

    @staticmethod
    def extract_answer(state: State) -> str:
        return "Repair instructions: visit nearest service center."

    @staticmethod
    def store_answer(state: State) -> dict:
        return {"answer": "Stored in system"}

    @staticmethod
    def knowledge_base_search(state: State) -> str:
        return "KB Result: Laptop repair policy"

    @staticmethod
    def store_data(state: State) -> dict:
        return {"kb_data": "Stored in payload"}

    @staticmethod
    def escalation_decision(state: State) -> str:
        return "Escalated to human agent"

    @staticmethod
    def update_ticket(state: State):
        state["ticket_status"] = "Resolved"
        state["last_updated"] = "now"

    @staticmethod
    def close_ticket(state: State):
        state["ticket_status"] = "Closed"

    @staticmethod
    def execute_api_calls(state: State):
        return "API executed"

    @staticmethod
    def trigger_notifications(state: State):
        return "Customer notified"

atlas_mcp = AtlasMCP()

# -------------------------
# Stage Nodes
# -------------------------
def accept_payload(state: State) -> State:
    # just return state, assuming payload already filled
    return state

def understand(state: State) -> State:
    parsed = common_mcp.parse_request_text(state)
    entities = atlas_mcp.extract_entities(state)
    state.update(parsed)
    state["parser"] = parsed        # <--- explicitly add parser key
    state.update(entities)
    state["entities"] = entities    # <--- explicitly add entities key
    return state

def prepare(state: State) -> State:
    state.update(common_mcp.normalize_fields(state))
    state.update(common_mcp.add_flags_calculations(state))
    return state

def ask(state: State) -> State:
    state["messages"].append(atlas_mcp.clarify_question(state))
    return state

def wait(state: State) -> State:
    ans = atlas_mcp.extract_answer(state)
    atlas_mcp.store_answer(state)
    state["response"] = ans
    return state

def retrieve(state: State) -> State:
    kb = atlas_mcp.knowledge_base_search(state)
    atlas_mcp.store_data(state)
    state["kb_info"] = kb
    return state

def decide(state: State) -> State:
    score = common_mcp.solution_evaluation(state)
    state["solution_score"] = score
    if score < 90:
        state["escalation"] = atlas_mcp.escalation_decision(state)
    else:
        state["escalation"] = None
    state["decision_record"] = {"score": score, "escalation": state["escalation"]}
    return state

def update(state: State) -> State:
    atlas_mcp.update_ticket(state)
    atlas_mcp.close_ticket(state)
    return state

def create(state: State) -> State:
    state["response"] = common_mcp.response_generation(state)
    return state

def do_stage(state: State) -> State:
    atlas_mcp.execute_api_calls(state)
    atlas_mcp.trigger_notifications(state)
    return state

def complete(state: State) -> State:
    """
    Stage 11: COMPLETE (Payload Output Only)
    - Print the final structured payload
    """
    print("\n[COMPLETE] Final Payload:")
    for k, v in state.items():
        print(f"{k}: {v}")
    return state

# -------------------------
# Graph setup
# -------------------------
graph = StateGraph(State)

# add nodes
graph.add_node("intake", accept_payload)
graph.add_node("understand", understand)
graph.add_node("prepare", prepare)
graph.add_node("ask", ask)
graph.add_node("wait", wait)
graph.add_node("retrieve", retrieve)
graph.add_node("decide", decide)
graph.add_node("update", update)
graph.add_node("create", create)
graph.add_node("do_stage", do_stage)
graph.add_node("complete", complete)


# add edges
graph.add_edge(START, "intake")
graph.add_edge("intake", "understand")
graph.add_edge("understand", "prepare")
graph.add_edge("prepare", "ask")
graph.add_edge("ask", "wait")
graph.add_edge("wait", "retrieve")
graph.add_edge("retrieve", "decide")
# conditional edge from decide
graph.add_conditional_edges(
    "decide",
    lambda state: "update" if state["solution_score"] >= 90 else "ask"
)
graph.add_edge("update", "create")
graph.add_edge("create", "do_stage")
graph.add_edge("do_stage", "complete")
graph.add_edge("complete", END)

# entry & finish
graph.set_entry_point("intake")
graph.set_finish_point("complete")

# -------------------------
# Run graph with sample payload
# -------------------------
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

compiled_graph = graph.compile()
final_state = compiled_graph.invoke(sample_state)

print("\nFinal State:")
print(final_state)
