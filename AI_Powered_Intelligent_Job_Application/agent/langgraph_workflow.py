# agent/langgraph_workflow.py
"""
LangGraph StateGraph wiring for the flow:
START -> fetch_jd_node -> parse_jd_node -> generate_node -> format_node -> END

This is a skeleton. Each node is a function that reads/writes to the graph state.
"""
from langgraph.graph import StateGraph, START, END
from langgraph.states import DictState

from backend.app.services.jd_fetcher import fetch_jd_from_linkedin
from backend.app.services.genai import generate_resume_and_cover
from backend.app.config import settings

def fetch_jd_node(state: DictState):
    # state expected to contain: job_url or jd_text and optionally linkedin creds
    if state.get("jd_text"):
        return {"jd_text": state["jd_text"]}
    if state.get("job_url"):
        # uses settings creds — ensure you run locally
        jd = fetch_jd_from_linkedin(state["job_url"], settings.LINKEDIN_EMAIL, settings.LINKEDIN_PASSWORD)
        return {"jd_text": jd}
    return {"jd_text": ""}

def generate_node(state: DictState):
    user_profile = state.get("user_profile", {})
    jd_text = state.get("jd_text", "")
    output = generate_resume_and_cover(user_profile=user_profile, jd_text=jd_text)
    return {"gen_output": output}

def format_node(state: DictState):
    # For MVP we simply forward the gen output. You can implement DOCX/PDF generation here.
    return {"artifacts": state.get("gen_output")}

def build_and_run_graph(initial_state: dict):
    graph = StateGraph(DictState)
    graph.add_node(fetch_jd_node)
    graph.add_node(generate_node)
    graph.add_node(format_node)

    graph.add_edge(START, "fetch_jd_node")
    graph.add_edge("fetch_jd_node", "generate_node")
    graph.add_edge("generate_node", "format_node")
    graph.add_edge("format_node", END)

    graph = graph.compile()
    result = graph.invoke(initial_state)
    return result
