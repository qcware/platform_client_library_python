from distutils.version import StrictVersion


def parameter_api_version():
    return "2.1"


def version_is_greater(version_str):
    return StrictVersion(version_str) > StrictVersion(parameter_api_version())
