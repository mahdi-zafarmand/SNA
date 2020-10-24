from CommunitySearch import CommunitySearcher
from CommunityDetection import CommunityDetector
import utils


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
		# # for debug
		# print('community =', self.community)
		# print('boundary =', self.boundary)
		# print('shell =', self.shell)

		return sorted(self.community)  # sort is only for a better representation, can be ignored to boost performance.

	def compute_modularity(self, candidate_node):
		pass

	def find_best_next_node(self, improvements):
		pass


class ModularityMCommunityDetection(CommunityDetector):
	# the class to detect all communities of a social network by applying Modularity M algorithm over and over.

	def __init__(self, graph):
		# initialize the object
		super().__init__('Modularity M', graph)
		self.local_searcher = ModularityMCommunityDiscovery(graph)
