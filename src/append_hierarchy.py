# two columns to generate hierarchy
# python3 two_col_hierarchy.py human_reactome_pathways_relation.tsv R-HSA-8964572
import sys
import numpy as np
import pandas as pd
import xlrd
from graph import Node, Edge, Graph


ora_table = sys.argv[1]

def build_graph(f):
    # build graph
    handle = open(f,"r")

    l = handle.readline().strip() # header line
    l = handle.readline().strip()

    # create the first node
    graph = Graph()
    parent = Node(l.split("\t")[0])
    child = Node(l.split("\t")[1])
    graph.add_node(parent)
    graph.add_node(child)
    graph.add_edge(parent,child)
    l = handle.readline().strip()

    while l:
        parent = Node(l.split("\t")[0])
        child = Node(l.split("\t")[1])
        graph.add_node(parent)
        graph.add_node(child)
        graph.add_edge(parent,child)
        l = handle.readline().strip()

    handle.close()
    return graph


def check_term_parent(x):
    x = str(x)
    if x.startswith("hsa"):
        return kegg_graph.find_all_parent(x)
    elif x.startswith("R-HSA"):
        return reactome_graph.find_all_parent(x)
    else:
        return None

def check_term_children(x):
    x = str(x)
    if x.startswith("hsa"):
        return kegg_graph.find_all_children(x)
    elif x.startswith("R-HSA"):
        return reactome_graph.find_all_children(x)
    else:
        return None

def check_term_one_child(x):
    x = str(x)
    if x.startswith("hsa"):
        return kegg_graph.find_one_child(x)
    elif x.startswith("R-HSA"):
        return reactome_graph.find_one_child(x)
    else:
        return ""

def append_description(x):
    x = x.replace("Top|","")  # skip "Top,"
    if x.startswith("R-HSA"):
        x = x.split("|")
        return "".join([i+":"+reactome_dict[i]+"|" if reactome_dict.get(i) else i+"|" for i in x ])[:-1]
    else:
        x = x.split("|")
        return "".join([i+":"+kegg_dict[i]+"|" if kegg_dict.get(i) else i+"|" for i in x ])[:-1]


# build graph
kegg_graph = build_graph("data/human_kegg_pathways_relationship.tsv")
reactome_graph = build_graph("data/human_reactome_pathways_relation.tsv")

# load sif
#reactome_sif = pd.read_csv("human_reactome.sif",sep="\t",header=0)
#kegg_sif = pd.read_csv("human_kegg.sif",sep="\t",header=0)

# load annotation of Reactome
reactome_df = pd.read_csv("data/human_reactome_pathways.tsv",sep="\t",header=0)
reactome_dict = {}
for idx in reactome_df.index.values.tolist():
    reactome_dict[reactome_df.at[idx,"id"]] = reactome_df.at[idx,"description"]

# load annotation of KEGG
kegg_df = pd.read_csv("data/hsa_annotation.tsv",sep="\t",header=0)
kegg_dict = {}
for idx in kegg_df.index.values.tolist():
    kegg_dict[kegg_df.at[idx,"id"]] = kegg_df.at[idx,"annotation"]

# append hierarchy column to ora_table:
#ora_df = pd.read_csv(ora_table,sep="\t",header=0)
ora_df = pd.read_excel(ora_table)
ora_df = ora_df.fillna("")

ora_df["hierarchy"] = ora_df["gs_exact_source"].apply(lambda x: check_term_parent(x) + "|" + x if check_term_parent(x) else x)
ora_df["hierarchy"] = ora_df["hierarchy"].apply(lambda x: x.replace("None|","Top|"))
ora_df["hierarchy"] = ora_df["hierarchy"].apply(lambda x: append_description(x))
ora_df["child"] = ora_df["gs_exact_source"].apply(lambda x: check_term_one_child(x))
# x[1:]: remove | at the beginning
ora_df["child"] = ora_df["child"].apply(lambda x: append_description(x[1:]) if x and x != "" and x != "None" else "")

# three columns, as Malik suggested, try
ora_df["top_hierarchy"] = ora_df["hierarchy"].apply(lambda x: x.split("|")[0] if x else "")
ora_df["one_uplevel_hierarchy"] = ora_df["hierarchy"].apply(lambda x: x.split("|")[-2] if x and (len(x.split("|")) > 2) else "")
ora_df["self_hierarchy"] = ora_df["hierarchy"].apply(lambda x: x.split("|")[-1] if x else "")

# output:
# mark hierarchy nodes in graph
chosen_nodes = list(set([n for i in ora_df["hierarchy"].tolist() for n in i.split("|") if n != "" and n != "None"]))
children_nodes = list(set([x for j in ora_df["child"].tolist() for x in j.split("|") if x != "" and x != "None"]))
children_nodes = [x for x in children_nodes if x not in chosen_nodes]

with open(ora_table.replace(".xlsx","_hierarchy.txt"),"w") as out_handle:
    out_handle.write("name;type\n")
    for n in chosen_nodes:
        if n.split(":")[0].strip() in ora_df["gs_exact_source"].tolist():
             out_handle.write(n+";"+"aim\n")
        else:
           out_handle.write(n+";"+"around\n")
    for c in children_nodes:
        out_handle.write(c +";"+"child\n")

# to xlsx file
#ora_df.to_csv("hierchy_"+ora_table,sep="\t",index=False)
writer = pd.ExcelWriter(ora_table.replace(".xlsx","_hierarchy.xlsx"),engine='xlsxwriter')
ora_df.to_excel(writer, sheet_name='sheet1', index=False)#, freeze_panes=(0, 1))
writer.close()

