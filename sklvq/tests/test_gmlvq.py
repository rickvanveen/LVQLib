import numpy as np
from sklearn import datasets
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score, GridSearchCV, ParameterGrid
from sklearn.pipeline import make_pipeline

from sklvq import GMLVQClassifier

import pandas as pd


def test_gmlvq_iris():
    iris = datasets.load_iris()

    iris.data = preprocessing.scale(iris.data)

    classifier = GMLVQClassifier(solver_type='lbfgs', activation_type='sigmoid', activation_params={'beta': 2})
    classifier = classifier.fit(iris.data, iris.target)

    predicted = classifier.predict(iris.data)

    accuracy = np.count_nonzero(predicted == iris.target) / iris.target.size

    print("Iris accuracy: {}".format(accuracy))


def test_gmlvq_with_multiple_prototypes_per_class():
    iris = datasets.load_iris()

    iris.data = preprocessing.scale(iris.data)

    classifier = GMLVQClassifier(activation_type='sigmoid', activation_params={'beta': 6}, prototypes_per_class=4)
    classifier = classifier.fit(iris.data, iris.target)

    predicted = classifier.predict(iris.data)

    accuracy = np.count_nonzero(predicted == iris.target) / iris.target.size

    print("Iris accuracy: {}".format(accuracy))


def test_gmlvq_pipeline_iris():
    iris = datasets.load_iris()

    pipeline = make_pipeline(preprocessing.StandardScaler(), GMLVQClassifier(activation_type='sigmoid',
                                                                             activation_params={'beta': 6}))
    accuracy = cross_val_score(pipeline, iris.data, iris.target, cv=5)
    print("Cross validation (k=5): " + "{}".format(accuracy))


def test_gmlvq_gridsearch_iris():
    iris = datasets.load_iris()

    estimator = GMLVQClassifier()
    pipeline = make_pipeline(preprocessing.StandardScaler(), estimator)

    param_grid = [{'gmlvqclassifier__solver_type': ['lbfgs'],
                   'gmlvqclassifier__activation_type': ['sigmoid', 'swish'],
                   'gmlvqclassifier__activation_params': [{'beta': beta} for beta in list(range(2, 10, 2))]}]

    search = GridSearchCV(pipeline, param_grid, scoring='accuracy', cv=5, n_jobs=4)

    search.fit(iris.data, iris.target)

    df = pd.DataFrame(search.cv_results_)
    df.to_clipboard()

    print("Best parameter (CV score=%0.3f):" % search.best_score_)
    print(search.best_params_)
