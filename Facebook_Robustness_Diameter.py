import collections

import matplotlib.pyplot as plt
import networkx as nx

# ------------------------------------
# -------------------useful functions
# ------------------------------------
def connected_component_subgraphs(t, copy=True):
    for c in nx.connected_components(t):
        if copy:
            yield t.subgraph(c).copy()
        else:
            yield t.subgraph(c)


def draw_graph(g, layout, title, namefile):
    plt.title(title)
    if g.number_of_nodes() < 100:
        nx.draw_networkx(g, node_size=150, font_size=9, arrowsize=3, node_color='b', pos=layout)
    else:
        nx.draw_networkx(g, node_size=50, font_size=6, arrowsize=3, node_color='b', pos=layout)
    plt.savefig(namefile + '.png', dpi=500)
    plt.close()


def plot_distribution(values, label):
    values_count = collections.Counter(values)
    val, cnt = zip(*values_count.items())
    fig, ax = plt.subplots()
    plt.bar(val, cnt, width=0.80, color='b')
    plt.title(label + " Histogram")
    plt.ylabel("Count")
    plt.xlabel(label)
    plt.savefig("prova.png", dpi=500)
    plt.show()


# _________________________________________________________________________________#
# closeness
# betweenness
# Page Rank
# high degree
def attack():
    # G = nx.read_edgelist("facebook_combined.txt", nodetype=int)
    G = nx.petersen_graph()

    div = 5  # Realistic graph div = 20
    print(nx.info(G))
    N = len(G)
    n = int(N / div)
    print(nx.density(G))

    g = G.copy()
    # g.to_undirected()
    g_remove_most_important = g.copy()
    list_components = []  # contains number of connected component
    list_removed = []
    list_diameters = []
    list_diameters_max = []
    list_diameters_min = []
    list_giantcomponentnodes = []

    spare = N % div
    x = 0
    val = x / N * 100

    print("_________________ Computing... _________________")
    while val <= 100:
        # closeness---------------------------------------------------
        # cc = nx.closeness_centrality(g_remove_most_important)
        # betweenness-------------------------------------------------
        # cc = nx.betweenness_centrality(g_remove_most_important)
        # Page Rank---------------------------------------------------
        # cc = nx.pagerank_numpy(g_remove_most_important, alpha=0.9)
        # degree---------------------------------------------------
        cc = nx.degree(g_remove_most_important)
        cc = dict(cc)

        # --- Sorting
        list_cc = {k: v for k, v in sorted(cc.items(), key=lambda item: item[1], reverse=True)}

        first_nodes = list(list_cc.keys())[:(n + spare)]
        spare = 0  # senza resto

        # compute: diameter measure
        if len(g_remove_most_important) > 0:

            comps = list(connected_component_subgraphs(g_remove_most_important))
            comp_len = len(comps)

            # saved for plot
            list_components.append(comp_len)

            # diameter of the network
            diameters = [nx.diameter(comp.to_undirected()) for comp in comps]
            list_diameters_max.append(max(diameters))
            list_diameters_min.append(min(diameters))
            list_giantcomponentnodes.append((sum(diameters) / len(diameters)))

            print("remove nodes")
            list_removed.append(val)
        else:
            list_giantcomponentnodes.append(0)
            list_removed.append(100)
            list_diameters_max.append(0)
            list_diameters_min.append(0)
            list_diameters.append(0)

        # update value
        x += n
        val = x / N * 100

        g_remove_most_important.remove_nodes_from(first_nodes)

    print(list_removed)
    print(list_giantcomponentnodes)
    plt.plot(list_removed, list_giantcomponentnodes, 'y-', label='Attack')

