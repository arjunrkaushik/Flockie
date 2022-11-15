import uvicorn
import pickle
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
# from model.main import run
from model.server import Server
from model.client import Client
from sklearn.utils import shuffle
import pandas as pd
import os
import json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import requests

class Input(BaseModel):
    x: int

# Initializing the fast API server
app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setting up the home route
@app.get("/")
def read_root():
    return {"data": "Welcome to Flockie"}

@app.post("/aggregate/")
async def aggregate(request:Request):
    projectId = "2HWWSM26k2fOYJGFAiAxCsF2TRF"
    projectSecret = "ab5fa9048e3166641c0a2726b6351230"
    endpoint = "https://ipfs.infura.io:5001"
    # print(await request.json())
    res = await request.json()
    print("result")
    print(res)
    for i in res:
        params = {
            'arg': i
        }
        response2 = requests.post(endpoint + '/api/v0/cat', params=params, auth=(projectId, projectSecret))
        # print(response2)
        # print(response2.text)
        clients = list()
        with open(response2.text) as f:
            for line in f:
                x = line.split(",")
                # print(x)
                client=list()
                coef=list()
                intercept=list()
                classes=list()
                x[0]=x[0][2:]
                for i in range(13):
                    coef.append(float(x[i][1:]))
                x[13] = x[13][1:]
                x[13] = x[13][:-1]
                coef.append(float(x[13]))
                x[14]=x[14][2:]
                x[14]=x[14][:-1]
                intercept.append(float(x[14]))
                classes.append(int(x[15][-1]))
                classes.append(int(x[16][1]))
                client.append(coef)
                client.append(intercept)
                client.append(classes)
                clients.append(client)

    server = Server()
    server.update_model(clients)
    df = pd.read_csv('../model/framingham.csv')
    # print(df.head())
    df = df.dropna()
    df.fillna(method='bfill', inplace=True)
    df = shuffle(df)
    y = df["TenYearCHD"]
    X = df.drop(columns=['TenYearCHD', 'education'], axis=1)

    acc = server.test(X, y)

    server_grads=list()
    server_grads.append(server.model.coef_[0].tolist())
    server_grads.append(server.model.intercept_.tolist())
    server_grads.append(server.model.classes_.tolist())
    print('Server Grads: ', server_grads)

    server_file = open("server.txt", "w+")

    # Saving the 2D array in a text file
    server_content = str(server_grads)

    server_file.write(server_content)
    server_file.close()
    file = {
        'server_file': 'server.txt',
    }

    ### ADD FILE TO IPFS AND SAVE THE HASH ###
    server_response = requests.post(endpoint + '/api/v0/add', files=file, auth=(projectId, projectSecret))
    print("Server Response:",server_response)
    server_hash = server_response.text.split(",")[1].split(":")[1].replace('"', '')
    print("Server Hash:", server_hash)
    return {
        "data": {
            "accuracy": int(acc*(10**5)),
            "hash": server_hash
        }
    }

# Setting up the prediction route
@app.post("/train/")
async def train(input:Input):
    client_list = list()

    for i in range(input.x):
        client_list.append(Client(i))

    df = pd.read_csv('../model/framingham.csv')
    # print(df.head())
    df = df.dropna()
    df.fillna(method='bfill', inplace=True)
    df = shuffle(df)
    y = df["TenYearCHD"]
    X = df.drop(columns=['TenYearCHD', 'education'], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=0)

    client_count = len(client_list)
    for i in range(len(client_list)):
        client_list[i].train(X_train[i*len(X_train)//client_count:(i+1)*len(X_train)//client_count], y_train[i*len(y_train)//client_count:(i+1)*len(y_train)//client_count])

    client0=list()
    client0.append(client_list[0].model.coef_[0].tolist())
    client0.append(client_list[0].model.intercept_.tolist())
    client0.append(client_list[0].model.classes_.tolist())

    client1 = list()
    client1.append(client_list[1].model.coef_[0].tolist())
    client1.append(client_list[1].model.intercept_.tolist())
    client1.append(client_list[1].model.classes_.tolist())

    client2 = list()
    client2.append(client_list[2].model.coef_[0].tolist())
    client2.append(client_list[2].model.intercept_.tolist())
    client2.append(client_list[2].model.classes_.tolist())


    # Displaying the array
    print('Array:\n', client0)
    print('Array:\n', client1)
    print('Array:\n', client2)
    file0 = open("client0.txt", "w+")
    file1 = open("client1.txt", "w+")
    file2 = open("client2.txt", "w+")

    # Saving the 2D array in a text file
    content0 = str(client0)
    content1 = str(client1)
    content2 = str(client2)

    file0.write(content0)
    file0.close()
    file1.write(content1)
    file1.close()
    file2.write(content2)
    file2.close()

    projectId = "2HWWSM26k2fOYJGFAiAxCsF2TRF"
    projectSecret = "ab5fa9048e3166641c0a2726b6351230"
    endpoint = "https://ipfs.infura.io:5001"

    ### CREATE AN ARRAY OF TEST FILES ###
    files0 = {
        'file0': 'client0.txt',
    }
    files1 = {
        'file1': 'client1.txt',
    }
    files2 = {
        'file2': 'client2.txt',
    }

    ### ADD FILE TO IPFS AND SAVE THE HASH ###
    response0 = requests.post(endpoint + '/api/v0/add', files=files0, auth=(projectId, projectSecret))
    print(response0)
    hash0 = response0.text.split(",")[1].split(":")[1].replace('"', '')
    print(hash0)

    response1 = requests.post(endpoint + '/api/v0/add', files=files1, auth=(projectId, projectSecret))
    print(response1)
    hash1 = response1.text.split(",")[1].split(":")[1].replace('"', '')
    print(hash1)

    response2 = requests.post(endpoint + '/api/v0/add', files=files2, auth=(projectId, projectSecret))
    print(response2)
    hash2 = response2.text.split(",")[1].split(":")[1].replace('"', '')
    print(hash2)

    return {
        "data": {
            "client0": hash0,
            "client1": hash1,
            "client2": hash2
        }
    }

# Configuring the server host and port
if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')