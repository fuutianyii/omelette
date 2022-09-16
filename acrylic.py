# coding:utf-8
import numpy as np
from PIL import Image
from PyQt5.QtGui import QPixmap,QImage
from PyQt5.QtWidgets import QMainWindow
from scipy.ndimage.filters import gaussian_filter
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QPalette,QColor,QBrush
from PyQt5.QtGui import *


 


def gaussianBlur(imagePath: str, blurRadius=18, brightFactor=1, blurPicSize: tuple = None) -> np.ndarray:
    """ 对图片进行高斯模糊处理

    Parameters
    ----------
    imagePath: str
        图片路径

    blurRadius: int
        模糊半径

    brightFactor：float
        亮度缩放因子

    blurPicSize: tuple
        高斯模糊前将图片缩放到指定大小，可以加快模糊速度

    Returns
    -------
    image: `~np.ndarray` of shape `(w, h, c)`
        高斯模糊后的图像
    """
    if not imagePath.startswith(':'):
        image = Image.open(imagePath)
    else:
        image = Image.fromqpixmap(QPixmap(imagePath))

    if blurPicSize:
        # 调整图片尺寸，减小计算量，还能增加额外的模糊
        w, h = image.size
        ratio = min(blurPicSize[0] / w, blurPicSize[1] / h)
        w_, h_ = w * ratio, h * ratio

        if w_ < w:
            image = image.resize((int(w_), int(h_)), Image.ANTIALIAS)

    image = np.array(image)

    # 处理图像是灰度图的情况
    if len(image.shape) == 2:
        image = np.stack([image, image, image], axis=-1)

    # 对每一个颜色通道分别磨砂
    for i in range(3):
        image[:, :, i] = gaussian_filter(
            image[:, :, i], blurRadius) * brightFactor

    return image


class AcrylicTextureLabel(QMainWindow):
    """ 亚克力纹理标签 """

    def __init__(self, tintColor: QColor, luminosityColor: QColor, noiseOpacity=0.03, parent=None):
        """
        Parameters
        ----------
        tintColor: QColor
            RGB 主色调

        luminosityColor: QColor
            亮度层颜色

        noiseOpacity: float
            噪声层透明度

        parent:
            父级窗口
        """
        super().__init__(parent=parent)
        self.tintColor = QColor(tintColor)
        self.luminosityColor = QColor(luminosityColor)
        self.noiseOpacity = noiseOpacity
        self.noiseImage = QImage('resource/noise.png')
        self.setAttribute(Qt.WA_TranslucentBackground)

    def setTintColor(self, color: QColor):
        """ 设置主色调 """
        self.tintColor = color
        self.update()

    def paintEvent(self, e):
        """ 绘制亚克力纹理 """
        acrylicTexture = QImage(64, 64, QImage.Format_ARGB32_Premultiplied)

        # 绘制亮度层
        acrylicTexture.fill(self.luminosityColor)

        # 绘制主色调
        painter = QPainter(acrylicTexture)
        painter.fillRect(acrylicTexture.rect(), self.tintColor)

        # 绘制噪声
        painter.setOpacity(self.noiseOpacity)
        painter.drawImage(acrylicTexture.rect(), self.noiseImage)

        acrylicBrush = QBrush(acrylicTexture)
        painter = QPainter(self)
        painter.fillRect(self.rect(), acrylicBrush)

class AcrylicLabel(QMainWindow):
    """ 亚克力标签 """

    def __init__(self, blurRadius: int, tintColor: QColor, luminosityColor=QColor(255, 255, 255, 0),
                maxBlurSize: tuple = None, parent=None):

        """
        Parameters
        ----------
        blurRadius: int
            磨砂半径

        tintColor: QColor
            主色调

        luminosityColor: QColor
            亮度层颜色

        maxBlurSize: tuple
            最大磨砂尺寸，越小磨砂速度越快

        parent:
            父级窗口
        """
        super().__init__(parent=parent)
        self.imagePath = ''
        self.blurPixmap = QPixmap()
        self.blurRadius = blurRadius
        self.maxBlurSize = maxBlurSize
        self.acrylicTextureLabel = AcrylicTextureLabel(
            tintColor, luminosityColor, parent=self)

    def setImage(self, imagePath: str):
        """ 设置图片 """
        if imagePath == self.imagePath:
            return

        self.imagePath = imagePath
        image = Image.fromarray(gaussianBlur(
            imagePath, self.blurRadius, 0.85, self.maxBlurSize))
        self.blurPixmap = image.toqpixmap()  # type:QPixmap
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(self.blurPixmap))  
        self.setPalette(palette)
        self.adjustSize()
        return self.blurPixmap

    def setTintColor(self, color: QColor):
        """ 设置主色调 """
        self.acrylicTextureLabel.setTintColor(color)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.acrylicTextureLabel.resize(self.size())
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(self.blurPixmap.scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)))  
        self.setPalette(palette)

