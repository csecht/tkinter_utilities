# modified from:
# https://stackoverflow.com/questions/10865116/
#    tkinter-creating-buttons-in-for-loop-passing-command-arguments
import tkinter as tk
from sys import platform


class WidgetTable(tk.Frame):
    """
    Grid contiguous widgets, usually Labels or Buttons, in columns and
    rows. Mouseovers, clicks, and right-clicks change background color
    of widgets. Table cells can grid to any number of columns and rows.
    Frame contents are proportionally resizable with window.
    """
    def __init__(self, columns, rows):
        super().__init__()

        # Set table dimensions: horizontal and vertical cell numbers (W x H).
        self.columns = columns
        self.rows = rows

        # Note: self.master is inherited from tk.Frame.

        # Prevent window over-shrinkage with errant click-drag &
        #   provide space for full header text.
        self.master.minsize(200, 100)

        # Allow the frame to fill the window and resize with it.
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        # Put a near-white border around the Frame;
        #   bd changes to darker shade for click-drag and loss of focus.
        self.master.config(
            bg='khaki3', # Color of Frame; is border color with kw border.
            border=5, # Thickness of Frame border. Lies inside highlight border.
            highlightthickness=5, # The outer Frame border focus highlighting.
            highlightcolor='grey95',  # Replace default highlight black border with near-white.
            highlightbackground='grey55',  # Change to mid-gray when window looses focus (unclicked or dragged).
            )

        # Widgets' background colors.
        self.color1 = "blue2"
        self.color2 = "goldenrod"
        # If mouseover color matches default, then widgets don't change on mouseover.
        self.mouseover = 'khaki'
        # self.mouseover = 'gray86'  # Use this to not change widget color on mouse over.
        # The default tkinter widget background color.
        self.default = 'gray86'

        self.draw_table()

    def draw_table(self):
        """
        Fill in the frame with contiguous Labels and bind background
        color change functions to each. Number of columns and rows
        of labels are specified in WidgetTable() call parameters. Here
        Labels are used, but can use Button(); just need to modify for
        kw activebackground and command functions.
        """
        col_indx = 0
        row_indx = 1  # row[0] reserved for table header.
        num_cells = self.columns * self.rows
        for _ in range(num_cells):
            label = tk.Label()
            label.grid(column=col_indx, row=row_indx, sticky=tk.NSEW)
            row_indx += 1
            label.bind('<Button-1>', lambda event, l=label: self.color_widget(l))
            label.bind("<Enter>", lambda event, l=label: self.enter(l))
            label.bind("<Leave>", lambda event, l=label: self.leave(l))

            # Bind a right-click event to "erase" cell color.
            #   MacOS uses different button-ID than Linux and Windows.
            if platform == 'darwin':
                label.bind('<Button-2>', lambda event, l=label: self.decolor(l))
            else:
                label.bind('<Button-3>', lambda event, l=label: self.decolor(l))

            # When a column has all table rows gridded, move to next column.
            if row_indx > self.rows:
                col_indx += 1
                row_indx = 1

        # Need to allow proportional resizing of Frame contents with window resize.
        for _col in range(self.columns):
            self.master.columnconfigure(_col, weight=1)

        for _row in range(self.rows + 1):
            self.master.rowconfigure(_row, weight=1)

        header = tk.Label(text='Click to color widget, again for 2nd color, right-click to erase.',
                          font='TkTooltipFont',
                          fg='khaki',
                          bg='firebrick')
        header.grid(column=0, row=0, columnspan=self.columns, sticky=tk.NSEW)

    def enter(self, cell: tk):
        """
        Indicate mouseover cells with a color() change
        (if different from default bg).

        :param cell: The active tkinter widget.
        """

        # Use this to not have mouseover change color (mouseover = default bg).
        # entered_color = cell['bg']
        # if cell['bg'] == entered_color:
        #     cell['bg'] = entered_color

        # Use this to change cell color with mouseover.
        if cell['bg'] == self.color1:
            cell['bg'] = self.color1
        elif cell['bg'] == self.color2:
            cell['bg'] = self.color2
        else:
            cell['bg'] = self.mouseover

    def leave(self, cell: tk):
        """
        On mouse leave, cell returns to entry color.

        :param cell: The active tkinter widget.
        """
        entered_color = cell['bg']
        if cell['bg'] == self.mouseover:
            cell['bg'] = self.default
        else:
            cell['bg'] = entered_color

        # Use this statement instead to color in cursor path with the
        #   mouseover color (when mouseover color is different from default bg).
        # if cell['bg'] == entered_color:
        #     cell['bg'] = entered_color

    def color_widget(self, cell: tk):
        """
        Click on a table cell (widget) to color it; click it
        again or double click to change color.

        :param cell: The active tkinter widget.
        """
        if cell['bg'] == self.color1:
            cell['bg'] = self.color2
        else:
            cell['bg'] = self.color1

    def decolor(self, cell: tk):
        """
        Used with a right-click binding to remove cell color.

        :param cell: The active tkinter widget.
        """
        if cell['bg'] == self.color1 or cell['bg'] == self.color2:
            cell['bg'] = self.default


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Widget Table')
    # Set table dimensions (# cells: W, H) in Class call.
    WidgetTable(15, 10)
    root.mainloop()
