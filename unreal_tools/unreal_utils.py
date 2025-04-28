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
import os

# Third party
import unreal
from Pyside2 import QtGui, QtCore, QtWidgets

# Internal

# External


# ----------------------------------------------------------------------------------------#
# --------------------------------------------------------------------------- FUNCTIONS --#

def parent_gui_to_unreal(gui):
    """
    Parents the PyQt or PySide window to the Unreal editor.
    The window will always sit on top of the editor and will be minimized along with it.

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

    if not QtWidgets.QApplication.instance():
        app = _create_qt_app()

    return app

def _create_qt_app():
    """
    Creates the default PyQt6 application.

    :return: The application
    :type: QtWidgets.QApplication
    """
    app = QtWidgets.QApplication(sys.argv)
    return app

# ----------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------- CLASSES --#

class TestGUI(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        # unreal context
        # self.context = get_unreal_pipe_context()
        # self.project = self.context.project_obj

    def init_gui(self):
        # Make a layout.
        main_vb = QtWidgets.QVBoxLayout(self)

        btn = QtWidgets.QPushButton('Create Turntable')
        main_vb.addWidget(btn)



        # Set up the usual stuff.
        self.setGeometry(300, 300, 250, 120)
        self.setWindowTitle('Look Dev')
        self.show()

    @classmethod
    def show_gui(cls):
        """
        This is a helper method to show the GUI.
        """
        # Unreal crashes without this.
        app = get_qt_app()

        # Window disappears without the global.
        global look_dev_gui

        look_dev_gui = __class__()
        look_dev_gui.show_gui()

        parent_gui_to_unreal(look_dev_gui)

        return look_dev_gui

# ----------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------- MAIN --#

gui = TestGUI()
gui.init_gui()