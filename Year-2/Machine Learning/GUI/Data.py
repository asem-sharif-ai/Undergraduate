
import time
import numpy

def wait():
    time.sleep(3)

# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

APP_MODE = 'System'
CLR_MODE = 'dark-blue'
APP_TITLE = 'Machine Learning Program'


WIDTH  = 'Width'
HEIGHT = 'Height'


CSV_IMPORT_LABEL = 'Select Dataset CSV or EXEL File.'
CSV_EXPORT_LABEL = 'Select A Directory For The Exported Dataset CSV.'
CSV_FILES = [('CSV Files', '*.csv'), ('Excel Files', '*.xls *.xlsx')]


NULL = ''
ETC = '...'


A = 'a'
FILL_X  = X    = 'x'
FILL_Y  = Y    = 'y'
FILL_XY = BOTH = 'both'


STICKY_X  = 'ew'
STICKY_Y  = 'ns'
STICKY_XY = 'nsew'


UP     = 'up'
CENTER = 'center'
BOTTOM = 'bottom'
RIGHT  = 'right'
LEFT   = 'left'


VRT = 'vertical'
HRZ = 'horizontal'

DIS       = 'disabled'
NRM       = 'normal'
READ_ONLY = 'readonly'
MSG       = 'message'
ERR       = 'error'

THEME     = 'alt'
SELECTED  = 'selected'
TREE      = 'Treeview'
TREE_HEAD = 'Treeview.Heading'

ROW  = 'row '
COL  = 'column'
COLS = 'columns'
SHOW =  'show'
HEAD = 'headings'

END = 'end'

WHT = 'white'
BLK = 'black'

RED = 'red'
GRN = 'green'
D_RED = '#8b0000'

TXT_FG = 'gray25'
TXT_BD = 'gray30'

SLV = 'silver'

EVEN = 'even'
ODD = 'odd'

DF_FRAME_BG_1 = '#1a1a1a'
DF_FRAME_BG_2 = '#262626'
DF_FRAME_BG_3 = '#bfbfbf'

FRAME_DEFAULT_COLOR = '#212121'
BD_CLR = '#565B5E'
BD_WDH = 3

SCROLLBAR_DEFAULT_COLOR = FRAME_DEFAULT_COLOR
SCROLLBAR_HOVER_DEFAULT = ('gray60', 'gray30')

MENU_FG  = '#343638'
MENU_BTN = '#565B5E'
MENU_HVR = '#7A848D'
MENU_BTN_HVR = '#7A848D'

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

DTYPES = {
    'float': float,
    'int': int,
    'str': str,
    'bool': bool,
    'complex': complex,
    'list': list,
    'tuple': tuple,
    'dict': dict,
    'set': set,
    'frozenset': frozenset,
    'bytes': bytes,
    'bytearray': bytearray,
    'memoryview': memoryview,
    'NoneType': type(None),
}


EXCLUDE = 'Exclude'

ROWS    = 'Rows'
COLUMNS = 'Columns'

IMPUTE   = 'Impute'
DROP_COL = 'Drop Column'
DROP_ROW = 'Drop Row'

DROP_VAL = 'Drop Where Value'

DROP_NA     = 'Drop NA'
FILL_NA     = 'Fill NA'
REPLACE_VAL = 'Replace'

RESOLVE_IMBALANCE  = 'Resolve Imbalance'
SELECT_FEATURES    = 'Select Features'
ANALYSE_COMPONENTS = 'Analyse Components'

SUB_MODEL  = 'Sub Model'
SUB_MODELS = ['Decision Tree',
              'Random Forest',
              'Neural Network',
              'Logistic Regression',
              'Support Vector Machine',
              'K-Neighbors']

BALANCING_METHODS = ['Oversampling - SMOTE',
                     'Oversampling - ADASYN',
                     'Oversampling - SMOTEN',
                     'Oversampling - SMOTENC',
                     'Oversampling - Random',
                     'Undersampling - NearMiss',
                     'Undersampling - Random']

TRAIN = 'Train'
TEST  = 'Test'

NAN = 'NaN'

MEAN   = 'Mean'
MEDIAN = 'Median'
MOST_FREQUENT = 'Most Frequent'
F_FILL = 'Forward'
B_FILL = 'Backward'
FILL_NA_OPTIONS = [F_FILL, B_FILL, MEAN, MEDIAN, MOST_FREQUENT]

IMPUTING_OPTIONS = [MEAN, MEDIAN, MOST_FREQUENT]

ENCODE   = 'Encode'
ENCODER  = 'Encoder'
ENCODERS = ['Label', 'One Hot']

SCALE   = 'Scale'
SCALER  = 'Scaler'
SCALERS = ['Standard', 'Min Max']

