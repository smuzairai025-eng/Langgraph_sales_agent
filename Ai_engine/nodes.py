from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
from .prompts import PITCH_SYSTEM,PROFILER_SYSTEM,EXPERT_SYSTEM
from .rag_service import get_retriever
from .state import AgentState
from langgraph.graph import StateGraph
from dotenv import load_dotenv

load_dotenv()

model=ChatOpenAI(model='gpt-4o-mini')

def profiler_node(state:AgentState):

    profile_str=str(state.get("profile",{}))
    messages = [("system", PROFILER_SYSTEM.format(user_profile=profile_str))] + state['messages']
    response=model.invoke(messages)
    return {"messages":[response]}

def expert_node(state: AgentState):
    last_msg=state["messages"][-1].content
    retriever=get_retriever()
    docs=retriever.invoke(last_msg)
    context_text="\n".join([d.page_content for d in docs])
    system_prompt=EXPERT_SYSTEM.format(context=context_text)
    response=model.invoke([
        ("system",system_prompt),
        ("human",last_msg)
    ])
    return {"messages":[response]}

def objection_node(state:AgentState):
    return {"messages":[("ai", "I understand. No problem at all. Let us know if you change your mind!")]}

def irrelevant_node(state:AgentState):
     return {"messages":[("ai", "I'm just a sales bot! Let's talk about your business website.")]}
