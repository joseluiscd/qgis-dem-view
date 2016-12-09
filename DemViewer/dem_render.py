import PyQt4
from PyQt4 import QtGui, QtOpenGL

from OpenGL.GL import *
from OpenGL.GLU import *

class DemRenderer(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        super(QtOpenGL.QGLWidget, self).__init__(parent)

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)
        glMatrixMode(GL_PROJECTION)

        glLoadIdentity()
        gluPerspective(40.0, 1.0, 1.0, 30.0)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

class DemViewerWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(QtGui.QWidget, self).__init__(parent)
        self.renderer = DemRenderer(self)

        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addWidget(self.renderer)


        self.setLayout(mainLayout)
        self.setWindowTitle("DEM viewer")
