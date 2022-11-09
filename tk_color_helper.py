#!/usr/bin/env python3
"""
A Python utility to help choose colors and their color blind equivalents
for tkinter GUIs. Draws an interactive color table for 760 color names
found in X11 rgb.txt that are recognized by tkinter 8.6. Works with
Linux, Windows, and MacOS.
   Usage: Click on a color name to show its hex code and RGB
value and display that color as background. Right-click a different color
to change the text foreground. Clicking on another color will retain
that selected foreground. Click with a modifier key to show the
color blind simulation of the selected color: Shift = deuteranopia,
Ctrl = protanopia, Alt(Command) = tritanopia, Shift-Ctrl = grayscale;
the displayed foreground color will automatically match the simulation
type. Simulated color hex codes and RGB values may not correspond to any
named color but the hex string will be recognized by tkinter.
    Using the Ctrl key (or Command in macOS) while pressing D, P, T, or
G will pop-up a non-interactive color table simulated for deuteranopia,
protanopia, tritanopia, or grayscale, respectively.
    Text in the color display and data fields can be cut, copied, pasted,
or edited with standard keyboard and click commands. Runs with Python 3.6
and tkinter 8.6 or later.
Color table construction based on code from
https://stackoverflow.com/questions/4969543/colour-chart-for-tkinter-and-tix
"""
# 'Copyright (C) 2021- 2022 C.S. Echt, under GNU General Public License'

# Standard library import:
import sys
from pathlib import Path

# Local program import:
from tk_utils import (constants as const,
                      utils,
                      vcheck)

try:
    import tkinter as tk
except (ImportError, ModuleNotFoundError):
    print('Requires tkinter, which is included with \n'
          'Python 3.7+ distributions.\n'
          'Install the most recent version or re-install Python and include Tk/Tcl.\n\n'
          'On Linux you may also need:$ sudo apt-get install python3-tk\n'
          'See also: https://tkdocs.com/tutorial/install.html\n')


