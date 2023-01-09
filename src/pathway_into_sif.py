# two columns to generate hierachy
# python3 two_col_hierachy.py human_reactome_pathways_relation.tsv R-HSA-8964572
import sys
import numpy as np
import pandas as pd
from graph import Node, Edge, Graph

# read graph table
kegg_df = pd.read_csv("data/human_kegg_pathways_relationship.tsv",sep="\t",header=0)
reactome_df = pd.read_csv("data/human_reactome_pathways_relation.tsv",sep="\t",header=0)

# load annotation of Reactome
reactome_anno = pd.read_csv("data/human_reactome_pathways.tsv",sep="\t",header=0)
reactome_dict = {}
for idx in reactome_anno.index.values.tolist():
    reactome_dict[reactome_anno.at[idx,"id"]] = reactome_anno.at[idx,"description"]

# load annotation of KEGG
kegg_anno = pd.read_csv("data/hsa_annotation.tsv",sep="\t",header=0)
kegg_dict = {}
for idx in kegg_anno.index.values.tolist():
    kegg_dict[kegg_anno.at[idx,"id"]] = kegg_anno.at[idx,"annotation"]

# Add annotation to graph table
reactome_df["parent"] = reactome_df["parent"].apply(lambda x: x + ":" + reactome_dict[x])
reactome_df["child"] = reactome_df["child"].apply(lambda x: x + ":" + reactome_dict[x])
kegg_df["parent"] = kegg_df["parent"].apply(lambda x: x + ":" + kegg_dict[x] if kegg_dict.get(x) else x)
kegg_df["child"] = kegg_df["child"].apply(lambda x: x + ":" + kegg_dict[x] if kegg_dict.get(x) else x)

# Add relation column
reactome_df["relation"] = "is_parent_of"
kegg_df["relation"] = "is_parent_of"

reactome_df[["parent","relation","child"]].to_csv("data/human_reactome.sif",sep="\t",index=False,header=False)
kegg_df[["parent","relation","child"]].to_csv("data/human_kegg.sif",sep="\t",index=False,header=False)
