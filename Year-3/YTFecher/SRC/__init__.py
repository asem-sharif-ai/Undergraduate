import os, sys, subprocess, socket, ctypes
from pathlib import Path

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from SRC.Tabs import Tabs

from SRC.About import *
from SRC.Style import styleApp, setIcon, window