class ColorChart(tk.Frame):
    """
    Set up main frame and fill it with interactive widgets for all valid
    named colors that can be used in tkinter. Generate simulations for
    different types of color blindness. Apply perceived brightness
    contrasts to use either default black or white foregrounds.
    """

    __slots__ = (
        'use_info', 'bg_info', 'fg_info', 'bg_text', 'fg_text', 'bg_hex',
        'fg_color', 'fg_hex', 'fg_rgb', 'sim_type', 'info_width'
    )

    def __init__(self):
        super().__init__()

        self.use_info = tk.Label(self)
        self.bg_info = tk.Entry(self)
        self.fg_info = tk.Entry(self)
        self.bg_text = tk.StringVar()
        self.fg_text = tk.StringVar()
        self.bg_hex = tk.StringVar()
        self.fg_color = tk.StringVar()
        self.fg_hex = tk.StringVar()
        self.fg_rgb = ('None',)
        self.sim_type = tk.StringVar()

        # Width of row1; total number of columns gridded in make_colortable().
        self.info_width = 0

        self.make_colortable()

        # config_master() needs to run after make_colortable() to define the
        #   number of columns needed for self.info_width.
        self.config_master()

    def make_colortable(self) -> None:
        """
        Make the tkinter color table.
        Call simulate_color(), black_or_white(), foreground_info.
        """

        # row 0 reserved for standing usage instructions, row 1 reserved for
        #   color information Entry() fields.
        _col = 0
        _row = 2
        for color_name in const.X11_RGB_NAMES:
            label = tk.Label(self,
                             text=color_name,
                             bg=color_name,
                             font=('TkTooltipFont', const.LABEL_FONT_SIZE),
                             )
            label.grid(row=_row, column=_col, sticky=tk.NSEW)
            _row += 1

            # Need to convert winfo_rgb 16-bit RGB tuple (in range 0-65535)
            #  to 8-bit values for 256 RGB color (256^2 = 65536).
            # source: https://stackoverflow.com/questions/58758439/
            #   how-can-i-get-hex-or-rgb-color-code-of-the-window-background-color
            #   The operator >> is used for Right circular rotation of a BitVector
            #     through N positions: operator.__rshift__().
            #   Equivalent to: _R, _G, _B = [x // 256 for x in label.winfo_rgb(color_name)]
            _R, _G, _B = [x >> 8 for x in label.winfo_rgb(color_name)]
            rgb = (_R, _G, _B)
            color_hex = f'#{_R:02x}{_G:02x}{_B:02x}'

            # Set default label text B&W fg for best contrast against color_name bg.
            label.config(fg=self.black_or_white(rgb))

            # Use clicks to bind color label to color and data display.
            # Click selects background, rt-click selects foreground.
            # Rt-click Button is OS-specific.
            # MacOS cannot use the Alt/option modifier, so use Command.
            # Universal bindings:
            label.bind('<Button-1>',
                       lambda _, c=color_name, r_b=rgb:
                       self.simulate_color(c, r_b, 'nosim'))
            label.bind('<Shift-Button-1>', lambda _, c=color_name, r_b=rgb:
                       self.simulate_color(c, r_b, 'deuteranopia'))
            label.bind('<Control-Button-1>', lambda _, c=color_name, r_b=rgb:
                       self.simulate_color(c, r_b, 'protanopia'))
            label.bind('<Shift-Control-Button-1>', lambda _, c=color_name, r_b=rgb:
                       self.simulate_color(c, r_b, 'grayscale'))
            # OS-specific bindings:
            if utils.MY_OS in 'lin, win':
                label.bind('<Alt-Button-1>', lambda _, c=color_name, r_b=rgb:
                           self.simulate_color(c, r_b, 'tritanopia'))
                label.bind('<Button-3>',
                           lambda _, c=color_name, h=color_hex, r_b=rgb:
                           self.foregrnd_info(c, r_b))
            elif utils.MY_OS == 'dar':
                label.bind('<Command-Button-1>', lambda _, c=color_name, r_b=rgb:
                           self.simulate_color(c, r_b, 'tritanopia'))
                label.bind('<Button-2>',
                           lambda _, c=color_name, h=color_hex, r_b=rgb:
                           self.foregrnd_info(c, r_b))

            # Grid Labels col x row, reset to top row once a column is filled.
            if _row >= const.MAX_ROWS:
                _col += 1
                _row = 2

        # Used in config_master()
        self.info_width = _col

    def config_master(self) -> None:
        """
        Set up universal and OS-specific keybindings and popup menus
        with standard key and click commands. Set default info text and
        grid info widgets. Define font type and OS-specific sizes.
        """

        self.master.minsize(600, 300)

        # Need to color in all the top Tk window to create near-white border;
        #    border changes to grey for click-drag and not focus.
        self.master.config(highlightthickness=3,
                           highlightcolor='gray95',
                           highlightbackground='gray')

        for _row in range(const.MAX_ROWS):
            self.rowconfigure(_row, weight=1)
        for _col in range(self.info_width):
            self.columnconfigure(_col, weight=1)

        self.master.bind_all('<Escape>', lambda: utils.quit_gui(app))

        # Provide an exit msg in Terminal when click on the close window icon.
        self.master.protocol('WM_DELETE_WINDOW', lambda: utils.quit_gui(app))

        # Need to specify Ctrl-a for Linux b/c in tkinter that key is
        #   bound to <<LineStart>>, not <<SelectAll>>.
        if utils.MY_OS == 'lin':
            self.master.bind_all('<Control-a>', lambda event:
                                 Chart.focus_get().event_generate('<<SelectAll>>'))

        cmdkey = ''
        if utils.MY_OS in 'lin, win':
            cmdkey = 'Control'
        elif utils.MY_OS == 'dar':
            cmdkey = 'Command'

        utils.keybind('quit', toplevel=self.master, mainwin=app)

        # Keybindings to show the simulated color table images in Toplevel windows.
        self.master.bind(
            f'<{f"{cmdkey}"}-d>', lambda _: self.show_simtable('d'))
        self.master.bind(
            f'<{f"{cmdkey}"}-p>', lambda _: self.show_simtable('p'))
        self.master.bind(
            f'<{f"{cmdkey}"}-t>', lambda _: self.show_simtable('t'))
        self.master.bind(
            f'<{f"{cmdkey}"}-g>', lambda _: self.show_simtable('g'))

        utils.click('right', self.bg_info)
        utils.click('right', self.fg_info)

        if utils.MY_OS in 'lin, win':
            self.use_info.configure(font=('TkTooltipFont', 9))
            self.bg_info.config(font=('TkTooltipFont', 12))
            self.fg_info.config(font=('TkTooltipFont', 9))
        elif utils.MY_OS == 'dar':
            self.use_info.configure(font=('TkTooltipFont', 12))
            self.bg_info.config(font=('TkTooltipFont', 16))
            self.fg_info.config(font=('TkTooltipFont', 12))

        # This usage information goes on the top row and is always visible.
        usage = ('Click changes background, right-click changes foreground.'
                 ' Click modifiers simulate color blindness; Shift:deuteranopia,'
                 ' Ctrl:protanopia, Alt(Command on Mac):tritanopia,'
                 ' Shift-Crtl:grayscale.')
        self.use_info.configure(text=usage, bg='gray25', fg='gray90')

        # Note: bg and fg of info Entry() widgets will change with click
        #   bindings, but start with a default bg.
        self.bg_info.configure(textvariable=self.bg_text,
                               justify='center',
                               bg='gray90',
                               relief='sunken',
                               )

        self.fg_info.configure(textvariable=self.fg_text,
                               justify='center',
                               bg='gray90',
                               relief='sunken',
                               )

        # Startup text for the two Entry widgets.
        self.bg_text.set('Background color name, hex code, '
                         'and RGB values are displayed here.')
        self.fg_text.set('Foreground color name, hex code, '
                         'and RGB values are displayed here.')

        # NOTE: fg_info col width needs to be enough to handle the longest
        #   color name plus hex and RGB; depends on font size.
        # Need to use sticky=tk.NSEW to expand Entry to fill the grid 'cell'
        #   whatever the font size may be.
        self.use_info.grid(row=0, column=0,
                           columnspan=20,
                           sticky=tk.NSEW,
                           )
        self.bg_info.grid(row=1, column=0,
                          columnspan=self.info_width - 10,
                          sticky=tk.EW,
                          )
        self.fg_info.grid(row=1, column=self.info_width - 10,
                          columnspan=10,
                          sticky=tk.NSEW,
                          )

        # Need 'nosim' as default start value.
        self.sim_type.set('nosim')

        # It's all set up, so now display all widgets in the app Tk window.
        self.pack(expand=True, fill=tk.BOTH)

    def simulate_color(self, color: str,
                       rgb: tuple,
                       sim_type: str,
                       fg_do=None) -> tuple:
        """
        Convert listed named color RGB values to values that simulate the
        specified type of color blindness or grayscale. RGB is defined in
        self.make_colortable() from label.winfo_rgb(color_name).
        Source: http://mkweb.bcgsc.ca/colorblind/math.mhtml

        :param color: A color name from const.X11_RGB_NAMES
        :param rgb: (R, G, B) tuple of integers in range(0-255)
        :param sim_type: 'deuteranopia', 'protanopia',
                         'tritanopia', 'grayscale', 'nosim'
        :param fg_do: Flags a call from foregrnd_info() as 'yes'

        :returns: (sim_hex: str, sim_rgb: tuple)
        """

        self.sim_type.set(sim_type)
        _r, _g, _b = rgb
        _R = 0
        _G = 0
        _B = 0

        # Need to restrict RGB values to integers in range (0 - 255).
        # source: https://stackoverflow.com/questions/5996881/
        #   how-to-limit-a-number-to-be-within-a-specified-range-python
        def clip(_c):
            return max(min(255, _c), 0)

        # Calculate color-blind simulation using T matrix RGB conversion.
        # All T matrix values from http://mkweb.bcgsc.ca/colorblind/math.mhtml
        #   and are conversion summaries with the LMSD65 XYZ-LMS conversion matrix.
        #   Author: Martin Krzywinski
        if sim_type == 'deuteranopia':
            # Simulate deuteranopia - greens are greatly reduced (1% men)
            _R = clip(round((0.33066007 * _r) + (0.66933993 * _g) + (0 * _b)))
            _G = clip(round((0.33066007 * _r) + (0.66933993 * _g) + (0 * _b)))
            _B = clip(round((-0.02785538 * _r) + (0.02785538 * _g) + (1 * _b)))
        elif sim_type == 'protanopia':
            # Simulate protanopia - reds are greatly reduced (1% men)
            _R = clip(round((0.170556992 * _r) + (0.829443014 * _g) + (0 * _b)))
            _G = clip(round((0.170556991 * _r) + (0.829443008 * _g) + (0 * _b)))
            _B = clip(round((-0.004517144 * _r) + (0.004517144 * _g) + (1 * _b)))
        elif sim_type == 'tritanopia':
            # Simulate tritanopia - blues are greatly reduced (0.003% population)
            _R = clip(round((1 * _r) + (0.1273989 * _g) + (-0.1273989 * _b)))
            _G = clip(round((0 * _r) + (0.8739093 * _g) + (0.1260907 * _b)))
            _B = clip(round((0 * _r) + (0.8739093 * _g) + (0.1260907 * _b)))
        elif sim_type == 'grayscale':
            # Simulate grayscale - standard color luminance
            _R = _G = _B = int(round((.2126 * _r) + (.7152 * _g) + (.0722 * _b), 0))
        elif sim_type == 'nosim':
            _R = _r
            _G = _g
            _B = _b

        sim_hex = f'#{_R:02x}{_G:02x}{_B:02x}'
        sim_rgb = (_R, _G, _B)

        # Need to distinguish whether sim is for default fg, new bg, or new fg.
        prior_fg = self.fg_hex.get()
        # 'fg_click is None' is true when call is from button1 click.
        #  Note: Once sync_simtypes() is called, fg no longer defaults to the
        #     color label's black or white.
        if sim_type == 'nosim' and fg_do is None:
            # Note: here, fg_hex is the color name, not the hexcode.
            fg_hex = self.black_or_white(sim_rgb)
            self.fg_hex.set(fg_hex)
            if prior_fg not in 'black, white':
                self.fg_hex.set(prior_fg)
            else:
                self.fg_hex.set(fg_hex)
            self.display_colors(color, sim_rgb, sim_type)
        elif sim_type != 'nosim' and fg_do is None:
            fg_hex = self.black_or_white(sim_rgb)
            if prior_fg in 'black, white':
                self.fg_hex.set(fg_hex)
                self.fg_color.set(fg_hex)
            self.display_colors(color, sim_rgb, sim_type)
        # 'fg_click is yes' when call is from button2 or 3, via foregrnd_info().
        if fg_do == 'yes':
            self.fg_hex.set(sim_hex)

        return sim_hex, sim_rgb

    def display_colors(self,
                       color: str,
                       rgb: tuple,
                       sim_type: str) -> None:
        """
        Displays click-selected color and its data in main display field.
        Preserves prior foreground color.
        Called from simulate_color().

        Args:
            color: The color name, as string
            rgb: (R, G, B) of either the named color or its displayed
                 simulated color, as tuple
            sim_type: Use 'deuteranopia', 'protanopia', 'tritanopia',
                      'grayscale', or 'nosim'.

        Returns: None
        """

        _r, _g, _b = rgb
        bg_hex = f'#{_r:02x}{_g:02x}{_b:02x}'

        self.sim_type.set(sim_type)
        # self.fg_hex is first set in simulate_color(). It will be the
        #   default 'black' or 'white' until rt-click binding changes the fg.
        fg_hex = self.fg_hex.get()

        # Click binding sends color selection to simulate_color(),
        #   with a sim_type tag.
        if sim_type == 'nosim':
            self.bg_text.set(
                f"bg='{color}' or bg='{bg_hex}'; RGB {rgb}")
        else:
            self.bg_text.set(
                f"{sim_type} sees '{color}' as bg='{bg_hex}'; RGB {rgb}")
        self.bg_info.configure(bg=bg_hex, fg=fg_hex)
        self.fg_info.configure(bg=bg_hex, fg=fg_hex)

        self.sync_simtypes()

        # Need to clear any previously selected text highlighting.
        self.bg_info.select_clear()
        self.fg_info.select_clear()
        self.update_idletasks()

    def foregrnd_info(self, color: str, rgb: tuple) -> None:
        """
        Assign foreground color to Entry() fields. Provide fg data.
        Convert selected color to current background simulation type.
        Called from make_colortable() in a keybinding lambda function.

        :param color: The color name
        :param rgb: (R,G,B) of either the named color or its displayed
                    simulated color.
        """
        _r, _g, _b = rgb
        fg_hex = f'#{_r:02x}{_g:02x}{_b:02x}'
        sim_type = self.sim_type.get()

        # Used in sync_simtypes() to synchronize fg to bg sim_types.
        self.fg_color.set(color)
        self.fg_rgb = rgb

        if sim_type == 'nosim':
            self.fg_hex.set(fg_hex)
            self.fg_text.set(
                f"fg='{color}' or fg='{fg_hex}'; RGB {rgb}")
            self.bg_info.configure(fg=fg_hex)
            self.fg_info.configure(fg=fg_hex)
        else:
            # To match fg to bg sim_type, fg selection calls simulated_color(),
            #   which .sets() the fg sim hex and rgb control variables.
            sim_hex, sim_rgb = self.simulate_color(color=color,
                                                   rgb=rgb,
                                                   sim_type=sim_type,
                                                   fg_do='yes')
            self.fg_text.set(
                f"{sim_type} sees '{color}' as fg='{sim_hex}'; RGB {sim_rgb}")
            self.bg_info.configure(fg=sim_hex)
            self.fg_info.configure(fg=sim_hex)

        # Need to clear any previously selected text edit-highlighting.
        self.bg_info.select_clear()
        self.fg_info.select_clear()
        self.update_idletasks()

    def sync_simtypes(self) -> None:
        """
        Convert foreground color to match the simulation (or
        lack of simulation) to that of the selected background color.
        Called from display_colors().
        """

        bg_text = self.bg_text.get()
        fg_text = self.fg_text.get()
        sim_type = self.sim_type.get()
        color = self.fg_color.get()
        fg_hex = self.fg_hex.get()

        # Need to set self.fg_rgb to default color fg of black or white
        #   in cases of sim color selected before a fg color is selected.
        if fg_hex == 'black':
            self.fg_rgb = (0, 0, 0)
        elif fg_hex == 'white':
            self.fg_rgb = (255, 255, 255)

        sim_list = ['deuteranopia', 'protanopia', 'tritanopia',
                    'grayscale', 'nosim']
        match = False
        for sim in sim_list:
            if sim in bg_text and sim in fg_text:
                match = True

        # NOTE: 'sees' matches when simulations not used; works ONLY because
        #  'sees' is part of the text StringVar whenever a simulation is run.
        if 'sees' not in bg_text and 'sees' not in fg_text:
            match = True
        if not match:
            sim_hex, sim_rgb = self.simulate_color(color, self.fg_rgb, sim_type, 'yes')
            if sim_type == 'nosim':
                self.fg_text.set(
                    f"fg='{color}' or fg='{sim_hex}'; RGB {sim_rgb}")
            else:
                self.fg_text.set(
                    f"{sim_type} sees '{color}' as fg='{sim_hex}'; RGB {sim_rgb}")
            self.bg_info.configure(fg=sim_hex)
            self.fg_info.configure(fg=sim_hex)

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
        # Cutoff of perceived brightness, -pb, in range(128-145) to switch from
        #   black to white foreground will give acceptable visual contrast when
        #   background below that PB. 130 has a cutoff of gray51.
        # Range of 128-145 will give acceptable results, says author @NirDobovizki.
        _pb = ((.241 * _R ** 2) + (.691 * _G ** 2) + (.068 * _B ** 2)) ** 0.5

        if _pb > 138:
            return 'black'
        return 'white'

    @staticmethod
    def show_simtable(image: str) -> None:
        """
        Show in new toplevel window the full color table PNG in specified
        color-blind simulated colors.  Called only as keybindings.

        :param image: Descriptor of color simulation image file to
                      retrieve: 'd', 'p', 't', 'g'.
        """
        simwin = tk.Toplevel()
        simwin.minsize(1200, 580)
        utils.keybind('close', toplevel=simwin, mainwin=app)

        img = tk.PhotoImage

        if image == 'd':
            img = tk.PhotoImage(
                file=utils.valid_path_to('images/deuteranopia_colortable.png'))
            simwin.title('X11 named colors with deuteranopia simulation')
        elif image == 'p':
            img = tk.PhotoImage(
                file=utils.valid_path_to('images/protanopia_colortable.png'))
            simwin.title('X11 named colors with protanopia simulation')
        elif image == 't':
            img = tk.PhotoImage(
                file=utils.valid_path_to('images/tritanopia_colortable.png'))
            simwin.title('X11 named colors with tritanopia simulation')
        elif image == 'g':
            img = tk.PhotoImage(
                file=utils.valid_path_to('images/grayscale_colortable.png'))
            simwin.title('X11 named colors with grayscale simulation')

        simwin.image = img
        simtable = tk.Text(simwin)
        simtable.image_create(tk.END, image=img)
        simtable.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)


if __name__ == "__main__":

    # System platform and version checks are run in tk_utils __init__.py
    #   Program exits if checks fail.

    utils.check_platform()
    vcheck.minversion('3.7')

    utils.manage_args()

    app = tk.Tk()
    app.title('tkinter Named Colors')

    # Developer: Custom handlers for unexpected system and tkinter exceptions.
    # sys.excepthook = utils.handle_exception
    # canvas_window.report_callback_exception = utils.handle_exception

    # Need to set correct relative path for icon image file.
    try:
        icon_img = tk.PhotoImage(
            file=utils.valid_path_to('images/helper_icon512.png'))
        app.iconphoto(True, icon_img)
    except tk.TclError as err:
        print('Cannot display program icon,'
              ' so it will be left blank or tk default.')
        print(f'tk error message: {err}')

    Chart = ColorChart()
    print(f'{Path(__file__).name} is now running...')

    try:
        app.mainloop()
    except KeyboardInterrupt:
        print(' *** Quit program on keyboard interrupt by user ***\n')
