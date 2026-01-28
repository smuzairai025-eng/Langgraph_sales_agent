from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
from .prompts import PITCH_SYSTEM,PROFILER_SYSTEM,EXPERT_SYSTEM
from .rag_service import get_retriever
from .state import AgentState
from langgraph.graph import StateGraph,START,END
from .router import route_response,get_next_node
from .nodes import expert_node,profiler_node,objection_node,irrelevant_node
from dotenv import load_dotenv

load_dotenv()

model=ChatOpenAI(model='gpt-4o-mini')

def build_workflow():
    
    graph=StateGraph(AgentState)

    graph.add_node("router", route_response)
    graph.add_node("profiler",profiler_node)
    graph.add_node("expert",expert_node)
    graph.add_node("objection",objection_node)
    graph.add_node("chitchat",irrelevant_node)

    graph.add_edge(START,"router")
    graph.add_conditional_edges("router",get_next_node,
    {
        "profiler":"profiler",
        "expert":"expert",
        "objection":"objection",
        "chitchat":"chitchat",

    })
    graph.add_edge("profiler",END)
    graph.add_edge("expert",END)
    graph.add_edge("objection",END)
    graph.add_edge("chitchat",END)

    return graph.compile()

agent=build_workflow()


