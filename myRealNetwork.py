import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()

# node=italian region, weight = cases
# weight collected in date: 15/04/2020
G.add_node('Aosta', weight='1093')
G.add_node('Piemonte', weight='21955')
G.add_node('Lombardia', weight='67931')
G.add_node('Liguria', weight='6764')
G.add_node('Trentino', weight='6024')
G.add_node('Fvgiulia', weight='2792')
G.add_node('Veneto', weight='16404')
G.add_node('Emilia', weight='23092')
G.add_node('Toscana', weight='8603')
G.add_node('Marche', weight='5877')
G.add_node('Umbria', weight='1353')
G.add_node('Abruzzo', weight='2667')
G.add_node('Lazio', weight='5895')
G.add_node('Molise', weight='282')
G.add_node('Campania', weight='4135')
G.add_node('Basilicata', weight='350')
G.add_node('Puglia', weight='3622')
G.add_node('Calabria', weight='1047')
G.add_node('Sardegna', weight='1236')
G.add_node('Sicilia', weight='2835')

G.add_edges_from([('Aosta', 'Piemonte'),
                  ('Piemonte', 'Aosta'), ('Piemonte', 'Lombardia'), ('Piemonte', 'Liguria'), ('Piemonte', 'Emilia'),
                  ('Lombardia', 'Piemonte'), ('Lombardia', 'Emilia'), ('Lombardia', 'Trentino'),
                  ('Lombardia', 'Veneto'),
                  ('Liguria', 'Piemonte'), ('Liguria', 'Emilia'), ('Liguria', 'Toscana'),
                  ('Trentino', 'Lombardia'), ('Trentino', 'Veneto'), ('Trentino', 'Fvgiulia'),
                  ('Fvgiulia', 'Veneto'),
                  ('Veneto', 'Fvgiulia'), ('Veneto', 'Trentino'), ('Veneto', 'Lombardia'), ('Veneto', 'Piemonte'),
                  ('Emilia', 'Veneto'), ('Emilia', 'Lombardia'), ('Emilia', 'Piemonte'), ('Emilia', 'Liguria'),
                  ('Emilia', 'Toscana'), ('Emilia', 'Marche'),
                  ('Toscana', 'Liguria'), ('Toscana', 'Emilia'), ('Toscana', 'Marche'), ('Toscana', 'Umbria'),
                  ('Toscana', 'Lazio'),
                  ('Marche', 'Emilia'), ('Marche', 'Toscana'), ('Marche', 'Umbria'), ('Marche', 'Abruzzo'),
                  ('Marche', 'Lazio'),
                  ('Umbria', 'Marche'), ('Umbria', 'Toscana'), ('Umbria', 'Lazio'),
                  ('Abruzzo', 'Marche'), ('Abruzzo', 'Lazio'), ('Abruzzo', 'Molise'),
                  ('Lazio', 'Toscana'), ('Lazio', 'Umbria'), ('Lazio', 'Marche'), ('Lazio', 'Abruzzo'),
                  ('Lazio', 'Molise'), ('Lazio', 'Campania'),
                  ('Molise', 'Abruzzo'), ('Molise', 'Lazio'), ('Molise', 'Campania'), ('Molise', 'Puglia'),
                  ('Campania', 'Lazio'), ('Campania', 'Molise'), ('Campania', 'Puglia'), ('Campania', 'Basilicata'),
                  ('Basilicata', 'Campania'), ('Basilicata', 'Puglia'), ('Basilicata', 'Calabria'),
                  ('Puglia', 'Molise'), ('Puglia', 'Campania'), ('Puglia', 'Basilicata'),
                  ('Calabria', 'Basilicata'),
                  ])
# Sardegna and Sicilia are islands!

list(G.nodes)
list(G.edges)
# G.degree([2, 3])

totalweightssum = 0
for n in G.nodes(data='weight'):
    totalweightssum += int(n[1])
print('total cases = %d' % totalweightssum)

# some properties
print("-node degree clustering: ")
for v in nx.nodes(G):
    print('%s %d %f' % (v, nx.degree(G, v), nx.clustering(G, v)))

# print the adjacency list
print("-print the adjacency list: ")
for line in nx.generate_adjlist(G):
    print(line)


# planar_layout = Position nodes without edge intersections.
pos = nx.planar_layout(G)
nx.draw(G,
        pos,
        with_labels=True,
        font_weight='bold',
        node_size=100,
        node_color='r')

plt.axis('off')
plt.show()

# plt.savefig("covid-19_scenario.png")
