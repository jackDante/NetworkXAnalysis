import networkx as nx
import matplotlib.pyplot as plt
import collections

from numpy import mean

G_fb = nx.read_edgelist("facebook_combined.txt", create_using=nx.Graph(), nodetype=int)
print(nx.info(G_fb))
print('Density: %f' % nx.density(G_fb))
print('is_directed: %s' % nx.is_directed(G_fb))
print('average_clustering: %f' % nx.average_clustering(G_fb))
print('average_degree_connectivity: %s' % nx.average_degree_connectivity(G_fb))
print('Diameter (it is the maximum eccentricity): %d' % nx.diameter(G_fb))

# ---------------------- some properties
# --NODE DEGREE CLUSTERING
"""
print("-Node degree clustering: ")
for v in nx.nodes(G_fb):
    print('%s %d %f' % (v, nx.degree(G_fb, v), nx.clustering(G_fb, v)))
    if nx.degree(G_fb, v) == 1045:
        vtemp = v

print('>>>here it is the max degree %d' % vtemp)
"""

degree_sequence = sorted([d for n, d in G_fb.degree()], reverse=True)
# --NODE WITH MAX DEGREE
dmax = max(degree_sequence)
print('>>node with max-degree: %d' % dmax)
print('>>node 107 (that has max degree) has clustering: %f' % nx.clustering(G_fb, 107))
# degree_sequence.remove(dmax)
# --AVG DEGREE
avgdegree = mean(degree_sequence)
print('>>avg-degree: %d' % avgdegree)



# --PLOT DEGREE HISTOGRAM
degreeCount = collections.Counter(degree_sequence)
deg, cnt = zip(*degreeCount.items())

fig, ax = plt.subplots()
plt.bar(deg, cnt, width=0.80, color='b')

plt.title("Degree Histogram")
plt.ylabel("Count")
plt.xlabel("Degree")
# deg2 = deg[1::15] in order to compute a readable graph: I take 1 elem every 15 in the list.
ax.set_xticks([d for d in deg])
ax.set_xticklabels(deg)

plt.show()


"""
# --PRINT THE ADJACENCY LIST
print("-Print the adjacency list: ")
for line in nx.generate_adjlist(G_fb):
    print(line)
"""


# Compute the shortest-path betweenness centrality for nodes.
# Betweenness_centrality of a node v is the sum of the fraction of all-pairs shortest paths
# that pass through v. So the node's size it's related with the node's betweenness_centrality.
# in practice: how many pairs of individuals would
# have to go through you in order to reach one
# another in the minimum number of hops?
betCent = nx.betweenness_centrality(G_fb, normalized=True, endpoints=True)
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
print('I have just finished the calculation phase!')
print('node with max-betweenness_centrality: %f' % max(betCent))
closenessCent = nx.closeness_centrality(G_fb)
print('node with max-closeness_centrality: %f' % max(closenessCent))
print('node with min-closeness_centrality: %f' % min(closenessCent))
clustering = nx.clustering(G_fb)
print('node with max-clustering: %f' % max(clustering))
print('node with min-clustering: %f' % min(clustering))

plt.show()

