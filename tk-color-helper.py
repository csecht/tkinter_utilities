#!/usr/bin/env python3
"""
A Python utility to help choose colors and their color blind equivalents
in tkinter GUIs. Draws an interactive tkinter table of 760 named colors
included in X11 rgb.txt.
   Program usage: Click on a color name to show its hex code and RGB
value showing that color as background. Right-click a different color to
change the text foreground. Foreground colors can be changed for a given
background color, but selecting a new background will reset the
foreground to its default value. Click with a key modifier to show the
color blind simulation of the selected color: Shift = deuteranopia,
Ctrl = protanopia, Alt(Command) = tritanopia, Shift-Ctrl = grayscale.
Simulated color hex codes and RGB values may not correspond to any named
color but the hex string will be recognized by tkinter. Hex and RGB
values can also be used in other graphics applications.
    Using the Ctrl or Command (macOS) key in combination with the key
D, P, T, or G will pop-up a non-interactive color table simulated for
deuteranopia, protanopia, tritanopia, or grayscale, respectively.
    Text in the color display and data fields can be cut, copied, pasted,
or edited with standard keyboard and click commands. Runs with Python 3.6
and tkinter 8.6 or later in Linux, Windows, and MacOS systems.
Table construction based on code from
https://stackoverflow.com/questions/4969543/colour-chart-for-tkinter-and-tix
"""
# ^^ Text for --about invocation argument and use as __doc__>>
__author__ = 'csecht'
__copyright__ = 'Copyright (C) 2021 C.S. Echt'
__license__ = 'GNU General Public License'
__version__ = '0.3.2'
__program_name__ = 'tk-color-helper.py'
__project_url__ = 'https://github.com/csecht/'
__docformat__ = 'reStructuredText'
__status__ = 'Development Status :: 2 - Beta'
__dev__ = 'Development environment: Python 3.8, Linux 5.4, tkinter 8.6'

import argparse
import sys
from math import sqrt

try:
    import tkinter as tk
    from tkinter import messagebox
except (ImportError, ModuleNotFoundError) as error:
    print('Requires tkinter, which is included with \n'
          'Python 3.7+ distributions.\n'
          'Install the most recent version or re-install Python and include Tk/Tcl.\n'
          '\n'
          'On Linux you may also need:$ sudo apt-get install python3-tk\n'
          f'See also: https://tkdocs.com/tutorial/install.html \n{error}')

# import functools
# def trackcalls(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         wrapper.has_been_called = True
#         return func(*args, **kwargs)
#     wrapper.has_been_called = False
#     return wrapper

MY_OS = sys.platform[:3]
if MY_OS not in 'lin, win, dar':
    print(f'Sorry, but {sys.platform} is not yet supported. '
          'Linux, MacOS, and Windows are though!')
    sys.exit(0)

if sys.version_info < (3, 6):
    print('Sorry, but Python 3.6 or later is required.\n'
          'Current Python version: '
          f'{sys.version_info.major}.{sys.version_info.minor}\n'
          'Python downloads are available from https://docs.python.org/')
    sys.exit(0)

# 40 rows provide nice spatial organization for 760 color names.
MAX_ROWS = 40
# Cutoff of perceived brightness in range(128-145) to switch from black to white
#  foreground will give acceptable visual contrast when background below that pB.
#  130 has a cutoff of gray51.
CUTOFF_PB = 138

if MY_OS in 'lin, win':
    LABEL_FONT_SIZE = 6
elif MY_OS == 'dar':
    LABEL_FONT_SIZE = 9

