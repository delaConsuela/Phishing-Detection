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

def build_model(X_ds, Y_ds, n, f, d, l, s, rand_states, n_jobs):
    rf = RandomForestClassifier(n_estimators=n,
                                max_features=f,
                                max_depth=d,
                                min_samples_leaf=l,
                                min_samples_split=s,
                                random_state=rand_states,
                                bootstrap=True,
                                oob_score=True,
                                n_jobs=n_jobs,
                                verbose=0)

    rf.fit(X_ds, Y_ds)
        
    oob_accuracy = np.round(rf.oob_score_, 5)
    print("Random Forest with " + str(len(rf.estimators_)) + " trees has:\nOOB score: " + str(oob_accuracy))

    y_pred = rf.predict(X_ds)

    print("\nRandom Forest Training scores")

    print("Classifier accuracy: ", np.round(accuracy_score(Y_ds, y_pred), 5))
    print("Classifier recall: ", np.round(recall_score(Y_ds, y_pred), 5))
    print("Classifier precision: ", np.round(precision_score(Y_ds, y_pred), 5))

    return rf

def evaluate_model(rf, X_ds, Y_ds):
    print("\nRandom Forest Evaluation")

    y_pred = rf.predict(X_ds)

    print("Classifier accuracy test: ", np.round(accuracy_score(Y_ds, y_pred), 5))
    print("Classifier recall test: ", np.round(recall_score(Y_ds, y_pred), 5))
    print("Classifier precision test: ", np.round(precision_score(Y_ds, y_pred), 5))

def main():
    DATASET = 'features.csv'
    dataset = get_data(DATASET)
    ds = dataset.to_numpy(copy=True)
    X_ds, y_ds = get_features_and_labels(ds)
    X_train, X_test, y_train, y_test = train_test_split(X_ds, y_ds, test_size=0.2)

    n_estimators = [30, 50, 100, 200]
    max_features = ['auto', 1, 3, 'sqrt', 'log2']
    max_depth = [None, 25, 35, 50]
    min_sample_leaf = [1, 2, 4]
    min_sample_split = [2, 5, 10]
    rand_states = 1450
    n_jobs = 6
    
    for n,f,d,l,s in it.product(n_estimators, max_features, max_depth, min_sample_leaf, min_sample_split):
        print("\n####################################")
        print(f"\nConfiguration:\nn_estimators\t {n}"
        + f"\nmax feature\t {f}"
        + f"\nmax depth\t {d}"
        + f"\nmin sample lead  {l}"
        + f"\nmin sample split {s}\n")

        rf = build_model(X_train, y_train, n, f, d, l, s, rand_states, n_jobs)
        evaluate_model(rf, X_test, y_test)
    
if __name__ == '__main__':
	main()