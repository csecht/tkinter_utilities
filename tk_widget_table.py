#!/usr/bin/env python3

"""
A template for positioning contiguous widgets in a column-row format and
binding multiple mouse button actions to each widget.

Table construction is modified from:
https://stackoverflow.com/questions/10865116/
   tkinter-creating-buttons-in-for-loop-passing-command-arguments
Separating double clicks from clicks source:
https://stackoverflow.com/questions/27262580/tkinter-binding-mouse-double-click
   Bruno Vermeulen's answer.
"""

import sys
from tk_utils import vcheck

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
    of widgets. Double-clicks change foreground. Table cells can grid to
    any number of columns and rows. Frame contents are proportionally
    resizable with window; self.master is the implicit parent.
    """
    def __init__(self, columns: int, rows: int):
        super().__init__()

        # Set table dimensions: horizontal and vertical cell numbers (W x H).
        self.columns = columns
        self.rows = rows

        # Widgets' colors.
        self.theme = 'khaki'  # Used for outer frame border and header fg.
        self.frame_bg = 'khaki3'  # Used for inner frame border and mouseover.
        self.header_bg = 'firebrick'
        self.hilite_bg = 'khaki4' # Darker off-focus color of outer border.
        self.label_bg1 = 'blue2'
        self.label_bg2 = 'goldenrod'
        # The default_bg tkinter widget background color varies with operating system.
        self.default_bg = 'gray86'  # Linux and Windows default widget bg.
        if sys.platform == 'darwin':  # macOS
            self.default_bg = 'white'
        self.label_fg1 = 'MediumPurple2'
        # Have the alternate fg match the bg so it "disappears", except on mouseover.
        self.label_fg2 = self.default_bg

        self.double_click_flag = False

        self.draw_table()

    def draw_table(self) -> None:
        """
        Fill in the frame with contiguous Labels and bind fg and bg
        color change functions to each. Number of columns and rows of
        widgets are specified in WidgetTable() call parameters. Labels
        are used here, but can also use Buttons; just need to modify for
        kw activebackground and command functions.
        """
        # Note: self.master refers to the tk.Frame.
        # Allow the frame to fill the root window and resize with it.
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
        labels = []
        event_handlers = {
            '<Button-1>': self.single_click,
            '<Double-1>': self.double_click,
            '<Shift-1>': self.shift_click,
            '<Enter>': self.on_enter,
            '<Leave>': self.on_leave,
            '<Button-2>' if sys.platform == 'darwin' else '<Button-3>': self.decolor
        }

        for i in range(num_cells):
            label_text = str(i + 1).rjust(3)
            label = tk.Label(text=label_text,
                             fg=self.label_fg1,
                             font='TkFixedFont',
                             )
            labels.append((label, row_indx, col_indx))

            # Bind events to label using a dispatch dictionary of handlers.
            for event, handler in event_handlers.items():
                label.bind(event, lambda e, h=handler, l=label: h(l))

            # Use this to sort cell numbers (text) vertically, by column.
            #   Once a column has all rows gridded, move left to next column.
            # row_indx += 1
            # if row_indx > self.rows:
            #     col_indx += 1
            #     row_indx = 1

            # Use this to sort cell numbers horizontally, by row.
            #   Once a row has all columns gridded, move down to next row.
            col_indx += 1
            if col_indx > self.columns - 1:
                row_indx += 1
                col_indx = 0

        # Needed for proportional resizing of Frame contents upon window resize.
        for _col in range(self.columns):
            self.master.columnconfigure(_col, weight=1)

        for _row in range(self.rows + 1):
            self.master.rowconfigure(_row, weight=1)

        header = tk.Label(text='Click colors a cell, again recolors,'
                               ' rt-click removes color,\n'
                               'shift-click or double-click changes text color',
                          font='TkTooltipFont',
                          fg=self.theme,
                          bg=self.header_bg)
        header.grid(column=0, row=0, columnspan=self.columns, sticky=tk.NSEW)

        # Grid all table labels from the loop.
        for label, row, col in labels:
            label.grid(row=row, column=col, sticky=tk.NSEW)

    def on_enter(self, cell: tk) -> None:
        """
        Indicate mouseover cells with a color() change
        (if different from default_bg bg).

        :param cell: The active tkinter widget.
        :return: None
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

    def on_leave(self, cell: tk) -> None:
        """
        On mouse leave, cell returns to entry color.

        :param cell: The active tkinter widget.
        :return: None
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

    def single_click(self, cell: tk) -> None:
        """
        Delay a single click on the cell to allow double_click action.
        Binding to a mouse click event.

        :param cell: The active tkinter widget, a passthrough parameter.
        :return: None
        """
        self.double_click_flag = False
        self.after(300, self.click_control, cell)

    def double_click(self, event) -> None:
        """
        Set flag to permit a double click event to change foreground in
        click_control().
        Binding to a mouse double-click event.

        :param event: Any general mouse event.
        :return: None
        """
        self.double_click_flag = True
        return event

    def click_control(self, cell: tk) -> None:
        """
        Separate single and double mouse button events such that a
        double-click will not call a single-click function.
        Click a table cell (widget) to color it; click it again to
        change the cell's background color.
        Double-click a table cell to change its foreground color.
        Double-click again to change it back.
        When the cell's fg is set to the default_bg color, the cell's
        text will blend into the default bg on alternate double-clicks.

        :param cell: The active tkinter widget.
        :return: None
        """
        if self.double_click_flag:
            if cell['fg'] == self.label_fg1:
                cell['fg'] = self.label_fg2
            else:
                cell['fg'] = self.label_fg1
            self.double_click_flag = False

        else:  # Is single click.
            if cell['bg'] == self.label_bg1:
                cell['bg'] = self.label_bg2
            else:
                cell['bg'] = self.label_bg1

    def shift_click(self, cell: tk) -> None:
        """
        Toggles foreground color of *cell*.
        Binding to a shift-click event.

        :param cell: The active tkinter widget.
        :return: None
        """
        if cell['fg'] == self.label_fg1:
            cell['fg'] = self.label_fg2
        else:
            cell['fg'] = self.label_fg1

    def decolor(self, cell: tk) -> None:
        """
        Removes background color of *cell*.
        Binding to right-click event.

        :param cell: The active tkinter widget.
        :return: None
        """
        if cell['bg'] in (self.label_bg1, self.label_bg2):
            cell['bg'] = self.default_bg


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Widget Table')

    # Prevent over-shrinkage of tk window with errant click-drag and
    #   provide a minimum area for all the table header text.
    root.minsize(350, 200)

    # Set table dimensions (# columns, # rows) as Class parameters.
    WidgetTable(15, 10)
    root.mainloop()
