import networkx as nx
import matplotlib.pyplot as plt
import collections
from numpy import mean

# ---------------------------------------------------------
# -----------------------Select the graph
# ---------------------------------------------------------
G_fb = nx.read_edgelist("facebook_combined.txt", create_using=nx.Graph(), nodetype=int)
# G_fb = nx.petersen_graph()  # Synthetic graphs

print(nx.info(G_fb))
print('Density: %f' % nx.density(G_fb))

print('Number of connected components: %f' % nx.number_connected_components(G_fb))
# print(nx.connected_components(G_fb))

A = sorted(nx.connected_components(G_fb), key=len, reverse=True)
print(A)
# print('Strongly connected?: %s' % nx.is_strongly_connected(G_fb))


"""
print('is_directed: %s' % nx.is_directed(G_fb))
print('average_clustering: %f' % nx.average_clustering(G_fb))
print('average_degree_connectivity: %s' % nx.average_degree_connectivity(G_fb))  # required time
print('Diameter (it is the maximum eccentricity): %d' % nx.diameter(G_fb))  # required time
print('average_clustering: %f' % nx.average_clustering(G_fb))
print('assortativity: %f' % nx.degree_assortativity_coefficient(G_fb))
# ------------------------------------------------------------------------------

# -------------------------- some properties -----------------------------------
# --NODE DEGREE CLUSTERING----------------------------------------------------

print("-Node degree clustering: ")
for v in nx.nodes(G_fb):
    print('%s %d %f' % (v, nx.degree(G_fb, v), nx.clustering(G_fb, v)))

# --NODE WITH MAX DEGREE----------------------------------------------------
degree_sequence = sorted([d for n, d in G_fb.degree()], reverse=True)
dmax = max(degree_sequence)
# --print top 7 high-degree nodes
for v in nx.nodes(G_fb):
    if nx.degree(G_fb, v) > 290:
        print('node: %s degree:%d' % (v, nx.degree(G_fb, v)))

# --AVG DEGREE----------------------------------------------------
avgdegree = mean(degree_sequence)
print('>>avg-degree: %d' % avgdegree)

# --PLOT DEGREE HISTOGRAM----------------------------------------------------
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

# --PRINT THE ADJACENCY LIST----------------------------------------------------
print("-Print the adjacency list: ")
for line in nx.generate_adjlist(G_fb):
    print(line)

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

print('I have just finished the calculation phase!')
print('betCent: %s' % betCent)
sortedbetCent = {k: v for k, v in sorted(betCent.items(), key=lambda item: item[1])}
print('sorted-betCent: %s' % sortedbetCent)

# Compute the closeness_centrality for nodes.
closenessCent = nx.closeness_centrality(G_fb)  # It takes a long time
sortedclosenessCent = {k: v for k, v in sorted(closenessCent.items(), key=lambda item: item[1])}
print('sorted-closenessCent: %s' % sortedclosenessCent)

# Compute the clustering for nodes.
clustering = nx.clustering(G_fb)  # It takes a long time
sortedclustering = {k: v for k, v in sorted(clustering.items(), key=lambda item: item[1])}
print('sorted-clustering: %s' % sortedclustering)

plt.show()
"""
