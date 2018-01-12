#hello.py
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

for sg in stargazers:
    g.add_node(sg.login + '(user)', type='user')
    g.add_edge(sg.login + '(user)', repo.name + '(repo)', type='gazes')
	
for i, sg in enumerate(stargazers):   
    # 增加关注联系，如果有关注者的话
    try:
        for follower in sg.get_followers():
            if follower.login + '(user)' in g:
                g.add_edge(follower.login + '(user)', sg.login + '(user)', 
                           type='follows')
    except Exception: #ssl.SSLError
        sys.stderr.write( "Encountered an error fetching followers for", \
                             sg.login, "Skipping.")

    print ("Processed", i+1, " stargazers. Num nodes/edges in graph", \
          g.number_of_nodes(), "/", g.number_of_edges())
    print ("Rate limit remaining", client.rate_limiting)

# 看下更新的图信息
print (nx.info(g),'\n')

# 每个打星用户的关注者数量不同
print (len([e for e in g.edges_iter(data=True) if e[2]['type'] == 'follows']),'\n')

# 查看某个打星用户有多少关注者
print (len([e 
           for e in g.edges_iter(data=True) 
               if e[2]['type'] == 'follows' and e[1] == 'freeman-lab(user)']),'\n')


# 打印度最多的前10个结点
print (list(sorted([n for n in g.degree_iter()], key=itemgetter(1), reverse=True)[:10]),'\n')


# 对每个打星用户的关注者数目计数
c = Counter([e[1] for e in g.edges_iter(data=True) if e[2]['type'] == 'follows'])
popular_users = [ (u, f) for (u, f) in c.most_common() if f > 0 ]
print ("Number of popular users", len(popular_users))
print ("Top popular users:", popular_users[:10])
h = g.copy()
# 移除中心结点
h.remove_node('findspark(repo)')

dc = sorted(nx.degree_centrality(h).items(), 
            key=itemgetter(1), reverse=True)

print ("Degree Centrality")
print (dc[:10],'\n')
bc = sorted(nx.betweenness_centrality(h).items(), 
            key=itemgetter(1), reverse=True)

print ("Betweenness Centrality")
print (bc[:10],'\n')

print ("Closeness Centrality")
cc = sorted(nx.closeness_centrality(h).items(), 
            key=itemgetter(1), reverse=True)
print (cc[:10])