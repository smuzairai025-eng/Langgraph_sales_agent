from langchain_openai import ChatOpenAI
from pydantic import BaseModel,Field
from .prompts import ROUTER_SYSTEM
from .state import AgentState
from dotenv import load_dotenv
from typing import Literal
load_dotenv()

class RouterResponse(BaseModel):
    intent :Literal["inquiry","informative","objection","irrelevant"]=Field(description="One of: inquiry, informative, objection, irrelevant")

def route_response(state : AgentState):
    model=ChatOpenAI(model='gpt-4o-mini')
    structured_model=model.with_structured_output(RouterResponse)

    last_msg=state['messages'][-1]
    response=structured_model.invoke([
        ("system", ROUTER_SYSTEM),
        ("human", last_msg.content)
        ])
    
    return {'intent':[response.intent]}

def check_profile_status(state :AgentState):
     profile=state.get("profile",{})
     if (profile.get("industry") and
         profile.get("website") and
         profile.get("customer_size")):
          return "pitch_node"
     return "end"

def get_next_node(state: AgentState):
        intent = state.get("intent")
        print(intent)
        if intent == ["inquiry"]: return "expert"
        if intent == ["informative"]: return "profiler"
        if intent == ["objection"]: return "objection"
        return ["chitchat"]