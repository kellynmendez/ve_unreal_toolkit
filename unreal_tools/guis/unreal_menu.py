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
from unreal_tools.utils.gui_utils import create_qt_app

# External

# ----------------------------------------------------------------------------------------#
# ------------------------------------------------------------------------- QT START UP --#

# This is the first script to run. Make sure Qt is initialized early.
if not QtWidgets.QApplication.instance():
    app = create_qt_app()


# ----------------------------------------------------------------------------------------#
# --------------------------------------------------------------------------- FUNCTIONS --#

def add_menu_entry(name='', label='', tool_tip='', str_command=''):
    """
    Creates an entry and returns it.

    :param name: Entry name in editor
    :type: str

    :param label: Name that will show up in the menu
    :type: str

    :param tool_tip: Tool tip that will show up when hovering on the entry
    :type: str

    :param str_command: Command to run
    :type: str

    :return: The created entry
    :type: unreal.ToolMenuEntry
    """
    # Build the entry
    entry = unreal.ToolMenuEntry(type=unreal.MultiBlockType.MENU_ENTRY)
    entry.set_label(label)
    entry.set_tool_tip(tool_tip)

    # This is what gets executed on click for the entry created above.
    entry.set_string_command(unreal.ToolMenuStringCommandType.PYTHON, '',
                             string=str_command)
    return entry


def add_create_folder_hier_button():
    """
    Adds a button to create a folder hierarchy in the content browser.
    """
    # Grabbing the content browser menu
    menus = unreal.ToolMenus.get()
    content_menu = menus.find_menu('ContentBrowser.AddNewContextMenu')
    # Names
    entry_name = 'CreateBaseFolders'
    section_name = 'ContentBrowserNewFolder'
    # Adding new button to menu
    entry = add_menu_entry(name=entry_name,
                           label='Create Base Folders',
                           tool_tip='Create a folder hierarchy in content browser',
                           str_command='from unreal_tools.guis.folder_hier_gui import '
                                       'CreateFolderHierGUI;gui=CreateFolderHierGUI();'
                                       'gui.show_gui()')
    entry.set_icon("Icons.Documentation")

    content_menu.add_menu_entry(section_name, entry)
    # Refresh all menus
    menus.refresh_all_widgets()

    return True
