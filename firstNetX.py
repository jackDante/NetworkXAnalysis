import networkx as nx
import matplotlib.pyplot as plt
from examples.drawing.plot_edge_colormap import colors

n = 10  # 10 nodes
m = 20  # 20 edges

G = nx.gnm_random_graph(n, m)

# some properties
print("node degree clustering")
for v in nx.nodes(G):
    print('%s %d %f' % (v, nx.degree(G, v), nx.clustering(G, v)))

# print the adjacency list
print("print the adjacency list")
for line in nx.generate_adjlist(G):
    print(line)

nx.draw(G, node_size=250, with_labels=True)
plt.show()
