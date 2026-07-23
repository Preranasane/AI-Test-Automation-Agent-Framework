from typing import TypedDict, List, Any
from workflow import llm
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from pprint import pformat

# ==========================================================
# Define Agent State
# ==========================================================

class AgentState(TypedDict):
    input: Any
    analysis: str
    root_cause: str
    recommendations: str
    history: List[str]


# ==========================================================
# Prompt Templates
# ==========================================================

failure_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert Failure Analysis Engineer. Analyze the given technical issue step by step."
        ),
        (
            "human",
            "{input}"
        ),
    ]
)

root_cause_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a Root Cause Analysis specialist."
        ),
        (
            "human",
            "Based on the following failure analysis, identify the most likely root cause.\n\n{analysis}"
        ),
    ]
)

recommendation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a Reliability Engineer."
        ),
        (
            "human",
            "Given the following root cause, provide practical recommendations to prevent recurrence.\n\n{root_cause}"
        ),
    ]
)


# ==========================================================
# Node 1 - Failure Analysis
# ==========================================================

def analyze_failure(state: AgentState) -> AgentState:
    logs = pformat(state["input"])
    messages = failure_prompt.invoke(
        {
            "input": logs
        }
    )

    response = llm.invoke(messages)

    state["analysis"] = response.content
    state["history"].append("Failure Analysis Completed")

    return state


# ==========================================================
# Node 2 - Root Cause Analysis
# ==========================================================

def identify_root_cause(state: AgentState) -> AgentState:

    messages = root_cause_prompt.invoke(
        {
            "analysis": state["analysis"]
        }
    )

    response = llm.invoke(messages)

    state["root_cause"] = response.content
    state["history"].append("Root Cause Analysis Completed")

    return state


# ==========================================================
# Node 3 - Recommendations
# ==========================================================

def suggest_recommendations(state: AgentState) -> AgentState:

    messages = recommendation_prompt.invoke(
        {
            "root_cause": state["root_cause"]
        }
    )

    response = llm.invoke(messages)

    state["recommendations"] = response.content
    state["history"].append("Recommendations Generated")

    return state


# ==========================================================
# Build LangGraph Workflow
# ==========================================================

workflow = StateGraph(AgentState)

workflow.add_node("failure_analysis", analyze_failure)
workflow.add_node("root_cause_analysis", identify_root_cause)
workflow.add_node("recommendations", suggest_recommendations)

workflow.set_entry_point("failure_analysis")

workflow.add_edge("failure_analysis", "root_cause_analysis")
workflow.add_edge("root_cause_analysis", "recommendations")
workflow.add_edge("recommendations", END)

failure_analysis_agent = workflow.compile()


# ==========================================================
# Run Agent
# ==========================================================

if __name__ == "__main__":

    initial_state: AgentState = {
        "input": r"""Traceback (most recent call last):
  File "e:\Agent_workspace\AI_Agent\app.py", line 2, in <module>
    from workflow import agent
  File "e:\Agent_workspace\AI_Agent\workflow.py", line 3, in <module>
    from tools import (open_url, click, hello, fill, take_screenshot)
ImportError: cannot import name 'take_screenshot' from 'tools' (e:\Agent_workspace\AI_Agent\tools.py)""",
        "analysis": "",
        "root_cause": "",
        "recommendations": "",
        "history": [],
    }

    result = failure_analysis_agent.invoke(initial_state)

    print("\n========== FAILURE ANALYSIS REPORT ==========\n")

    print("Issue:")
    print(result["input"])

    print("\nFailure Analysis:")
    print(result["analysis"])

    print("\nRoot Cause:")
    print(result["root_cause"])

    print("\nRecommendations:")
    print(result["recommendations"])

    print("\nExecution History:")
    for step in result["history"]:
        print(f"- {step}")