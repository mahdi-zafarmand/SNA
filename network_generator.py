import networkx as nx


def create_network_using_lfr(network_info):
	n = network_info['n']
	tau1 = network_info['tau1']
	tau2 = network_info['tau2']
	mu = network_info['mu']
	min_degree = network_info['min_degree']
	# min_community = network_info['min_community']
	# return nx.LFR_benchmark_graph(n, tau1, tau2, mu, min_degree=min_degree, min_community=min_community)
	return nx.LFR_benchmark_graph(n, tau1, tau2, mu, min_degree=min_degree)


def write_network_info(graph, network_info, partition):
	num_nodes = graph.number_of_nodes()
	num_edges = graph.number_of_edges()
	avg_degree = num_edges * 2 / num_nodes
	modularity = nx.algorithms.community.modularity(graph, partition)

	file_name = make_file_name_out_of_network_info(network_info, 'info')
	with open(file_name, 'w') as file:
		file.write('Number of nodes: ' + str(num_nodes) + '\n')
		file.write('Number of edges: ' + str(num_edges) + '\n')
		file.write('Average degree: ' + str(avg_degree) + '\n')
		file.write('Modularity: ' + str(modularity) + '\n')


def extract_partition(graph):
	communities = {frozenset(graph.nodes[v]['community']) for v in graph}
	partition = list()
	n = 0
	for nodes_in_community in communities:
		partition.append(list(nodes_in_community))
	return partition


def extract_communities(partition):
	communities = {}
	for community in partition:
		for node in community:
			communities[node] = community
	return communities


def make_file_name_out_of_network_info(network_info, str_type):
	n = network_info['n']
	tau1 = network_info['tau1']
	tau2 = network_info['tau2']
	mu = network_info['mu']
	min_degree = network_info['min_degree']
	# min_community = network_info['min_community']

	file_name = 'Datasets/' + str_type + '_' + str(n)
	file_name += '_' + str(tau1)
	file_name += '_' + str(tau2)
	file_name += '_' + str(mu)
	file_name += '_' + str(min_degree)
	# file_name += '_' + str(min_community)

	if str_type == 'network' or str_type == 'info':
		file_name += '.mtx'
	else:
		file_name += '.txt'

	return file_name


def write_network(network_info, network):
	file_name = make_file_name_out_of_network_info(network_info, 'network')
	nx.write_edgelist(network, file_name, delimiter='\t', data=False)


def write_partition(network_info, partition):
	file_name = make_file_name_out_of_network_info(network_info, 'partition')
	with open(file_name, 'w') as file:
		for community in sorted(partition):
			community.sort()
			line = str(community) + ' (' + str(len(community)) + ')\n'
			file.write(line)


def write_communities(network_info, communities):
	file_name = make_file_name_out_of_network_info(network_info, 'communities')
	with open(file_name, 'w') as file:
		for key, value in sorted(communities.items()):
			value.sort()
			line = str(key) + ' : ' + str(value) + ' (' + str(len(value)) + ')\n'
			file.write(line)


def make_networks_for_experiments():
	network_specs = []
	# 1. for testing size of the network (7 networks)
	network_specs.append({'n': 100,       'tau1': 20, 'tau2': 10, 'mu': 0.1, 'min_degree': 10})
	network_specs.append({'n': 500,       'tau1': 20, 'tau2': 10, 'mu': 0.1, 'min_degree': 10})
	network_specs.append({'n': 1000,      'tau1': 20, 'tau2': 10, 'mu': 0.1, 'min_degree': 10})
	network_specs.append({'n': 5000,      'tau1': 20, 'tau2': 10, 'mu': 0.1, 'min_degree': 10})
	network_specs.append({'n': 10000,     'tau1': 20, 'tau2': 10, 'mu': 0.1, 'min_degree': 10})
	network_specs.append({'n': 50000,     'tau1': 20, 'tau2': 10, 'mu': 0.1, 'min_degree': 10})
	network_specs.append({'n': 100000,    'tau1': 20, 'tau2': 10, 'mu': 0.1, 'min_degree': 10})

	# 2. for testing compactness of the network (8 networks)
	# network_specs.append({'n': 1000, 'tau1': 20, 'tau2': 10, 'mu': 0.1, 'min_degree': 10})    # already generated
	network_specs.append({'n': 1000, 'tau1': 20, 'tau2': 10, 'mu': 0.1, 'min_degree': 15})
	network_specs.append({'n': 1000, 'tau1': 20, 'tau2': 10, 'mu': 0.1, 'min_degree': 20})
	network_specs.append({'n': 1000, 'tau1': 20, 'tau2': 10, 'mu': 0.1, 'min_degree': 25})
	network_specs.append({'n': 1000, 'tau1': 20, 'tau2': 10, 'mu': 0.1, 'min_degree': 30})
	network_specs.append({'n': 1000, 'tau1': 20, 'tau2': 10, 'mu': 0.1, 'min_degree': 35})
	network_specs.append({'n': 1000, 'tau1': 20, 'tau2': 10, 'mu': 0.1, 'min_degree': 40})
	network_specs.append({'n': 1000, 'tau1': 20, 'tau2': 10, 'mu': 0.1, 'min_degree': 45})

	# 3. for testing mixing parameter of the network (8 networks)
	# network_specs.append({'n': 1000, 'tau1': 20, 'tau2': 10, 'mu': 0.10, 'min_degree': 10})    # already generated
	network_specs.append({'n': 1000, 'tau1': 20, 'tau2': 10, 'mu': 0.15, 'min_degree': 10})
	network_specs.append({'n': 1000, 'tau1': 20, 'tau2': 10, 'mu': 0.20, 'min_degree': 10})
	network_specs.append({'n': 1000, 'tau1': 20, 'tau2': 10, 'mu': 0.25, 'min_degree': 10})
	network_specs.append({'n': 1000, 'tau1': 20, 'tau2': 10, 'mu': 0.30, 'min_degree': 10})
	network_specs.append({'n': 1000, 'tau1': 20, 'tau2': 10, 'mu': 0.35, 'min_degree': 10})
	network_specs.append({'n': 1000, 'tau1': 20, 'tau2': 10, 'mu': 0.40, 'min_degree': 10})
	network_specs.append({'n': 1000, 'tau1': 20, 'tau2': 10, 'mu': 0.45, 'min_degree': 10})

	for ith_network in range(len(network_specs)):
		network_spec = network_specs[ith_network]

		lfr_network = create_network_using_lfr(network_spec)
		partition = extract_partition(lfr_network)
		communities = extract_communities(partition)

		write_network_info(lfr_network, network_spec, partition)
		write_network(network_spec, lfr_network)
		write_partition(network_spec, partition)
		write_communities(network_spec, communities)
		print('Network', ith_network + 1, '/', len(network_specs), ' is generated.')

	print('All networks are generated.')
