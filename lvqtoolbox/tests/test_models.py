import scipy as sp
import numpy as np
from sklearn import datasets
from sklearn.utils.multiclass import unique_labels
from sklearn import preprocessing

from lvqtoolbox.glvq import GLVQClassifier


def test_costfun():
    iris = datasets.load_iris()

    iris.data = preprocessing.scale(iris.data)

    classifier = GLVQClassifier()
    classifier = classifier.fit(iris.data, iris.target)

    print(classifier.prototypes_)

    predicted = classifier.predict(iris.data)

    accuracy = np.count_nonzero(predicted == iris.target) / iris.target.size

    print(accuracy)


