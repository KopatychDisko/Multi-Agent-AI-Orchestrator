from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser

from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_experimental.tools.python.tool import PythonREPLTool

from langgraph.prebuilt import create_react_agent

from app.prompt import system_supervisor_prompt, system_coder_prompt
from app.config import base_url

import app.schema as sh
import functools


gpt_4_mini = ChatOpenAI(base_url=base_url, model='openai/gpt-4o-mini', temperature=0)

deepseek = ChatOpenAI(base_url=base_url, model='deepseek/deepseek-chat-v3-0324:free', temperature=0)

def supervisor_node(state):
    supervisor_prompt = ChatPromptTemplate([
    ('system', system_supervisor_prompt),
    MessagesPlaceholder(variable_name='messages'),
    ('system', "Given the conversation above, who should act next? "
            "Or should we FINISH? Select one of: {options}")
    ]).partial(options=str(sh.members), members=sh.members)

    supervisor = supervisor_prompt | gpt_4_mini.with_structured_output(sh.Supervisor)
    
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

python_exex = PythonREPLTool()

coder_agent = create_react_agent(
    model=deepseek,
    prompt=system_coder_prompt,
    tools=[python_exex]
)

coder_node = functools.partial(agent_node, agent=coder_agent, name='coder_agent')
tavily_search = TavilySearch(max_results=5)

research_agent = create_react_agent(
    model=deepseek,
    tools=[tavily_search]
)

research_node = functools.partial(agent_node, agent=research_agent, name='research_agent')

def answer_node(state):
    answer_prompt = ChatPromptTemplate([
        ('system', 'You are summarize all context and give user answer with his query.'),
        MessagesPlaceholder(variable_name='messages'),
        ('system', 'With this context answer to user useful information. Without talk what do agents - just answer')
    ])
    
    answer_agent = answer_prompt | gpt_4_mini | StrOutputParser()
    
    responce = answer_agent.invoke(state['messages'])
    
    return {'message_for_user': responce}