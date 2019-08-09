from OntoSimImports import *
import OntoSimConstants as cnst
from Tree import Tree
from TreeTyp import TreeTyp


class TreeLSTM(nn.Module):
    def __init__(self, insize, hiddensize, device):
        super(TreeLSTM, self).__init__()
        self.in_dim = insize
        self.hidden_dim = hiddensize

        # To keep the weight initialization for all LSTM cell same
        #    torch.manual_seed(999)
        #    self.lstm_root = torch.nn.LSTMCell(self.in_dim,self.hidden_dim)
        #    self.lstm_root.to(device)#transfering to GPU
        torch.manual_seed(999)
        self.lstm_parent = torch.nn.LSTMCell(self.in_dim, self.hidden_dim)
        self.lstm_parent.to(device)  # transfering to GPU
        torch.manual_seed(999)
        self.lstm_child = torch.nn.LSTMCell(self.in_dim, self.hidden_dim)
        self.lstm_child.to(device)  # transfering to GPU
        torch.manual_seed(999)
        self.lstm_eqcls = torch.nn.LSTMCell(self.in_dim, self.hidden_dim)
        self.lstm_eqcls.to(device)  # transfering to GPU
        torch.manual_seed(999)
        self.lstm_disjcls = torch.nn.LSTMCell(self.in_dim, self.hidden_dim)
        self.lstm_disjcls.to(device)  # transfering to GPU
        torch.manual_seed(999)
        self.lstm_rescls = torch.nn.LSTMCell(self.in_dim, self.hidden_dim)
        self.lstm_rescls.to(device)  # transfering to GPU

    def get_child_states(self, tree, device):
        num_children = len(tree.children)
        if (num_children == 0):
            child_h = Variable(torch.zeros(1, 1, self.hidden_dim, dtype=torch.float64))
            child_c = Variable(torch.zeros(1, 1, self.hidden_dim, dtype=torch.float64))
        else:
            child_h = torch.Tensor(num_children, 1, self.hidden_dim)
            child_c = torch.Tensor(num_children, 1, self.hidden_dim)
            for idx in range(num_children):
                child = tree.children[idx]
                child_h[idx] = child.state[0]
                child_c[idx] = child.state[1]

        child_h = child_h.to(device)  # transfering to GPU
        child_c = child_c.to(device)  # transfering to GPU
        return child_h, child_c

    def calc_cell_op(self, tree, child_h, child_c, device):

        child_h_sum = torch.mean(child_h, dim=0, keepdim=False).float()
        child_c_sum = torch.mean(child_c, dim=0, keepdim=False).float()

        x_in = tree.tree_vec
        x_in = np.asarray(x_in)
        if(x_in.shape[0] == 1):
            print(tree.tree_nm)
            print(x_in.shape)
            print(x_in)
        x_in = np.reshape(x_in, (1, x_in.shape[0]))
        x_in_tensor = torch.tensor(x_in, dtype=torch.float64).float()
        x_in_tensor = x_in_tensor.to(device)  # transfering to GPU
        if (tree.tree_typ == TreeTyp.ROOT[0]):
            #      self_h, self_c =  self.lstm_root(child_h_sum,(child_h_sum,child_c_sum)) #h, c
            #      root_in_tensor = torch.ones(1, self.hidden_dim, dtype=torch.float64).float()
            #      root_in_tensor = root_in_tensor.to(device)
            #      self_h, self_c =  self.lstm_root(root_in_tensor,(child_h_sum,child_c_sum)) #h, c
            self_h, self_c = child_h_sum, child_c_sum
        if (tree.tree_typ == TreeTyp.PARENT[0]):
            self_h, self_c = self.lstm_parent(x_in_tensor, (child_h_sum, child_c_sum))  # h, c
        if (tree.tree_typ == TreeTyp.CHILD[0]):
            self_h, self_c = self.lstm_child(x_in_tensor, (child_h_sum, child_c_sum))  # h, c
        if (tree.tree_typ == TreeTyp.EQCLS[0]):
            self_h, self_c = self.lstm_eqcls(x_in_tensor, (child_h_sum, child_c_sum))  # h, c
        if (tree.tree_typ == TreeTyp.DISJCLS[0]):
            self_h, self_c = self.lstm_disjcls(x_in_tensor, (child_h_sum, child_c_sum))  # h, c
        if (tree.tree_typ == TreeTyp.RES[0]):
            self_h, self_c = self.lstm_rescls(x_in_tensor, (child_h_sum, child_c_sum))  # h, c

        self_h = self_h.to(device)  # transfering to GPU
        self_c = self_c.to(device)  # transfering to GPU

        return self_h, self_c

    def forward(self, tree, device):
        num_children = len(tree.children)
        for idx in range(num_children):
            self.forward(tree.children[idx], device)

        child_h, child_c = self.get_child_states(tree, device)
        tree.state = self.calc_cell_op(tree, child_h, child_c, device)

        return tree.state[0]
