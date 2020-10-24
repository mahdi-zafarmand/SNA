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

	def community_search(self, start_node, with_amend=False):   # no use for 'with_amend' in this algorithm.
		# THE MAIN FUNCTION OF THE CLASS, finds all other nodes that belong to the same community as the start_node does.
		self.set_start_node(start_node)
		modularity_r = 0.0
		T = self.graph.degree[start_node]

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
			self.community.append(new_node)
			self.update_shell(new_node)
			self.update_boundary(new_node)

		return sorted(self.community)   # sort is only for a better representation, can be ignored to boost performance.

	def compute_modularity(self, former_modularity_info, candidate_node):
		R, T = former_modularity_info
		neighbors_of_candidate = self.graph.neighbors(candidate_node)

		x, y, z = 0, 0, 0
		for neighbor in neighbors_of_candidate:
			if neighbor in self.boundary:
				x += 1
			else:
				y += 1

		for neighbor in [node for node in neighbors_of_candidate if node in self.boundary]:
			if self.should_leave_boundary(neighbor, candidate_node):
				z = z + self.graph.degree[neighbor]
				z = z - len([node for node in self.graph.neighbors(neighbor) if node in self.boundary])

		return float(x - R * y - z * (1 - R)) / float(T - z + y), -z + y

	def should_leave_boundary(self, main_node, neighbor_node):
		# we need to find if 'main_node' should leave 'self.boundary' because of the agglomeration of 'neighbor_node'.
		neighbors = set(self.graph.neighbors(main_node))
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
