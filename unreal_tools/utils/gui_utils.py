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
import sys

# Third party
import unreal
from PySide6 import QtWidgets, QtCore

# Internal

# External


# ----------------------------------------------------------------------------------------#
# --------------------------------------------------------------------------- FUNCTIONS --#

# ----------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------- CLASSES --#


def parent_gui_to_unreal(gui):
    """
    Parents the PyQt or PySide window to the Unreal editor.
    The window will always sit on top of the editor and will be
    minimized along with it.

    :param gui: The PyQt or PySide to affect
    :type: QtWidgets.QWidget
    """
    unreal.parent_external_window_to_slate(int(gui.winId()))

def get_qt_app():
    """
    Lazy-load the PyQt6 application.

    :return: The application
    :type: QtWidgets.QApplication
    """
    app = QtWidgets.QApplication.instance()

    if not app:
        app = create_qt_app()

    return app

def create_qt_app():
    """
    Creates the default PyQt6 application.

    :return: The application
    :type: QtWidgets.QApplication
    """
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    # window = QtWidgets.QWidget()
    # window.show()
    # app.exec_()
    return app