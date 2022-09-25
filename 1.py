import sys
 
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from acrylic import AcrylicLabel
import numpy as np
from PIL import Image
from PyQt5.QtGui import QPixmap,QImage
from PyQt5.QtWidgets import QMainWindow
from scipy.ndimage.filters import gaussian_filter
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QPalette,QColor,QBrush
from PyQt5.QtGui import *

 
app = QApplication(sys.argv)
M=QMainWindow()
w = AcrylicLabel(20, QColor(105, 114, 168, 102))
M.setMinimumSize(QtCore.QSize(800, 400))
p=w.setImage('daily/September16thbg.jpg')
palette = QPalette()
palette.setBrush(QPalette.Background, QBrush(p))  
M.setPalette(palette)
# M.adjustSize()
M.show()
app.exec_()


# app = QApplication(sys.argv)
# M=QMainWindow()
# palette = QPalette()
# palette.setBrush(QPalette.Background, QBrush(QPixmap("daily/September17thbg.jpg")))
# M.setPalette(palette)
# M.show()
# app.exec_()