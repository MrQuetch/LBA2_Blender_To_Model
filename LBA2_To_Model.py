import os
import bpy
import sys
import math
import time
import random
import struct

from bgl import *

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty,)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup,)


#from bgl import *

os.system('cls')

#objects = []

#names = ["Cube","Cube.001"]

#if (bpy.data.objects["Cube"] is not None):
    #print("%s \n" % (bpy.data.objects["Cube"]))
    #objects.append(bpy.data.objects["Cube"])

#if (bpy.data.objects["Cube.001"] is not None):
#    objects.append(bpy.data.objects["Cube.001"])

#if (bpy.data.objects["Cube" + ".001"] is not None):
    #objects.append(bpy.data.objects["Cube" + ".001"])

#objects = [bpy.data.objects["Cube"],
#           bpy.data.objects["Cube.001"]]

#objects = [names[0],names[1]]
#objects = [bpy.data.objects[names[0]],
#           bpy.data.objects[names[1]]]

#print(bpy.data.objects["Cube.001"].location)
#print(bpy.data.objects["Cube.001"].matrix_world.translation)

# Add a location constraint and set its properties.
#bpy.data.objects["Cube.001"].constraints.new('LIMIT_LOCATION')
#bpy.data.objects["Cube.001"].constraints["Limit Location"].use_min_x = True
#bpy.data.objects["Cube.001"].constraints["Limit Location"].use_max_x = True
#bpy.data.objects["Cube.001"].constraints["Limit Location"].use_transform_limit = True
#bpy.data.objects["Cube.001"].constraints["Limit Location"].owner_space = "LOCAL"
#bpy.data.objects["Cube.001"].constraints["Limit Location"].influence = 0.1

# Add a rotation constraint and set its properties.
#bpy.data.objects["Cube.001"].constraints.new('LIMIT_ROTATION')
#bpy.data.objects["Cube.001"].constraints["Limit Rotation"].use_limit_x = True
#bpy.data.objects["Cube.001"].constraints["Limit Rotation"].use_limit_y = True
#bpy.data.objects["Cube.001"].constraints["Limit Rotation"].use_limit_z = True
#bpy.data.objects["Cube.001"].constraints["Limit Rotation"].use_transform_limit = True
#bpy.data.objects["Cube.001"].constraints["Limit Rotation"].owner_space = "LOCAL"
#bpy.data.objects["Cube.001"].constraints["Limit Rotation"].influence = 0.1

# Similar to above, but does not need to use constraints.
#bpy.data.objects["Cube.2"].lock_location[0] = True
#bpy.data.objects["Cube.2"].lock_location[1] = True
#bpy.data.objects["Cube.2"].lock_location[2] = True

#index = 5
#print(bpy.data.objects["Cube.00" + str(index)].location)

#index = "005"
#print(bpy.data.objects["Cube." + str(index)].location)

#print(bpy.data.objects["Cube.2"].matrix_local.translation)

# Function to draw a line using OpenGL code.
#def draw_line():
    #print("stuff")
    #glColor3f(1.0, 0.0, 0.0)
    #glLineWidth(2.0)
    #glBegin(GL_LINES)
    #glVertex3f(0.0, 0.0, 0.0)
    #glVertex3f(1.0, 1.0, 1.0)
    #glEnd()

# The drawings will only be deleted when Blender is restarted.
#handle = bpy.types.SpaceView3D.draw_handler_add(draw_line, (), 'WINDOW', 'POST_VIEW')
#handle = bpy.types.SpaceView3D.draw_handler_add(draw_line, (), 'WINDOW', 'POST_PIXEL')
#bpy.types.SpaceView3D.draw_handler_remove(handle, 'WINDOW')

#start_time = time.time()

# testing for-loops
#for i in range(0, 50):
    #for j in range(0, 50):
        #for k in range(0, 50):
            #print("i %d j %d k %d" % (i, j, k))

#end_time = time.time()

#print("The script took ", end_time - start_time, " seconds to complete.")



# Change the color of this cube to red.
#bpy.data.objects["Cube.2"].color[0] = 1
#bpy.data.objects["Cube.2"].color[1] = 0
#bpy.data.objects["Cube.2"].color[2] = 0

#print("R: %.2f " % (bpy.data.objects["Cube.2"].color[0]))

#number_index = 0
#string_index = "0"

#for i in range(0, 20):
    #if (bpy.data.objects["Cube." + str(string_index)] is not None):
        #print(bpy.data.objects["Cube." + str(string_index)])
        
        #number_index += 1
        #string_index = str(number_index)


        

#print(objects)

#print(objects[0])
#print(objects[1])

#print(bpy.context.selected_objects)
#print(bpy.context.selected_objects[0].name)
#print(bpy.context.selected_objects[1].name)
#print(bpy.context.selected_objects[2].name)

#if (len(bpy.context.selected_objects) == 3):
#    print("3 objects")
#else:
#    print("oops")

#myOps = ["mesh.primitive_cube_add", "mesh.primitive_uv_sphere_add"]

#increment = [0]


#bpy.data.objects['1'].color = (0.0, 1.0, 0.0, 1.0)
#colors = bpy.data.objects['1'].getData(mesh=True)
#colors.faceUV = True
#for f in bpy.data.objects['1'].faces:
#    f.mode |= Mesh.FaceModes.OBCOL
#bpy.data.objects['1'].update()
#Window.RedrawAll()