LABEL = 'Label ' #! KEEP THIS SPACE


HOW      = 'How'
AXIS     = 'Axis'
METHOD   = 'Method'
STRATEGY = 'Strategy'

RND        = 1048576
INDEX      = 'Index'
TREE_INDEX = 'Tree Index'

DATASET = 'Dataset'
BALANCE = 'Resolve Imbalance'

AXIS_OPTIONS = ['0', '1']
HOW_OPTIONS  = ['All', 'Any']

SPLITTER         = 'Splitter'
SPLITTER_OPTIONS = ['Best', 'Random']

CRITERION      = 'Criterion'
CLS_CRITERIONS = ['Gini', 'Entropy', 'Log Loss']
REG_CRITERIONS = ['Absolute Error', 'Squared Error', 'Friedman MSE', 'Poisson']

DATA_SPLIT_METHOD  = 'Data Split Method'
DATA_SPLIT_METHODS = ['Holdout', 'K-Fold']

KERNEL = 'Kernel'
DECISION_FUNCTION = 'Decision Function'

SVM_KERNELS = ['Linear', 'Poly', 'RBF', 'Sigmoid', 'Precomputed']
DECISION_FUNCTIONS = ['OVO', 'OVR']

PLOT_AXIS = 'Plot Axis'

ACTIVATION = 'Activation'
ACTIVATIONS = ['Identity', 'Logistic', 'Tanh', 'ReLU']

SOLVER = 'Solver'
SOLVERS = ['LBFGS', 'SGD', 'ADAM']

LEARNING_RATE = 'Learning Rate'
LEARNING_RATES = ['Constant', 'Invscaling', 'Adaptive']


ALGORITHM = 'Algorithm'

K_ALGORITHMS = ['LLOYD', 'ELKAN']
KN_ALGORITHMS = ['Auto', 'Ball Tree', 'KD Tree', 'Brute']

WEIGHT = 'Weight'
KN_WEIGHTS = ['Uniform', 'Distance']

INIT = 'Init'
K_INITS = ['K-Means++', 'Random']

N_INIT = 'N Init'

LABEL_NAMES = ['Cluster', 'Label', 'Class', '']

# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

PRE_PREPROCESSING  = '     Pre-Preprocessing     '

IMPUTING           = '   Imputing   '
BALANCING          = '     Balancing     '
ENCODING           = '     Encoding     '
SCALING            = '     Scaling     '
DROPPING           = '   Dropping   '
FEATURE_SELECTION  = '     Feature Selection     '


SUPERVISED     = '     Supervised     '
UNSUPERVISED   = '     UnSupervised     '

REGRESSION     = '     Regression     '
CLASSIFICATION = '     Classification     '

DECISION_TREE  = '     Decision Tree     '
RANDOM_FOREST  = '     Random Forest     '
SVM            = '   Support Vector Machine   '
ANN            = '   Artificial Neural Network   '
KNN            = '     k-Nearest Neighbors     '

K_MEANS      = '     K-Means     '

SUPERVISED_TABS = [DECISION_TREE,
                   RANDOM_FOREST,
                   SVM,
                   ANN,
                   KNN]

UNSUPERVISED_TABS = [K_MEANS]

# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

LOG_TAB  = '     Help / Log     '
PLOT_TAB = '     Visualizations     '

MAIN_MENU_TABS = [PRE_PREPROCESSING,
                  SUPERVISED,
                  UNSUPERVISED,
                #   PLOT_TAB,
                  LOG_TAB]


# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
TERMINL = 'Terminal'
FONTS = {
    'Font': ('Segoe UI', 10),
    'Bold': ('Segoe UI', 10, 'bold'),
    'Bold +': ('Segoe UI', 15, 'bold'),
    PRE_PREPROCESSING: ('Arial', 14),
    TERMINL: ('Courier', 15)
}

CONFUSION_MATRIX = '''
┌─────────────────────────────────────────────────────────┐
│               P   R   E   D   I   C   T   E   D         |
│     ┌─────────────────────────┬─────────────────────────┤
│     |                         |                         |
│  A  | TN | True Negative:     | FP | False Positive:    |
│     |                         |                         |
│  C  | Actual Class    [0]     | Actual Class    [0]     |
│     | Predicted Class [0]     | Predicted Class [1]     |
│  T  |                         |                         |
│     ├─────────────────────────┼─────────────────────────┤
│  U  |                         |                         |
│     | FN | False Negative:    | TP | True Positive:     |
│  A  |                         |                         |
│     | Actual Class    [1]     | Actual Class    [1]     |
│  L  | Predicted Class [0]     | Predicted Class [1]     |
│     |                         |                         |
└─────┴─────────────────────────┴─────────────────────────┘
'''

GUIDE_MESSAGE = '''
'''
