#!/usr/bin/env python
# SETMODE 777

# ----------------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Kellyn Mendez
:description:

"""

# ----------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------- IMPORTS --#

# Built-in
import os
import sys

# Third party

# Internal

# External


# ----------------------------------------------------------------------------------------#
# --------------------------------------------------------------------------- FUNCTIONS --#

def get_user_python_installation_path():
    """
    Retrieves the path to a Python39 installation (not unreal's python) by reading
    the user's path variable.

    :return: The global python installation path
    :type: str
    """
    possible_paths = os.environ['path'].split(';')
    possible_paths = [path for path in possible_paths if 'Python39' in path]
    shortest_path = min(possible_paths, key=len)

    python_path = os.path.join(shortest_path, 'Lib', 'site-packages')
    return python_path


def append_python_path_values():
    """
    Attempts to append the values referenced in PYTHONPATH using sys.  This is being
    done because it seems Unreal does not allow you to import from areas pointed at by
    PYTHONPATH.  So, we have to force it to recognize those paths so we can import any
    modules stored there.

    :return: The success of the operation.
    :type: bool
    """
    # See if PYTHONPATH is set.
    if not os.environ['PYTHONPATH']:
        print('The PYTHONPATH variable does not seem to be set.')
        return None

    # Get the values in PYTHONPATH and append them with sys.
    values = os.environ['PYTHONPATH']
    values = values.split(';')
    if not values:
        print("There don't seem to be any values set in PYTHONPATH")
        return None
    for path_value in values:
        sys.path.append(path_value)

    # Add a path to PySide2, which is in the Python 3.7.7 site-packages.  This will
    # need to be checked vs the school's installation path.
    site_packages = get_user_python_installation_path()
    sys.path.append(site_packages)
    return True

# ----------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------- CLASSES --#

# ----------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------- MAIN --#
result = append_python_path_values()
print(result)