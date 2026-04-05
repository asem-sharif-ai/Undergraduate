import numpy as np

def get_permutations(string):
    from itertools import permutations
    _permutations = [L]
    for i in range(1, len(string) + 1):
        _permutations.extend([''.join(p) for p in permutations(string, i)])
    return _permutations

def extension(file_path: str):
    return file_path.split('.')[-1].upper()

def clean(str):
    str = ''.join(char for char in str if char.isalpha() or char.isspace())
    return str.lower().strip()

def fill_operation_name(text, options):
    matches = []
    for element in options:
        if element.startswith(text):
            matches.append(element)
    return matches

def eval_expression(expression_string, x):
    expression_string = ''.join(char for char in expression_string.upper() if char in EXPRESSION_STATEMENT)
    expression_string = expression_string.split('X')
    expression_string[1:] = [expression_string[1][0], expression_string[1][1:]]

    a = float(expression_string[0])
    b = float(expression_string[2])
    operator = expression_string[1]

    if len(expression_string) != 3 or a > 255 or b > 255: raise

    if operator == '+':
        return int(np.clip(np.clip(a*x, 0, 255) + b, 0, 255))
    elif operator == '-':
        return int(np.clip(np.clip(a*x, 0, 255) - b, 0, 255))
    elif operator == '*':
        return int(np.clip(np.clip(a*x, 0, 255) * b, 0, 255))
    elif operator == '/':
        return int(np.clip(np.clip(a*x, 0, 255) / b, 0, 255))
    else: raise 

def is_expression(expression_string, x=0):
    if expression_string.startswith('e(') and expression_string.endswith(')'):
        try:
            eval_expression(expression_string, x)
        except:
            return False
        else:
            return True
    else:
        return False

EXPRESSION_STATEMENT = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'X', '+', '-', '*', '/', '.']

IMG_MODES = ['RGB', 'L']
RGB = 'RGB'
RGBA = 'RGBA'
L = 'L'
A = 'a'
APP_TITLE = 'Digital Image Processing Project'
APP_GEOMETRY = f'{1000}x{750}'
APP_LABEL = 'DIP Project'

APP_MODE = 'System'
CLR_MODE = 'dark-blue'

KEY_RELEASE = '<KeyRelease>'

READ_ONLY = 'readonly'
NSEW = 'nsew'
BOTH = 'both'
ALL = 'all'
OK = 'ok'
NO = 'no'
ON = 'on'
OFF = 'off'
SET = 'set'
NRM = 'normal'
DIS = 'disabled'
MSG = 'message'
ERR = 'error'
TXT = 'text'

U8 = 'uint8'
CONST = 'constant'

POINT_OPERATION = 'Point Operations'
POINT_OPERATION_ADV = 'Point Operations Advanced'
SIMPLE = 'Simple'
ADVANCED = 'Advanced'

ADD = 'add'
SUBTRACT = 'subtract'
DIVIDE = 'divide'
MULTIPLY = 'multiply'
COMPLEMENT = 'complement'
SOLARIZE_D = 'solarize dark'
SOLARIZE_L = 'solarize light'
ELIMINATE = 'eliminate'
SWAP = 'swap'
AVERAGE = 'average'
MIN = 'min'
MAX = 'max'
MATCH = 'match'

CHN = 'channel'
FAC = 'factor'
OPR = 'operation'

FLT = 'filter'
INF = 'info (size type)'

NULL_ENTRY = [None, '']
CHANNELS_LIST = get_permutations(RGB)

POINT_OPERATIONS_LIST = [ADD, SUBTRACT, DIVIDE, MULTIPLY, COMPLEMENT, SOLARIZE_D, SOLARIZE_L, ELIMINATE, SWAP]
ADVANCED_POINT_OPERATIONS_LIST = [ADD, SUBTRACT, DIVIDE, MULTIPLY, AVERAGE, MIN, MAX, MATCH]

