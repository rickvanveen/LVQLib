from abc import ABC, abstractmethod
import scipy as sp
import numpy as np


class AbstractDistance(ABC):

    @abstractmethod
    def __call__(self, data, prototypes):
        raise NotImplementedError("You should implement this!")

    @abstractmethod
    def gradient(self, data, prototype):
        raise NotImplementedError("You should implement this!")


class SquaredEuclidean(AbstractDistance):

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
        """ Implements the derivative of the squared euclidean distance.

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


class Euclidean(AbstractDistance):

    def __call__(self, data, prototypes):
        """ Wrapper function for scipy's cdist(x, y, 'euclidean') function

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
        return sp.spatial.distance.cdist(data, prototypes, 'euclidean')

    def gradient(self, data, prototype):
        """ Implements the derivative of the euclidean distance.

            Parameters
            ----------
            data       : ndarray, shape = [n_observations, n_features]

            prototype  : ndarray, shape = [n_features,]

            Returns
            -------
            gradient : ndarray, shape = [n_observations, n_features]
                       The gradient with respect to the prototype and every observation in data.
        """
        difference = data - prototype
        return (-1 * difference) / np.sqrt(np.sum(difference ** 2))


class RelevanceSquaredEuclidean(AbstractDistance):

    # TODO: Why set omega in the init but not prototypes etc...
    def __init__(self, omega=None):
        self.omega = omega

    # TODO: make omega a property and normalise everytime 'automatically' when it is set?
    def normalise(self):
        self.omega = self.omega / np.sqrt(np.sum(np.diagonal(self.omega.T.dot(self.omega))))

    def __call__(self, data, prototypes):
        """ Implements a weighted variant of the squared euclidean distance.

                Note uses scipy.spatial.distance.cdist see scipy documentation.

                Note that any custom function should still accept and return the same as this function.

                Parameters
                ----------
                data       : ndarray, shape = [n_obervations, n_features]
                             Inputs are converted to float type.
                prototypes : ndarray, shape = [n_prototypes, n_features]
                             Inputs are converted to float type.
                omega      : ndarray, shape = [n_features, n_features]
                TODO: Rectangular Omega... nfeatures, x or x, nfeatures

                Returns
                -------
                distances : ndarray, shape = [n_observations, n_prototypes]
                    The dist(u=XA[i], v=XB[j]) is computed and stored in the
                    ij-th entry.
            """
        return sp.spatial.distance.cdist(data, prototypes, 'mahalanobis', VI=self.omega.T.dot(self.omega)) ** 2

    # Returns: shape = [num_samples, num_features]
    def gradient(self, data, prototype):
        return np.apply_along_axis(lambda x, l: l.dot(np.atleast_2d(x).T).T,
                                   1, (-2 * (data - prototype)), (self.omega.T.dot(self.omega))).squeeze()

    # Returns: shape = [num_samples, omega.size]
    def omega_gradient(self, data, prototype):
        return np.apply_along_axis(lambda x, o: (o.dot(np.atleast_2d(x).T).dot(2 * np.atleast_2d(x))).ravel(),
                                   1, (data - prototype), self.omega)


class DistanceFactory:

    # TODO: In __init__.py and with dict {'sqeuclidean': 'SquaredEuclidean'}
    # TYPES = {'sqeuclidean': 'SquaredEuclidean',
    #                   'euclidean': 'Euclidean',
    #                   'releuclidean': 'RelevanceSquaredEuclidean'}

    @staticmethod
    def create(distance_type, *args, **kwargs):
        # try:
        #     distance_object = getattr(sys.module[__name__], DistanceFactory.TYPES[distance_type])
        if distance_type == 'sqeuclidean':
            return SquaredEuclidean(*args, **kwargs)
        if distance_type == 'euclidean':
            return Euclidean(*args, **kwargs)
        if distance_type == 'rel-sqeuclidean':
            return RelevanceSquaredEuclidean(*args, **kwargs)
        else:
            print("Distance type does not exist")
