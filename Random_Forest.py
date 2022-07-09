from enum import auto
import numpy as np
import pandas as pd
import itertools as it
from sklearn.metrics import ConfusionMatrixDisplay, RocCurveDisplay, accuracy_score, recall_score, precision_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from sklearn.tree import export_graphviz
import pydot

def get_data(DATASET):
    dataset = pd.read_csv(DATASET, sep=',', header=0)

    return dataset

def get_features_and_labels(dataset):
    X_ds = []
    Y_ds = []

    for values in dataset:
        X_ds.append(values[:-1])
        Y_ds.append(values[-1])
    
    return X_ds, Y_ds

def build_model(X_ds, Y_ds):
    n_estimators = 30
    max_feature = 3
    max_depth = 25
    min_sample_leaf = 1
    min_sample_split = 5
    rand_states = 1237
    n_jobs = 6

    rf = RandomForestClassifier(n_estimators=n_estimators,
                                random_state=rand_states,
                                max_features=max_feature,
                                max_depth=max_depth,
                                min_samples_leaf=min_sample_leaf,
                                min_samples_split=min_sample_split,
                                bootstrap=True,
                                oob_score=True,
                                n_jobs=n_jobs,
                                verbose=0)

    rf.fit(X_ds, Y_ds)
    y_pred = rf.predict(X_ds)
   
    oob_accuracy = np.round(rf.oob_score_, 5)

    print("\nRandom Forest with " + str(len(rf.estimators_)) + " trees has:\nOOB score: " + str(oob_accuracy)
    + "\nnumber of features seen in fit: " + str(rf.n_features_in_) )

    print("Classifier accuracy: ", accuracy_score(Y_ds, y_pred))
    print("Classifier recall: ", recall_score(Y_ds, y_pred))
    print("Classifier precision: ", precision_score(Y_ds, y_pred))

    return rf

def evaluate_model(X_ds, Y_ds, rf):
    y_pred = rf.predict(X_ds)

    print("\nClassifier accuracy test: ", np.round(accuracy_score(Y_ds, y_pred), 5))
    print("Classifier recall test: ", np.round(recall_score(Y_ds, y_pred), 5))
    print("Classifier precision test: ", np.round(precision_score(Y_ds, y_pred), 5))
        
    ConfusionMatrixDisplay.from_predictions(Y_ds, y_pred)
    plt.show()

    RocCurveDisplay.from_predictions(Y_ds, y_pred)
    plt.show()

def main():
    DATASET = 'features.csv'
    dataset = get_data(DATASET)
    ds = dataset.to_numpy(copy=True)

    X_ds, y_ds = get_features_and_labels(ds)
    X_train, X_test, y_train, y_test = train_test_split(X_ds, y_ds, test_size=0.2)

    rf = build_model(X_train, y_train)
    evaluate_model(X_test, y_test, rf)
    
if __name__ == '__main__':
	main()