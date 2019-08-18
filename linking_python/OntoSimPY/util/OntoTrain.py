import sys

sys.path.append("./")

from OntoSimImports import *
import OntoSimConstants as cnst
from Tree import Tree
from TreeTyp import TreeTyp
from TreeLSTM import TreeLSTM

epoch_num = 3
show_epoch_info = 1

load_prev_model = False
prev_model_nm = "model/onto_model/model_v1_300_mean_final.pt"
saved_epoch = -1

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if (torch.cuda.is_available()):
    print("GPU is available ")
    print("Is GPU available :- " + str(torch.cuda.is_available()))
    print("GPU device name :- " + torch.cuda.get_device_name(0))
else:
    print("CPU is available ")


def assignVar():
    conf_300 = {
        'vec_dim': 300,
        'train_file': "ontodata/train_test_tree/source_300_mean.pt",
        'model_file': "model/onto_model/model_300_mean"
    }

    conf_arr = []
    conf_arr.append(conf_300)
    return conf_arr


def loadTrainTree(conf):
    trees = torch.load(cnst.code_path + conf["train_file"])
    return trees


def trainOnto(trees, conf):
    if (load_prev_model):
        tree_lstm_model = TreeLSTM(conf['vec_dim'], conf['vec_dim'], device)
        tree_lstm_model.load_state_dict(torch.load(cnst.code_path + prev_model_nm))
    else:
        tree_lstm_model = TreeLSTM(conf['vec_dim'], conf['vec_dim'], device)

    tree_lstm_model.to(device)  # transfering to GPU

    # in-place operator, i.e to method will change the net itself moves it to device
    # but this is not true for Tensor object, for tensor you need to do this inputs = inputs.to(device)

    optimizer = optim.Adam(tree_lstm_model.parameters(), lr=0.001)
    loss_fn = nn.MSELoss()
    tree_lstm_model.train()  # setting into train mode

    #   print("begining======================\n")
    #   for name, param in tree_lstm_model.named_parameters():
    #       if param.requires_grad:
    #           print(name, torch.mean(param.cpu().data).numpy())

    total_train_len = len(trees)

    for epoch in range(saved_epoch + 1, epoch_num):
        LOSS = 0
        for tree_key in trees:
            tree = trees[tree_key]
            optimizer.zero_grad()
            pred = tree_lstm_model(tree, device)
            pred = pred.to(device)
            y_in = tree.tree_vec
            y_in = np.asarray(y_in)
            y_in = np.reshape(y_in, (1, y_in.shape[0]))
            y_in_tensor = torch.tensor(y_in, dtype=torch.float64).float()
            y_in_tensor = y_in_tensor.to(device)  # transfering to GPU
            loss = loss_fn(pred, y_in_tensor)
            loss.backward()
            optimizer.step()
            LOSS += loss.item()
        if ((epoch + 1) % show_epoch_info) == 0:
            print("epoch = %4d  loss = %0.10f" % ((epoch + 1), (LOSS / total_train_len)))
            torch.save(tree_lstm_model.state_dict(), cnst.dev_onto_model_path + conf['model_file'] + "_" + str(epoch) + ".pt")
    #       print("======================\n")
    #       for name, param in tree_lstm_model.named_parameters():
    #           if param.requires_grad:
    #               print(name, torch.mean(param.cpu().data).numpy())
    return tree_lstm_model


def saveModel(model, conf):
    torch.save(model.state_dict(), cnst.onto_model_path + conf['model_file'] + "_final.pt")


def sendJobStatusEmail(strt_tm, end_tm, total_time_taken):
    email_subj = "Job  Done"
    fl_nm = "06_OntoTrain_v1"
    email_body = "Job Start: {}\n" \
                 "Job End: {}\n" \
                 "Time taken: {}\n" \
                 "File Name: {}".format(strt_tm, end_tm, total_time_taken, fl_nm)
    try:
        import send_cust_email
        send_cust_email.sendJobEmail(email_subj, email_body)
    except Exception as exception:
        print("Error: %s!\n\n" % exception)
        email_subj = "Job Exception"
        import send_cust_email
        send_cust_email.sendJobEmail(email_subj, email_body)


#################### Main Code START ####################
def trainOntoSim():
    try:
        print("#################### OntoTraining START ####################")
        strt_tm = datetime.datetime.now()
        conf_arr = assignVar()

        for conf in conf_arr:
            train_trees = loadTrainTree(conf)
            onto_model = trainOnto(train_trees, conf)
            saveModel(onto_model, conf)
            time.sleep(30)  # wait for 30 seconds
    except Exception as exp:
        print(traceback.format_exc())
    finally:
        end_tm = datetime.datetime.now()
        total_time_taken = end_tm - strt_tm
        print("Total time taken :- " + str(total_time_taken))
        # sendJobStatusEmail(strt_tm, end_tm, total_time_taken)
        print("#################### OntoTraining FINISH ####################")


#################### Main Code END ####################

if __name__ == "__main__":
    trainOntoSim()
