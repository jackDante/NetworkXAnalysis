import networkx as nx
import matplotlib.pyplot as plt

G_fb = nx.read_edgelist("facebook_combined.txt", create_using=nx.Graph(), nodetype=int)
print(nx.info(G_fb))
print('Density: %d' % nx.density(G_fb))
print('is_directed: %s' % nx.is_directed(G_fb))
# print('Diameter (it is the maximum eccentricity): %d' % nx.diameter(G_fb))

# some properties
print("-Node degree clustering: ")
for v in nx.nodes(G_fb):
    print('%s %d %f' % (v, nx.degree(G_fb, v), nx.clustering(G_fb, v)))
    if nx.degree(G_fb, v) == 1045:
        vtemp = v

print('>>>eccolo il max degree %d' % vtemp)

degree_sequence = sorted([d for n, d in G_fb.degree()], reverse=True)
# print "Degree sequence", degree_sequence
dmax = max(degree_sequence)
print(dmax)
"""
plt.loglog(degree_sequence, 'b-', marker='o')
plt.title("Degree rank plot")
plt.ylabel("degree")
plt.xlabel("rank")

# draw graph in inset
plt.axes([0.45, 0.45, 0.45, 0.45])
Gcc = G_fb.subgraph(sorted(nx.connected_components(G_fb), key=len, reverse=True)[0])
pos = nx.spring_layout(Gcc)
plt.axis('off')
nx.draw_networkx_nodes(Gcc, pos, node_size=10)
nx.draw_networkx_edges(Gcc, pos, alpha=0.4)

plt.show()


# print the adjacency list
print("-Print the adjacency list: ")
for line in nx.generate_adjlist(G_fb):
    print(line)


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
plt.show()
plt.savefig("G_fb.png")
"""
# shortest_path = dict(nx.all_pairs_shortest_path(G_fb))

# sorted(betCent, key=betCent.get, reverse=True)[:5]
