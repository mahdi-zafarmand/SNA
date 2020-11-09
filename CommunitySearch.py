from copy import deepcopy
import utils


class CommunitySearcher:
	# the high-level class to search for the community of a given node in a social network.
	minimum_improvement = 0.000001     # if an improvement is less than minimum, the process stops considering stability

	def __init__(self, name, graph, nodes_to_be_ignored=None):
		# initializes the object, not all attributes are useful for every algorithm
		if nodes_to_be_ignored is None:
			nodes_to_be_ignored = set()
		self.name = name
		self.graph = deepcopy(graph)
		self.nodes_to_be_ignored = nodes_to_be_ignored
		self.starting_node = None
		self.community = []
		self.boundary = set()
		self.shell = set()
		self.remove_self_loops()

	def __str__(self):
		return 'CS:' + self.name

	def reset(self):
		# clears auxiliary sets in order to use the same CommunitySearcher object to find next communities.
		self.community.clear()
		self.boundary.clear()
		self.shell.clear()

	def fill_ignored_nodes(self, nodes):
		# to populate the nodes that should be ignored when candidates are being picked.
		self.nodes_to_be_ignored.update(set(nodes))

	def empty_ignored_nodes(self):
		# should be called when we need community detection with overlap.
		self.nodes_to_be_ignored.clear()

	def exclude_ignored_nodes(self, given_obj):
		for node in self.nodes_to_be_ignored:
			if node in given_obj:
				given_obj.remove(node)

	def remove_self_loops(self):
		# algorithms tend to work better if there is no self-loop in the given graph, so we call this method at first.
		utils.remove_self_loops(self.graph)

	def set_start_node(self, start_node):
		# check the validity of the given start_node, then puts it in the community and initialize the shell set.
		if start_node in self.graph.nodes():
			self.starting_node = start_node
			self.community.append(start_node)
			self.boundary.add(start_node)
			self._find_initial_shell_set()
		else:
			print('Invalid starting node! Try with another one.')
			exit(-1)

	def _find_initial_shell_set(self):
		# constructs the initial shell set, which contains the candidates for the next node to join the community.
		self.shell = set(self.graph.neighbors(self.starting_node))
		self.exclude_ignored_nodes(self.shell)

	def community_search(self, start_node):
		# has different implementation for different algorithms, using "polymorphism" and "method overriding".
		pass

	def compute_modularity(self, auxiliary_info, candidate_node):
		# has different implementation for different algorithms, using "polymorphism" and "method overriding".
		pass

	def update_sets_when_node_joins(self, node, change_boundary=False):
		self.community.append(node)
		if change_boundary:
			self.update_boundary_when_node_joins(node)
		self.update_shell_when_node_joins(node)

	def update_sets_when_node_leaves(self, node, change_boundary=False):
		self.community.remove(node)
		if change_boundary:
			self.update_boundary_when_node_leaves(node)
		self.update_shell_when_node_leaves(node)

	def update_boundary_when_node_joins(self, new_node):
		# after a new_node expands the community, boundary set should be updated by adding and removing some nodes.
		neighbors_of_new_node = list(self.graph.neighbors(new_node))
		self.exclude_ignored_nodes(neighbors_of_new_node)
		should_be_boundary = False
		for neighbor in neighbors_of_new_node:
			if (neighbor in self.community) is False:
				should_be_boundary = True
				break
		if should_be_boundary:
			self.boundary.add(new_node)

		# if the only neighbor of a node that was out of community was new_node, then it should leave the boundary.
		possibles_leaving_nodes = [node for node in neighbors_of_new_node if node in self.boundary]
		for node in possibles_leaving_nodes:
			should_leave_boundary = True
			neighbors = list(self.graph.neighbors(node))
			self.exclude_ignored_nodes(neighbors)
			for neighbor in neighbors:
				if (neighbor in self.community) is False:
					should_leave_boundary = False
					break
			if should_leave_boundary:
				self.boundary.remove(node)

	def update_boundary_when_node_leaves(self, old_node):
		if old_node in self.boundary:
			self.boundary.remove(old_node)
			joining_nodes = [node for node in self.graph.neighbors(old_node) if node in self.community]
			self.exclude_ignored_nodes(joining_nodes)
			for node in joining_nodes:
				self.boundary.add(node)

	def update_shell_when_node_joins(self, new_node):
		# after a new_node expands the community, the shell set should be updated.
		self.shell.update(self.graph.neighbors(new_node))
		self.exclude_ignored_nodes(self.shell)
		for node in self.community:
			self.shell.discard(node)

	def update_shell_when_node_leaves(self, old_node):
		possibles_leaving_nodes = [node for node in self.graph.neighbors(old_node) if node in self.shell]
		for node in possibles_leaving_nodes:
			should_leave_shell = True
			for neighbor in self.graph.neighbors(node):
				if neighbor in self.community:
					should_leave_shell = False
					break
			if should_leave_shell:
				self.shell.remove(node)
		self.shell.add(old_node)