# X11_RGB_NAMES: 760 named colors from the intersection of the rbg.txt files in
#   Linux /usr/share/X11/rgb.txt and MacOS /opt/X11/share/X11/rgb.txt.
#   Names containing 'X11' and 'Debian were removed, as well as a few others.
#   The retained names are valid for tkinter 8.6 on Linux, MacOS, and Windows.
# NOTE: Many Tcl/Tk colors from https://www.tcl.tk/man/tcl8.4/TkCmd/colors.html
#   are invalid in tkinter 8.6.
X11_RGB_NAMES = ('white', 'black', 'snow', 'ghost white', 'GhostWhite', 'white smoke',
                 'WhiteSmoke', 'gainsboro', 'floral white', 'FloralWhite', 'old lace',
                 'OldLace', 'linen', 'antique white', 'AntiqueWhite', 'papaya whip',
                 'PapayaWhip', 'blanched almond', 'BlanchedAlmond', 'bisque', 'peach puff',
                 'PeachPuff', 'navajo white', 'NavajoWhite', 'moccasin', 'cornsilk',
                 'ivory', 'lemon chiffon', 'LemonChiffon', 'seashell', 'honeydew',
                 'mint cream', 'MintCream', 'azure', 'alice blue', 'AliceBlue',
                 'lavender', 'lavender blush', 'LavenderBlush', 'misty rose',
                 'MistyRose', 'dim gray', 'DimGray',
                 'dim grey', 'DimGrey', 'slate gray', 'SlateGray', 'slate grey',
                 'SlateGrey', 'light slate gray', 'LightSlateGray', 'light slate grey',
                 'LightSlateGrey', 'gray', 'grey', 'light grey', 'LightGrey', 'light gray',
                 'LightGray', 'dark grey', 'DarkGrey', 'dark gray', 'DarkGray', 'silver',
                 'midnight blue', 'MidnightBlue', 'navy', 'navy blue',
                 'NavyBlue', 'cornflower blue', 'CornflowerBlue', 'dark slate blue',
                 'DarkSlateBlue', 'slate blue', 'SlateBlue', 'medium slate blue',
                 'MediumSlateBlue', 'light slate blue', 'LightSlateBlue', 'royal blue',
                 'RoyalBlue', 'blue', 'medium blue', 'MediumBlue', 'dark blue', 'DarkBlue',
                 'dodger blue', 'DodgerBlue', 'steel blue', 'SteelBlue', 'deep sky blue',
                 'DeepSkyBlue', 'sky blue', 'SkyBlue', 'light sky blue', 'LightSkyBlue',
                 'light steel blue', 'LightSteelBlue', 'light blue', 'LightBlue',
                 'powder blue', 'PowderBlue', 'pale turquoise', 'PaleTurquoise',
                 'dark turquoise', 'DarkTurquoise', 'medium turquoise', 'MediumTurquoise',
                 'turquoise', 'cyan', 'aqua', 'light cyan', 'LightCyan', 'dark cyan', 'DarkCyan',
                 'dark slate gray', 'DarkSlateGray', 'dark slate grey', 'DarkSlateGrey',
                 'cadet blue', 'CadetBlue', 'aquamarine', 'medium aquamarine',
                 'MediumAquamarine', 'dark sea green', 'DarkSeaGreen', 'sea green', 'SeaGreen',
                 'medium sea green', 'MediumSeaGreen', 'light sea green', 'LightSeaGreen',
                 'teal', 'pale green', 'PaleGreen', 'spring green', 'SpringGreen',
                 'green', 'lime', 'light green', 'LightGreen', 'dark green', 'DarkGreen',
                 'chartreuse', 'lawn green', 'LawnGreen', 'medium spring green',
                 'MediumSpringGreen', 'green yellow', 'GreenYellow', 'lime green',
                 'LimeGreen', 'yellow green', 'YellowGreen', 'forest green', 'ForestGreen',
                 'olive', 'olive drab', 'OliveDrab', 'dark olive green', 'DarkOliveGreen',
                 'khaki', 'dark khaki', 'DarkKhaki', 'pale goldenrod',
                 'PaleGoldenrod', 'light goldenrod yellow', 'LightGoldenrodYellow',
                 'light yellow', 'LightYellow', 'yellow',
                 'gold', 'light goldenrod', 'LightGoldenrod', 'goldenrod',
                 'dark goldenrod', 'DarkGoldenrod', 'rosy brown', 'RosyBrown',
                 'indian red', 'IndianRed', 'saddle brown', 'SaddleBrown', 'sienna',
                 'peru', 'burlywood', 'beige', 'wheat', 'sandy brown', 'SandyBrown',
                 'tan', 'chocolate', 'firebrick', 'brown', 'dark salmon', 'DarkSalmon',
                 'salmon', 'light salmon', 'LightSalmon', 'orange', 'dark orange',
                 'DarkOrange', 'coral', 'light coral', 'LightCoral', 'tomato',
                 'orange red', 'OrangeRed', 'red', 'crimson', 'dark red', 'DarkRed',
                 'hot pink', 'HotPink', 'deep pink', 'DeepPink', 'pink', 'light pink',
                 'LightPink', 'violet red', 'VioletRed', 'medium violet red',
                 'MediumVioletRed', 'pale violet red', 'PaleVioletRed', 'maroon',
                 'magenta', 'fuchsia', 'dark magenta', 'DarkMagenta', 'plum', 'orchid',
                 'medium orchid', 'MediumOrchid', 'dark orchid', 'DarkOrchid', 'violet',
                 'dark violet', 'DarkViolet', 'blue violet', 'BlueViolet', 'indigo',
                 'purple', 'medium purple', 'MediumPurple', 'thistle', 'snow1', 'snow2',
                 'snow3', 'snow4', 'seashell1', 'seashell2', 'seashell3', 'seashell4',
                 'AntiqueWhite1', 'AntiqueWhite2', 'AntiqueWhite3', 'AntiqueWhite4',
                 'bisque1', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff1', 'PeachPuff2',
                 'PeachPuff3', 'PeachPuff4', 'NavajoWhite1', 'NavajoWhite2',
                 'NavajoWhite3', 'NavajoWhite4', 'LemonChiffon1', 'LemonChiffon2',
                 'LemonChiffon3', 'LemonChiffon4', 'cornsilk1', 'cornsilk2',
                 'cornsilk3', 'cornsilk4', 'ivory1', 'ivory2', 'ivory3', 'ivory4',
                 'honeydew1', 'honeydew2', 'honeydew3', 'honeydew4', 'LavenderBlush1',
                 'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose1',
                 'MistyRose2', 'MistyRose3', 'MistyRose4', 'azure1', 'azure2',
                 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
                 'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4',
                 'blue1', 'blue2', 'blue3', 'blue4', 'DodgerBlue1', 'DodgerBlue2',
                 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2', 'SteelBlue3',
                 'SteelBlue4', 'DeepSkyBlue1', 'DeepSkyBlue2', 'DeepSkyBlue3',
                 'DeepSkyBlue4', 'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4',
                 'LightSkyBlue1', 'LightSkyBlue2', 'LightSkyBlue3', 'LightSkyBlue4',
                 'SlateGray1', 'SlateGray2', 'SlateGray3', 'SlateGray4',
                 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
                 'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3',
                 'LightBlue4', 'LightCyan1', 'LightCyan2', 'LightCyan3', 'LightCyan4',
                 'PaleTurquoise1', 'PaleTurquoise2', 'PaleTurquoise3', 'PaleTurquoise4',
                 'CadetBlue1', 'CadetBlue2', 'CadetBlue3', 'CadetBlue4', 'turquoise1',
                 'turquoise2', 'turquoise3', 'turquoise4', 'cyan1', 'cyan2', 'cyan3',
                 'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3',
                 'DarkSlateGray4', 'aquamarine1', 'aquamarine2', 'aquamarine3',
                 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
                 'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'SeaGreen4',
                 'PaleGreen1', 'PaleGreen2', 'PaleGreen3', 'PaleGreen4', 'SpringGreen1',
                 'SpringGreen2', 'SpringGreen3', 'SpringGreen4', 'green1', 'green2',
                 'green3', 'green4', 'chartreuse1', 'chartreuse2', 'chartreuse3',
                 'chartreuse4', 'OliveDrab1', 'OliveDrab2', 'OliveDrab3', 'OliveDrab4',
                 'DarkOliveGreen1', 'DarkOliveGreen2', 'DarkOliveGreen3', 'DarkOliveGreen4',
                 'khaki1', 'khaki2', 'khaki3', 'khaki4', 'LightGoldenrod1',
                 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4', 'LightYellow1',
                 'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow1', 'yellow2',
                 'yellow3', 'yellow4', 'gold1', 'gold2', 'gold3', 'gold4', 'goldenrod1',
                 'goldenrod2', 'goldenrod3', 'goldenrod4', 'DarkGoldenrod1',
                 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4', 'RosyBrown1',
                 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
                 'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4',
                 'burlywood1', 'burlywood2', 'burlywood3', 'burlywood4', 'wheat1',
                 'wheat2', 'wheat3', 'wheat4', 'tan1', 'tan2', 'tan3', 'tan4',
                 'chocolate1', 'chocolate2', 'chocolate3', 'chocolate4', 'firebrick1',
                 'firebrick2', 'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3',
                 'brown4', 'salmon1', 'salmon2', 'salmon3', 'salmon4', 'LightSalmon1',
                 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange1', 'orange2',
                 'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3',
                 'DarkOrange4', 'coral1', 'coral2', 'coral3', 'coral4', 'tomato1',
                 'tomato2', 'tomato3', 'tomato4', 'OrangeRed1', 'OrangeRed2',
                 'OrangeRed3', 'OrangeRed4', 'red1', 'red2', 'red3', 'red4',
                 'DeepPink1', 'DeepPink2', 'DeepPink3', 'DeepPink4',
                 'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2',
                 'pink3', 'pink4', 'LightPink1', 'LightPink2', 'LightPink3',
                 'LightPink4', 'PaleVioletRed1', 'PaleVioletRed2', 'PaleVioletRed3',
                 'PaleVioletRed4', 'maroon1', 'maroon2', 'maroon3', 'maroon4',
                 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4', 'magenta1',
                 'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3',
                 'orchid4', 'plum1', 'plum2', 'plum3', 'plum4', 'MediumOrchid1',
                 'MediumOrchid2', 'MediumOrchid3', 'MediumOrchid4', 'DarkOrchid1',
                 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4', 'purple1', 'purple2',
                 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2', 'MediumPurple3',
                 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4',
                 'gray0', 'grey0', 'gray1', 'grey1', 'gray2', 'grey2', 'gray3', 'grey3',
                 'gray4', 'grey4', 'gray5', 'grey5', 'gray6', 'grey6', 'gray7', 'grey7',
                 'gray8', 'grey8', 'gray9', 'grey9', 'gray10', 'grey10', 'gray11',
                 'grey11', 'gray12', 'grey12', 'gray13', 'grey13', 'gray14', 'grey14',
                 'gray15', 'grey15', 'gray16', 'grey16', 'gray17', 'grey17', 'gray18',
                 'grey18', 'gray19', 'grey19', 'gray20', 'grey20', 'gray21', 'grey21',
                 'gray22', 'grey22', 'gray23', 'grey23', 'gray24', 'grey24', 'gray25',
                 'grey25', 'gray26', 'grey26', 'gray27', 'grey27', 'gray28', 'grey28',
                 'gray29', 'grey29', 'gray30', 'grey30', 'gray31', 'grey31', 'gray32',
                 'grey32', 'gray33', 'grey33', 'gray34', 'grey34', 'gray35', 'grey35',
                 'gray36', 'grey36', 'gray37', 'grey37', 'gray38', 'grey38', 'gray39',
                 'grey39', 'gray40', 'grey40', 'gray41', 'grey41', 'gray42', 'grey42',
                 'gray43', 'grey43', 'gray44', 'grey44', 'gray45', 'grey45', 'gray46',
                 'grey46', 'gray47', 'grey47', 'gray48', 'grey48', 'gray49', 'grey49',
                 'gray50', 'grey50', 'gray51', 'grey51', 'gray52', 'grey52', 'gray53',
                 'grey53', 'gray54', 'grey54', 'gray55', 'grey55', 'gray56', 'grey56',
                 'gray57', 'grey57', 'gray58', 'grey58', 'gray59', 'grey59', 'gray60',
                 'grey60', 'gray61', 'grey61', 'gray62', 'grey62', 'gray63', 'grey63',
                 'gray64', 'grey64', 'gray65', 'grey65', 'gray66', 'grey66', 'gray67',
                 'grey67', 'gray68', 'grey68', 'gray69', 'grey69', 'gray70', 'grey70',
                 'gray71', 'grey71', 'gray72', 'grey72', 'gray73', 'grey73', 'gray74',
                 'grey74', 'gray75', 'grey75', 'gray76', 'grey76', 'gray77', 'grey77',
                 'gray78', 'grey78', 'gray79', 'grey79', 'gray80', 'grey80', 'gray81',
                 'grey81', 'gray82', 'grey82', 'gray83', 'grey83', 'gray84', 'grey84',
                 'gray85', 'grey85', 'gray86', 'grey86', 'gray87', 'grey87', 'gray88',
                 'grey88', 'gray89', 'grey89', 'gray90', 'grey90', 'gray91', 'grey91',
                 'gray92', 'grey92', 'gray93', 'grey93', 'gray94', 'grey94', 'gray95',
                 'grey95', 'gray96', 'grey96', 'gray97', 'grey97', 'gray98', 'grey98',
                 'gray99', 'grey99', 'gray100', 'grey100')


