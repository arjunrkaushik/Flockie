import uvicorn
import pickle
from pydantic import BaseModel
from fastapi import FastAPI
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

class Input(BaseModel):
    x: int
    first: bool
    # params: list
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
    # if input.first == False:
    #     server = Server()
    #     server.model.coef_ = np.array(input.params[0])
    #     server.model.intercept_ = np.array(input.params[1])
    #     server.model.classes_ = np.array(input.params[2])
    #     for i in range(len(client_list)):
    #         client_list[i].get_server_model(server)
    y = df["TenYearCHD"]
    X = df.drop(columns=['TenYearCHD', 'education'], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=0)

    client_count = len(client_list)
    for i in range(len(client_list)):
        client_list[i].train(X_train[i*len(X_train)//client_count:(i+1)*len(X_train)//client_count], y_train[i*len(y_train)//client_count:(i+1)*len(y_train)//client_count])


    # encoded1 = list()
    # for i in range(len(client_list)):
    #     encoded.append((client_list[i].model.coef_.tolist(), client_list[i].model.intercept_.tolist(), client_list[i].model.classes_.tolist()))

    # encoded = json.dumps((aggregated_model.model.coef_.tolist(), aggregated_model.model.intercept_.tolist(), aggregated_model.model.classes_.tolist()))
    client0=list()
    client0.append(client_list[0].model.coef_.tolist())
    client0.append(client_list[0].model.intercept_.tolist())
    client0.append(client_list[0].model.classes_.tolist())

    client1=list()
    client1.append(client_list[1].model.coef_.tolist())
    client1.append(client_list[1].model.intercept_.tolist())
    client1.append(client_list[1].model.classes_.tolist())

    client2=list()
    client2.append(client_list[2].model.coef_.tolist())
    client2.append(client_list[2].model.intercept_.tolist())
    client2.append(client_list[2].model.classes_.tolist())
    
    return {
        "data": {
            "client0":client0,
            "client1":client1,
            "client2":client2

        }
    }

# class Candidate(BaseModel):
#     gender: int

# @app.post("/prediction/")
# async def get_predict(data: Candidate):
#     sample = [[
#         data.gender
#     ]]
#     hired = 1
#     return {
#         "data": {
#             'prediction': hired,
#             'interpretation': 'Candidate can be hired.' if hired == 1 else 'Candidate can not be hired.'
#         }
#     }
# Configuring the server host and port
if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')