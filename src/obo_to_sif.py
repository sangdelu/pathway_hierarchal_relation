import sys


f = sys.argv[1]

handle = open(f,"r")

l = handle.readline()

lines = []
start = False
while l:
    if l.strip() == "[Term]":
        # start a new term
    
        start = True
        if lines:
            for i in lines:
              i_lst = [x.strip() for x in i.split(":",1)]
              if i_lst[0] == "id":
                source_id = i_lst[1]
              elif i_lst[0] == "name":
                source_name = i_lst[1]
              elif i_lst[0] == "namespace":
                out_handle = open(i_lst[1] + ".sif", "a")
              elif i_lst[0] == "is_a":
                relation = "subtype of"
                target_id = i_lst[1].split(" ! ")[0]
                target_name = i_lst[1].split(" ! ")[1]
                out_handle.write(source_id + ";" + source_name + "\t" + \
                                 relation + "\t" + target_id + ";" + target_name + "\n")
              elif i_lst[0] == "relationship":
                relation = i_lst[1].split(" ",1)[0]
                target_temp = i_lst[1].split(" ",1)[1].strip()
                target_id = target_temp.split(" ! ")[0]
                target_name = target_temp.split(" ! ")[1]
                out_handle.write(source_id + ";" + source_name + "\t" + \
                                 relation + "\t" + target_id + ";" + target_name + "\n")   
           
        lines = []
        l = handle.readline() 
    elif start == True:
        lines.append(l.strip())
        l = handle.readline()    
    else:
        # skip lines before the first GO term
        l = handle.readline()
