# a.py
import sys
from github import Github
import networkx as nx
from operator import itemgetter
from collections import Counter
from operator import itemgetter
ACCESS_TOKEN = '9fa23cb8b17d7ac53a7fdfa5b89baeb94d24029f'
USER='minrk'
REPO='findspark'
client = Github(ACCESS_TOKEN)
user = client.get_user(USER)
repo=user.get_repo(REPO)
stargazers=list(repo.get_stargazers())#加星的用户集合
g = nx.DiGraph()
g.add_node(repo.name + '(repo)', type='repo', lang=repo.language, owner=user.login)
MAX_REPOS = 500
for i, sg in enumerate(stargazers):
    print (sg.login)
    try:
        for starred in sg.get_starred()[:MAX_REPOS]: # Slice to avoid supernodes
            g.add_node(starred.name + '(repo)', type='repo', lang=starred.language, \
                       owner=starred.owner.login)
            g.add_edge(sg.login + '(user)', starred.name + '(repo)', type='gazes')
    except Exception: #ssl.SSLError:
        print ("Encountered an error fetching starred repos for", sg.login, "Skipping.")

    print ("Processed", i+1, "stargazers' starred repos")
    print ("Num nodes/edges in graph", g.number_of_nodes(), "/", g.number_of_edges())
    print ("Rate limit", client.rate_limiting)