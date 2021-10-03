# tkinter_utilities
## tk-color-helper.py
A utility to help choose colors in tkinter GUIs and display their simulated colorblind colors.
Draws a table using color names from X11 rgb.txt; names not recognized by tkinter are excluded.
Use command line options to simulate those colors as might be perceived by people having different types of colorblindness, including grayscale equivalents. 

Click on a color to bring up its tkinter-ready hex code and RGB value. Values can be cut and pasted with standard keyboard and mouse commands. Right-click on a different color to change font color; this can aid in choosing effective color combinations.
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
Example usage: Click on khaki, then right-click on VioletRed4 to change foreground.
![named-colors](images/tkinter_colors.png)

TIP:
Type or paste your own text to replace, or add to, the background color information. (If you remove the color information, don't forget to copy it, so you don't forget that awesome background color.)
![custom_text](images/custom_text.png)

Run as `$ ./tk-color-helper.py --d`
![deuteranopeia-simulated-colors](images/deuteranopia_sim.png)

Run as `$ ./tk-color-helper.py --p`
![protanopia-simulated-colors](images/protanopia_sim.png)

Run as `$ ./tk-color-helper.py --t`
![tritanopia-simulated-colors](images/tritanopia_sim.png)

Run as `$ ./tk-color-helper.py --gray`
![grayscale-tk-colors](images/grayscale_sim.png)

