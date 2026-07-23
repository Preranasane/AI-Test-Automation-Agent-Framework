from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from tools import (open_url, click, hello, fill)
from typing import TypedDict
import asyncio

class AgentState(TypedDict):
    query: str
    current_url: str
    retrieved_context: str
    result: str

llm = ChatOllama(
    model="qwen2.5:0.5b",
    temperature=0
)


tools = [open_url, click, hello, fill]
llm_withTools = llm.bind_tools(tools)
agent = create_agent(llm_withTools, tools)