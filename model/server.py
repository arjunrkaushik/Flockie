import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class Server:
    def __init__(self):
        self.model = LogisticRegression()
        # df = pd.read_csv('../model/framingham.csv')
        # # print(df.head())
        # df = df.dropna()
        # df.fillna(method='bfill', inplace=True)
        # self.train(df[:10])

    def train(self, data):
        y = data["TenYearCHD"]
        X = data.drop(columns=['TenYearCHD', 'education'], axis=1)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=0)
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)

        self.model.fit(X_train, y_train)

        # encoded = json.dumps((self.model.coef_.tolist(), self.model.intercept_.tolist(), self.model.classes_.tolist()))
        print("Server ready")
        return

    def update_model(self,clients):
        coeffs = np.array(clients[0][0])
        intercepts = np.array(clients[0][1])
        classes = set(clients[0][2])

        for i in range(1, len(clients)):
            coeffs = np.add(coeffs,clients[i][0])
            intercepts = np.add(intercepts,clients[i][1])
            temp_class = set(clients[i][2])
            classes = classes.union(temp_class)
        
        agg_coeffs = np.divide(coeffs, len(clients))
        agg_intercepts = np.divide(intercepts, len(clients))
        
        self.model.coef_ = np.array([agg_coeffs])
        self.model.intercept_ = agg_intercepts
        self.model.classes_ = np.array(list(classes))

    # def update_model(self,clients):
    #     coeffs = np.array(clients[0].model.coef_)
    #     intercepts = np.array(clients[0].model.intercept)
    #     classes = set(clients[0].model.classes_)
    #
    #     for i in range(1, len(clients)):
    #         coeffs = np.add(coeffs,clients[i].model.coef_)
    #         intercepts = np.add(intercepts,clients[i].model.intercept)
    #         temp_class = set(clients[i].model.classes_)
    #         classes = classes.union(temp_class)
    #
    #     agg_coeffs = np.divide(coeffs, len(clients))
    #     agg_intercepts = np.divide(intercepts, len(clients))
    #
    #     self.model.coef_ = agg_coeffs
    #     self.model.intercept_ = agg_intercepts
    #     self.model.classes_ = np.array(list(classes))

    # def test(self, data):
    #     y = data["TenYearCHD"]
    #     X = data.drop(columns=['TenYearCHD', 'education'], axis=1)
    #     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=0)
    #
    #     scaler = StandardScaler()
    #     X_train = scaler.fit_transform(X_train)
    #     X_test = scaler.transform(X_test)
    #     predictions = self.model.predict(X_test)
    #     accuracy = np.sum(predictions == y_test) / y_test.shape[0] * 100
    #
    #     return accuracy

    def test(self, X, y):
        # y = self.data["TenYearCHD"]
        # X = self.data.drop(columns=['TenYearCHD', 'education'], axis=1)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=0)

        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        predictions = self.model.predict(X_test)
        accuracy = np.sum(predictions == y_test) / y_test.shape[0] * 100

        return accuracy
