from CommunitySearch import CommunitySearcher
import networkx as nx
from copy import deepcopy


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

		while len(self.community) < self.graph.number_of_nodes() and self.shell != []:
			improvements = {}  # key: candidate nodes from the shell set, value: total improved strength after a node joins.
			for node in self.shell:
				self.compute_modularity(node)

			new_node, improvement = self.find_best_next_node(improvements)
			if improvement < CommunitySearcher.minimum_improvement:
				break

			self.community.append(new_node)
			self.update_shell(new_node)
			self.update_boundary(new_node)

		return sorted(self.community)   # sort is only for a better representation, can be ignored to boost performance.

	def compute_modularity(self, candidate_node):
		pass

	def find_best_next_node(self, improvements):
		pass