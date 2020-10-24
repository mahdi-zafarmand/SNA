import networkx as nx
from LoadGraph import load_graph
from LocalSiwo import LocalSiwoCommunityDiscovery, LocalSiwoCommunityDetection
from ModularityR import ModularityRCommunityDiscovery, ModularityRCommunityDetection
from ModularityM import ModularityMCommunityDiscovery, ModularityMCommunityDetection
import time


def test_for_community_search_local_siwo(G):
	# to test the LocalSiwoCommunityDiscovery class which discovers a community using Local SIWO algorithm.
	start = time.time()
	community_searcher = LocalSiwoCommunityDiscovery(G)
	for n in sorted(G.nodes()):
		community = community_searcher.community_search(start_node=n, with_amend=True)
		community_searcher.reset()
		print(n, ':\t', community, len(community))
	print(time.time() - start)


def test_for_community_detection_local_siwo(G):
	# to test the LocalSiwoCommunityDetection class which detects all communities using Local SIWO algorithm.
	start = time.time()
	community_detector = LocalSiwoCommunityDetection(G)
	partition = community_detector.community_detection('random', overlap_enabled=False, with_amend=True)
	for e, p in enumerate(partition):
		print(e + 1, p, len(p))
	print(time.time() - start)


def test_for_community_search_modularity_r(G):
	# to test the ModularityRCommunityDiscovery class which discovers a community using Modularity R algorithm.
	start = time.time()
	community_searcher = ModularityRCommunityDiscovery(G)
	for n in sorted(G.nodes()):
		community = community_searcher.community_search(start_node=n, with_amend=True)
		community_searcher.reset()
		print(n, ':\t', community, len(community))
	print(time.time() - start)


def test_for_community_detection_modularity_r(G):
	# to test the ModularityRCommunityDetection class which detects all communities using Modularity R algorithm.
	start = time.time()
	community_detector = ModularityRCommunityDetection(G)
	partition = community_detector.community_detection('random', overlap_enabled=False, with_amend=True)
	for e, p in enumerate(partition):
		print(e + 1, p, len(p))
	print(time.time() - start)


def test_for_community_search_modularity_m(G):
	# to test the ModularityMCommunityDiscovery class which discovers a community using Modularity M algorithm.
	start = time.time()
	community_searcher = ModularityMCommunityDiscovery(G)
	for n in sorted(G.nodes()):
		community = community_searcher.community_search(start_node=n, with_amend=True)
		community_searcher.reset()
		print(n, ':\t', community, len(community))
	print(time.time() - start)


def test_for_community_detection_modularity_m(G):
	# to test the ModularityMCommunityDetection class which detects all communities using Modularity M algorithm.
	start = time.time()
	community_detector = ModularityMCommunityDetection(G)
	partition = community_detector.community_detection('random', overlap_enabled=False, with_amend=True)
	for e, p in enumerate(partition):
		print(e + 1, p, len(p))
	print(time.time() - start)


if __name__ == '__main__':
	graph = load_graph('karate_edgelist.mtx')
	print(nx.info(graph))

	# test_for_community_search_local_siwo(graph)
	# print('-' * 50)
	# test_for_community_detection_local_siwo(graph)
	# print('-' * 50)

	test_for_community_search_modularity_r(graph)
	print('-' * 50)
	test_for_community_detection_modularity_r(graph)
	print('-' * 50)

	# test_for_community_search_modularity_m(graph)
	# print('-' * 50)
	# test_for_community_detection_modularity_m(graph)
	# print('-' * 50)
