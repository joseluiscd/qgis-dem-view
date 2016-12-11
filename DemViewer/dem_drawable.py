#The future is a great place!! But Python3 has been out there for a while...
from __future__ import division

from OpenGL import GL
from qgis.core import *
import numpy

def normalize(n):
    lens = numpy.sqrt(n[:,0]**2 + n[:,1]**2 + n[:,2]**2 )
    n[:,0] /= lens
    n[:,1] /= lens
    n[:,2] /= lens

    return n

class DemDrawable:
    def __init__(self, heightData, colorData, divisions):
        self.divisions = divisions

        self.heightData = heightData
        self.extent = heightData.extent()

        self.buildMesh()

    def buildMesh(self):
        vertices = []
        indices = []

        w = self.divisions
        h = self.divisions
        quad = 0
        for x in range(w-1):
            for y in range(h-1):
                print("Punto:",(x,y))
                z1 = self.getValue(x/w, y/h)
                z2 = self.getValue((x+1)/w, y/h)
                z3 = self.getValue(x/w, (y+1)/h)
                z4 = self.getValue((x+1)/w, (y+1)/h)

                v1 = (x/w, z1, y/h)
                v2 = ((x+1)/w, z2, y/h)
                v3 = (x/w, z3, (y+1)/h)
                v4 = ((x+1)/w, z4, (y+1)/h)

                vertices.append(v1)
                vertices.append(v2)
                vertices.append(v3)
                vertices.append(v4)

                indices.append((quad+1, quad+0, quad+2))
                indices.append((quad+1, quad+2, quad+3))

                quad += 4

        vertices = numpy.array(vertices)
        indices = numpy.array(indices)
        normals = numpy.zeros(vertices.shape, dtype=vertices.dtype)
        print(indices)
        tris = vertices[indices]

        n = numpy.cross(tris[::,1]-tris[::,0], tris[::,2]-tris[::,0])

        n = normalize(n)

        normals[indices[:,0]] += n
        normals[indices[:,1]] += n
        normals[indices[:,2]] += n

        self.vertices = vertices[indices]
        self.normals = normalize(normals[indices])



    def getValue(self, x, y):
        """
        x and y between 0 and 1
        """

        realX = self.extent.xMinimum() + (x*(self.extent.xMaximum()-self.extent.xMinimum()))
        realY = self.extent.yMinimum() + (y*(self.extent.yMaximum()-self.extent.yMinimum()))

        print((realX, realY))
        val = self.heightData.identify(QgsPoint(realX, realY), QgsRaster.IdentifyFormatValue)
        if val.isValid():
            print(val.results())
            return val.results()[1]

    def draw(self):
        GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_AMBIENT, (0.1,0.1,0.1,1))
        GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_DIFFUSE, (1,1,1,1))
        GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_SPECULAR, (0.6,0.6,0.6,1))
        GL.glMaterialf(GL.GL_FRONT_AND_BACK, GL.GL_SHININESS, 20)
        GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_EMISSION, (0,0,0,0));


        GL.glEnableClientState(GL.GL_VERTEX_ARRAY)
        GL.glEnableClientState(GL.GL_NORMAL_ARRAY)
        GL.glVertexPointer(3, GL.GL_FLOAT, 0, self.vertices)
        GL.glNormalPointer(GL.GL_FLOAT, 0, self.normals)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(self.vertices)*3)
