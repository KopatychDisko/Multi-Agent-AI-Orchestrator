from app.team_agents import invoke_graph
from app.config import get_api

if __name__ == '__main__':
    get_api()
    while 1:
        print('=' * 20)
        invoke_graph(input('How can i help you?\n'))