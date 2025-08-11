from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_experimental.tools.python.tool import PythonREPLTool

from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import create_react_agent
from langgraph.constants import END

from pydantic import BaseModel
from typing import Literal

from config import base_url

from 

import functools

members = ['coder_agent', 'files_agent', 'research_agent']
options = ['END'] + members

class Supervisor(BaseModel):
    next_agent: Literal[*options]
    prompt: str

class State(MessagesState):
    next_agent: str
    prompt: str
    

system_prompt = '''
You are a supervisor AI managing three specialized agents with the following responsibilities:

{members}

Code Agent – writes, reviews, and fixes code  this agnet return only code. And also he can execute code
File Agent – works with files in a folder: reads, modifies, creates, or deletes files as instructed. Dont forget add context or code that neede to write
Info Agent - find info if needed for code or for query from user in Internet, do not ask how write a script
- ask only info about topic. 

Given the following user request,
respond with the worker to act next. Each worker will perform a
task and respond with their results and status. 

For Agent you need to add instruction - what he need to do with context
if you need code_agent give instruction with data.
if files_agent - not just send instruction, send also what need write to file (for example)

When finished,
respond with END.
'''


def supervisor_node(state: State):
    return supervisor.invoke(state)
def agent_node(state, agent, name):
    responce = agent.invoke({'messages': [HumanMessage(content=state['prompt'])]})

    return {'messages': [HumanMessage(content=responce['messages'][-1].content, name=name)]}
toolkit = FileManagementToolkit(root_dir='./').get_tools()

files_agent = create_react_agent(
    model=deepseek, tools=toolkit, 
    prompt='You re a FileAgent. You can read, write update files in directory with tools'
    'Dont wirte code in file or something else'
)

files_node = functools.partial(agent_node, agent=files_agent, name='files_agent')
system_prompt = ''' 
Instructions:
You must return the code snippet exactly as it.

Expected response:

def factorial(n):
    return 1 if n == 0 else n * factorial(n - 1)
'''

python_exex = PythonREPLTool()

coder_agent = create_react_agent(
    model=deepseek,
    prompt=system_prompt,
    tools=[python_exex]
)

coder_node = functools.partial(agent_node, agent=coder_agent, name='coder_agent')
tavily_search = TavilySearch(max_results=5)

research_agent = create_react_agent(
    model=deepseek,
    tools=[tavily_search]
)

research_node = functools.partial(agent_node, agent=research_agent, name='research_agent')
def router(state: State):
    return state['next_agent']
graph = StateGraph(State)

graph.add_node('supervisor', supervisor_node)
graph.add_node('files_agent', files_node)
graph.add_node('coder_agent', coder_node)
graph.add_node('research_agent', research_node)

for m in members:
    graph.add_edge(m, 'supervisor')

conditional_map = {m: m for m in members}
conditional_map['END'] = END 

graph.add_conditional_edges('supervisor', router, conditional_map)

graph.set_entry_point('supervisor')
graph.add_edge('supervisor', END)

app = graph.compile()

def invoke_graph(message: str):
    temp_state = State(messages=HumanMessage(message))

    for step in app.stream(temp_state, stream_mode='values'):
        for k, v in step.items():
            if k != "__end__":
                print('==============')
                print(v)

