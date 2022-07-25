#!/usr/bin/env python3
"""
Functions to set tkinter mouse click and keyboard bindings.
Functions:
    click() - Mouse button bindings for a named object.
    keyboard() - Bind a key to a function for the specified toplevel.

    Copyright (C) 2020-2021  C. Echt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see https://www.gnu.org/licenses/.
"""
# 'Copyright (C) 2021- 2022 C.S. Echt, under GNU General Public License'

import sys
from pathlib import Path
from tkinter import constants, Menu

MY_OS = sys.platform[:3]


def quit_gui(mainwin):
    """
    Error-free and informative exit from the program.
    Called from widgets or keybindings.

    :param mainwin: The tk mainloop object, e.g. root, app, etc.
    """
    print('\n  *** User has quit the program. Exiting...\n')
    # noinspection PyBroadException
    # pylint: disable=broad-except
    try:
        mainwin.update_idletasks()
        mainwin.after(200)
        mainwin.destroy()
    except Exception:
        sys.exit(0)


def position_wrt_window(window, offset_x=0, offset_y=0) -> str:
    """
    Get screen position of *window* and apply optional offsets.
    Used to set screen position of a Toplevel object with respect to
    a parent's window position. Example use with the geometry() method:
      mytopwin.geometry(utils.position_wrt_window(root, 15, -15))
    When used with get_toplevel(), it is expected that all Button()
    widgets are configured for 'takefocus=False'.

    :param window: The main window object (e.g., 'root', 'app',
                   '.!toplevel2') of the tk() mainloop for which to get
                   its screen pixel coordinates.
    :param offset_x: optional pixels to add/subtract to x coordinate of
                     *window*.
    :param offset_y: optional pixels to add/subtract to x coordinate of
                     *window*.
    :return: x and y screen pixel coordinates as string, f'+{x}+{y}'
    """
    coord_x = window.winfo_x() + offset_x
    coord_y = window.winfo_y() + offset_y
    return f'+{coord_x}+{coord_y}'


def get_toplevel(action: str, mainwin):
    """
    Identify the parent tkinter.Toplevel() window when it, or its
    child widget, has focus.
    Works as intended when Button widgets in parent toplevel or
    *mainwin* do not retain focus, i.e., 'takefocus=False'.

    :param action: The action needed for the parent; e.g.,
                   'position', 'winpath'.
    :param mainwin: The main window object of the tk() mainloop, e.g.,
                    'root', 'main', or 'app', etc.
    :return: For *action* 'position', returns string of screen
             coordinates for the parent toplevel window.
             For *action* 'winpath', returns the tk window path
             name for the parent toplevel window.
    """
    # Based on https://stackoverflow.com/questions/66384144/
    # Need to cover all cases when the focus is on any toplevel window,
    #  or on a child of that window path, i.e. '.!text' or '.!frame'.
    # There may be many children in *mainwin* and any target toplevel
    #   window will likely be listed at or toward the end, so read
    #   children list in reverse.
    if action == 'position':
        coordinates = None
        for child in reversed(mainwin.winfo_children()):
            if child == child.focus_get():
                coordinates = position_wrt_window(child, 30, 20)
            elif '.!text' in str(child.focus_get()):
                parent = str(child.focus_get())[:-6]
                if parent in str(child):
                    coordinates = position_wrt_window(child, 30, 20)
            elif '.!frame' in str(child.focus_get()):
                parent = str(child.focus_get())[:-7]
                if parent in str(child):
                    coordinates = position_wrt_window(child, 30, 20)
            elif str(child.focus_get()) == '.':
                coordinates =  position_wrt_window(mainwin, 30, 20)
        return coordinates
    if action == 'winpath':
        relative_path = mainwin.winfo_children()[-1]
        for child in reversed(mainwin.winfo_children()):
            if child == child.focus_get():
                relative_path = child
            elif '.!text' in str(child.focus_get()):
                parent = str(child.focus_get())[:-6]
                if parent in str(child):
                    relative_path = child
            elif '.!frame' in str(child.focus_get()):
                parent = str(child.focus_get())[:-7]
                if parent in str(child):
                    relative_path = child
            elif str(child.focus_get()) == '.':
                relative_path = mainwin
        return relative_path
    return None


