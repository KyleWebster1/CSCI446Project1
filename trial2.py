import networkx as nx
import random
import matplotlib.pyplot as plt
import matplotlib.colors as c

X= []
Y= []
Colors= { 1:'blue',2 :'red', 3:'green', 4:'black'}
graph = nx.Graph()

graph.add_node([0,6])
#
#
# #fig, ax = plt.subplots()
# #graph[1][3]['color']='red'
#
# #my_color.set_color_cycle(['#1f77b4', '#ff7f0e', '#2ca02c'])
# graph.add_edges_from([(1,3), (3,5),(1,5), (2,4)])
nx.draw(graph, with_labels=True)
#

plt.show()
# #def randowvalues(graph, int(x), int (y),color):
#    # for color in ['#1f77b4', '#ff7f0e', '#2ca02c']:
#      #   plt(x,y, color = color)
#
#
# def random_edge(graph, del_orig=True):
#
#     edges = list(graph.edges)
#     edge2= list(graph.edges)
#     nonedges = list(nx.non_edges(graph))
#
#     #graph.add_edge_from([(X[i] , Y[i], Colors)])
#     # random edge choice
#     if edge2 == 1 or edges == 1:
#
#         chosen_edge = random.choice(edges)
#         chosen_edge=random.choice(edge2)
#     chosen_edge = random.choice(edges)
#     chosen_edge=random.choice(edge2)
#     chosen_nonedge = random.choice([x for x in nonedges if chosen_edge[0] == x[0]])
#
#     if del_orig:
#         # delete chosen edge
#         graph.remove_edge(chosen_edge[0], chosen_edge[1])
#     # add new edge
#     graph.add_edge(chosen_nonedge[0], chosen_nonedge[1])
#
#     return graph