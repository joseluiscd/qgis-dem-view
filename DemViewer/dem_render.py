import PyQt4
from PyQt4 import QtGui, QtOpenGL

from OpenGL import GL, GLU

class DemRenderer(QtOpenGL.QGLWidget):
    def __init__(self, dem, parent=None):
        super(QtOpenGL.QGLWidget, self).__init__(parent)
        self.dem = dem

    def initializeGL(self):
        GL.glClearColor(0.1,0.1,0.1,1)
        GL.glShadeModel(GL.GL_FLAT)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_AUTO_NORMALS)
        GL.glEnable(GL.GL_NORMALIZE)
        GL.glEnable(GL.GL_LIGHTING)



    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return

        GL.glViewport((width - side) / 2, (height - side) / 2, side, side)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        #GL.glOrtho(-1, +1, +1, -1, 0.1, 15.0)
        GLU.gluPerspective(40, 1, 0.1, 15)
        GL.glMatrixMode(GL.GL_MODELVIEW)

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glLoadIdentity()
        GLU.gluLookAt(2,2,2,0,0,0,0,1,0)

        self.dem.draw()


class DemViewerWindow(QtGui.QWidget):
    def __init__(self, dem, parent=None):
        super(QtGui.QWidget, self).__init__(parent)
        self.renderer = DemRenderer(dem, self)

        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addWidget(self.renderer)

        self.setLayout(mainLayout)
        self.setWindowTitle("DEM viewer")
