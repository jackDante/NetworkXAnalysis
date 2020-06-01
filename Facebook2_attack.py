import matplotlib.pyplot as plt
import networkx as nx

# G_fb = nx.read_edgelist("facebook_combined.txt", create_using=nx.Graph(), nodetype=int)
G_fb = nx.petersen_graph()
print(nx.info(G_fb))
print('Density: %f' % nx.density(G_fb))
print('is_directed: %s' % nx.is_directed(G_fb))

"""
Here we try to calculate the random attack and the high degree attack removing at each iterations
only one nodes. Note that this process uses the avg_degree of the graph. Calculate the diameter or giant components
of the graph is too expensive...and in particular it requires a very long time.
"""
# ------------------------------------
# -------------------useful functions
# ------------------------------------
def remove_random_node(g, n):
    import random  # This because it crashes against the import at the top which works for the plot
    for i in range(n):
        try:
            node = random.choice(list(g.nodes()))
            g.remove_node(node)
        except nx.NetworkXError:
            print("not found")


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


# -------------------1-----------------------
def random_attack():
    degree_list = []  # remember that list is mutable!
    counter = 0
    for node in list(G_fb):
        degree = nx.degree(G_fb)
        degree_sorted = sorted(degree, key=lambda x: (x[1]), reverse=True)

        avg = avg_degree(degree_sorted)
        degree_list.append(avg)

        remove_random_node(G_fb, 1)
        counter = counter + 1
    return degree_list


# -------------------2-----------------------
def highdegree_attack():
    degree_list = []  # remember that list is mutable!
    for node in list(G_fb):
        degree = nx.degree(G_fb)
        degree_sorted2 = sorted(degree, key=lambda x: (x[1]), reverse=True)
        nodes_elements = [node_tuple[0] for node_tuple in degree_sorted2]

        avg2 = avg_degree(degree_sorted2)
        degree_list.append(avg2)

        remove_nodes_from_list(G_fb, nodes_elements)
    return degree_list

# ----------------------------------------------
# -------------------PLOT-----------------------
# ----------------------------------------------
plt.plot(random_attack(), 'r--', label='Random Attack')
# reload all information
# G_fb = nx.read_edgelist("facebook_combined.txt", create_using=nx.Graph(), nodetype=int)
G_fb = nx.petersen_graph()
plt.plot(highdegree_attack(), color='b', linewidth=2.0, label='High Degree Attack')


plt.suptitle('Attacks Plotting')
plt.ylabel('AVG degree')
plt.xlabel('# nodes')
plt.legend(loc='upper right', frameon=False)
plt.show()

