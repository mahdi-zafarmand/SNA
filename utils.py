import fileinput
from random import choice


def spaces2tabs(filename):
	# changes the delimiter in edge_list file from spaces to tabs. This change is inplace: (a b) -> (a  b)
	for line in fileinput.FileInput(filename, inplace=1):
		print(line.replace(' ', '\t'), end='')


def remove_self_loops(graph):
	# removes any edges that connects a node of the given graph to itself.
	for node in graph.nodes():
		if graph.has_edge(node, node):
			graph.remove_edge(node, node)


def find_random_node_in_graph(graph, sets_of_nodes_to_ignore):
	# returns a random node from the graph that is not supposed to be ignored.
	nodes = list(graph.nodes())
	for a_set_of_nodes_to_ignore in sets_of_nodes_to_ignore:
		for node in a_set_of_nodes_to_ignore:
			nodes.remove(node)
	return choice(nodes)


def find_highest_degree_node_in_graph(graph, sets_of_nodes_to_ignore):
	# returns the node with the highest degree from the graph that is not supposed to be ignored.
	nodes = list(graph.nodes())
	for a_set_of_nodes_to_ignore in sets_of_nodes_to_ignore:
		for node in a_set_of_nodes_to_ignore:
			nodes.remove(node)

	node_with_highest_degree = nodes[0]
	for node_index in range(1, len(nodes)):
		if graph.degree[nodes[node_index]] > graph.degree[node_with_highest_degree]:
			node_with_highest_degree = nodes[node_index]

	return node_with_highest_degree


def find_best_next_node(improvements):
	best_candidate = None
	best_improvement = - float('inf')
	for candidate, improvement in improvements.items():
		if improvement > best_improvement:
			best_candidate = candidate
			best_improvement = improvement
	return best_candidate
