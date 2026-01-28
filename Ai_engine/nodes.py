from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
from .prompts import PITCH_SYSTEM,PROFILER_SYSTEM,EXPERT_SYSTEM,OBJECTION_SYSTEM,IRRELEVANT_SYSTEM
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
    print(last_msg)
    retriever=get_retriever()
    docs=retriever.invoke(last_msg)
    context_text="\n".join([d.page_content for d in docs]) if docs else "No specific documents found"
    system_prompt=EXPERT_SYSTEM.format(context=context_text)
    response=model.invoke([
        ("system",system_prompt),
        ("human",last_msg)
    ])
    return {"messages":[response]}

def objection_node(state: AgentState):
    last_msg = state["messages"][-1].content
    # Dynamic response using LLM
    prompt = OBJECTION_SYSTEM.format(last_msg=last_msg)
    response = model.invoke([SystemMessage(content=prompt)])
    return {"messages": [response]}

def irrelevant_node(state: AgentState):
    last_msg = state["messages"][-1].content
    # Dynamic response using LLM
    prompt = IRRELEVANT_SYSTEM.format(last_msg=last_msg)
    response = model.invoke([SystemMessage(content=prompt)])
    return {"messages": [response]}

def pitch_node(state:AgentState):
    profile=state.get("profile",{})
    prompt=PITCH_SYSTEM.format(
        industry=profile.get("industry"),
        website=profile.get("website"),
        size=profile.get("customer_size")
    )
    response=model.invoke(prompt)
    return {"messages":[response]}