def click(click_type, click_obj) -> None:
    """
    Mouse button bindings for the named object.
    Creates pop-up menu of commands for the clicked object.
    Example: from tk_utils import utils
             utils.click(myentryobject, 'right')

    :param click_type: Example mouse button or button modifiers;
                     'left', 'right', 'shift', 'ctrl', 'shiftctrl', etc.
    :param click_obj: Name of the object in which click commands are
                      to be active.
    """

    def on_click(event, command):
        """
        Sets menu command to the selected predefined virtual event.
        Event is a unifying binding across multiple platforms.
        https://www.tcl.tk/man/tcl8.6/TkCmd/event.htm#M7
        """
        # Need to set possible Text widgets to be editable in case
        #   they are set to be readonly, tk.DISABLED.
        click_obj.configure(state=constants.NORMAL)
        event.widget.event_generate(f'<<{command}>>')

    # Based on: https://stackoverflow.com/questions/57701023/
    def popup_menu(event):
        right_click_menu = Menu(None, tearoff=0, takefocus=0)

        right_click_menu.add_command(
            label='Select all',
            command=lambda: on_click(event, 'SelectAll'))
        right_click_menu.add_command(
            label='Copy',
            command=lambda: on_click(event, 'Copy'))
        right_click_menu.add_command(
            label='Paste',
            command=lambda: on_click(event, 'Paste'))
        right_click_menu.add_command(
            label='Cut',
            command=lambda: on_click(event, 'Cut'))

        right_click_menu.tk_popup(event.x_root + 10, event.y_root + 15)

    if click_type == 'right':
        if MY_OS in 'lin, win':
            click_obj.bind('<Button-3>', popup_menu)
        elif MY_OS == 'dar':
            click_obj.bind('<Button-2>', popup_menu)


def keyboard(func: str, toplevel, mainwin=None) -> None:
    """
    Bind a key to a function for the specified Toplevel() window. Use to
    add standard keyboard actions or to provide keybinding equivalents
    for button commands used in the Toplevel() window.

    Example usage in a function that creates a mytopwin Toplevel and
    using 'from COUNTmodules import binds':
    binds.keyboard(mytopwin, 'close')
    binds.keyboard(mytopwin, 'append', MYFILEPATH, txt)

    :param func: Function to execute: 'close', 'append', 'saveas'.
                 For 'close', the key is 'w' with OS-specific modifier.
                 For 'append' and 'saveas', the key is 's' with
                 OS-specific modifier.
    :param toplevel: Name of tk.Toplevel() object of *func*.
    :param mainwin: The main window object of the tk() mainloop, e.g.,
                    root', 'main', or 'app'. Used only as a pass-through
                    parameter when calling other utils functions.
    """
    cmd_key = ''
    if MY_OS in 'lin, win':
        cmd_key = 'Control'
    elif MY_OS == 'dar':
        cmd_key = 'Command'

    if func == 'close':
        toplevel.bind(
            f'<{f"{cmd_key}"}-w>',
            lambda _: get_toplevel('winpath', mainwin).destroy())
    if func == 'quit':
        toplevel.bind(f'<{f"{cmd_key}"}-q>', lambda _: quit_gui(mainwin))


def valid_path_to(relative_path: str) -> Path:
    """
    Get absolute path to files and directories.
    _MEIPASS var is used by distribution programs from
    PyInstaller --onefile; e.g. for images dir.

    :param relative_path: File or dir name path, as string.
    :return: Absolute path as pathlib Path object.
    """
    # Modified from: https://stackoverflow.com/questions/7674790/
    #    bundling-data-files-with-pyinstaller-onefile and PyInstaller manual.
    if getattr(sys, 'frozen', False):  # hasattr(sys, '_MEIPASS'):
        base_path = getattr(sys, '_MEIPASS', Path(Path(__file__).resolve()).parent)
        return Path(base_path) / relative_path
    return Path(relative_path).resolve()
