import networkx as nx
import matplotlib.pyplot as plt
import collections

from networkx.algorithms.community import greedy_modularity_communities
from numpy import mean

G_fb = nx.read_edgelist("facebook_combined.txt", create_using=nx.Graph(), nodetype=int)
print(nx.info(G_fb))
print('Density: %f' % nx.density(G_fb))
print('is_directed: %s' % nx.is_directed(G_fb))
# print('average_clustering: %f' % nx.average_clustering(G_fb))
# print('average_degree_connectivity: %s' % nx.average_degree_connectivity(G_fb))  # required time
# print('Diameter (it is the maximum eccentricity): %d' % nx.diameter(G_fb))  # required time

r = nx.degree_assortativity_coefficient(G_fb)  # Assortativity of graph by degree.
print("degree_assortativity_coefficient (the network is non-assortative): %f \n \n" % r)
# It is positive so the #edges within groups exceeds the #expected on the basis of chance

# ------------------------------------------Clauset-Newman-Moore greedy modularity maximization
# Find communities in graph using Clauset-Newman-Moore greedy modularity maximization.
list_of_communities = list(greedy_modularity_communities(G_fb))
for community in list_of_communities:
    print(community)
    print(len(community))

# ------------------------------------------PageRank
"""
PageRank computes a ranking of the nodes in the graph G based on the structure of the incoming links. 
It was originally designed as an algorithm to rank web pages.
"""
pr = nx.pagerank(G_fb, alpha=0.9)
# print(pr)
pr_sorted = {k: v for k, v in sorted(pr.items(), key=lambda item: item[1])}
print('\n PageRank (5sec):')
print(pr_sorted)
""""
The matrix returned represents the transition matrix that describes the Markov chain used in PageRank. 
For PageRank to converge to a unique solution (i.e., a unique stationary distribution in a Markov chain), 
the transition matrix must be irreducible. 
In other words, it must be that there exists a path between every pair of nodes in the graph, 
or else there is the potential of “rank sinks.”

print('\n GoogleMatrix (2sec):')
m = nx.google_matrix(G_fb)
print(m)
"""
# ------------------------------------------HITS (hubs and authorities)
"""
Return HITS hubs and authorities values for nodes.
The HITS algorithm computes two numbers for a node. 
Authorities estimates the node value based on the incoming links. 
Hubs estimates the node value based on outgoing links.
---Note that: In my case of UNDIRECTED GRAPH -> Hubs=Authorities!
"""
print('\n HITS (20sec):')
calculate_hits = nx.hits(G_fb)
hits = calculate_hits[0]
hits_sorted = {k: v for k, v in sorted(hits.items(), key=lambda item: item[1])}
print(hits_sorted)

"""
# Compute the shortest-path betweenness centrality for nodes. And then plot the graph!!!
betCent = nx.betweenness_centrality(G_fb, normalized=True, endpoints=True)  # It takes a long time

node_color = [20000.0 * G_fb.degree(v) for v in G_fb]
node_size = [v * 10000 for v in betCent.values()]
plt.figure(figsize=(20, 20))
pos = nx.spring_layout(G_fb)
nx.draw(G_fb,
        pos=pos,
        with_labels=False,
        node_color=node_color,
        node_size=node_size)
plt.axis('off')

plt.show()
"""
