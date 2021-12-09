#!/usr/bin/env python3

"""
A template for an MVC architecture (model, view, controller) in tkinter
applications. Demonstrates basic functions and Class interactions.
A modification of template provided by Brian Oakley at:
https://stackoverflow.com/questions/32864610/
"""

import tkinter as tk


class DataModeler:
    """
    A stub modeler class.
    The modeler crunches input from viewer, then sends results back via
    shared 'share' objects handled through the AppController class.
    """

    def __init__(self, share):
        self.share = share

    def double_it(self):
        user_entry = int(self.share.tkdata['entry'].get())
        answer = user_entry * 2
        self.share.tkdata['result'].set(answer)


class GuiViewer(tk.Frame):
    """
    The viewer communicates with modeler via 'share' objects handled
    through the controller class. All GUI widgets go here.
    """

    # def __init__(self, share, master=None):
    #     super().__init__(master)
    # ^^This is the formal construction, but 'master' is internal, hence:
    def __init__(self, share):
        super().__init__()
        self.frame = self  # Total unnecessary, but can clarify location.
        self.share = share

        self.menubar = tk.Menu()
        self.app_bg = 'SkyBlue4'
        self.viewer_bg = 'yellow'

        # Note that 'self' type is __main__.GuiViewer class;
        #    use as the parent to place a widget in the Frame.
        # 'self.share' and 'self.master' both refer to __main__.AppController;
        #    use either or nothing as a widget's parent to be the app Tk window.
        # When outside the GuiViewer class, can use app. for reference instead
        #    of self.master or self.share; when outside MVC structure, can
        #    use only app. Examples:
        #    app.destroy(), app.update_idletasks(), pos_x = app.winfo_x(), etc.

        self.entry_header = tk.Label(self.frame)  # Same as tk.Label(self).
        self.entry_number = tk.Entry(self)
        self.result_header = tk.Label(self.frame)
        self.result_show = tk.Label(self.frame)

        # Use a dictionary for tkinter control variables that will
        #   be shared between Viewer and Modeler.
        # Default values are set in configure_widgets().
        self.share.tkdata = {
            'entry': tk.IntVar(self),
            'result': tk.IntVar(self)
        }

        # Having the button parent be 'self.share', 'self.master',
        #   or nothing will put the button in the app top window.
        #   Having the parent be 'self' puts it in the GuiViewer Frame.
        self.button1 = tk.Button()

        # For tidiness, put additional __init__ work into methods.
        self.app_menus()
        self.configure_widgets()
        self.grid_widgets()

    def app_menus(self):
        """
        Add pull-down menus to the app window.
        """
        self.master.config(menu=self.menubar)
        file = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file)
        file.add_command(label="Exit", command=self.share.destroy)

    def configure_widgets(self):
        """
        Configure main window, Frame, buttons, and labels, and set
        control variables.
        """
        # Configure weight of enclosing app window columns and rows
        #   to pin resizing of the Frame (self) to app window resizing.
        # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/root-resize.html
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        for i in range(3):
            self.columnconfigure(i, weight=1)
            self.rowconfigure(i, weight=1)

        # Color in the app window and GuiViewer Frame to see what is where.
        self.master.config(bg=self.app_bg)  # Same as self.share.config(...).
        self.configure(bg=self.viewer_bg, relief='groove', bd=4)

        # Labels are not colored in to show exactly where they are:
        self.entry_header.configure(text='Enter # to double:')
        self.entry_number.configure(textvariable=self.share.tkdata['entry'],
                                    width=4)

        self.result_header.configure(text='Result:')
        # Note that with no kw width configured for result_show,
        #   the width will expand to the value length and column and window
        #   widths will expand accordingly. Use kw width for a fixed length.
        self.result_show.configure(textvariable=self.share.tkdata['result'])

        # On macOS, may need to use ttk.Button and kw active** may not work.
        self.button1.configure(text="Run DataModeler",
                               command=self.share.doubleit,
                               # kw active** means mouseover the button.
                               activebackground=self.app_bg,
                               activeforeground=self.viewer_bg,
                               )

        # Set default values of control variables.
        self.share.tkdata['result'].set(0)
        self.share.tkdata['entry'].set(4)

    def grid_widgets(self) -> None:
        """
        Grid Viewer Frame and all widgets.
        """

        # Position the inner GuiViewer frame in the app window;
        #   padding is with respect to the app window and displays a
        #   border around the GuiViewer frame.
        #   Sticky allows frame resizing with window resizing.
        # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/root-resize.html
        self.grid(column=0, row=0, padx=5, pady=5, sticky=tk.NSEW)

        # Position widgets within the internal frame. Sorted by row number.
        self.button1.grid(
            column=2, row=0, padx=(0, 5), pady=0, sticky=tk.W)
        self.entry_header.grid(
            column=0, row=1, padx=5, pady=5, sticky=tk.E)
        self.entry_number.grid(
            column=1, row=1, padx=5, pady=5, sticky=tk.W)
        self.result_header.grid(
            column=0, row=2, padx=5, pady=5, sticky=tk.E)
        self.result_show.grid(
            column=1, row=2, padx=5, pady=5, sticky=tk.W)


class AppController(tk.Tk):
    """
    The controller through which the viewer and the modeler interact.
    """

    def __init__(self):
        super().__init__()
        # From https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/root-resize.html
        self.winfo_toplevel()
        GuiViewer(share=self)
        # NOTE: Instead of self.winfo_toplevel(), can use tk.Frame().grid().
        # It creates a tkinter.Frame object as the first child widget, but
        #   it makes no difference to function or layout.
        # Using winfo_toplevel() first creates the __main__.CountViewer child,
        #   without any enclosing Frame.
        # In neither case is it necessary to name the child as a master
        #   parameter to call CountViewer() b/c self.master is implicit.

    def doubleit(self) -> None:
        """
        Called from the viewer and sends results from modeler back to
        viewer.
        """
        DataModeler(share=self).double_it()


if __name__ == "__main__":
    app = AppController()
    app.title("MVC App")
    app.minsize(320, 85) # Adjust size to make a nice fit of all widgets.
    app.mainloop()
