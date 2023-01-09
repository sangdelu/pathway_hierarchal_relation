# two columns to generate hierarchy
# python3 two_col_hierarchy.py human_reactome_pathways_relation.tsv R-HSA-8964572
import sys
import numpy as np
import pandas as pd
import xlrd
from graph import Node, Edge, Graph


#ora_table = sys.argv[1]

def build_graph(f):
    # build graph
    handle = open(f,"r")

    l = handle.readline().strip() # header line
    l = handle.readline().strip()

    # create the first node
    graph = Graph()
    parent = Node(l.split("\t")[0],"1")
    child = Node(l.split("\t")[1],"2")
    graph.add_node(parent)
    graph.add_node(child)
    graph.add_edge(parent,child)
    l = handle.readline().strip()

    ids = 3
    while l:
        parent = Node(l.split("\t")[0],str(ids))
        child = Node(l.split("\t")[1],str(ids + 1))
        graph.add_node(parent)
        graph.add_node(child)
        graph.add_edge(parent,child)
        ids += 2
        l = handle.readline().strip()

    handle.close()
    return graph


def check_term_parent(x):
    x = str(x)
    if x.startswith("R-HSA"):
        return graph.find_all_parent(x)
    else:
        return None

def check_term_children(x):
    x = str(x)
    if x.startswith("R-HSA"):
        return graph.find_all_children(x)
    else:
        return None

def check_term_one_child(x):
    x = str(x)
    if x.startswith("R-HSA"):
        return graph.find_one_child(x)
    else:
        return ""

# build graph
#reactome_graph = build_graph("human_reactome_pathways_relation.tsv")

# load sif
graph = build_graph("reduced.sif")

# write into mm
nodes = []
id_dict = {}
for e in graph.edge.values():
    nodes.append(e.start.name)
    nodes.append(e.end.name)
    id_dict[e.start.name] = e.start.id
    id_dict[e.end.name] = e.end.id

def export_single_chain(chain, exist_chain):
    chain_list = []
    ends = []
    for node in chain:
        temp_n = "<node ID=\"" + id_dict[node] + "\" TEXT=\"" +\
                 re.sub("R-HSA-\d+:", "", node).replace(" ", "&#x20;") + "\">"
        if temp_n not in exist_chain:
            chain_list.append(temp_n)
            ends.append("</node>")
    return chain_list + ends

print(len(graph.edge))
#print(graph.find_all_parent("R-HSA-500792:GPCR ligand binding"))
#exit()
import regex as re
#nodes = [re.sub(":.*","",n) for n in list(set(nodes))]
nodes = list(set(nodes))
cl = []
for i in range(1,len(nodes) + 1):
    """
    print(nodes[i - 1])
    if graph.find_all_children(nodes[i - 1]):
        chain = graph.find_all_children(nodes[i - 1]).split("|")[:-1]
        cl = cl + export_single_chain(chain, cl)
    """
    if graph.find_all_children(nodes[i-1]) == None:
        print(nodes[i-1])
        chain = graph.find_all_parent(nodes[i-1]).split("|")[2:] + [nodes[i-1]]
        cl = cl + export_single_chain(chain,cl)

print(len(cl))
print("".join(cl))