# pylint: disable=unused-argument
def quit_gui(event=None) -> None:
    """Safe and informative exit from the program.

    :param event: Needed for keybindings.
    :type event: Direct call from key bindings.
    """
    print('\n  *** User has quit the program. Exiting...\n')
    app.destroy()
    sys.exit(0)


def right_click_menu(event=None) -> None:
    """
    Right-click pop-up option to select and copy text;
    bind to Button-2 (Linux, Windows) or Button-3 (macOS).

    :param event: Direct call from key bindings.
    """

    # Based on: https://stackoverflow.com/questions/57701023/
    rtclick_menu = tk.Menu(None, tearoff=0, takefocus=0)

    rtclick_menu.add_command(
        label='Select all',
        command=lambda: right_click_edit(event, 'SelectAll'))
    rtclick_menu.add_command(
        label='Copy',
        command=lambda: right_click_edit(event, 'Copy'))
    rtclick_menu.add_command(
        label='Cut',
        command=lambda: right_click_edit(event, 'Cut'))
    rtclick_menu.add_command(
        label='Paste',
        command=lambda: right_click_edit(event, 'Paste'))

    rtclick_menu.tk_popup(event.x_root + 10, event.y_root + 15)


def right_click_edit(event, command):
    """
    Sets menu command to the selected predefined virtual event.
    Event is a unifying binding across multiple platforms.
    https://www.tcl.tk/man/tcl8.6/TkCmd/event.htm#M7
    """
    event.widget.event_generate(f'<<{command}>>')


