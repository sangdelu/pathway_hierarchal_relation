# pathway_hierarchal_relation
Get biological pathway's hierarchal relationships.

Support KEGG, Reactome and GO database.

Usage:
Download KEGG/Reactome/GO databases from their official website:

Reactome:
ReactomePathwaysRelation.txt
Process into: human\_reactome\_pathways\_relation.tsv
ReactomePathways.txt
Process into: human\_reactome\_pathways.tsv

KEGG:
Download human's pathway modules and pathway maps.
Process into: human\_kegg\_pathways\_relationship.tsv and hsa\_annotation.tsv.

GO database:
OBO file.

1. Generate network file in SIF format
python3 pathway\_into\_sif.py
Two files human\_reactome.sif and human\_kegg.sif will be generated.

2. Process the ORA result files (in xlsx format):
For KEGG and Reactome: python3 append\_hierarchy.py \<input.xlsx\>

For GO database: python3 append\_hierarchy\_go.py \<input.xlsx\>

Two files will be generated: 
    - XLSX table with extra columns containing the hierarchial terms in corresponding database.
    - TXT file with two ";" sepearated columns. First column is the pathway's ID, the second column is indicating whether the pathway is result pathway from ORA ("aim") or its child pathway ("child") or between result pathways ("around").

3. The generated SIF file and TXT file can be loaded into Cytoscape for further visualization.

4. Single chain of a pathway can be extracted and converted into minmup format:
    - Run reduce\_sif.py to keep necessary network part.
    - Run export\_single\_chain.py to get all levels of a pathway. 
    - Copy the output from the last step into data/minmup.mm.
    - Use Mindmup to visualize the result.
