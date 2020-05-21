import matplotlib.pyplot as plt
import networkx as nx

G_fb = nx.read_edgelist("facebook_combined.txt", create_using=nx.Graph(), nodetype=int)
print(nx.info(G_fb))
print('Density: %f' % nx.density(G_fb))
print('is_directed: %s' % nx.is_directed(G_fb))


# print('Diameter (it is the maximum eccentricity): %d' % nx.diameter(G_fb))  # required time


def remove_random_node(g, n):
    import random  # This because it crashes against the import at the top which works for the plot
    for i in range(n):
        node = random.choice(list(g.nodes()))
        g.remove_node(node)


def remove_nodes_from_list(g, list):
    try:
        g.remove_node(next(iter(list or []), None))
    except nx.NetworkXError:
        print("not found")


def avg_degree(degree_list):
    total_degree = 0
    cnt = len(nx.nodes(G_fb))
    for k, v in degree_list:
        total_degree = total_degree + v
    avg = (total_degree / cnt) if cnt != 0 else 0
    return avg


def random_attack():
    degree_list = []  # remember that list is mutable!
    counter = 0
    for node in range(4037):
        degree = nx.degree(G_fb)
        degree_sorted = sorted(degree, key=lambda x: (x[1]), reverse=True)
        avg = avg_degree(degree_sorted)
        # if avg<=0:
        #    break
        degree_list.append(avg)
        remove_random_node(G_fb, 1)
        counter = counter + 1
    return degree_list


def highdegree_attack():
    degree_list = []  # remember that list is mutable!
    for node in range(4037):
        degree = nx.degree(G_fb)
        degree_sorted2 = sorted(degree, key=lambda x: (x[1]), reverse=True)
        nodes_elements = [node_tuple[0] for node_tuple in degree_sorted2]
        avg2 = avg_degree(degree_sorted2)
        degree_list.append(avg2)
        remove_nodes_from_list(G_fb, nodes_elements)
    return degree_list



plt.plot(random_attack(), 'r--', label='Random Attack')
# reload all information
G_fb = nx.read_edgelist("facebook_combined.txt", create_using=nx.Graph(), nodetype=int)
plt.plot(highdegree_attack(), color='b', linewidth=2.0, label='High Degree Attack')
# reload all information
G_fb = nx.read_edgelist("facebook_combined.txt", create_using=nx.Graph(), nodetype=int)


plt.suptitle('Categorical Plotting')
plt.ylabel('AVG degree')
plt.xlabel('# nodes')
plt.legend(loc='upper right', frameon=False)
plt.show()

"""
print(my_list)
print("counter=%d" % counter)



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
