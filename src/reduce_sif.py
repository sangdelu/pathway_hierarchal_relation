import pandas as pd
import numpy as np
import sys

# arg 1: sif files
# arg 2: result of hierarcharl relation analysis, in TXT format

sif = pd.read_csv(sys.argv[1],sep="\t",names=["parent","relation","child"])

aim = pd.read_csv(sys.argv[2],sep=";",header=0)

aim_list = aim[aim["type"].isin(["aim","around"])]["name"].tolist()
select = sif[sif['parent'].isin(aim_list) & sif['child'].isin(aim_list)][['parent','child']]

for i in select.index.values.tolist():
    if select.at[i,'parent'] not in aim_list:
        select.at[i,'parent'] = select.at[i,'child'] + "_"
    if select.at[i,'child'] not in aim_list:
        select.at[i,'child'] = select.at[i,'parent'] + "_"

select = select.drop_duplicates()

drop_idx = []
for i in select.index.values.tolist():
    if select.at[i,'parent'] == select.at[i,'child'] and select.at[i,'parent'] not in aim_list:
        drop_idx.append(i)

select.to_csv("reduced.sif",sep="\t",index=False)
