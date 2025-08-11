from pydantic import BaseModel
from typing import Literal

from langgraph.graph import MessagesState

members = ['coder_agent', 'files_agent', 'research_agent', 'answer_agent']

class Supervisor(BaseModel):
    next_agent: Literal[*members]
    prompt: str

class State(MessagesState):
    next_agent: str
    prompt: str
    
    message_for_user: str