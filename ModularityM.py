from CommunitySearch import CommunitySearcher
from CommunityDetection import CommunityDetector


class ModularityMCommunityDiscovery(CommunitySearcher):
	def __init__(self, graph):
		# initialize the object.
		super(ModularityMCommunityDiscovery, self).__init__('Modularity M', graph)

	def reset(self):
		# resets the object to prepare it for another use.
		super(ModularityMCommunityDiscovery, self).reset()

	def community_search(self, start_node, with_amend=False):  # no use for 'with_amend' in this algorithm.
		# THE MAIN FUNCTION OF THE CLASS, finds all other nodes that belong to the same community as the start_node does.
		self.set_start_node(start_node)
		sorted_shell = list(self.shell)

		modularity = 0.0
		while len(self.community) < self.graph.number_of_nodes() and len(self.shell) > 1:
			# addition step
			Q_list = []
			sorted_shell.sort(key=self.graph.degree)
			for candidate_node in sorted_shell:
				new_modularity = self.compute_modularity('addition', candidate_node)
				if new_modularity > modularity:
					modularity = new_modularity
					self.update_sets_when_node_joins(candidate_node)
					sorted_shell.remove(candidate_node)
					Q_list.append(candidate_node)

			while True:
				# deletion step
				Q_delete = []
				for candidate_node in self.community:
					new_modularity = self.compute_modularity('deletion', candidate_node)
					if new_modularity > modularity:
						modularity = new_modularity
						self.update_sets_when_node_leaves(candidate_node)
						Q_delete.append(candidate_node)

						if candidate_node in Q_list:
							Q_list.remove(candidate_node)

				if len(Q_delete) == 0:
					break

			for node in Q_list:
				neighbors_of_node = list(self.graph.neighbors(node))
				self.exclude_ignored_nodes(neighbors_of_node)
				for neighbor in neighbors_of_node:
					if (neighbor in self.community) is False:
						self.shell.add(neighbor)
						if (neighbor in sorted_shell) is False:
							sorted_shell.append(neighbor)

			if len(Q_list) == 0:
				break

		if self.starting_node in self.community:
			return sorted(self.community)
		return []

	def compute_modularity(self, auxiliary_info, candidate_node):
		mode = auxiliary_info
		ind_s, outd_s = 0, 0

		community = list(self.community)
		if mode == 'addition':
			community.append(candidate_node)
		elif mode == 'deletion':
			community.remove(candidate_node)

		for node in community:
			neighbors = list(self.graph.neighbors(node))
			self.exclude_ignored_nodes(neighbors)
			for neighbor in neighbors:
				if neighbor in community:
					ind_s += 1
				else:
					outd_s += 1

		return float(ind_s) / float(outd_s)


class ModularityMCommunityDetection(CommunityDetector):
	# the class to detect all communities of a social network by applying Modularity M algorithm over and over.

	def __init__(self, graph):
		# initialize the object
		super().__init__('Modularity M', graph)
		self.local_searcher = ModularityMCommunityDiscovery(graph)