# Macros
SCALE           = 100
HEADER          = 0x60
BONES           = 0x20
BONES_OFFSET    = 0x24
VERTICES        = 0x28
VERTICES_OFFSET = 0x2C
NORMALS         = 0x30
NORMALS_OFFSET  = 0x34
UNKNOWNS        = 0x38
UNKNOWNS_OFFSET = 0x3C
POLYGONS        = 0x40
POLYGONS_OFFSET = 0x44
LINES           = 0x48
LINES_OFFSET    = 0x4C
SPHERES         = 0x50
SPHERES_OFFSET  = 0x54
TEXTURES        = 0x58
TEXTURES_OFFSET = 0x5C

bones = [0]
tempBones = [0]

vertices = []
vertices_bones = []

triangles = [-1]
tempTriangles = [-1]

bones_parents = []
bones_vertex = []
bones_vertices = []
bones_types = []

temp_x = []
temp_y = []
temp_z = []

triangles_x = []
triangles_y = []
triangles_z = []

triangles_x1_p = []
triangles_y1_p = []
triangles_z1_p = []

triangles_x2_p = []
triangles_y2_p = []
triangles_z2_p = []

triangles_x3_p = []
triangles_y3_p = []
triangles_z3_p = []

# Populate arrays.
for i in range(0, 530):
    bones_parents.append(0)
    bones_vertex.append(0)
    bones_vertices.append(0)
    bones_types.append(0)
    
    temp_x.append(0)
    temp_y.append(0)
    temp_z.append(0)
    
    triangles_x.append(0)
    triangles_y.append(0)
    triangles_z.append(0)
    
    triangles_x1_p.append(0)
    triangles_y1_p.append(0)
    triangles_z1_p.append(0)
    
    triangles_x2_p.append(0)
    triangles_y2_p.append(0)
    triangles_z2_p.append(0)
    
    triangles_x3_p.append(0)
    triangles_y3_p.append(0)
    triangles_z3_p.append(0)


