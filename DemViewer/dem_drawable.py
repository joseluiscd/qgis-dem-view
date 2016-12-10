from OpenGL import GL

class DemDrawable:
    def __init__(self, heightData, colorData, divisions):
        self.divisions = divisions

        self.heightData = heightData.block(
            0, heightData.extent(), 1, 1
        )

        print(heightData.extent())


        self.buildMesh()

    def buildMesh(self):
        vertices = []

        w = self.divisions
        h = self.divisions
        for x in range(w-1):
            for y in range(h-1):
                z1 = 0#self.heightData.value(y, x)
                z2 = 0#self.heightData.value(y, x+1)
                z3 = 0#self.heightData.value(y+1, x)
                z4 = 0#self.heightData.value(y+1, x+1)

                v1 = (x//w, y//h, z1)
                v2 = (x+1//w, y//h, z2)
                v3 = (x//w, y+1//h, z3)
                v4 = (x+1//w, y+1//h, z4)

                vertices.append(v1)
                vertices.append(v2)
                vertices.append(v3)

                vertices.append(v3)
                vertices.append(v2)
                vertices.append(v4)


        self.vertices = vertices


    def draw(self):
        GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_AMBIENT, (0.1,0.1,0.1))
        GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_DIFFUSE, (0.6,0.6,0.6))

        GL.glBegin(GL.GL_TRIANGLES)
        GL.glColor(1,1,1)
        for v in self.vertices:
            GL.glVertex(*v)
            print(v)
        #GL.glVertex(0, 0, 0)
        #GL.glVertex(1, 0, 0)
        #GL.glVertex(1, 1, 0)

        GL.glEnd()
