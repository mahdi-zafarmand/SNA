from LoadGraph import load_graph
import network_generator
from copy import deepcopy
import utils


if __name__ == '__main__':

	# uncomment the next two lines to generate networks only.
	# network_generator.make_networks_for_experiments()
	# exit(0)

	args = utils.create_argument_parser()
	dataset_folder = 'Datasets'
	graph = load_graph(dataset_folder + '/' + args.network + '.mtx')

	num_repeats = 10
	for n in range(num_repeats):
		algorithm = utils.determine_algorithm(args, deepcopy(graph))
		try:
			if args.type.lower() == 'search':
				utils.test_for_community_search(algorithm, args.network, n + 1)
			elif args.type.lower() == 'detection':
				utils.test_for_community_detection(algorithm, args.network, n + 1)
			print('Task', (n + 1), '/', num_repeats, 'is done.')
		except:
			print('- An error happened in task', (n + 1), '/', num_repeats, '.')
	print('Finish!')
