from app.team_agents import invoke_graph

if __name__ == '__main__':
    while 1:
        print('=' * 20)
        invoke_graph(input('How can i help you?\n'))