class Node:
    def __init__(self, name):
        self.name = name
        self.next = None
        self.previous = None

    def set_next(self,node):
        self.next = node
    
    def set_previous(self,node):
        self.previous = node

    def get_previous(self):
        return self.previous

    def get_next(self):
        return self.next


class Edge:
    def __init__(self,start_node,end_node):
        self.start = start_node
        self.end = end_node

    def set_relation(self):
        self.start.set_next(self.end)
        self.end.set_previous(self.start)


class Graph:
    def __init__(self):
        self.node_number = 1
        self.edge = {}

    def add_node(self,node):
        self.node_number = self.node_number + 1

    def add_edge(self,start_node,end_node):
        new_edge = Edge(start_node,end_node)
        new_edge.set_relation()
        self.edge[start_node.name + ":" + end_node.name] = new_edge

    def get_edge(self,node_name1, node_name2):
        return self.edge[node_name1 + ":" + node_name2]

    def find_all_parent(self,node_name):
        for k in list(self.edge.keys()):
            if k.endswith(node_name):
                search_node = self.edge[k].start
                return str(self.find_all_parent(search_node.name)) + "|" + search_node.name

    def find_all_children(self,node_name):
        for k in list(self.edge.keys()):
            if k.split(":")[0].startswith(node_name):
                search_node = self.edge[k].end
                return search_node.name + "|" + str(self.find_all_children(search_node.name))

    def find_one_child(self,node_name):
        children = ""
        for k in list(self.edge.keys()):
            if k.split(":")[0].startswith(node_name):
                search_node = self.edge[k].end
                children = children + "|" + search_node.name
        return children
