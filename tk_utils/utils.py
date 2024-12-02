#!/usr/bin/env python3
"""
General housekeeping and mouse binding functions.
Functions:
    check_platform - Get current OS platform, exit if not supported.
    program_name - Get the script or executable name.
    set_icon - Set the custom program icon image file.
    manage_args - Handle of common command line arguments.
    handle_exceptions - Catches uncaught system and tkinter exceptions.
    quit_gui - Error-free and informative exit from the program.
    position_wrt_window - Get screen position of a window; apply offsets.
    click - Mouse button bindings for a named object.
    get_toplevel - Identify a parent tk window when it, or its child,
                    has focus.
    keyboard - Bind a key to a function for the specified toplevel.
    valid_path_to - Get absolute path to files and directories.
"""
# 'Copyright (C) 2021- 2022 C.S. Echt, under GNU General Public License'

# Standard library imports:
import argparse
import logging
import platform
import sys
import tkinter as tk
from __main__ import __doc__
from pathlib import Path

# Local program import:
from tk_utils import (__author__,
                      __version__,
                      __dev_status__,
                      __copyright__,
                      URL,
                      LICENSE)
from tk_utils.constants import MY_OS

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


def handle_exception(exc_type, exc_value, exc_traceback) -> None:
    """
    Changes an unhandled exception to go to stdout rather than
    stderr. Ignores KeyboardInterrupt so a console program can exit
    with Ctrl + C. Relies entirely on python's logging module for
    formatting the exception. Sources:
    https://stackoverflow.com/questions/6234405/
    logging-uncaught-exceptions-in-python/16993115#16993115
    https://stackoverflow.com/questions/43941276/
    python-tkinter-and-imported-classes-logging-uncaught-exceptions/
    44004413#44004413

    Usage: in mainloop,
     - sys.excepthook = utils.handle_exception
     - app.report_callback_exception = utils.handle_exception

    Args:
        exc_type: The type of the BaseException class.
        exc_value: The value of the BaseException instance.
        exc_traceback: The traceback object.

    Returns: None

    """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Uncaught exception",
                 exc_info=(exc_type, exc_value, exc_traceback))


def check_platform():
    if MY_OS not in 'lin, win, dar':
        print(f'Platform <{sys.platform}> is not supported.\n'
              'Windows, Linux, and MacOS (darwin) are supported.')
        sys.exit(1)

    # Need to account for scaling in Windows10 and earlier releases.
    if MY_OS == 'win':
        from ctypes import windll

        if platform.release() < '10':
            windll.user32.SetProcessDPIAware()
        else:
            windll.shcore.SetProcessDpiAwareness(1)


def program_name() -> str:
    """
    Returns the script name or, if called from a PyInstaller stand-alone,
    the executable name. Use for setting file paths and naming windows.

    :return: Context-specific name of the main program, as string.
    """
    if getattr(sys, 'frozen', False):  # hasattr(sys, '_MEIPASS'):
        return Path(sys.executable).stem
    return Path(sys.modules['__main__'].__file__).stem


def set_icon(window) -> None:
    """
    Set the program icon image file.  If the icon cannot be displayed,
    print a message to the console.

    Args:  window: The main tk.Tk() window running the mainloop or a
        tk.Toplevel window.
    """
    # The custom app icon is expected to be in the program's images folder.
    try:
        icon = tk.PhotoImage(file=valid_path_to('images/helper_icon512.png'))
        window.wm_iconphoto(True, icon)
    except tk.TclError as err:
        print('Cannot display program icon, so it will be blank or the tk default.\n'
              f'tk error message: {err}')
    except FileNotFoundError as fnf:
        print(f'Cannot find program icon file: {fnf}.\n'
              'The program will run without a custom icon.')


