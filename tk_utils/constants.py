"""
Constants used in main script and in other tk_utils modules.
"""
# Standard library import:
from sys import platform

#  Supported OS platforms: 'win', 'lin', 'dar'.
MY_OS = platform[:3]

# 40 rows (19 columns) provide nice spatial organization for 760 color
#  names; add 2 for info rows at top of the table.
#  Color names are in X11_RGB_NAMES.
MAX_ROWS = 42

# OS-specific font sizes for color names in table.
LABEL_FONT_MAP = {
    'dar': ('SF Pro', 9),  # macOS
    'lin': ('DejaVu Sans', 6),  # Linux (Ubuntu)
    'win': ('Segoe UI', 8)  # Windows (10, 11)
}

# Defaults to generic font if OS is not recognized
LABEL_FONT = LABEL_FONT_MAP.get(MY_OS, ('Arial', 10))

INFO_FONT_MAP = {
    'dar': ('SF Pro', 12),  # macOS
    'lin': ('DejaVu Sans', 10),  # Linux (Ubuntu)
    'win': ('Segoe UI', 10)  # Windows (10, 11)
}
INFO_FONT = INFO_FONT_MAP.get(MY_OS, ('Arial', 12))

# X11_RGB_NAMES: 760 color names from the intersection of the rbg.txt files in
#   Linux /usr/share/X11/rgb.txt and macOS /opt/X11/share/X11/rgb.txt.
#   Names containing 'X11' and 'Debian' were removed, as well as a few others.
#   The retained names are valid for tkinter 8.6 on Linux, macOS, and Windows.
# NOTE: Many Tcl/Tk color names from https://www.tcl.tk/man/tcl8.4/TkCmd/colors.html
#   are invalid in tkinter 8.6.
# 760 name Labels fit precisely into a 19 x 40 table.
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
                 'powder blue', 'PowderBlue', 'turquoise', 'pale turquoise', 'PaleTurquoise',
                 'dark turquoise', 'DarkTurquoise', 'medium turquoise', 'MediumTurquoise',
                 'cyan', 'aqua', 'light cyan', 'LightCyan', 'dark cyan', 'DarkCyan',
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
                 'khaki', 'dark khaki', 'DarkKhaki', 'pale goldenrod', 'PaleGoldenrod',
                 'light goldenrod', 'LightGoldenrod', 'light goldenrod yellow',
                 'LightGoldenrodYellow', 'beige', 'light yellow', 'LightYellow', 'yellow',
                 'gold', 'goldenrod', 'dark goldenrod', 'DarkGoldenrod', 'rosy brown',
                 'RosyBrown', 'indian red', 'IndianRed', 'saddle brown', 'SaddleBrown',
                 'sienna', 'peru', 'burlywood', 'wheat', 'sandy brown', 'SandyBrown',
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
