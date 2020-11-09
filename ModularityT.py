from CommunitySearch import CommunitySearcher
from CommunityDetection import CommunityDetector
import utils


class ModularityTCommunityDiscovery(CommunitySearcher):
	def __init__(self, graph):
		# initialize the object.
		super(ModularityTCommunityDiscovery, self).__init__('Modularity T', graph)

	def reset(self):
		# resets the object to prepare it for another use.
		super(ModularityTCommunityDiscovery, self).reset()

	def community_search(self, start_node, with_amend=False):   # no use for 'with_amend' in this algorithm.
		# THE MAIN FUNCTION OF THE CLASS, finds all other nodes that belong to the same community as the start_node does.
		self.set_start_node(start_node)

		t_in = 0.0
		t_ex = self.compute_initial_t_ex()
		t_score = 0.0

		t_in_dict = {}
		t_ex_dict = {}
		t_score_dict = {}
		while len(self.community) < self.graph.number_of_nodes() and len(self.shell) > 0:
			t_in_dict.clear()
			t_ex_dict.clear()
			t_score_dict.clear()
			for node in self.shell:
				t_in_dict[node], t_ex_dict[node] = self.compute_modularity((t_in, t_ex), node)
				t_score_dict[node] = t_in_dict[node] * (t_in_dict[node] - t_ex_dict[node])
				t_score_dict[node] *= float(t_in_dict[node] > t_ex_dict[node])

			new_node = utils.find_best_next_node_metric_t(t_score_dict, t_ex_dict)
			new_t_score = t_score_dict[new_node]
			if new_t_score >= t_score:
				t_score, t_in, t_ex = new_t_score, t_in_dict[new_node], t_ex_dict[new_node]
				self.update_sets_when_node_joins(new_node)
			else:
				break

		return sorted(self.community)

	def compute_modularity(self, auxiliary_info, candidate_node):
		t_in, t_ex = auxiliary_info[0], auxiliary_info[1]

		incr_in = 0.0
		incr_ex = 0.0
		decr_ex = 0.0

		neighbors = list(self.graph.neighbors(candidate_node))
		self.exclude_ignored_nodes(neighbors)

		for i in range(len(neighbors)):
			for j in range(i+1, len(neighbors)):
				if self.graph.has_edge(neighbors[i], neighbors[j]):
					if (neighbors[i] in self.community) and (neighbors[j] in self.community):
						incr_in += 1
					elif ((neighbors[i] in self.community) or (neighbors[j] in self.community)) is False:
						incr_ex += 1
					elif (neighbors[i] in self.community) != (neighbors[j] in self.community):
						decr_ex += 1

		t_in += incr_in
		t_ex += (incr_ex - decr_ex)
		return t_in, t_ex

	def compute_initial_t_ex(self):
		T_ex = 0.0
		for node1 in self.shell:
			for node2 in self.shell:
				if self.graph.has_edge(node1, node2):
					T_ex += 1

		return T_ex / 2.0


class ModularityTCommunityDetection(CommunityDetector):
	# the class to detect all communities of a social network by applying Modularity L algorithm over and over.

	def __init__(self, graph):
		# initialize the object
		super().__init__('Modularity T', graph)
		self.local_searcher = ModularityTCommunityDiscovery(graph)
