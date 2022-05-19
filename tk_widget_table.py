#!/usr/bin/env python3

"""
A template for positioning contiguous widgets in a column-row format.
"""
# modified from:
# https://stackoverflow.com/questions/10865116/
#    tkinter-creating-buttons-in-for-loop-passing-command-arguments
import sys
from tkutils_modules import vcheck

vcheck.minversion('3.7')

try:
    import tkinter as tk
except (ImportError, ModuleNotFoundError):
    print('This program requires tkinter, which is included with \n'
          'Python 3.7+ distributions.\n'
          'Install the most recent version or re-install Python and include Tk/Tcl.\n'
          '\nOn Linux, you may also need: $ sudo apt-get install python3-tk\n'
          'See also: https://tkdocs.com/tutorial/install.html\n')


class WidgetTable(tk.Frame):
    """
    Grid contiguous widgets, usually Labels or Buttons, in columns and
    rows. Mouseovers, clicks, and right-clicks change background color
    of widgets. Table cells can grid to any number of columns and rows.
    Frame contents are proportionally resizable with window.
    """
    def __init__(self, columns: int, rows: int):
        super().__init__()

        # Set table dimensions: horizontal and vertical cell numbers (W x H).
        self.columns = columns
        self.rows = rows

        # Note: self.master refers to the tk.Frame.

        # Widgets' background colors.
        self.theme = 'khaki'  # Used for outer frame border and header fg.
        self.header_bg = 'firebrick'
        self.frame_bg = 'khaki3'  # Used for inner frame border and mouseover.
        self.hilite_bg = 'khaki4'
        self.label_bg1 = 'blue2'
        self.label_bg2 = 'goldenrod'
        self.default_bg = 'gray86'  # Linux and Windows default widget bg.
        self.label_fg1 = 'MediumPurple2'
        self.label_fg2 = self.default_bg

        # The default_bg tkinter widget background color varies with operating system.
        if sys.platform == 'darwin':
            self.default_bg = 'white'

        self.draw_table()

    def draw_table(self):
        """
        Fill in the frame with contiguous Labels and bind background
        color change functions to each. Number of columns and rows
        of labels are specified in WidgetTable() call parameters. Here
        Labels are used, but can use Button(); just need to modify for
        kw activebackground and command functions.
        """
        # Prevent over-shrinkage of tk window with errant click-drag and
        #   provide minimum area for a readable table header text.
        self.master.minsize(250, 200)

        # Allow the frame to fill the window and resize with it.
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        self.master.config(
            bg=self.frame_bg,  # Fill color of Frame; is border color when kw border is used.
            border=5,  # Thickness of Frame border. Lies inside highlight border.
            highlightthickness=5,  # Outer Frame border used for window focus highlighting.
            highlightcolor=self.theme,  # Lighter color of outer border on focus.
            highlightbackground=self.hilite_bg,  # Darker color of outer border off focus.
        )

        col_indx = 0
        row_indx = 1  # row[0] is reserved for table header.
        num_cells = self.columns * self.rows
        for i in range(num_cells):
            label_text = str(i + 1).rjust(3)
            label = tk.Label(text=label_text,
                             fg=self.label_fg1,
                             font='TkFixedFont', )
            label.grid(column=col_indx, row=row_indx, sticky=tk.NSEW)
            row_indx += 1
            label.bind('<Button-1>', lambda event, l=label: self.color_widget_bg(l))
            label.bind('<Double-Button-1>', lambda event, l=label: self.color_widget_fg(l))
            label.bind("<Enter>", lambda event, l=label: self.on_enter(l))
            label.bind("<Leave>", lambda event, l=label: self.on_leave(l))

            # Bind a right-click event to "erase" cell color (change to default_bg).
            #   MacOS uses different button-ID than Linux and Windows.
            if sys.platform == 'darwin':
                label.bind('<Button-2>', lambda event, l=label: self.decolor(l))
            else:
                label.bind('<Button-3>', lambda event, l=label: self.decolor(l))

            # Once a column has all rows gridded, move to next column.
            if row_indx > self.rows:
                col_indx += 1
                row_indx = 1

        # Needed for proportional resizing of Frame contents with window resize.
        for _col in range(self.columns):
            self.master.columnconfigure(_col, weight=1)

        for _row in range(self.rows + 1):
            self.master.rowconfigure(_row, weight=1)

        header = tk.Label(text='Click colors a widget, 2nd click recolors,'
                               ' rt-click decolors,\ndbl-click changes text color.',
                          font='TkTooltipFont',
                          fg=self.theme,
                          bg=self.header_bg)
        header.grid(column=0, row=0, columnspan=self.columns, sticky=tk.NSEW)

    def on_enter(self, cell: tk):
        """
        Indicate mouseover cells with a color() change
        (if different from default_bg bg).

        :param cell: The active tkinter widget.
        """

        # Use this to not have mouseover change color (mouseover = default bg).
        # entered_color = cell['bg']
        # if cell['bg'] == entered_color:
        #     cell['bg'] = entered_color

        # Use this to change cell color with mouseover.
        if cell['bg'] == self.label_bg1:
            cell['bg'] = self.label_bg1
        elif cell['bg'] == self.label_bg2:
            cell['bg'] = self.label_bg2
        else:
            cell['bg'] = self.frame_bg

    def on_leave(self, cell: tk):
        """
        On mouse leave, cell returns to entry color.

        :param cell: The active tkinter widget.
        """
        entered_color = cell['bg']
        if cell['bg'] == self.frame_bg:
            cell['bg'] = self.default_bg
        else:
            cell['bg'] = entered_color

        # Use this statement instead to color in cursor path with the
        #   mouseover color (when mouseover color is different from default_bg bg).
        # if cell['bg'] == entered_color:
        #     cell['bg'] = entered_color

    def color_widget_bg(self, cell: tk):
        """
        Click on a table cell (widget) to color it; click it
        again to change background color.

        :param cell: The active tkinter widget.
        """
        if cell['bg'] == self.label_bg1:
            cell['bg'] = self.label_bg2
        else:
            cell['bg'] = self.label_bg1

    def color_widget_fg(self, cell: tk):
        """
        Double click on a table cell (widget) to change foreground color.
        When label fg is set to the default_bg color, the label text
        will blend into the default bg on alternate double-clicks.

        :param cell: The active tkinter widget.
        """
        if cell['fg'] == self.label_fg1:
            cell['fg'] = self.label_fg2
        else:
            cell['fg'] = self.label_fg1

    def decolor(self, cell: tk):
        """
        Used with a right-click binding to remove cell color.

        :param cell: The active tkinter widget.
        """
        if cell['bg'] in (self.label_bg1, self.label_bg2):
            cell['bg'] = self.default_bg


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Widget Table')
    # Set table dimensions (# cells: col, row) as Class parameters.
    WidgetTable(15, 10)
    root.mainloop()
