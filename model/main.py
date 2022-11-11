from client import Client
from server import Server
from client import Client
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
from web3 import Web3
from sklearn.utils import shuffle

def run(NUM_CLIENTS):
    ''''Reads input data'''
    df = pd.read_csv('framingham.csv')
    # print(df.head())
    df = df.dropna()
    df.fillna(method='bfill', inplace=True)

    '''Assign number of clients and iterations'''
    # NUM_CLIENTS = 2
    NUM_ITERATIONS = 10

    client_list = list()
    for i in range(NUM_CLIENTS):
        client_list.append(f"Device_{i}")

    Bina = Server()
    Bina.train(df[:10])

    for j in range(NUM_ITERATIONS):
        df = shuffle(df)
        client_params_new = list()
        for i in range(len(client_list)):
            client_list[i] = Client(i, df[i*len(df)//NUM_CLIENTS:(i+1)*len(df)//NUM_CLIENTS])
            # print(client_list[i].client_name)
            client_list[i].train(df[i*len(df)//NUM_CLIENTS:(i+1)*len(df)//NUM_CLIENTS])
            client_params_new.append(client_list[i].broadcast_model())




        Bina.update_model(client_params_new)
        print(Bina.model.coef_.tolist())


