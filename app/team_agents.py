from langchain_core.messages import HumanMessage

from langgraph.graph import StateGraph
from langgraph.constants import END
from app.schema import State, members

from app.agents import supervisor_node, files_node, coder_node, research_node, answer_node


def router(state: State):
    return state['next_agent']

graph = StateGraph(State)

graph.add_node('supervisor', supervisor_node)
graph.add_node('files_agent', files_node)
graph.add_node('coder_agent', coder_node)
graph.add_node('research_agent', research_node)
graph.add_node('answer_agent', answer_node)

for m in members:
    if m != 'answer_agent':
        graph.add_edge(m, 'supervisor')

conditional_map = {m: m for m in members}

graph.add_conditional_edges('supervisor', router, conditional_map)

graph.set_entry_point('supervisor')

graph.add_edge('answer_agent', END)

app = graph.compile()

def invoke_graph(message: str):
    temp_state = State(messages=HumanMessage(message))

    for step in app.stream(temp_state, stream_mode='values'):
        for k, v in step.items():
            if k != "__end__":
                print('==============')
                print(v)