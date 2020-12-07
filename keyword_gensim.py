from gensim.summarization import keywords
from gensim.summarization.keywords import get_graph
import networkx as nx
import matplotlib.pyplot as plt
import re

def main():
    tweets = open('1.source_preprocess/corpora/tweets.txt', 'r')
    read_tweets = tweets.readlines()

    output = open('keywords_gensim.txt', 'w')

    alltweets = []
    string_to_add = ""

    for line in read_tweets:
        line = line.strip('\n')
        if (bool(re.search('C.\d+',line))):
            continue
        elif (line == ""):
            alltweets.append(string_to_add)
            string_to_add = ""
            continue
        else:
            string_to_add += line

    allsent = ' '.join(alltweets)
    portion = allsent[0:len(allsent)//3500]
    
    #display a graph showing the network of keywords
    #NOTE: cut down the text to a portion to cut down number of keywords
    displayGraph(get_graph(portion))
    output.write(keywords(allsent, words=100, lemmatize=True))

    tweets.close()
    output.close()


def displayGraph(textGraph):
    graph = nx.Graph()
    for edge in textGraph.edges():
        graph.add_node(edge[0])
        graph.add_node(edge[1])
        graph.add_weighted_edges_from([(edge[0], edge[1], textGraph.edge_weight(edge))])

        textGraph.edge_weight(edge)
    pos = nx.spring_layout(graph)
    plt.figure()

    nx.draw(graph, pos, edge_color = 'black', width=1, linewidths=1,
            node_size=500, node_color='seagreen', alpha=0.9,
            labels={node: node for node in graph.nodes()})
    plt.axis('off')
    plt.show()

main()
