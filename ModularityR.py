from CommunitySearch import CommunitySearcher
from CommunityDetection import CommunityDetector
import utils


class ModularityRCommunityDiscovery(CommunitySearcher):
	def __init__(self, graph):
		# initialize the object.
		super(ModularityRCommunityDiscovery, self).__init__('Modularity R', graph)

	def reset(self):
		# resets the object to prepare it for another use.
		super(ModularityRCommunityDiscovery, self).reset()

	def community_search(self, start_node):   # no use for 'with_amend' in this algorithm.
		# THE MAIN FUNCTION OF THE CLASS, finds all other nodes that belong to the same community as the start_node does.
		self.set_start_node(start_node)
		modularity_r = 0.0
		neighbors = list(self.graph.neighbors(start_node))
		self.exclude_ignored_nodes(neighbors)
		T = len(neighbors)

		while len(self.community) < self.graph.number_of_nodes() and len(self.shell) > 0:
			delta_r = {}  # key: candidate nodes from the shell set, value: total improved strength after a node joins.
			delta_T = {}  # key: candidate nodes from the shell set, value: delta T (based on notations of the paper).
			for node in self.shell:
				delta_r[node], delta_T[node] = self.compute_modularity((modularity_r, T), node)

			new_node = utils.find_best_next_node(delta_r)
			if delta_r[new_node] < CommunitySearcher.minimum_improvement:
				break

			modularity_r += delta_r[new_node]
			T += delta_T[new_node]
			self.update_sets_when_node_joins(new_node, change_boundary=True)

		return sorted(self.community)   # sort is only for a better representation, can be ignored to boost performance.

	def compute_modularity(self, auxiliary_info, candidate_node):
		R, T = auxiliary_info
		neighbors_of_candidate = list(self.graph.neighbors(candidate_node))
		self.exclude_ignored_nodes(neighbors_of_candidate)

		x, y, z = 0, 0, 0
		for neighbor in neighbors_of_candidate:
			if neighbor in self.boundary:
				x += 1
			else:
				y += 1

		for neighbor in [node for node in neighbors_of_candidate if node in self.boundary]:
			if self.should_leave_boundary(neighbor, candidate_node):
				for node in self.graph.neighbors(neighbor):
					if (node in self.community) and ((node in self.boundary) is False):
						z += 1
		return float(x - R * y - z * (1 - R)) / float(T - z + y), -z + y

	def should_leave_boundary(self, possibly_leaving_node, neighbor_node):
		# to find if 'possibly_leaving_node' should leave 'self.boundary' because of the agglomeration of 'neighbor_node'.
		neighbors = set(self.graph.neighbors(possibly_leaving_node))
		self.exclude_ignored_nodes(neighbors)
		neighbors.discard(neighbor_node)
		for neighbor in neighbors:
			if (neighbor in self.community) is False:
				return False
		return True


class ModularityRCommunityDetection(CommunityDetector):
	# the class to detect all communities of a social network by applying Modularity R algorithm over and over.

	def __init__(self, graph):
		# initialize the object
		super().__init__('Modularity R', graph)
		self.local_searcher = ModularityRCommunityDiscovery(graph)