def manage_args() -> None:
    """Allow handling of common command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--about',
                        help='Provides description, version, GNU license',
                        action='store_true',
                        default=False)
    args = parser.parse_args()
    if args.about:
        print(__doc__)
        print(f'{"Author:".ljust(13)}', __author__)
        print(f'{"Version:".ljust(13)}', __version__)
        print(f'{"Status:".ljust(13)}', __dev_status__)
        print(f'{"URL:".ljust(13)}', URL)
        print(__copyright__)
        print(LICENSE)
        print()
        sys.exit(0)


def quit_gui(mainloop: tk.Tk) -> None:
    """
    Error-free and informative exit from the program.
    Called from widgets or keybindings.

    :param mainloop: The tk mainloop object, e.g. app, self.
    """

    try:
        mainloop.update()
        print('\n*** User has quit the program. Exiting...\n')
        mainloop.destroy()
        # Need explicit exit if for some reason a tk window isn't destroyed.
        sys.exit(0)
    except Exception as unk:
        print('An unknown error occurred on exit:', unk)
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


def click(click_type: str, click_obj) -> None:
    """
    Mouse button bindings for the named object.
    Creates pop-up menu of commands for the clicked object.
    Example: utils.click('right', my_tk_object)

    :param click_type: Example mouse button or button modifiers;
                     'left', 'right', 'shift', 'ctrl', 'shiftctrl', etc.
    :param click_obj: Name of the tk object in which click command is to
                      be active.
    """

    def on_click(event, command):
        """
        Sets menu command to the selected predefined virtual event.
        Event is a unifying binding across multiple platforms.
        https://www.tcl.tk/man/tcl8.6/TkCmd/event.htm#M7
        """
        # Need to set possible Text widgets to be editable in case
        #   they are set to be readonly, tk.DISABLED.
        click_obj.configure(state=tk.NORMAL)
        event.widget.event_generate(f'<<{command}>>')

    # Based on: https://stackoverflow.com/questions/57701023/
    def popup_menu(event):
        right_click_menu = tk.Menu(None, tearoff=0, takefocus=0)

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


def get_toplevel(action: str, mainwin):
    """
    Identify the parent tkinter.Toplevel() window when it, or its
    child widget, has focus.
    Works as intended when Button widgets in parent toplevel or
    *mainwin* do not retain focus, i.e., 'takefocus=False'.
    Called only from utils.keyboard().

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
                coordinates = position_wrt_window(window=child,
                                                  offset_x=30,
                                                  offset_y=20)
            elif '.!text' in str(child.focus_get()):
                parent = str(child.focus_get())[:-6]
                if parent in str(child):
                    coordinates = position_wrt_window(child, 30, 20)
            elif '.!frame' in str(child.focus_get()):
                parent = str(child.focus_get())[:-7]
                if parent in str(child):
                    coordinates = position_wrt_window(child, 30, 20)
            elif str(child.focus_get()) == '.':
                coordinates = position_wrt_window(mainwin, 30, 20)
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
    # return None


def keybind(func: str, toplevel, mainwin=None) -> None:
    """
    Bind a key to a function for the specified Toplevel() window. Use to
    add standard keyboard actions or to provide keybinding equivalents
    for button commands used in the Toplevel() window.

    Example usage in a function that creates a mytopwin Toplevel and
    using 'from COUNTmodules import binds':
    binds.keyboard(mytopwin, 'close')
    binds.keyboard(mytopwin, 'append', MYFILEPATH, txt)

    :param func: Function to execute: 'quit', 'close', 'append', 'saveas'.
        For 'quit', the key is 'q'.
        For 'close', the key is 'w'.
        For 'append' and 'saveas', the key is 's'.
        All keys use an OS-specific modifier.
    :param toplevel: Name of tk.Toplevel() object of *func*.
    :param mainwin: The main window object of the tk() mainloop, e.g.,
        root', 'main', or 'app'. Used only as a pass-through parameter
        when calling other utils functions.
    """
    cmd_key = 'Command' if MY_OS == 'dar' else 'Control'  # is 'lin' or 'win'

    if func == 'close':
        toplevel.bind(
            f'<{f"{cmd_key}"}-w>',
            lambda _: get_toplevel('winpath', mainwin).destroy())
    if func == 'quit':
        toplevel.bind(f'<{f"{cmd_key}"}-q>', lambda _: quit_gui(mainwin))


def valid_path_to(relative_path: str) -> Path:
    """
    Get correct path to program's directory/file structure
    depending on whether program invocation is a standalone app or
    the command line. Works with symlinks. Allows command line
    using any path; does not need to be from parent directory.
    _MEIPASS var is used by distribution programs from
    PyInstaller --onefile; e.g. for images dir.

    :param relative_path: Program's local dir/file name, as string.
    :return: Absolute path as pathlib Path object.
    """
    # Modified from: https://stackoverflow.com/questions/7674790/
    #    bundling-data-files-with-pyinstaller-onefile and PyInstaller manual.
    if getattr(sys, 'frozen', False):  # hasattr(sys, '_MEIPASS'):
        base_path = getattr(sys, '_MEIPASS', Path(Path(__file__).resolve()).parent)
        valid_path = Path(base_path) / relative_path
    else:
        valid_path = Path(Path(__file__).parent, f'../{relative_path}').resolve()
    return valid_path