class ColorChart(tk.Frame):
    """
    Set up main frame and fill with interactive widgets for all valid
    named colors that can be used in tkinter. Generate simulations for
    different types of color blindness. Apply perceived brightness
    contrasts to use either default black or white foregrounds.
    """

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.colorinfo = tk.StringVar()
        self.colorinfo.set('Click for color data; use Shift, Ctrl,'
                           ' Alt (or Command), or Shift+Ctrl to simulate color blindness')
        self.bg_info = tk.Entry(self, textvariable=self.colorinfo)
        self.new_fg = tk.StringVar()
        self.new_fg.set('<- Right-click different color to change text color')
        self.fg_info = tk.Entry(self, textvariable=self.new_fg)

        # Width of row0, as total number of columns gridded.
        self.info_width = 0

        self.color_dict = {}
        self.bw_dict = {}
        self.d_sim = {}
        self.p_sim = {}
        self.t_sim = {}
        self.g_sim = {}

        self.sim_type = tk.StringVar(value='orig')
        self.img = tk.PhotoImage

        self.draw_table()
        # config_master() needs to run after draw_table() to define the
        #   number of columns needed for self.info_width.
        self.config_master()

    def draw_table(self) -> None:
        """
        Make the tkinter color table.
        Call simulate_color(), black_or_white(), show_orig().
        """
        # row 0 reserved for color info Entry(), gridded in config_master().
        row = 1
        col = 0

        for color_name in X11_RGB_NAMES:
            label = tk.Label(self, text=color_name, bg=color_name,
                             font=('TkTooltipFont', LABEL_FONT_SIZE))
            label.grid(row=row, column=col, sticky=tk.NSEW)
            row += 1
            _r, _g, _b, = label.winfo_rgb(color_name)
            r = _r // 256
            g = _g // 256
            b = _b // 256
            rgb = (r, g, b)
            bw = self.black_or_white(rgb)
            label.config(fg=bw)
            orig_hex = f'#{r:02x}{g:02x}{b:02x}'
            # Use clicks to bind color label to color and data display.
            # Click selects background, rt-click selects foreground.
            # Rt-click Button is OS-specific.
            # MacOS cannot use the Alt/option modifier, so use Command.
            # Universal bindings:
            label.bind('<Button-1>',
                       lambda event, c=color_name, h=orig_hex, r_b=rgb, fg=bw:
                       self.show_bg(c, h, r_b, fg, 'orig'))
            # These binds display the simulated color and data.
            label.bind('<Shift-Button-1>', lambda event, c=color_name, r_b=rgb:
                       self.simulate_color(c, r_b, 'deuteranopia'))
            label.bind('<Control-Button-1>', lambda event, c=color_name, r_b=rgb:
                       self.simulate_color(c, r_b, 'protanopia'))
            label.bind('<Shift-Control-Button-1>', lambda event, c=color_name, r_b=rgb:
                       self.simulate_color(c, r_b, 'grayscale'))
            # OS-specific bindings:
            if MY_OS in 'lin, win':
                label.bind('<Alt-Button-1>', lambda event, c=color_name, r_b=rgb:
                           self.simulate_color(c, r, 'tritanopia'))
                label.bind('<Button-3>',
                           lambda event, c=color_name, h=orig_hex, r_b=rgb:
                           self.update_fg(c, r_b, 'orig'))
                label.bind('<Shift-Button-3>', lambda event, c=color_name, r_b=rgb:
                           self.update_fg(c, r_b, 'deuteranopia'))
                label.bind('<Control-Button-3>', lambda event, c=color_name, r_b=rgb:
                           self.update_fg(c, r, 'protanopia'))
                label.bind('<Alt-Button-3>', lambda event, c=color_name, r_b=rgb:
                           self.update_fg(c, r_b, 'tritanopia'))
                label.bind('<Shift-Control-Button-3>', lambda event, c=color_name, r_b=rgb:
                           self.update_fg(c, r_b, 'grayscale'))
            elif MY_OS == 'dar':
                label.bind('<Command-Button-1>', lambda event, c=color_name, r_b=rgb:
                           self.simulate_color(c, r_b, 'tritanopia'))
                label.bind('<Button-2>',
                           lambda event, c=color_name, h=orig_hex, r_b=rgb:
                           self.update_fg(c, r_b, 'orig'))
                label.bind('<Shift-Button-2>', lambda event, c=color_name, r_b=rgb:
                           self.update_fg(c, r_b, 'deuteranopia'))
                label.bind('<Control-Button-2>', lambda event, c=color_name, r_b=rgb:
                           self.update_fg(c, r_b, 'protanopia'))
                label.bind('<Command-Button-2>', lambda event, c=color_name, r_b=rgb:
                           self.update_fg(c, r_b, 'tritanopia'))
                label.bind('<Shift-Control-Button-2>', lambda event, c=color_name, r_b=rgb:
                           self.update_fg(c, r_b, 'grayscale'))

            if row > MAX_ROWS:
                row = 1
                col += 1

        self.pack(expand=True, fill="both")

        # Used in config_master()
        self.info_width = col

    def config_master(self) -> None:
        """
        Set up universal and OS-specific keybindings and popup menus
        with standard key and click commands.
        Grid row0 color information here, with its keybindings.
        """

        self.master.minsize(600, 300)

        # Need to color in all of master Frame to create near-shite border;
        #    border changes to grey for click-drag and not focus.
        self.master.configure(highlightthickness=3,
                              highlightcolor='gray95',
                              highlightbackground='gray')

        for _row in range(MAX_ROWS + 1):
            self.rowconfigure(_row, weight=1)
        for _col in range(self.info_width):
            self.columnconfigure(_col, weight=1)

        self.master.bind_all('<Escape>', quit_gui)
        # A click on the close window icon will provide exit msg in Terminal.
        self.master.protocol('WM_DELETE_WINDOW', quit_gui)

        cmdkey = ''
        if MY_OS in 'lin, win':
            cmdkey = 'Control'
        elif MY_OS == 'dar':
            cmdkey = 'Command'
        self.master.bind(f'<{f"{cmdkey}"}-q>', quit_gui)

        # Need to specify Ctrl-A for Linux b/c in tkinter that key is
        #   bound to <<LineStart>>, not <<SelectAll>>, for some reason?
        if MY_OS == 'lin':
            def select_all():
                app.focus_get().event_generate('<<SelectAll>>')

            self.master.bind_all('<Control-a>', lambda event: select_all())

        if MY_OS in 'lin, win':
            self.bg_info.config(justify='center', bg='grey90',
                                font=('TkTooltipFont', 13))
            self.fg_info.config(bg='grey90', font=('TkTooltipFont', 9))
        elif MY_OS == 'dar':
            self.bg_info.config(justify='center', bg='grey90',
                                font=('TkTooltipFont', 16))
            self.fg_info.config(bg='grey90', font=('TkTooltipFont', 12))

        # NOTE: fg_info col width needs to be enough to handle the longest
        #   color name plus hex and RGB, and considering font size.
        self.bg_info.grid(row=0, column=0, sticky=tk.EW,
                          columnspan=self.info_width - 9)
        self.fg_info.grid(row=0, column=self.info_width - 9, sticky=tk.EW,
                          columnspan=9)

        # Set up OS-specific right-click bindings for edit functions
        #   used with info entry fields.
        right_click = ''
        if MY_OS in 'lin, win':
            right_click = '<Button-3>'
        elif MY_OS == 'dar':
            right_click = '<Button-2>'
        self.bg_info.bind(f'{right_click}', right_click_menu)
        self.fg_info.bind(f'{right_click}', right_click_menu)

        # Keybindings to show the simulated color table images in Toplevel.
        # TODO: Add key commands (and click commands) to README.
        cmdkey = ''
        if MY_OS in 'lin, win':
            cmdkey = 'Control'
        elif MY_OS == 'dar':
            cmdkey = 'Command'
        self.master.bind(
            f'<{f"{cmdkey}"}-d>', lambda event, img='d': self.show_simtable(img))
        self.master.bind(
            f'<{f"{cmdkey}"}-p>', lambda event, img='p': self.show_simtable(img))
        self.master.bind(
            f'<{f"{cmdkey}"}-t>', lambda event, img='t': self.show_simtable(img))
        self.master.bind(
            f'<{f"{cmdkey}"}-g>', lambda event, img='g': self.show_simtable(img))

    def simulate_color(
            self, color: str, rgb: tuple, sim_type: str) -> tuple:
        """
        Convert listed named color RGB values to values that simulate a
        specified color blindness or a grayscale simulation.
        Source: http://mkweb.bcgsc.ca/colorblind/math.mhtml

        :param color: A color name from X11_RGB_NAMES
        :param rgb: (R, G, B) tuple of integers in range(0-255)
        :param sim_type: 'orig', 'deuteranopia', 'protanopia',
                         'tritanopia', 'grayscale'
        :returns: (color: str, sim_hex: str, sim_rgb: tuple)
        """
        r, g, b = rgb
        R = 0
        G = 0
        B = 0

        # Need to restrict RGB values to integers in range [0, 255].
        # source: https://stackoverflow.com/questions/5996881/
        #   how-to-limit-a-number-to-be-within-a-specified-range-python
        def clip(_c):
            return max(min(255, _c), 0)

        # Calculate color blind simulation using T matrix RGB conversion.
        # All T matrix values from http://mkweb.bcgsc.ca/colorblind/math.mhtml
        #   and are conversion summaries with the LMSD65 XYZ-LMS conversion matrix.
        if sim_type == 'deuteranopia':
            # Simulate deuteranopia- greens are greatly reduced (1% men)
            R = clip(round((0.33066007 * r) + (0.66933993 * g) + (0 * b)))
            G = clip(round((0.33066007 * r) + (0.66933993 * g) + (0 * b)))
            B = clip(round((-0.02785538 * r) + (0.02785538 * g) + (1 * b)))
        elif sim_type == 'protanopia':
            # Simulate protanopia- reds are greatly reduced (1% men)
            R = clip(round((0.170556992 * r) + (0.829443014 * g) + (0 * b)))
            G = clip(round((0.170556991 * r) + (0.829443008 * g) + (0 * b)))
            B = clip(round((-0.004517144 * r) + (0.004517144 * g) + (1 * b)))
        elif sim_type == 'tritanopia':
            # Simulate tritanopia - blues are greatly reduced (0.003% population)
            R = clip(round((1 * r) + (0.1273989 * g) + (-0.1273989 * b)))
            G = clip(round((0 * r) + (0.8739093 * g) + (0.1260907 * b)))
            B = clip(round((0 * r) + (0.8739093 * g) + (0.1260907 * b)))
        elif sim_type == 'grayscale':
            # Simulate grayscale - standard color luminance
            R = G = B = int(round((.2126 * r) + (.7152 * g) + (.0722 * b), 0))

        # Tuple: info = (hex, RGB).
        sim_hex = f'#{R:02x}{G:02x}{B:02x}'
        sim_rgb = (R, G, B)
        sim_contrast = self.black_or_white(sim_rgb)

        self.show_bg(color, sim_hex, sim_rgb, sim_contrast, sim_type)
        # Need return for a call from update_fg()
        return color, sim_hex, sim_rgb

    def show_bg(self, color, hexcode, rgb, contrast, sim_type):
        """
        Displays click-selected color and its data in main display field.
        """
        if sim_type == 'orig':
            self.colorinfo.set(
                f"bg='{color}' or bg='{hexcode}'; RGB {rgb}")
            self.bg_info.configure(bg=hexcode, fg=contrast)
        else:
            self.colorinfo.set(
                f"{sim_type} sees '{color}' as: bg='{hexcode}', RGB {rgb}")
            self.bg_info.configure(bg=hexcode, fg=contrast)

        # Need to clear any previously selected text highlighting
        self.bg_info.select_clear()
        self.fg_info.select_clear()

        # NOTE: fg_info resets each time a different bg color is selected,
        #   but bg is retained for any number of different fg selections.
        # TODO: Auto-retain clicked fg for each bg selection.
        self.new_fg.set(f"<-fg='{contrast}'; Right-click different color to change text color")

    @staticmethod
    def black_or_white(rgb: tuple) -> str:
        """
        Calculate perceived brightness value of input RGB to determine
        whether a black or white font foreground contrast is used on the
        input RGB background.

        :param rgb: (R, G, B) tuple of integers in range(0-255)

        :returns: 'black' or 'white' contrast for given RGB
        """
        _R, _G, _B = rgb

        # https://www.nbdtech.com /Blog/archive/2008/04/27/
        #   Calculating-the-Perceived-Brightness-of-a-Color.aspx
        # Brightness limit of 130 has grayscale cutoff at gray51
        # Range of 128-145 will give acceptable results, says author @NirDobovizki
        _pb = sqrt((.241 * _R ** 2) + (.691 * _G ** 2) + (.068 * _B ** 2))
        if _pb > CUTOFF_PB:
            return 'black'
        return 'white'

    def update_fg(self, color: str, rgb: tuple, sim_type: str) -> None:
        """
        As each color label is generated, assign its color name, the hex
        code and RGB strings for that (simulated) color.
        Foreground will be the color or the simulated color's hexcode.
        Called from draw_table() in a lambda .bind() function.

        :param color: The color name
        :param rgb: (R,G,B) of either the named color or its displayed
                    simulated color.
        :param sim_type: 'deuteranopia', 'protanopia', 'tritanopia',
                         'grayscale', 'orig'
        """
        if sim_type == 'orig':
            # No simulation, data for rt-clicked color.
            r, g, b = rgb
            color_hex = f'#{r:02x}{g:02x}{b:02x}'
            self.new_fg.set(
                f"<-Text: '{color}' or fg='{color_hex}'; RGB {rgb}")
            self.bg_info.configure(fg=color)
        else:
            # Generate simulated data for mod-rt-clicked color.
            # Because call to simulate_color() also runs show_bg, need to
            #   store and re-use current bg_info data so it isn't replaced
            #   with the new_fg selection.
            saved_bg = self.bg_info.cget('bg')
            saved_text = self.bg_info.getvar(str(self.bg_info.cget('textvariable')))
            color, sim_hex, sim_rgb = self.simulate_color(color, rgb, sim_type)
            self.new_fg.set(
                f"<-{sim_type} sees '{color}' as fg='{sim_hex}', {sim_rgb}")
            self.bg_info.configure(fg=sim_hex, bg=saved_bg)
            self.colorinfo.set(saved_text)

        # Need to clear any previously selected text edit highlighting.
        self.bg_info.select_clear()
        self.fg_info.select_clear()

        # Need to notify if new_fg and bg sim_types do not match.
        self.simtype_mismatch()

    def simtype_mismatch(self) -> None:
        """
        Check text string in data display fields; raise messagebox if
        color types of background and foreground do not match.
        """
        bg_text = self.colorinfo.get()
        fg_text = self.new_fg.get()
        match = False
        if 'deuteranopia' in bg_text and 'deuteranopia' in fg_text:
            match = True
        elif 'protanopia' in bg_text and 'protanopia' in fg_text:
            match = True
        elif 'tritanopia' in bg_text and 'tritanopia' in fg_text:
            match = True
        elif 'grayscale' in bg_text and 'grayscale' in fg_text:
            match = True
        # NOTE: matches when simulations not used; 'sees' works ONLY because
        #  that is part of the set textvariable whenever a simulation is run.
        elif 'sees' not in bg_text and 'sees' not in fg_text:
            match = True
        if not match:
            msg = ('Background and foreground color simulations differ.'
                   ' Use the same click modifiers when selecting each.'
                   ' Shift=deuteranopia, Ctrl=protanopia, '
                   'Alt(Command)=tritanopia, Shift-Ctrl=grayscale')
            messagebox.showinfo(title='MISMATCH NOTICE', detail=msg)

    def show_simtable(self, image: str) -> None:
        """
        Show in new toplevel window the full color table in specified
        color blind simulated colors.  Called only as keybindings.

        :param image: Descriptor of color simulation image file to
                      retrieve: 'd', 'p', 't', 'g'.
        """
        colorwin = tk.Toplevel()
        colorwin.minsize(1200, 580)
        if image == 'd':
            self.img = tk.PhotoImage(file="images/deuteranopia_colortable.png")
            colorwin.title('Named colors with deuteranopia simulation')
        elif image == 'p':
            self.img = tk.PhotoImage(file="images/protanopia_colortable.png")
            colorwin.title('Named colors with protanopia simulation')
        elif image == 't':
            self.img = tk.PhotoImage(file="images/tritanopia_colortable.png")
            colorwin.title('Named colors with tritanopia simulation')
        elif image == 'g':
            self.img = tk.PhotoImage(file="images/grayscale_colortable.png")
            colorwin.title('Named colors with grayscale simulation')

        colorwin.image = self.img
        colortable = tk.Text(colorwin)
        colortable.image_create(tk.END, image=self.img)
        colortable.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--about',
                        help='Provide description, usage, version, GNU license',
                        action='store_true',
                        default=False)

    args = parser.parse_args()
    if args.about:
        print(__doc__)
        print('Author:    ', __author__)
        print('License:   ', __license__)
        print('Copyright: ', __copyright__)
        print('URL:       ', __project_url__)
        print('Version:   ', __version__)
        print('Status:    ', __status__)
        print('Dev env:   ', __dev__)
        print()
        sys.exit(0)
    else:
        root = tk.Tk()
        root.title("tkinter Named Colors")
        app = ColorChart(root)
        root.mainloop()
