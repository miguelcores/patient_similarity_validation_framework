'''
Reference implementation of node2vec.

Author: Aditya Grover

For more details, refer to the paper:
node2vec: Scalable Feature Learning for Networks
Aditya Grover and Jure Leskovec
Knowledge Discovery and Data Mining (KDD), 2016
'''
import networkx as nx
from node2vec import node2vec
from gensim.models import Word2Vec

from Common import save_object

# genEmbeddings(input='_data/graph/hp-obo.edgelist', output='_data/emb/hp-obo_prueba.emb')
class genEmbeddings():
    def __init__(self, input, output, weighted=False, p=1, q=.05, window_size=10, num_walks=10,
                 walk_length=5, dimensions=128, directed=False, workers=8, iter=1):
        self.input = input
        self.output = output
        self.weighted = weighted
        self.p = p
        self.q = q
        self.window_size = window_size
        self.num_walks = num_walks
        self.walk_length = walk_length
        self.dimensions = dimensions
        self.directed = directed
        self.workers = workers
        self.iter = iter

        nx_G = self.read_graph()
        G = node2vec.Graph(nx_G, self.directed, self.p, self.q)
        G.preprocess_transition_probs()
        walks = G.simulate_walks(self.num_walks, self.walk_length)
        self.learn_embeddings(walks)

    def read_graph(self):
        '''
        Reads the input network in networkx.
        '''
        if self.weighted:
            G = nx.read_edgelist(self.input, nodetype=int, data=(('weight',float),), create_using=nx.DiGraph())
        else:
            G = nx.read_edgelist(self.input, nodetype=int, create_using=nx.DiGraph())
            for edge in G.edges():
                G[edge[0]][edge[1]]['weight'] = 1

        if not self.directed:
            G = G.to_undirected()

        return G

    def learn_embeddings(self, walks):
        '''
        Learn embeddings by optimizing the Skipgram objective using SGD.
        '''
        # walks = [map(str, walk) for walk in walks] #py2
        walks = [list(map(str, walk)) for walk in walks]
        save_object(walks, './_data/walks/walks.pkl')
        model = Word2Vec(walks, size=self.dimensions, window=self.window_size, min_count=0, sg=1, workers=self.workers, iter=self.iter)
        # model.save_word2vec_format(args.output) #deprecated
        model.wv.save_word2vec_format(self.output)

        return
