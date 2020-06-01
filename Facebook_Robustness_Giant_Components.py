import collections
import random

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


# ______________________________ATTACK___________________________________________#
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
        # ----closeness---------------------------------------------------
        cc = nx.closeness_centrality(g_remove_most_important)
        # ----betweenness-------------------------------------------------
        # cc = nx.betweenness_centrality(g_remove_most_important)
        # ----Page Rank---------------------------------------------------
        # cc = nx.pagerank_numpy(g_remove_most_important, alpha=0.9)
        # ----degree---------------------------------------------------
        # cc = nx.degree(g_remove_most_important)
        # cc = dict(cc)

        # --- Sorting
        list_cc = {k: v for k, v in sorted(cc.items(), key=lambda item: item[1], reverse=True)}

        first_nodes = list(list_cc.keys())[:(n + spare)]
        spare = 0  # senza resto

        # compute: giant measure
        if len(g_remove_most_important) > 0:

            comps = list(connected_component_subgraphs(g_remove_most_important))
            giant_comp = max(comps, key=len)
            comp_nodes_number = giant_comp.number_of_nodes()
            comp_len = len(comps)
            relative_size_giant = comp_nodes_number / len(g_remove_most_important)

            # saved for plot
            list_components.append(comp_len)

            # relative size Giant components
            list_giantcomponentnodes.append(relative_size_giant)

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
    # closeness_attack()
    A = [0.0, 4.976479326565982, 9.952958653131963, 14.929437979697946, 19.905917306263927, 24.88239663282991,
         29.858875959395892, 34.835355285961874, 39.81183461252785, 44.78831393909384, 49.76479326565982,
         54.7412725922258, 59.717751918791784, 64.69423124535776, 69.67071057192375, 74.64718989848973,
         79.6236692250557, 84.60014855162169, 89.57662787818768, 94.55310720475364, 99.52958653131964]
    B = [1.0, 0.3530484627410109, 0.22381083310420677, 0.20925494761350408, 0.2170015455950541, 0.18787079762689518,
         0.20120014119308155, 0.14817629179331307, 0.16042780748663102, 0.1717488789237668, 0.11779201577131591,
         0.13074398249452954, 0.06883835279655809, 0.047685834502103785, 0.05551020408163265, 0.0205078125,
         0.00850546780072904, 0.00482315112540193, 0.0023752969121140144, 0.004545454545454545, 0.0]
    plt.plot(A, B, 'r-', label='Closeness Attack')

    # 8 minutes
    # betweenness_attack()
    C = [0.0, 4.976479326565982, 9.952958653131963, 14.929437979697946, 19.905917306263927, 24.88239663282991,
         29.858875959395892, 34.835355285961874, 39.81183461252785, 44.78831393909384, 49.76479326565982,
         54.7412725922258, 59.717751918791784, 64.69423124535776, 69.67071057192375, 74.64718989848973,
         79.6236692250557, 84.60014855162169, 89.57662787818768, 94.55310720475364, 99.52958653131964]
    D = [1.0, 0.3170922355393434, 0.2271102557052516, 0.20256111757857975, 0.13199381761978363, 0.11931443638760712,
         0.09389339922343805, 0.07142857142857142, 0.07322089675030852, 0.07847533632286996, 0.07885657959586002,
         0.06455142231947483, 0.03073140749846343, 0.0182328190743338, 0.013061224489795919, 0.005859375,
         0.007290400972053463, 0.00964630225080386, 0.0056463022508038, 0.0027272727272727, 0.0]
    plt.plot(C, D, 'b-', label='Betweenness Attack')

    # 15 minutes
    # Page_Rank_attack()
    E = [0.0, 4.976479326565982, 9.952958653131963, 14.929437979697946, 19.905917306263927, 24.88239663282991,
         29.858875959395892, 34.835355285961874, 39.81183461252785, 44.78831393909384, 49.76479326565982,
         54.7412725922258, 59.717751918791784, 64.69423124535776, 69.67071057192375, 74.64718989848973,
         79.6236692250557, 84.60014855162169, 89.57662787818768, 94.55310720475364, 99.52958653131964]
    F = [1.0, 0.9054194893173528, 0.7475941710200715, 0.7427240977881258, 0.7360123647604327, 0.515161502966381,
         0.45746558418637484, 0.44642857142857145, 0.40682846565199504, 0.3704035874439462, 0.18482010842779695,
         0.16466083150984684, 0.11370620774431468, 0.019635343618513323, 0.010612244897959184, 0.005859375,
         0.007290400972053463, 0.001607717041800643, 0.001307700041800643, 0.000007717041800643, 0.0]

    plt.plot(E, F, 'v-', label='Page Rank Attack')

    # 20 minutes
    # degree attack()
    G = [0.0, 4.976479326565982, 9.952958653131963, 14.929437979697946, 19.905917306263927, 24.88239663282991,
         29.858875959395892, 34.835355285961874, 39.81183461252785, 44.78831393909384, 49.76479326565982,
         54.7412725922258, 59.717751918791784, 64.69423124535776, 69.67071057192375, 74.64718989848973,
         79.6236692250557, 84.60014855162169, 89.57662787818768, 94.55310720475364, 100]
    H = [1.0, 0.9766954700183295, 0.806799336650083, 0.7421714954638572, 0.7434701492537313, 0.5817578772802653,
         0.5671641791044776, 0.5625717566016073, 0.5186567164179104, 0.4690185436454093, 0.3288557213930348,
         0.12990602542841348, 0.08146766169154229, 0.011371712864250177, 0.005804311774461028, 0.001990049751243781,
         0.0024875621890547263, 0.001658374792703151, 0.0024875621890547263, 0.004975124378109453, 0]
    plt.plot(G, H, 'k-', label='Degree Attack')

    # if u want to perform an attack, you have to remove the comment and then choose which kind
    # of attack you want to perform.

    attack()

    plt.ylabel("Giant Component # of nodes")
    plt.xlabel("% nodes removed")
    plt.legend(loc='upper right', frameon=False)
    plt.savefig('Giant_components_GraphAnalysis.png', dpi=500)
    plt.show()
    """
    # --------------------------------
    # ----------- Syntetic Graph
    # --------------------------------

    # degree attack
    plt.plot([0.0, 20.0, 40.0, 60.0, 80.0, 100],
             [1.0, 1.0, 0.8333333333333334, 0.5, 0.5, 0],
             'k-', label='Degree Attack')

    # Page Rank attack
    plt.plot([0.0, 20.0, 40.0, 60.0, 80.0, 100],
             [1.0, 1.0, 0.8333333333333334, 0.25, 0.5, 0],
             'v-', label='Page Rank Attack')

    # Betweenness Attack
    plt.plot([0.0, 20.0, 40.0, 60.0, 80.0, 100],
             [1.0, 1.0, 0.8333333333333334, 0.5, 0.5, 0],
             'b-', label='Betweenness Attack')

    # Closeness Attack
    plt.plot([0.0, 20.0, 40.0, 60.0, 80.0, 100],
             [1.0, 1.0, 0.8333333333333334, 0.5, 0.5, 0],
             'r-', label='Closeness Attack')

    # attack()
    plt.ylabel("Giant Component # of nodes")
    plt.xlabel("% nodes removed")
    plt.legend(loc='upper right', frameon=False)
    plt.savefig('Giant_components_Synthetic_GraphAnalysis.png', dpi=500)
    plt.show()


main()
