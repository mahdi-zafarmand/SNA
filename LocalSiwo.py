from CommunitySearch import CommunitySearcher
from CommunityDetection import CommunityDetector
import networkx as nx
from random import choice


class LocalSiwoCommunityDiscovery(CommunitySearcher):
	# the class to search for the community of a given node in a social network using Local SIWO algorithm.

	def __init__(self, graph, nodes_to_be_ignored=None):
		# initializes the object
		super(LocalSiwoCommunityDiscovery, self).__init__('Local SIWO', graph, nodes_to_be_ignored)
		self.dict_common_neighbors = {}
		self.max_common_neighbors = {}
		self.strength_assigned_nodes = set()  # assigning strength values to the edges that are connected to these nodes.

	def reset(self):
		# resets the object to prepare it for another use
		super(LocalSiwoCommunityDiscovery, self).reset()

	def update_dicts_of_common_neighbors_info(self, node):
		# gathers info about the number/max number of common neighbors of the given node and its neighbors
		# (in another word): counts the number of triangles a node participates in and max number of triangles that
		# this node simultaneously participates in with a neighbor node.

		# initializing for a node that has not been visited yet.
		if (node in self.dict_common_neighbors) is False:
			self.dict_common_neighbors[node] = {}
			self.max_common_neighbors[node] = -1

		for neighbor in self.graph.neighbors(node):
			if (neighbor in self.dict_common_neighbors[node]) is False:
				if (neighbor in self.dict_common_neighbors) is False:
					self.dict_common_neighbors[neighbor] = {}
					self.max_common_neighbors[neighbor] = -1

				number_common_neighbors = sum(1 for _ in nx.common_neighbors(self.graph, node, neighbor))
				self.dict_common_neighbors[node][neighbor] = number_common_neighbors
				self.dict_common_neighbors[neighbor][node] = number_common_neighbors

				if number_common_neighbors > self.max_common_neighbors[node]:
					self.max_common_neighbors[node] = number_common_neighbors
				if number_common_neighbors > self.max_common_neighbors[neighbor]:
					self.max_common_neighbors[neighbor] = number_common_neighbors

	def assign_local_strength(self, node):
		# assigns strength to the edges that are connected to the given node, if the node has not been visited before.
		if node in self.strength_assigned_nodes:
			return

		self.update_dicts_of_common_neighbors_info(node)
		max_mutual_node = self.max_common_neighbors.get(node)

		for neighbor in self.graph.neighbors(node):
			max_mutual_neighbor = self.max_common_neighbors.get(neighbor)
			strength = self.dict_common_neighbors.get(node).get(neighbor)
			try:
				s1 = strength / max_mutual_node
			except ZeroDivisionError:
				s1 = 0.0
			try:
				s2 = strength / max_mutual_neighbor
			except ZeroDivisionError:
				s2 = 0.0

			strength = s1 + s2 - 1.0
			self.graph.add_edge(node, neighbor, strength=strength)
		self.strength_assigned_nodes.add(node)

	def find_best_next_node(self, improvements):
		# updates the improvement that can be achieved by merging a node from shell to community, then returns the max.
		new_node = self.community[-1]   # we only update improvements that are affected by adding the last node
		for node in self.shell:
			if (node in improvements) is False:
				improvements[node] = self.graph[node][new_node].get('strength', 0.0)
			elif self.graph.has_edge(node, new_node):
				improvements[node] += self.graph[node][new_node].get('strength', 0.0)
		if new_node in improvements:
			del improvements[new_node]

		best_candidate = None
		best_improvement = -float('inf')
		for candidate in self.shell:
			if improvements[candidate] > best_improvement:
				best_candidate = candidate
				best_improvement = improvements[candidate]

		return best_candidate, best_improvement

	def merge_dangling_nodes(self):
		# adds any dangling node in the neighborhood of the discovered community.
		neighborhood = set()
		for node in self.community:
			for neighbor in self.graph.neighbors(node):
				neighborhood.add(neighbor)

		dangling_neighbors = [node for node in neighborhood if self.graph.degree[node] == 1]
		self.exclude_ignored_nodes(dangling_neighbors)
		self.community = list(set(self.community + dangling_neighbors))
		self.fill_ignored_nodes(dangling_neighbors)

	def amend_small_communities(self):
		if len(self.community) < 3:
			neighbors = set()
			for node in self.community:
				neighbors.update(self.graph.neighbors(node))
			for node in self.community:
				neighbors.discard(node)
			self.exclude_ignored_nodes(neighbors)
			if len(neighbors) > 0:
				random_start_node = choice(list(neighbors))
				next_community_searcher = LocalSiwoCommunityDiscovery(self.graph, set(self.nodes_to_be_ignored))
				self.community += next_community_searcher.community_search(random_start_node)
				self.fill_ignored_nodes(self.community)

	def community_search(self, start_node):
		# THE MAIN FUNCTION OF THE CLASS, finds all other nodes that belong to the same community as the start_node does.
		self.set_start_node(start_node)
		self.assign_local_strength(self.starting_node)

		improvements = {}  # key: candidate nodes from the shell set, value: total improved strength after a node joins.
		while len(self.community) < self.graph.number_of_nodes() and len(self.shell) > 0:
			for node in self.shell:
				self.assign_local_strength(node)

			new_node, improvement = self.find_best_next_node(improvements)
			if improvement < CommunitySearcher.minimum_improvement:
				break

			self.update_sets_when_node_joins(new_node)

		self.amend_small_communities()
		self.merge_dangling_nodes()
		return sorted(self.community)   # sort is only for a better representation, can be ignored to boost performance.


class LocalSiwoCommunityDetection(CommunityDetector):
	# the class to detect all communities of a social network by applying Local SIWO algorithm over and over.

	def __init__(self, graph):
		# initialize the object
		super().__init__('Local SIWO', graph)
		self.local_searcher = LocalSiwoCommunityDiscovery(graph)
