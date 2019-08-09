class Tree():
    def __init__(self, tree_nm, tree_typ, tree_vec):
        self.tree_nm = tree_nm
        self.tree_vec = tree_vec
        self.tree_typ = tree_typ
        self.children = list() #we need to capture the type of the children
        self.state = [[], []] #h(hidden state), c(cell state)
