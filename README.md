# tkinter_utilities
## tk-color-helper.py

A Python utility to help choose colors and their colorblind equivalents
in tkinter GUIs. Draws an interactive tkinter table of 760 named colors
included in X11 rgb.txt. 
   Program usage: Click on a color name to show its hex code and RGB
value showing that color as background. Right-click a different color to
change the text foreground. Foreground colors can be changed for a given
background color, but selecting a new background will reset the
foreground to its default value. Click with a modifier key to show a
colorblind simulation of the selected color: Shift (deuteranopia), 
Ctrl (protanopia), Alt (tritanopia), Shift-Ctrl (grayscale).
Simulated color hex codes and RGB values may not correspond to any named
tkinter color, but the hex string will be recognized by tkinter. Hex and
RGB values can also be used in other graphics applications.
    Using the Ctrl or Command (macOS) key in combination with a key
'd', 'p', 't', or 'g' will pop-up simulations of the full color table 
(non-interactive) for, respectively, deuteranopia, protanopia, 
tritanopia, or grayscale.
    Text in the color display and data fields can be cut, pasted, or
edited with standard keyboard and click commands. Runs with Python 3.6 
and tkinter 8.6 or later in Linux, Windows, and MacOS systems.
```
$ ./tk-color-helper.py --help
usage: tk-color-helper.py [-h] [--about]

optional arguments:
  -h, --help      show this help message and exit
  --about         Provide description, version, GNU license
```
Run as `./tk-color-helper.py`
Table at startup:
![tkinter-colors](images/full_color_start.png)

Example usage: Click on khaki, then right-click on VioletRed4 to change foreground.
![named-colors](images/tkinter_colors.png)

TIP:
Type or paste your own text to replace, or add to, the background color information. (If you remove the color information, don't forget to copy it, so you don't forget that awesome background color.)
![custom_text](images/custom_text.png)

Use Ctrl-D (or Command-D on MacOS), to pop up non-interactive deuteranopia simulation of the color table.
![deuteranopeia-simulated-colors](images/deuteranopia_colortable.png)

Use Ctrl-P (or Command-P on MacOS), to pop up non-interactive protanopia simulation of the color table.
![protanopeia-simulated-colors](images/protanopia_colortable.png)

Use Ctrl-T (or Command-T on MacOS), to pop up non-interactive tritanopia simulation of the color table.
![tritanopia_-simulated-colors](images/tritanopia_colortable.png)

Use Ctrl-G (or Command-G on MacOS), to pop up non-interactive grayscale simulation of the color table.
![grayscale-simulated-colors](images/grayscale_colortable.png)

