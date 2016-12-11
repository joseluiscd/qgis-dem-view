import PyQt4
from PyQt4 import QtCore, QtGui, QtOpenGL

from OpenGL import GL, GLU

class DemRenderer(QtOpenGL.QGLWidget):
    def __init__(self, dem, parent=None):
        super(QtOpenGL.QGLWidget, self).__init__(parent)
        self.dem = dem

        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

        self.lastPos = QtCore.QPoint()

    def initializeGL(self):
        GL.glClearColor(0.8,0.8,1,1)
        GL.glShadeModel(GL.GL_SMOOTH)

        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_AUTO_NORMAL)
        GL.glEnable(GL.GL_NORMALIZE)
        GL.glEnable(GL.GL_LIGHTING)
        GL.glEnable(GL.GL_CULL_FACE)

        GL.glEnable(GL.GL_LIGHT0)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_AMBIENT, (0.2, 0.2, 0.2, 1))
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, (0.5, 0.5, 0.5, 1))
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_SPECULAR, (0.3, 0.3, 0.3, 1))
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, (-3, 3, -3, 1))




    def resizeGL(self, width, height):
        side = min(width, height)
        if side <= 0:
            return

        GL.glViewport(0, 0, width, height)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective(40, width//height, 0.1, 100)
        GL.glMatrixMode(GL.GL_MODELVIEW)

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glLoadIdentity()
        GLU.gluLookAt(2,2,2,0.5,0,0.5,0,1,0)

        GL.glRotate(self.xRot, 1, 0, 0)
        GL.glRotate(self.yRot, 0, 1, 0)
        GL.glRotate(self.zRot, 0, 0, 1)
        GL.glTranslate(-0.5, 0, -0.5)
        GL.glScale(1, 0.001, 1)
        self.dem.draw()

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & QtCore.Qt.LeftButton:
            self.xRot += dy
            self.yRot += dx
        elif event.buttons() & QtCore.Qt.RightButton:
            self.xRot += dy
            self.zRot += dx

        self.lastPos = event.pos()
        self.updateGL()


class DemViewerWindow(QtGui.QWidget):
    def __init__(self, dem, parent=None):
        super(QtGui.QWidget, self).__init__(parent)
        self.renderer = DemRenderer(dem, self)

        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addWidget(self.renderer)

        self.setLayout(mainLayout)
        self.setWindowTitle("DEM viewer")
