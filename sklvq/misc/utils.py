from importlib import import_module


# Argument must be the name of the class using '-', so 'squared_euclidean.SquaredEuclidean' -> 'squared-euclidean'


# TODO: Documentation
# TODO: Extend to include default rules similar to sklearn api
# TODO: Look into how to deal with the aliases better
# TODO: Look into how to restrict access to certain LVQ classifiers... e.g., not all distance measures are suitable for
#  every classifier

# PACKAGE, module_name, class_name, class_params, BASE_CLASS
def find(package, module_name, class_name, class_params, base_class):
    try:
        object_module = import_module('.' + module_name, package=package)
        object_class = getattr(object_module, class_name)

        # If for some reason the object_doesnt accept the arguments... TODO: This might not be correct
        try:
            instance = object_class(**class_params)
        except TypeError:
            instance = object_class()

    except (AttributeError, ModuleNotFoundError):
        raise ImportError('{} is not part of our collection or '
                          'an alias needs to be created!'.format(module_name.replace('_', '-')))
    else:
        if not issubclass(object_class, base_class):
            raise ImportError(
                "We currently don't have {}, "
                "but you are welcome to send in the request for it!".format(module_name.replace('_', '-')))

    return instance


def process(object_type_argument):
    # RULE: argument given as parameter to LVQ equals 'squared-euclidean' this will look for the SquaredEuclidean
    # object in the squared_euclidean module in the provided package.

    # Construct default module name
    object_type_argument = object_type_argument.casefold()
    module_name = object_type_argument.replace('-', '_')

    # Construct default class name
    class_name = ''
    object_type_parts = object_type_argument.rsplit('-')
    for part in object_type_parts:
        class_name += part.capitalize()

    return module_name, class_name