def drawTriangle(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    glEnable(GL_DEPTH_TEST)
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(x1, y1, z1)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(x2, y2, z2)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(x3, y3, z3)
    glEnd()

def getChildren(myObject):
    children = []
    
    for ob in bpy.data.objects:
        if ob.parent == myObject:
            children.append(ob)
    
    return children

class returnObjects(Operator):
    bl_idname = 'return.objects'
    bl_label = 'Return the objects'
    
    def execute(self, context):
        print(bpy.data.objects)
        print(len(bpy.data.objects))
        self.report({'INFO'}, "There are " + str(len(bpy.data.objects)) + " objects!")
        return {'FINISHED'}

class exportModel(Operator):
    bl_idname = 'export.model'
    bl_label = "Export a model"
    
    def execute(self, context):
        path = 'C:\\Users\\USER\\Desktop\\Parker\\Models\\LowPoly\\testModel18.txt'
        
        outfile = open(path, 'wb')
        
        # Byte Keys
        # A lowercase or uppercase determines the unsigned or signed-ness of a value.
        # ? = 1 Byte
        # b = 1 Byte
        # B = 1 Byte
        # 1B = 1 Byte
        # h = 2 Bytes
        # H = 2 Bytes
        # l = 4 Bytes
        # i = 4 Bytes
        # f = 4 Bytes
        # q = 8 Bytes
        
        # Clear vertex list before exporting.
        # Otherwise, we can only export once.
        vertices.clear()
        
        vertex_index = 0
        vertices.append(bpy.data.objects[str(0)]) # Append first vertex separately.
        
        # Loop through all vertices, check names, and append them.
        #for obj in bpy.data.objects:
        #    if (obj.name == str(vertex_index)):
        #        vertex_index += 1
        #        vertices.append(bpy.data.objects[str(vertex_index)])
        
        # Unfortunately, each vertex must be checked separately.
        # For-loops generated by external C++ program.
        for obj in bpy.data.objects:
            if (obj.name == str(1)):
                vertices.append(bpy.data.objects[str(1)])
        for obj in bpy.data.objects:
            if (obj.name == str(2)):
                vertices.append(bpy.data.objects[str(2)])
        for obj in bpy.data.objects:
            if (obj.name == str(3)):
                vertices.append(bpy.data.objects[str(3)])
        for obj in bpy.data.objects:
            if (obj.name == str(4)):
                vertices.append(bpy.data.objects[str(4)])
        for obj in bpy.data.objects:
            if (obj.name == str(5)):
                vertices.append(bpy.data.objects[str(5)])
        for obj in bpy.data.objects:
            if (obj.name == str(6)):
                vertices.append(bpy.data.objects[str(6)])
        for obj in bpy.data.objects:
            if (obj.name == str(7)):
                vertices.append(bpy.data.objects[str(7)])
        for obj in bpy.data.objects:
            if (obj.name == str(8)):
                vertices.append(bpy.data.objects[str(8)])
        for obj in bpy.data.objects:
            if (obj.name == str(9)):
                vertices.append(bpy.data.objects[str(9)])
        for obj in bpy.data.objects:
            if (obj.name == str(10)):
                vertices.append(bpy.data.objects[str(10)])
        for obj in bpy.data.objects:
            if (obj.name == str(11)):
                vertices.append(bpy.data.objects[str(11)])
        for obj in bpy.data.objects:
            if (obj.name == str(12)):
                vertices.append(bpy.data.objects[str(12)])
        for obj in bpy.data.objects:
            if (obj.name == str(13)):
                vertices.append(bpy.data.objects[str(13)])
        for obj in bpy.data.objects:
            if (obj.name == str(14)):
                vertices.append(bpy.data.objects[str(14)])
        for obj in bpy.data.objects:
            if (obj.name == str(15)):
                vertices.append(bpy.data.objects[str(15)])
        for obj in bpy.data.objects:
            if (obj.name == str(16)):
                vertices.append(bpy.data.objects[str(16)])
        
        vertices_bones.append(0) # Append first vertex separately.
        
        # Loop through all bones, vertices within bones, and append them.
        for i in range(0, len(vertices)):
            for j in range(0, bones_vertices[i]):
                vertices_bones.append(i)
        
        print(len(vertices))
        #print(vertex_index)
        #print(vertices_bones)
        
        # Stub header amounts and offsets.
        for i in range(0, 0x60):
            outfile.write(struct.pack('B', 0x00))
        
        for i in range(0, bones[0]):
            if (i == 0):
                outfile.write(struct.pack('H', bones_parents[i])) # Parent Bone
                outfile.write(struct.pack('H', bones_vertex[i])) # Parent Vertex
                outfile.write(struct.pack('H', bones_vertices[i]+1)) # Number Of Vertices
                outfile.write(struct.pack('H', 0x00))
            else:
                outfile.write(struct.pack('H', bones_parents[i])) # Parent Bone
                outfile.write(struct.pack('H', bones_vertex[i])) # Parent Vertex
                outfile.write(struct.pack('H', bones_vertices[i])) # Number Of Vertices
                outfile.write(struct.pack('H', 0x00))
        
        for i in range(0, len(vertices)):
            if (i == 0):
                outfile.write(struct.pack('h', int(vertices[i].matrix_world.to_translation().x * SCALE)))
                outfile.write(struct.pack('h', int(vertices[i].matrix_world.to_translation().z * SCALE)))
                outfile.write(struct.pack('h', int(vertices[i].matrix_world.to_translation().y * SCALE)))
            else:
                outfile.write(struct.pack('h', int((vertices[i].matrix_world.to_translation().x - vertices[i].parent.matrix_world.to_translation().x) * SCALE)))
                outfile.write(struct.pack('h', int((vertices[i].matrix_world.to_translation().z - vertices[i].parent.matrix_world.to_translation().z) * SCALE)))
                outfile.write(struct.pack('h', int((vertices[i].matrix_world.to_translation().y - vertices[i].parent.matrix_world.to_translation().y) * SCALE)))
            
            outfile.write(struct.pack('h', vertices_bones[i]))
        
        for i in range(0, triangles[0]+1):
            outfile.write(struct.pack('B', 0x05)) # Material
            outfile.write(struct.pack('B', 0x00)) # Triangle / Quad
            outfile.write(struct.pack('B', 0x01)) # 1 Triangle
            outfile.write(struct.pack('B', 0x00))
            outfile.write(struct.pack('B', 0x14)) # Size In Bytes
            outfile.write(struct.pack('B', 0x00))
            outfile.write(struct.pack('B', 0x00))
            outfile.write(struct.pack('B', 0x00))
            
            outfile.write(struct.pack('h', triangles_x[i])) # Vertex Index 1
            outfile.write(struct.pack('h', triangles_y[i])) # Vertex Index 2
            outfile.write(struct.pack('h', triangles_z[i])) # Vertex Index 3
            outfile.write(struct.pack('h', 0x00))
            outfile.write(struct.pack('B', 0x40)) # Color
            outfile.write(struct.pack('B', 0x10))
            outfile.write(struct.pack('h', 0x00))
        
        # Fill header amounts and offsets.
        outfile.seek(BONES, 0)
        outfile.write(struct.pack('h', bones[0]))
        
        outfile.seek(BONES_OFFSET, 0)
        outfile.write(struct.pack('h', HEADER))
        
        outfile.seek(VERTICES, 0)
        outfile.write(struct.pack('h', len(vertices)))
        
        outfile.seek(VERTICES_OFFSET, 0)
        outfile.write(struct.pack('h', HEADER + (bones[0] * 8)))
        
        outfile.seek(NORMALS_OFFSET, 0)
        outfile.write(struct.pack('h', HEADER + (bones[0] * 8) + (len(vertices) * 8)))
        
        outfile.seek(UNKNOWNS_OFFSET, 0)
        outfile.write(struct.pack('h', HEADER + (bones[0] * 8) + (len(vertices) * 8)))
        
        outfile.seek(POLYGONS, 0)
        outfile.write(struct.pack('h', triangles[0]+1))
        
        outfile.seek(POLYGONS_OFFSET, 0)
        outfile.write(struct.pack('h', HEADER + (bones[0] * 8) + (len(vertices) * 8)))
        
        outfile.seek(LINES_OFFSET, 0)
        outfile.write(struct.pack('h', HEADER + (bones[0] * 8) + (len(vertices) * 8) + ((triangles[0]+1) * 0x14)))
        
        outfile.seek(SPHERES_OFFSET, 0)
        outfile.write(struct.pack('h', HEADER + (bones[0] * 8) + (len(vertices) * 8) + ((triangles[0]+1) * 0x14)))
        
        outfile.seek(TEXTURES_OFFSET, 0)
        outfile.write(struct.pack('h', HEADER + (bones[0] * 8) + (len(vertices) * 8) + ((triangles[0]+1) * 0x14)))
        
        outfile.close()
        outfile = None
        
        #self.report({'WARNING'}, "LBA2 model exported successfully!")
        self.report({'INFO'}, "LBA2 model exported successfully!")
        
        return {'FINISHED'}

class exportAnimation(Operator):
    bl_idname = 'export.animation'
    bl_label = 'Export Animation'
    
    def execute(self, context):
        return {'FINISHED'}

class alignCursor(Operator):
    bl_idname = 'align.cursor'
    bl_label = 'Align Cursor'
    
    def execute(self, context):
        bpy.context.scene.cursor_location = (bpy.context.selected_objects[0].matrix_world.translation.x, bpy.context.selected_objects[0].matrix_world.translation.y, bpy.context.selected_objects[0].matrix_world.translation.z)
        return {'FINISHED'}

class setBoneRotation(Operator):
    bl_idname = 'set.bonerotation'
    bl_label = 'Set bone'
    
    def execute(self, context):
        bones[0] += 1
        
        # First object selected must be bone, then vertex.
        if (bones[0]-1 == 0):
            bones_parents[bones[0]-1] = 0xFFFF
        else:
            boneStr = bpy.context.selected_objects[0].parent.name
            boneStr = boneStr.rstrip('b') # Delete the last character from the string.
            
            bones_parents[bones[0]-1] = int(boneStr)
        
        bones_vertex[bones[0]-1] = int(bpy.context.selected_objects[1].name)
        bones_vertices[bones[0]-1] = len((getChildren(bpy.context.selected_objects[1])))
        
        # Lock location
        bpy.context.selected_objects[0].lock_location[0] = True
        bpy.context.selected_objects[0].lock_location[1] = True
        bpy.context.selected_objects[0].lock_location[2] = True
        
        # Lock scaling even though it's never needed anyway.
        bpy.context.selected_objects[0].lock_scale[0] = True
        bpy.context.selected_objects[0].lock_scale[1] = True
        bpy.context.selected_objects[0].lock_scale[2] = True
        
        # This bone can be rotated
        bones_types[bones[0]-1] = 0x00
        
        return {'FINISHED'}

class setBoneTranslation(Operator):
    bl_idname = 'set.bonetranslation'
    bl_label = 'Set bone'
    
    def execute(self, context):
        bones[0] += 1
        
        # First object selected must be bone, then vertex.
        if (bones[0]-1 == 0):
            bones_parents[bones[0]-1] = 0xFFFF
        else:
            boneStr = bpy.context.selected_objects[0].parent.name
            boneStr = boneStr.rstrip('b') # Delete the last character from the string.
        
            bones_parents[bones[0]-1] = int(boneStr)
        
        bones_vertex[bones[0]-1] = int(bpy.context.selected_objects[1].name)
        #bones_vertices[bones[0]-1] = len((getChildren(bpy.context.selected_objects[0])))
        bones_vertices[bones[0]-1] = 0x01
        
        # Lock rotation
        bpy.context.selected_objects[0].lock_rotation[0] = True
        bpy.context.selected_objects[0].lock_rotation[1] = True
        bpy.context.selected_objects[0].lock_rotation[2] = True
        
        # Lock scaling even though it's never needed anyway.
        bpy.context.selected_objects[0].lock_scale[0] = True
        bpy.context.selected_objects[0].lock_scale[1] = True
        bpy.context.selected_objects[0].lock_scale[2] = True
        
        # This bone can be translated
        bones_types[bones[0]-1] = 0x01
        
        return {'FINISHED'}

class saveBones(Operator):
    bl_idname = 'save.bones'
    bl_label = 'Save bones'
    
    def execute(self, context):
        path = 'C:\\Users\\USER\\Desktop\\Parker\\Models\\LowPoly\\testBoneSave2.txt'
        
        outfile = open(path, 'wb')
        
        outfile.write(struct.pack('h', bones[0]))
        
        for i in range(0, bones[0]):
            outfile.write(struct.pack('H', bones_parents[i]))
            outfile.write(struct.pack('H', bones_vertex[i]))
            outfile.write(struct.pack('H', bones_vertices[i]))
            outfile.write(struct.pack('H', bones_types[i]))
        
        outfile.close()
        outfile = None
        
        return {'FINISHED'}

class loadBones(Operator):
    bl_idname = 'load.bones'
    bl_label = 'Load bones'
    
    def execute(self, context):
        path = 'C:\\Users\\USER\\Desktop\\Parker\\Models\\LowPoly\\testBoneSave2.txt'
        
        outfile = open(path, 'rb')
        
        outfile.seek(0, 0)
        tempBones[0] = struct.unpack('h', outfile.read(2))
        
        bones[0] = tempBones[0][0]
        
        for i in range(0, tempBones[0][0]):
            bones_parents[i] = struct.unpack('H', outfile.read(2))
            bones_vertex[i] = struct.unpack('H', outfile.read(2))
            bones_vertices[i] = struct.unpack('H', outfile.read(2))
            bones_types[i] = struct.unpack('H', outfile.read(2))
            
        outfile.close()
        outfile = None
        
        return {'FINISHED'}

class clearBones(Operator):
    bl_idname = 'clear.bones'
    bl_label = 'Clear bones'
    
    def execute(self, context):
        for i in range(0, bones[0]+1):
            bpy.data.objects[str(i)].lock_location[0] = False
            bpy.data.objects[str(i)].lock_location[1] = False
            bpy.data.objects[str(i)].lock_location[2] = False
            
            bpy.data.objects[str(i)].lock_rotation[0] = False
            bpy.data.objects[str(i)].lock_rotation[1] = False
            bpy.data.objects[str(i)].lock_rotation[2] = False
            
            bpy.data.objects[str(i)].lock_scale[0] = False
            bpy.data.objects[str(i)].lock_scale[1] = False
            bpy.data.objects[str(i)].lock_scale[2] = False
            
            bones_parents[i] = 0
            bones_vertex[i] = 0
            bones_vertices[i] = 0
            bones_types[i] = 0
        
        bones[0] = 0
        
        return {'FINISHED'}

class saveTriangles(Operator):
    bl_idname = 'save.triangles'
    bl_label = 'Saves triangles'
    
    def execute(self, context):
        path = 'C:\\Users\\USER\\Desktop\\Parker\\Models\\LowPoly\\testModelSave.txt'
        
        outfile = open(path, 'wb')
        
        outfile.write(struct.pack('h', triangles[0]+1))
        
        for i in range(0, triangles[0]+1):
            outfile.write(struct.pack('h', triangles_x[i]))
            outfile.write(struct.pack('h', triangles_y[i]))
            outfile.write(struct.pack('h', triangles_z[i]))
        
        outfile.close()
        outfile = None
        
        return {'FINISHED'}

class loadTriangles(Operator):
    bl_idname = 'load.triangles'
    bl_label = 'Loads triangles'
    
    def execute(self, context):
        path = 'C:\\Users\\USER\\Desktop\\Parker\\Models\\LowPoly\\testModelSave.txt'
        
        outfile = open(path, 'rb')
        
        outfile.seek(0, 0)
        tempTriangles[0] = struct.unpack('h', outfile.read(2))
        
        triangles[0] = tempTriangles[0][0]
        
        #myStr = remove_chars(tempTriangles[0][0], 'x')
        
        #myStr = tuple(int(s) for s in tempTriangles[0].strip("()").split(","))
        #print(myStr)
        
        #print(str(triangles[0]))    # Displays (2,)
        #print(str(triangles[0][0])) # Displays 2
        
        # We reference with a double array to convert from a tuple to an int.
        for i in range(0, tempTriangles[0][0]):
            temp_x[i] = struct.unpack('h', outfile.read(2))
            temp_y[i] = struct.unpack('h', outfile.read(2))
            temp_z[i] = struct.unpack('h', outfile.read(2))
            
            triangles_x[i] = temp_x[i][0]
            triangles_y[i] = temp_y[i][0]
            triangles_z[i] = temp_z[i][0]
            
            triangles_x1_p[i] = bpy.data.objects[str(triangles_x[i])].matrix_world.translation.x
            triangles_y1_p[i] = bpy.data.objects[str(triangles_x[i])].matrix_world.translation.y
            triangles_z1_p[i] = bpy.data.objects[str(triangles_x[i])].matrix_world.translation.z
            
            triangles_x2_p[i] = bpy.data.objects[str(triangles_y[i])].matrix_world.translation.x
            triangles_y2_p[i] = bpy.data.objects[str(triangles_y[i])].matrix_world.translation.y
            triangles_z2_p[i] = bpy.data.objects[str(triangles_y[i])].matrix_world.translation.z
            
            triangles_x3_p[i] = bpy.data.objects[str(triangles_z[i])].matrix_world.translation.x
            triangles_y3_p[i] = bpy.data.objects[str(triangles_z[i])].matrix_world.translation.y
            triangles_z3_p[i] = bpy.data.objects[str(triangles_z[i])].matrix_world.translation.z
            
            vert = [(triangles_x1_p[i], triangles_y1_p[i], triangles_z1_p[i]),
                    (triangles_x2_p[i], triangles_y2_p[i], triangles_z2_p[i]),
                    (triangles_x3_p[i], triangles_y3_p[i], triangles_z3_p[i])]
            face = [(0, 1, 2)]
            edge = [(0,1), (1,2), (2,0)]
            
            my_mesh = bpy.data.meshes.new("triangle")
            my_obj = bpy.data.objects.new("triangle" + str(i), my_mesh)
            
            my_obj.location = bpy.context.scene.cursor_location
            bpy.context.scene.objects.link(my_obj)
            
            #my_mesh.from_pydata(vert,edge,[])
            my_mesh.from_pydata(vert,[],face)
            my_mesh.update(calc_edges=True)
        
        
        outfile.close()
        outfile = None
        
        return {'FINISHED'}

class createTriangle(Operator):
    bl_idname = 'create.triangle'
    bl_label = 'Create a triangle'
    
    def execute(self, context):
        triangles[0] += 1
        
        triangles_x[triangles[0]] = int(bpy.context.selected_objects[0].name)
        triangles_y[triangles[0]] = int(bpy.context.selected_objects[1].name)
        triangles_z[triangles[0]] = int(bpy.context.selected_objects[2].name)
        
        triangles_x1_p[triangles[0]] = bpy.context.selected_objects[0].matrix_world.translation.x
        triangles_y1_p[triangles[0]] = bpy.context.selected_objects[0].matrix_world.translation.y
        triangles_z1_p[triangles[0]] = bpy.context.selected_objects[0].matrix_world.translation.z
        
        triangles_x2_p[triangles[0]] = bpy.context.selected_objects[1].matrix_world.translation.x
        triangles_y2_p[triangles[0]] = bpy.context.selected_objects[1].matrix_world.translation.y
        triangles_z2_p[triangles[0]] = bpy.context.selected_objects[1].matrix_world.translation.z
        
        triangles_x3_p[triangles[0]] = bpy.context.selected_objects[2].matrix_world.translation.x
        triangles_y3_p[triangles[0]] = bpy.context.selected_objects[2].matrix_world.translation.y
        triangles_z3_p[triangles[0]] = bpy.context.selected_objects[2].matrix_world.translation.z
        
        vert = [(triangles_x1_p[triangles[0]], triangles_y1_p[triangles[0]], triangles_z1_p[triangles[0]]),
                (triangles_x2_p[triangles[0]], triangles_y2_p[triangles[0]], triangles_z2_p[triangles[0]]),
                (triangles_x3_p[triangles[0]], triangles_y3_p[triangles[0]], triangles_z3_p[triangles[0]])]
        face = [(0, 1, 2)]
        edge = [(0,1), (1,2), (2,0)]
        
        my_mesh = bpy.data.meshes.new("triangle")
        my_obj = bpy.data.objects.new("triangle" + str(triangles[0]), my_mesh)
        
        my_obj.location = bpy.context.scene.cursor_location
        bpy.context.scene.objects.link(my_obj)
        
        #my_mesh.from_pydata(vert,edge,[])
        my_mesh.from_pydata(vert,[],face)
        my_mesh.update(calc_edges=True)
        
        return {'FINISHED'}

class deleteTriangle(Operator):
    bl_idname = 'delete.triangle'
    bl_label = 'Delete a triangle'
    
    def execute(self, context):
        # We skip the last triangle here since we delete one in the process.
        # We check the last triangle in a separate statement below.
        for i in range(0, triangles[0]):
            #if (bpy.data.objects["triangle" + str(i)].select == True):
            if (bpy.data.objects["triangle" + str(i)] is not None):
                if (bpy.data.objects["triangle" + str(i)].select == True):
                    
                    # Check the triangles after this one
                    for j in range(i, triangles[0]+1):
                        
                        # If this is not the last triangle
                        if (j != (triangles[0]+1)):
                            triangles_x[j] = triangles_x[j + 1]
                            triangles_y[j] = triangles_y[j + 1]
                            triangles_z[j] = triangles_z[j + 1]
                            
                            if (j != (triangles[0])):
                                bpy.data.objects["triangle" + str(j + 1)].name = ("triangle" + str(j))
                            else:
                                bpy.data.objects.remove(bpy.context.selected_objects[0], True)
                                triangles[0] -= 1
        
        # Check the last triangle.
        if (bpy.data.objects["triangle" + str(triangles[0])] is not None):
            if (bpy.data.objects["triangle" + str(triangles[0])].select == True):
                bpy.data.objects.remove(bpy.context.selected_objects[0], True)
                triangles[0] -= 1
        return {'FINISHED'}

class flipTriangle(Operator):
    bl_idname = 'flip.triangle'
    bl_label = 'Flip triangle'
    
    def execute(self, context):
        # Flip the triangle in the viewport.
        tempX_x = bpy.context.selected_objects[0].data.vertices[0].co[0]
        tempX_y = bpy.context.selected_objects[0].data.vertices[0].co[1]
        tempX_z = bpy.context.selected_objects[0].data.vertices[0].co[2]
        
        bpy.context.selected_objects[0].data.vertices[0].co[0] = bpy.context.selected_objects[0].data.vertices[1].co[0]
        bpy.context.selected_objects[0].data.vertices[0].co[1] = bpy.context.selected_objects[0].data.vertices[1].co[1]
        bpy.context.selected_objects[0].data.vertices[0].co[2] = bpy.context.selected_objects[0].data.vertices[1].co[2]
        
        bpy.context.selected_objects[0].data.vertices[1].co[0] = tempX_x
        bpy.context.selected_objects[0].data.vertices[1].co[1] = tempX_y
        bpy.context.selected_objects[0].data.vertices[1].co[2] = tempX_z
        
        # lstrip strips the string contents from the left side
        # rstrip strips the string contents from the right side
        trianglesStr = bpy.context.selected_objects[0].name
        trianglesStr = trianglesStr.lstrip('triangle')
        
        # Flip the actual coordinates in the panel.
        tempX = triangles_x[int(trianglesStr)]
        triangles_x[int(trianglesStr)] = triangles_y[int(trianglesStr)]
        triangles_y[int(trianglesStr)] = tempX
        return {'FINISHED'}

class updateTriangles(Operator):
    bl_idname = 'update.triangles'
    bl_label = 'Update triangles'
    
    def execute(self, context):
        for i in range(0, triangles[0]+1):
            bpy.data.objects["triangle" + str(i)].data.vertices[0].co[0] = bpy.data.objects[str(triangles_x[i])].matrix_world.translation.x
            bpy.data.objects["triangle" + str(i)].data.vertices[0].co[1] = bpy.data.objects[str(triangles_x[i])].matrix_world.translation.y
            bpy.data.objects["triangle" + str(i)].data.vertices[0].co[2] = bpy.data.objects[str(triangles_x[i])].matrix_world.translation.z
            
            bpy.data.objects["triangle" + str(i)].data.vertices[1].co[0] = bpy.data.objects[str(triangles_y[i])].matrix_world.translation.x
            bpy.data.objects["triangle" + str(i)].data.vertices[1].co[1] = bpy.data.objects[str(triangles_y[i])].matrix_world.translation.y
            bpy.data.objects["triangle" + str(i)].data.vertices[1].co[2] = bpy.data.objects[str(triangles_y[i])].matrix_world.translation.z
            
            bpy.data.objects["triangle" + str(i)].data.vertices[2].co[0] = bpy.data.objects[str(triangles_z[i])].matrix_world.translation.x
            bpy.data.objects["triangle" + str(i)].data.vertices[2].co[1] = bpy.data.objects[str(triangles_z[i])].matrix_world.translation.y
            bpy.data.objects["triangle" + str(i)].data.vertices[2].co[2] = bpy.data.objects[str(triangles_z[i])].matrix_world.translation.z
        
        return {'FINISHED'}

# Doesn't really clear the GL triangles, but sets all their positions to 0 and sets the triangles counter to 0.
# We just use normal triangles in the end anyway.
class clearTriangles(Operator):
    bl_idname = 'clear.triangles'
    bl_label = 'Clears triangles'
    
    def execute(self, context):
        for i in range(0, triangles[0]+1):
            triangles_x[i] = 0
            triangles_y[i] = 0
            triangles_z[i] = 0
            
            triangles_x1_p[i] = 0
            triangles_y1_p[i] = 0
            triangles_z1_p[i] = 0
            
            triangles_x2_p[i] = 0
            triangles_y2_p[i] = 0
            triangles_z2_p[i] = 0
            
            triangles_x3_p[i] = 0
            triangles_y3_p[i] = 0
            triangles_z3_p[i] = 0
            
            bpy.data.objects.remove(bpy.data.objects["triangle" + str(i)], True)
        
        triangles[0] = -1
        return {'FINISHED'}

class LBA2Panel(bpy.types.Panel):
    bl_label = "LBA2 Panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    
    def draw(self, context):
        layout = self.layout
        
        button_return_objects = layout.row()
        button_return_objects.operator('return.objects', text='Return Objects Count')
        
        button_export_model = layout.row()
        button_export_model.alert = True # Shows button as red.
        #button_export_model.prop(context.object.data, "myColor")
        button_export_model.operator('export.model', text='Export Model')
        
        button_export_animation = layout.row()
        button_export_animation.operator('export.animation', text='Export Animation')
        
        button_align_cursor_to_vertex = layout.row()
        button_align_cursor_to_vertex.operator('align.cursor', text='Align Cursor To Vertex')
        
        box_bone_properties = layout.box()
        
        box_bone_label = box_bone_properties.row()
        box_bone_label.label(text='Bone Properties:')
        
        button_set_bone_rotation = box_bone_properties.row()
        button_set_bone_rotation.operator('set.bonerotation', text='Set Bone (Rotation)')
        
        button_set_bone_translation = box_bone_properties.row()
        button_set_bone_translation.operator('set.bonetranslation', text='Set Bone (Translation)')
        
        button_save_bones = box_bone_properties.row()
        button_save_bones.alert = True
        button_save_bones.operator('save.bones', text='Save Bones')
        
        button_load_bones = box_bone_properties.row()
        button_load_bones.operator('load.bones', text='Load Bones')
        
        button_clear_bones = box_bone_properties.row()
        button_clear_bones.operator('clear.bones', text='Clear Bones')
        
        boneAmount = box_bone_properties.row()
        boneAmount.label(text="bones: " + str(bones[0]))
        
        for i in range(0, bones[0]):
            amount = box_bone_properties.row()
            amount.label(text="parent: %d, v: %d, amt: %d, type: %d" % (bones_parents[i], bones_vertex[i], bones_vertices[i], bones_types[i]))
        
        box_triangle_properties = layout.box()
        
        box_label = box_triangle_properties.row()
        box_label.label(text='Triangle Properties:')
        
        button_add_triangle = box_triangle_properties.row()
        button_add_triangle.operator('create.triangle', text='Create Triangle')
        
        button_delete_triangle = box_triangle_properties.row()
        button_delete_triangle.operator('delete.triangle', text='Delete Triangle')
        
        button_flip_triangle = box_triangle_properties.row()
        button_flip_triangle.operator('flip.triangle', text='Flip Triangle')
        
        button_save_triangles = box_triangle_properties.row()
        button_save_triangles.alert = True
        button_save_triangles.operator('save.triangles', text='Save Triangles')
        
        button_load_triangles = box_triangle_properties.row()
        button_load_triangles.operator('load.triangles', text='Load Triangles')
        
        button_update_triangles = box_triangle_properties.row()
        button_update_triangles.operator('update.triangles', text='Update Triangles')
        
        button_clear_triangles = box_triangle_properties.row()
        button_clear_triangles.operator('clear.triangles', text='Clear Triangles')
        
        box_colors = layout.box()
        box_colors_label = box_colors.row()
        box_colors_label.label(text='Color Properties:')
        
        ts = context.tool_settings
        if ts.image_paint.palette:
            box_colors.template_palette(ts.image_paint, "palette", color=True)
        
        box_triangles = layout.box()
        
        # Print names of selected objects.
        if (len(bpy.context.selected_objects) <= 0):
            warning = box_triangles.row()
            warning.label(text="Please select at least three objects!")
        
        if (len(bpy.context.selected_objects) == 1):
            obj1 = box_triangles.row()
            obj1.label(text="v1 = " + str(bpy.context.selected_objects[0].name))
        
        if (len(bpy.context.selected_objects) == 2):
            obj1 = box_triangles.row()
            obj1.label(text="v1 = " + str(bpy.context.selected_objects[0].name))
            
            obj2 = box_triangles.row()
            obj2.label(text="v2 = " + str(bpy.context.selected_objects[1].name))
        
        if (len(bpy.context.selected_objects) == 3):
            obj1 = box_triangles.row()
            obj1.label(text="v1 = " + str(bpy.context.selected_objects[0].name))
            
            obj2 = box_triangles.row()
            obj2.label(text="v2 = " + str(bpy.context.selected_objects[1].name))
            
            obj3 = box_triangles.row()
            obj3.label(text="v3 = " + str(bpy.context.selected_objects[2].name))
        
        if (len(bpy.context.selected_objects) >= 4):
            warning = box_triangles.row()
            warning.label(text="Please select only three objects!")
        
        box_triangles_amount = layout.box()
        
        triangleAmount = box_triangles_amount.row()
        triangleAmount.label(text="triangles: " + str(triangles[0]))
        
        for i in range(0, triangles[0]+1):
            amount = box_triangles_amount.row()
            amount.label(text="v1: %d, v2: %d, v3: %d " % (triangles_x[i], triangles_y[i], triangles_z[i]))
            
            # Works with GL commands, but needs to be refreshed somehow.
            # We just disregard it for now.
            #drawTriangle(0, 0, 0, 4, 0, 0, 0, 4, 0)
            #handle = bpy.types.SpaceView3D.draw_handler_add(drawTriangle, (triangles_x1_p[i], triangles_y1_p[i], triangles_z1_p[i], triangles_x2_p[i], triangles_y2_p[i], triangles_z2_p[i], triangles_x3_p[i], triangles_y3_p[i], triangles_z3_p[i]), 'WINDOW', 'POST_VIEW')

def register():
    bpy.utils.register_class(LBA2Panel)
    bpy.utils.register_class(returnObjects)
    bpy.utils.register_class(exportModel)
    bpy.utils.register_class(exportAnimation)
    bpy.utils.register_class(alignCursor)
    bpy.utils.register_class(setBoneRotation)
    bpy.utils.register_class(setBoneTranslation)
    bpy.utils.register_class(saveBones)
    bpy.utils.register_class(loadBones)
    bpy.utils.register_class(clearBones)
    bpy.utils.register_class(createTriangle)
    bpy.utils.register_class(deleteTriangle)
    bpy.utils.register_class(flipTriangle)
    bpy.utils.register_class(saveTriangles)
    bpy.utils.register_class(loadTriangles)
    bpy.utils.register_class(updateTriangles)
    bpy.utils.register_class(clearTriangles)

def unregister():
    bpy.utils.unregister_class(LBA2Panel)
    bpy.utils.unregister_class(returnObjects)
    bpy.utils.unregister_class(exportModel)
    bpy.utils.unregister_class(exportAnimation)
    bpy.utils.unregister_class(alignCursor)
    bpy.utils.unregister_class(setBoneRotation)
    bpy.utils.unregister_class(setBoneTranslation)
    bpy.utils.unregister_class(saveBones)
    bpy.utils.runegister_class(loadBones)
    bpy.utils.unregister_class(clearBones)
    bpy.utils.unregister_class(createTriangle)
    bpy.utils.unregister_class(deleteTriangle)
    bpy.utils.unregister_class(flipTriangle)
    bpy.utils.unregister_class(saveTriangles)
    bpy.utils.unregister_class(loadTriangles)
    bpy.utils.unregister_class(updateTriangles)
    bpy.utils.unregister_class(clearTriangles)

if __name__ == "__main__":
    register()



pal = bpy.data.palettes.get("CustomPalette")

#if pal is None: # This doesn't refresh palette, but the one below does.
if pal is not None:
    pal = bpy.data.palettes.new("CustomPalette")
    
    red = pal.colors.new()
    red.color = (1, 0, 0)
    #red.weight = 1.0
    #pal.colors.active = red
    
    blue = pal.colors.new()
    blue.color = (0, 1, 0)
    
    green = pal.colors.new()
    green.color = (0, 0, 1)

ts = bpy.context.tool_settings
ts.image_paint.palette = pal

#bpy.ops.palette.color_add() = False


#children = getChildren(bpy.data.objects['1'])
#print("%d " % (len(children)))
#print("%d " % (len(getChildren(bpy.data.objects['1']))))

#class ScaleOperator(Operator):
    #bl_idname = 'my.scale'
    #bl_label = 'My scale operator'
    
    #def draw(self, context):
        #bpy.ops.object.transform_apply(scale=True)
        #self.report({'INFO'}, 'Scale applied!')
        #return {'FINISHED'}

        #button = layout.row()
        #button.operator('my.scale', text='Apply Scale')
        
        #slider_x = layout.row()
        #slider_x.prop(bpy.context.selected_objects[0], 'scale', index=0, text='Scale x:')
        
        #slider_y = layout.row()
        #slider_y.prop(bpy.context.selected_objects[0], 'scale', index=1, text='Scale y:')
        
        #slider_z = layout.row()
        #slider_z.prop(bpy.context.selected_objects[0], 'scale', index=2, text='Scale z:')
        
        #inc_button = layout.row()
        #inc_button.operator('my.increment', text='Apply increment')