from CommunitySearch import CommunitySearcher
from CommunityDetection import CommunityDetector
import utils


class ModularityLCommunityDiscovery(CommunitySearcher):
	def __init__(self, graph):
		# initialize the object.
		super(ModularityLCommunityDiscovery, self).__init__('Modularity L', graph)

	def reset(self):
		# resets the object to prepare it for another use.
		super(ModularityLCommunityDiscovery, self).reset()

	def community_search(self, start_node, with_amend=False):   # no use for 'with_amend' in this algorithm.
		# THE MAIN FUNCTION OF THE CLASS, finds all other nodes that belong to the same community as the start_node does.
		self.set_start_node(start_node)
		modularity, l_in, l_ex = 0.0, 0.0, 0.0
		new_l_in = {}
		new_l_ex = {}
		new_modularity = {}

		while len(self.community) < self.graph.number_of_nodes() and len(self.shell) > 0:
			new_modularity.clear()
			new_l_in.clear()
			new_l_ex.clear()
			for node in self.shell:
				new_l_in[node], new_l_ex[node] = self.compute_modularity('addition', node)
				new_modularity[node] = new_l_in[node] / new_l_ex[node]

			new_node = utils.find_best_next_node(new_modularity)
			if new_l_in[new_node] > l_in:
				self.update_sets_when_node_joins(new_node)
				modularity = new_modularity[new_node]
				l_in = new_l_in[new_node]
				l_ex = new_l_ex[new_node]
			else:
				self.shell.remove(new_node)

			if new_modularity[new_node] < modularity:
				break

		# new_l_in.clear()
		# new_l_ex.clear()
		# for node in list(self.community):
		# 	self.update_sets_when_node_leaves(node)
		# 	l_in, l_ex = self.compute_modularity('', None)
		# 	new_l_in[node], new_l_ex[node] = self.compute_modularity('addition', node)
		# 	if new_l_in[node] > l_in and new_l_ex[node] < l_ex:
		# 		print('-- return to C =', node)
		# 		self.update_sets_when_node_joins(node)
		# 		l_in = new_l_in[node]
		# 		l_ex = new_l_ex[node]

		if start_node in self.community:
			return sorted(self.community)
		return []

	def compute_modularity(self, mode, candidate_node):
		community = list(self.community)
		if mode == 'addition':
			community.append(candidate_node)

		boundary = list(self.boundary)
		if mode == 'addition':
			for neighbor in self.graph.neighbors(candidate_node):
				if (neighbor in community) is False:
					boundary.append(candidate_node)
					break

		num_internal_edge = 0
		num_external_edge = 0

		for node in community:
			for neighbor in self.graph.neighbors(node):
				if neighbor in community:
					num_internal_edge += 1
				elif node in boundary:
					num_external_edge += 1

		num_internal_edge /= 2

		l_in = float(num_internal_edge) / len(community)
		l_ex = float(num_external_edge) / len(boundary)
		return l_in, l_ex


class ModularityLCommunityDetection(CommunityDetector):
	# the class to detect all communities of a social network by applying Modularity L algorithm over and over.

	def __init__(self, graph):
		# initialize the object
		super().__init__('Modularity L', graph)
		self.local_searcher = ModularityLCommunityDiscovery(graph)