MEAN = 'mean'
MEDIAN = 'median'
MODE = 'mode'
RANGE = 'range'
RANK = 'rank'
SUM = 'sum'
STD = 'std'
STD_ = 'standard deviation'

OUTLIER = 'outlier'

NEIGHBORHOOD_OPERATION = 'Neighborhood Operations'
NEIGHBORHOOD_OPERATIONS_LIST = [MEAN, AVERAGE, MEDIAN, MODE, RANGE, MIN, MAX, SUM, STD, STD_]
PASS_FILTERS = ['LPF', 'HPF', 'CUSTOM']


THRESHOLDS = ['auto', 'otsu']
THRESHOLDING_OPTIONS_LIST = ['Global Single', 'Global Double'  , 'Global N-Layer' ,
                             'Local Mean'   , 'Local Median'   , 'Local Average'  ] # Local == Adaptive

EDGE_DETECTION = 'Edge Detection'
EDGE_FILTERS = ['Laplacian', 'Gradient', 'Roberts', 'Prewitt', 'Sobel']

EDGE_FILTERS_LIST_TITLE = 'Algorithms'
THRESHOLDING_LIST_TITLE = 'Modes'

THRESHOLDING = 'Thresholding'
THRESHOLDING_TAB = 'Thresholding'


LPF = np.array([[1, 2, 1],
                [2, 4, 2],
                [1, 2, 1]])

HPF = np.array([[-1, -1, -1],
                [-1,  8, -1],
                [-1, -1, -1]])

SOBEL_X = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]])

SOBEL_Y = np.array([[-1, -2, -1],
                    [ 0,  0,  0],
                    [ 1,  2,  1]])

PREWITT_X = np.array([[-1, 0, 1],
                      [-1, 0, 1],
                      [-1, 0, 1]])

PREWITT_Y = np.array([[-1, -1, -1],
                      [ 0,  0,  0],
                      [ 1,  1,  1]])

ROBERTS_X = np.array([[-1, 0],
                      [ 0, 1]])

ROBERTS_Y = np.array([[0, -1],
                      [1,  0]])

LAPLACIAN = np.array([[ 0, -1,  0],
                      [-1,  4, -1],
                      [ 0, -1,  0]])

KERNELS = {
    MEAN: np.mean,
    AVERAGE: np.mean,
    MEDIAN: np.median,
    RANGE: np.ptp,
    SUM: np.sum,
    MIN: np.min,
    MAX: np.max,
    STD: np.std,
    STD_: np.std,
}

MORPHOLOGY = 'Mathmatical Morphology'

DILATION = 'Dilation'
EROSION = 'Erosion'
OPENING = 'Opening'
CLOSING = 'Closing'
IN_BOUNDRY = 'Internal Boundry'
EX_BOUNDRY = 'External Boundry'
MORPH_GRADIENT = 'Morphological Gradient'
FILL_HOLES = 'Fill Holes'

MORPHOLOGY_LIST = [DILATION,
                   EROSION,
                   OPENING,
                   CLOSING,
                   IN_BOUNDRY,
                   EX_BOUNDRY,
                   MORPH_GRADIENT,
                   FILL_HOLES]

MORPHOLOGY_LIST_TITLE = 'Methods'

QUOTATION_MARKS = '"' + "'" + ' '
SLASH = '/'
BACK_SLASH = '\\'
ROTATE_VALUES = ['90', '180', '270', 'None']
TRANSFORM_AXIS_VALUES = ['X', 'Y', 'XY', 'None']
APPEARANCE_MODES = ['    System    ', '    Light    ', '    Dark    ']
SETTINGS_TAB = '     Settings     '
TOOLS_TAB = '     Tools     '

LOADING_BAR = 'indeterminnate'

DEFAULT_EXPORT_TYPE = '.png'

IMPORT_FILE_TYPES = [('Image files', '*.jpg *.jpeg *.png')]
EXPORT_FILE_TYPES = [('PNG files', '*.png'), ('JPG files', '*.jpg')]
EXPORT_FILE_EXTENTIONS = ['PNG', 'JPG', 'JPEG']

