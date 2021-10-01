# tkinter_utilities
## tk-color-helper.py
A utility to help choose colors in tkinter GUIs and display their simulated colorblind colors.
Draws a tkinter table of most named colors from X11 rgb.txt; those not recognized by tkinter are excluded.
Use command line options to simulate colors as perceived by various colorblind conditions,
or the grayscale equivalents, of each named color. 

Click on a color to get its RGB value and tkinter-ready hex code. Values can be cut and pasted with standard keyboard commands.
```
$ ./tk-color-helper.py --help
usage: tk-color-helper.py [-h] [--about] [--d] [--p] [--t] [--gray]

optional arguments:
  -h, --help      show this help message and exit
  --about         Provide description, version, GNU license
  --d             Generate deuteranopia simulated colors
  --p             Generate protanopia simulated colors
  --t             Generate tritanopia simulated colors
  --gray, --grey  Generate grayscale equivalents of named colors
```
Run as `./tk-color-helper.py`
![named-colors](images/tkinter_colors.png)

Run as `$ ./tk-color-helper.py --d`
![deuteranopeia-simulated-colors](images/deuteranopia_sim.png)

Run as `$ ./tk-color-helper.py --p`
![protanopia-simulated-colors](images/protanopia_sim.png)

Run as `$ ./tk-color-helper.py --t`
![tritanopia-simulated-colors](images/tritanopia_sim.png)

Run as `$ ./tk-color-helper.py --gray`
![grayscale-tk-colors](images/grayscale.png)
