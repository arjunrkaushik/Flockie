import pandas as pd
import numpy as np
import json
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class Client:

    def __init__(self,id):
        self.model = LogisticRegression()
        self.client_id = id
        self.client_name = "Device_"+str(id)
        # self.data = dataset
    
    def train(self, X, y):
        # y = data["TenYearCHD"]
        # X = data.drop(columns=['TenYearCHD', 'education'], axis=1)
        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=0)
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X)


        self.model.fit(X_train,y)
        
        # encoded = json.dumps((self.model.coef_.tolist(), self.model.intercept_.tolist(), self.model.classes_.tolist()))
        print("Training "+ str(self.client_name) + " done")
        return


    def test(self, X, y):
        # y = self.data["TenYearCHD"]
        # X = self.data.drop(columns=['TenYearCHD', 'education'], axis=1)
        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=0)

        scaler = StandardScaler()
        # X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X)
        predictions = self.model.predict(X)
        accuracy = np.sum(predictions == y) / y.shape[0] * 100

        return accuracy
    
    # def get_server_model(self, parameters):
    #     self.model.coef_ = np.array(parameters[0])
    #     self.model.intercept_ = np.array(parameters[1])
    #     self.model.classes_ = np.array(parameters[2])
    def get_server_model(self, server):
        self.model.coef_ = server.model.coef_
        self.model.intercept_ = server.model.intercept_
        self.model.classes_ = server.model.classes_

    def broadcast_model(self):
        model_params = list()
        model_params.append(np.array(self.model.coef_))
        model_params.append(np.array(self.model.intercept_))
        model_params.append(np.array(self.model.classes_))
        # print(model_params)
        return model_params
