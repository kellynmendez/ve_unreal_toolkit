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
import re

# Third party
import unreal
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

        # Create button layout
        create_btn_vb = QtWidgets.QVBoxLayout()
        create_btn_vb.setAlignment(QtCore.Qt.AlignRight)
        # Create Add button and customize it
        create_btn = QtWidgets.QPushButton('Create Folder Structure')
        create_btn.clicked.connect(self.create_folder_structure)
        create_btn.setStyleSheet('background-color: ForestGreen')
        create_btn_vb.addWidget(create_btn)
        main_vb.addLayout(create_btn_vb)

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
        new_item = QtWidgets.QTreeWidgetItem(['NewItem'])
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

    def create_folder_structure(self):
        """
        Creates the folder structure from the tree widget. This is done
        recursively by calling a helper method.

        :return: The success of the operation
        :type: bool
        """
        # Force save all text in tree as it is
        self.folder_tree.clearFocus()
        # Grabbing the path the content browser currently has open
        cb_path = (unreal.EditorUtilityLibrary.
                     get_current_content_browser_item_path().get_internal_path())
        if not cb_path:
            cb_path = '/Game'

        # Check that all folder names are valid
        invalid_names = []
        for i in range(self.folder_tree.topLevelItemCount()):
            top_item = self.folder_tree.topLevelItem(i)
            invalid_names.extend(self._check_folder_names_are_valid(top_item, cb_path))

        if invalid_names:
            self.warn_user(title='Invalid Folder Names',
                           msg=f'The following folder names were invalid:'
                               f'\n{invalid_names}')
            return None

        # For every top item, create the folder hierarchy under it
        for i in range(self.folder_tree.topLevelItemCount()):
            top_item = self.folder_tree.topLevelItem(i)
            self._create_folders_recursively(top_item, cb_path)

        self.close()
        return True

    def _create_folders_recursively(self, tree_item, current_path):
        """
        Creates the folders in the tree's hierarchy recursively

        :param tree_item: The current tree item
        :type: QtWidgets.QTreeWidgetItem

        :param current_path: The current path in the content browser to
                                create the folder
        :type: str
        """
        # Getting the name of the folder, building the path, and making it
        folder_name = tree_item.text(0)
        folder_path = f'{current_path}/{folder_name}'
        unreal.EditorAssetLibrary.make_directory(folder_path)
        # Create an empty text file in the new directory
        self.create_placeholder_asset(folder_path)

        # For every child of current item, create folder hierarchy under it
        for i in range(tree_item.childCount()):
            child = tree_item.child(i)
            if child:
                self._create_folders_recursively(child, folder_path)

    def create_placeholder_asset(self, folder_path):
        """

        :param folder_path:
        :return:
        """
        asset_name = 'PLACEHOLDER'
        asset_path = f'{folder_path}/{asset_name}'

        # Create an empty placeholder blueprint
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        factory = unreal.BlueprintFactory()
        #factory.set_editor_property("ParentClass", unreal.Object)
        asset_tools.create_asset(asset_name, folder_path, None, factory)

    def _check_folder_names_are_valid(self, tree_item, current_path):
        """


        :param tree_item: The current tree item
        :type: QtWidgets.QTreeWidgetItem

        :param current_path: The current path in the content browser to
                                create the folder
        :type: str

        :return: A list of all names that are invalid
        :type: list
        """
        invalid_names = []
        # Check the name is valid, add to invalid list if not
        folder_name = tree_item.text(0).strip()
        folder_path = f'{current_path}/{folder_name}'
        if not self.is_valid_name(folder_name):
            invalid_names.append(folder_path)

        for i in range(tree_item.childCount()):
            child = tree_item.child(i)
            if child:
                invalid_names.extend(self._check_folder_names_are_valid(
                    child, folder_path))

        return invalid_names

    def is_valid_name(self, name):
        """
        Checks if a folder name is valid (no spaces or special characters)

        :param name: Name to check is valid
        :type: str

        :return: Whether it's valid
        :type: bool
        """
        if not name.strip():
            return False
        # Use reg ex to check for special characters
        if re.search(r'[\[\]{}\\/,.<>;\"\'+=!@#$%^&*()| ]', name):
            return False
        return True

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
            #   Otherwise deselect all rows
            if event.type() == QtCore.QEvent.MouseButtonPress:
                clicked = self.folder_tree.indexAt(event.pos())
                if not clicked.isValid():
                    self.folder_tree.clearSelection()

    @classmethod
    def warn_user(cls, title=None, msg=None):
        """
        This function displays a message box that locks the screen until the user
        acknowledges it.

        :param title: The title of the message box window.
        :type: str

        :param msg: The text to show in the message box window.
        :type: str
        """
        if msg and title:
            # Create a QMessageBox
            msg_box = QtWidgets.QMessageBox()
            # Set the title and the message of the window
            msg_box.setWindowTitle(title)
            msg_box.setText(msg)
            # Show the message
            msg_box.exec_()
