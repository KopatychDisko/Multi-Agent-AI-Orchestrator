from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser

from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_experimental.tools.python.tool import PythonREPLTool

from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import create_react_agent
from langgraph.constants import END, START

from pydantic import BaseModel, Field
from typing import Literal, Annotated, List, TypedDict

from getpass import getpass
from os import environ, getcwd

import functools

