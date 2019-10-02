import scipy as sp

from . import DistanceBaseClass


class SquaredEuclidean(DistanceBaseClass):

    def __call__(self, data, prototypes):
        """ Wrapper function for scipy's cdist(x, y, 'sqeuclidean') function

            See scipy.spatial.distance.cdist for full documentation.

            Note that any custom function should still accept and return the same.

            Parameters
            ----------
            data       : ndarray, shape = [n_obervations, n_features]
                         Inputs are converted to float type.
            prototypes : ndarray, shape = [n_prototypes, n_features]
                         Inputs are converted to float type.

            Returns
            -------
            distances : ndarray, shape = [n_observations, n_prototypes]
                The dist(u=XA[i], v=XB[j]) is computed and stored in the
                ij-th entry.
        """
        return sp.spatial.distance.cdist(data, prototypes, 'sqeuclidean')

    def gradient(self, data, prototype):
        """ Implements the derivative of the squared euclidean distance, , with respect to 1 prototype.

            Parameters
            ----------
            data       : ndarray, shape = [n_observations, n_features]

            prototype  : ndarray, shape = [n_features,]

            Returns
            -------
            gradient : ndarray, shape = [n_observations, n_features]
                        The gradient with respect to the prototype and every observation in data.
        """
        return -2 * (data - prototype)