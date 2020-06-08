import collections
import random

import matplotlib.pyplot as plt
import networkx as nx

# ------------------------------------
# ------------------- useful functions
# ------------------------------------

a = 2
b = 3
number_of_infected = []


def from_bools_to_colors(contagion_list):
    for k, v in contagion_list.items():
        if v:
            contagion_list[k] = 'red'
        else:
            contagion_list[k] = 'blue'
    return contagion_list


# First Iteration of contagion
def initialize_graph(g, percentage):
    n = len(g) * percentage
    for i in range(int(n)):
        v = random.choice(list(g.nodes.keys()))
        g.nodes[v]['contagion'] = True


# ----------------------------------------------
# -------------------PLOT-----------------------
# ----------------------------------------------
# Saves graphs into data folder
def draw_graph(g, day, layout):
    colors = from_bools_to_colors(nx.get_node_attributes(g, 'contagion'))
    nx.draw(g, node_color=list(colors.values()), pos=layout, node_size=50, font_size=6, font_color='w', arrowsize=3)
    plt.draw()
    plt.savefig('social_contagion/' + str(day) + '.png', dpi=500)
    plt.close()


def draw_infected(n_infected):
    plt.plot((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), n_infected, 'v-')
    plt.ylabel("number of infected node")
    plt.xlabel("days")
    plt.legend(loc='upper right', frameon=False)
    # plt.savefig('Infected_per_day.png', dpi=500)
    plt.show()


# ______________________________ Social Contagion ___________________________________________#


def main():
    g = nx.read_edgelist("facebook_combined.txt", nodetype=int)
    # g = nx.petersen_graph()

    # g = nx.scale_free_graph(20)
    # g = nx.fast_gnp_random_graph(50, 1)

    layout = nx.spring_layout(g)
    nx.set_node_attributes(g, False, 'contagion')  # all false: nobody is infected
    draw_graph(g, 0, layout)

    initialize_graph(g, 0.1)  # 10%
    draw_graph(g, 1, layout)

    days = 10
    for day in range(days):
        print('------------- Day ', day)
        for n in g.nodes():
            nn_number = len(list(set(g.edges(n))))
            # print(nn_number)
            # check if we meet a node without edges = isolated vertex (degree zero)
            if nn_number == 0:
                continue

            blues = 0
            for frm, to in list(set(g.edges(n))):
                if not g.nodes[to]['contagion']:
                    blues += 1
            p = blues / nn_number
            not_contagion_percentage = p * nn_number * a
            contagion_percentage = (1 - p) * nn_number * b

            # print('p = %f' % p)
            # print('not_contagion_perc = %f;  contagion_perc = %f' % (not_contagion_percentage, contagion_percentage))
            if contagion_percentage > not_contagion_percentage:
                g.nodes[n]['contagion'] = True
        draw_graph(g, day + 2, layout)

        infected = []
        not_infected = []
        for n in g.nodes:
            if g.nodes[n]['contagion']:
                infected.append(n)
            else:
                not_infected.append(n)
        print('Infected nodes: \n\t', infected)
        print('Not-Infected nodes: \n\t', not_infected)
        number_of_infected.append(len(infected))

    plt.close()
    draw_infected(number_of_infected)


if __name__ == '__main__':
    main()

