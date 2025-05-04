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

# Third party
from PySide6 import QtWidgets, QtCore

# Internal
from unreal_tools.utils.gui_utils import get_qt_app, parent_gui_to_unreal

# External


# ----------------------------------------------------------------------------------------#
# --------------------------------------------------------------------------- FUNCTIONS --#

# ----------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------- CLASSES --#

class CreateFolderHierGUI(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        # The tree view
        self.folder_tree = None

    def init_gui(self):
        """
        Creates and displays the GUI to the user.
        """
        # Make the main layout
        main_vb = QtWidgets.QVBoxLayout(self)

        # Create horizontal layout for buttons
        btns_hb = QtWidgets.QHBoxLayout()
        # Create Add button and customize it
        add_btn = QtWidgets.QPushButton('Add Folder')
        add_btn.clicked.connect(self.add_row)
        add_btn.setStyleSheet('background-color: ForestGreen')
        # Create Delete button and customize it
        delete_btn = QtWidgets.QPushButton('Delete Folder')
        delete_btn.clicked.connect(self.delete_selected_row)
        delete_btn.setStyleSheet('background-color: OrangeRed')
        # Create Clear All button and customize it
        clear_all_btn = QtWidgets.QPushButton('Clear All')
        clear_all_btn.clicked.connect(self.clear_all)
        clear_all_btn.setStyleSheet('background-color: Red')
        # Add buttons to horizontal layout
        btns_hb.addWidget(add_btn)
        btns_hb.addWidget(delete_btn)
        btns_hb.addWidget(clear_all_btn)
        btns_hb.addWidget(QtWidgets.QLabel()) # spacer
        # Add the horizontal layout to the main layout
        main_vb.addLayout(btns_hb)

        # Creating tree
        self.folder_tree = QtWidgets.QTreeWidget()
        # Customizing tree
        self.folder_tree.setAlternatingRowColors(True)
        self.folder_tree.setMinimumWidth(200)
        self.folder_tree.setMinimumHeight(140)
        self.folder_tree.setHeaderLabel('File Hierarchy')
        # This needs to be set up so when a user clicks off
        #   the tree, all rows are deselected
        self.folder_tree.viewport().installEventFilter(self)

        # Add the horizontal layout to the main layout
        main_vb.addWidget(self.folder_tree)

        # Add title to window
        self.setWindowTitle('Create File Hierarchy')
        # Show the GUI to the user
        self.setGeometry(300, 300, 600, 350)
        self.show()

    @classmethod
    def show_gui(cls):
        """
        This is a helper method to show the GUI.
        """
        # Unreal crashes without this.
        app = get_qt_app()

        # Window disappears without the global.
        global file_hier_gui

        file_hier_gui = __class__()
        file_hier_gui.init_gui()

        parent_gui_to_unreal(file_hier_gui)

        return file_hier_gui

    def add_row(self):
        """
        Adds row to tree
        """
        # If there is a selected item, grab it
        sel_items = self.folder_tree.selectedItems()
        selected = None
        if sel_items:
            selected = sel_items[0]

        # Create the new item
        new_item = QtWidgets.QTreeWidgetItem(["New Item"])
        new_item.setFlags(new_item.flags() | QtCore.Qt.ItemIsEditable)

        # If there was a selected item, add the new item under that one
        if selected:
            selected.addChild(new_item)
            selected.setExpanded(True)
        # Otherwise, add the new item under the root
        else:
            self.folder_tree.addTopLevelItem(new_item)


    def delete_selected_row(self):
        """
        Deletes the row that is currently selected in the tree
        """
        # Grab the selected item
        sel_items = self.folder_tree.selectedItems()
        if not sel_items:
            return
        selected = sel_items[0]

        # If nested, remove the selected item from its parent
        parent = selected.parent()
        if parent:
            parent.removeChild(selected)
        # Otherwise this is a root item, so remove it
        else:
            index = self.folder_tree.indexOfTopLevelItem(selected)
            self.folder_tree.takeTopLevelItem(index)

    def clear_all(self):
        """
        Clears all rows from tree
        """
        self.folder_tree.clear()

    def eventFilter(self, received, event):
        """
        Grabs any events that are happening on the tree widget. If it is a click
        within the tree off of a row, deselect everything.

        :param received: The object that received the event, in this case
                            the tree's viewport is receiving it when clicked
        :type: QObject

        :param event: The event
        :type: QEvent
        """
        if received == self.folder_tree.viewport():
            # If it was a click, see if what was clicked was an item
            #   Otherwise, deselect all rows
            if event.type() == QtCore.QEvent.MouseButtonPress:
                clicked = self.folder_tree.indexAt(event.pos())
                if not clicked.isValid():
                    self.folder_tree.clearSelection()

        return True