# ----------------------------------------------
# -------------------PLOT-----------------------
# ----------------------------------------------
def main():
    # --------------------------------
    # ----------- Real Graph
    # --------------------------------
    """
    # 8 minutes
    # -----------------closeness_attack()
    A = [0.0, 4.976479326565982, 9.952958653131963, 14.929437979697946, 19.905917306263927, 24.88239663282991,
         29.858875959395892, 34.835355285961874, 39.81183461252785, 44.78831393909384, 49.76479326565982,
         54.7412725922258, 59.717751918791784, 64.69423124535776, 69.67071057192375, 74.64718989848973,
         79.6236692250557, 84.60014855162169, 89.57662787818768, 94.55310720475364, 100]
    B = [8.0, 0.7051282051282052, 0.7909090909090909, 0.8290598290598291, 0.859504132231405, 0.8527131782945736,
         0.9371069182389937, 0.945054945054945, 0.9435897435897436, 1.0138248847926268, 1.0271317829457365,
         1.0477815699658704, 1.0175953079178885, 0.969309462915601, 0.8571428571428571, 0.6727272727272727,
         0.41495327102803736, 0.177734375, 0.0, 0.0, 0]
    plt.plot(A, B, 'r-', label='Closeness Attack')

    # 8 minutes
    # -----------------betweenness_attack()
    C = [0.0, 4.976479326565982, 9.952958653131963, 14.929437979697946, 19.905917306263927, 24.88239663282991,
         29.858875959395892, 34.835355285961874, 39.81183461252785, 44.78831393909384, 49.76479326565982,
         54.7412725922258, 59.717751918791784, 64.69423124535776, 69.67071057192375, 74.64718989848973,
         79.6236692250557, 84.60014855162169, 89.57662787818768, 94.55310720475364, 100]
    D = [8.0, 0.8046875, 0.8841463414634146, 0.989247311827957, 1.0717703349282297, 1.0239043824701195,
         0.9721254355400697, 0.9758308157099698, 0.986737400530504, 0.9577464788732394, 0.9284210526315789,
         0.8474264705882353, 0.7299509001636661, 0.586608442503639, 0.38254172015404364, 0.2092426187419769,
         0.1971608832807571, 0.20169851380042464, 0.2012779552715655, 0.1987179487179487, 0]
    plt.plot(C, D, 'b-', label='Betweenness Attack')

    # 15 minutes
    # -----------------Page_Rank_attack()
    E = [0.0, 4.976479326565982, 9.952958653131963, 14.929437979697946, 19.905917306263927, 24.88239663282991,
         29.858875959395892, 34.835355285961874, 39.81183461252785, 44.78831393909384, 49.76479326565982,
         54.7412725922258, 59.717751918791784, 64.69423124535776, 69.67071057192375, 74.64718989848973,
         79.6236692250557, 84.60014855162169, 89.57662787818768, 94.55310720475364, 100]
    F = [8.0, 0.5229357798165137, 0.6911764705882353, 0.6709677419354839, 0.6384180790960452, 0.7150259067357513,
         0.7654867256637168, 0.8618181818181818, 0.9217391304347826, 0.7836538461538461, 0.853515625,
         0.7869362363919129, 0.5750962772785623, 0.40765765765765766, 0.21825813221406087, 0.12384259259259259,
         0.02554278416347382, 0.0, 0.0, 0.0, 0]

    plt.plot(E, F, 'v-', label='Page Rank Attack')

    # 8 minutes
    # -----------------degree attack()
    G = [0.0, 4.976479326565982, 9.952958653131963, 14.929437979697946, 19.905917306263927, 24.88239663282991,
         29.858875959395892, 34.835355285961874, 39.81183461252785, 44.78831393909384, 49.76479326565982,
         54.7412725922258, 59.717751918791784, 64.69423124535776, 69.67071057192375, 74.64718989848973,
         79.6236692250557, 84.60014855162169, 89.57662787818768, 94.55310720475364, 100]
    H = [8.0, 0.37333333333333335, 0.5119047619047619, 0.5779816513761468, 0.5575221238938053, 0.628099173553719,
         0.6090225563909775, 0.6282051282051282, 0.7213114754098361, 0.8169642857142857, 0.9310344827586207,
         1.1914893617021276, 1.1177474402730376, 0.7073791348600509, 0.3270300333704116, 0.13816534541336353,
         0.015151515151515152, 0.0, 0.0, 0.0, 0]

    plt.plot(G, H, 'k-', label='Degree Attack')

    # attack()

    plt.ylabel("Diameter of the graph")
    plt.xlabel("% nodes removed")
    plt.legend(loc='upper right', frameon=False)
    plt.savefig('Diameter_GraphAnalysis.png', dpi=500)
    plt.show()
    """
    # --------------------------------
    # ----------- Syntetic Graph
    # --------------------------------
    """ """
    # degree attack
    plt.plot([0.0, 20.0, 40.0, 60.0, 80.0, 100],
             [2.0, 3.0, 2.0, 0.3333333333333333, 0.0, 0],
             'k-', label='Degree Attack')

    # Page Rank attack
    plt.plot([0.0, 20.0, 40.0, 60.0, 80.0, 100],
             [2.0, 3.0, 2.0, 0.0, 0.0, 0],
             'v-', label='Page Rank Attack')

    # Betweenness Attack
    plt.plot([0.0, 20.0, 40.0, 60.0, 80.0, 100],
             [2.0, 3.0, 2.0, 0.3333333333333333, 0.0, 0],
             'b-', label='Betweenness Attack')

    # Closeness Attack
    plt.plot([0.0, 20.0, 40.0, 60.0, 80.0, 100],
             [2.0, 3.0, 2.0, 0.3333333333333333, 0.0, 0],
             'r-', label='Closeness Attack')

    # attack()
    plt.ylabel("Diameter of the graph")
    plt.xlabel("% nodes removed")
    plt.legend(loc='upper right', frameon=False)
    plt.savefig('Diameter_Synthetic_GraphAnalysis.png', dpi=500)
    plt.show()


main()
