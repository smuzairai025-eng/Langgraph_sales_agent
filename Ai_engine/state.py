from typing import TypedDict, List ,Annotated
from langgraph.graph.message import add_messages,BaseMessage
from pydantic import BaseModel,Field

class UserProfile(BaseModel):
    industry: str=Field(description="The industry in which the user operate")
    website: str=Field(description="do the user have website or not")
    customer_size: str=Field(description="Number of the customers")

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]
    profile: UserProfile
    intent: str