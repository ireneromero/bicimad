import pandas as pd
import math
from sklearn.linear_model import LinearRegression
from sklearn import metrics

def fit_model(model: LinearRegression, train_features, train_target) -> LinearRegression:
    return model.fit(train_features, train_target)

def create_model() -> LinearRegression:
    return LinearRegression()

def get_score(model, train_features, train_target) -> int:
    return model.score(train_features, train_target)