CANVAS_CLR = {'Dark'  : 'gray10',
              'Light' : 'gray95', 
              'System': 'gray10'
}

BINARY_DIALOG_TXT = 'Enter a Thereshold:'
BINARY_DIALOG_TITLE = 'Binary Conversion Thereshold'

BORDER_WIDTH = 3
WAIT_TIME = 3

DEFAULT_VALUES = {
    'Rotate'         : 0,
    'Transform Axis' : 'None',
    'Zoom'           : 0,
    'Brightness'     : 1,
    'Saturation'     : 1,
    'Contrast'       : 1,
    'Blur'           : 0,
    'Resolution'     : 1,
    
    'Noise'          : 0,
    'histogram operation'      : 'None',
    'Thresholding'             : 'None',
    'Edge Detection'           : 'None',

}

TRANSFORM_AXIS = 'Transform Axis'
ROTATE = 'Rotate'
ZOOM = 'Zoom'
BRIGHTNESS = 'Brightness'
SATURATION = 'Saturation'
CONTRAST = 'Contrast'
NOISE = 'Noise'
BLUR = 'Blur'
GREYSCALE = 'GreyScale'
BINARY = 'Binary'   
GAMMA = 'Gamma'
HISTOGRAM = 'Histogram'
HISTOGRAM_OPERATION = 'histogram operation'
STRETCH = 'Stretch'
EQUALIZE = 'Equalize'
RESOLUTION = 'Resolution'

HISTOGRAM_OPERATIONS = [STRETCH, EQUALIZE]

COLORS = {
    'FG':      ('gray80', 'gray20'),
    'BD':      ('gray60', 'gray30'),
    'MSG_FG':  ('gray75', 'gray25'),
    'TXT':     ('gray30', 'gray80'),
    'DIS_TXT': ('gray40', 'gray60'),
}

RED = 'red'
GRN = 'green'
BLU = ('#3a7ebf', '#1f538d')
BLK = 'black'
WHT = 'white'
GOLDEN = (0.84, 0.69, 0.12)


SCROLLBAR_DEFAULT_COLOR = COLORS['FG']
SCROLLBAR_HOVER_DEFAULT = COLORS['BD']
FRAME_DEFAULT_COLOR = COLORS['FG']

MSG_BOX_FG = COLORS['MSG_FG']
MSG_BOX_BD = COLORS['BD']

ENTRY_FG = COLORS['FG']
ENTRY_BD = COLORS['BD']

TXT_CLR = COLORS['TXT']
TXT_CLR_DIS = COLORS['DIS_TXT']

BTN_FG = ('#3a7ebf', '#1f538d')
BTN_HOVER = ('#325882', '#14375e')

MSG_BANK = {
    ERR: {
        'Import': 'Import Cancelled or Failed.',
        'Invalid Path': 'Invalid or Empty Path, Try Again.',
        'Converted': 'Image Was Converted To $ Mode Due To Unsupported $$ Format.',
        'Histogram': 'Could Not Plot Histogram For Yet Set Image.',
        'Binary Theresold None': 'Binary Theresold Was Not Given, Conversion Cancelled.',
        'Binary Theresold Not Accepted': 'Binary Theresold Must Be An Integer, Between 0 And 255, Conversion Failed.',
        'No Image': 'No Image Was Set, Set An Image Frist.',
        'Undefined': 'Undefined Error Occurred, Task Failed.',
        'Export': 'Export Cancelled or Failed.',
    },

    MSG: {
        'Mode': 'Appearance Mode Switched Successfully.',
        'Valid Path': 'Valid Image Path, Image Is Ready.',
        'Histogram': 'Histogram Plotted Sccessfully.',
        'Binary Done': 'Image Converted To Binary Mode (1-Bit) Base On Thereshold:',
        'Export': 'Export Completed Successfully.',
    },
}