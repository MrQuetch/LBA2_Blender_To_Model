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

os.system('cls')

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

global_scale = [0]

bones = [0]
tempBones = [0]

vertices = []
vertices_bones = []
vertices_amount = [0]

triangles = [-1]
tempTriangles = [-1]

temp_bones_parents = []
temp_bones_vertex = []
temp_bones_vertices = []
temp_bones_types = []

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

triangles_color = []

temp_triangles_color = []

# Populate arrays.
for i in range(0, 530):
    temp_bones_parents.append(0)
    temp_bones_vertex.append(0)
    temp_bones_vertices.append(0)
    temp_bones_types.append(0)
    
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
    
    triangles_color.append(0)
    temp_triangles_color.append(0)


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

#mesh_current = None
mesh_vertices = []
mesh_vertices_x = []
mesh_vertices_y = []
mesh_vertices_z = []

class createVertex(Operator):
    bl_idname = 'create.vertex'
    bl_label = 'Create vertex'
    
    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add()
        
        bpy.context.active_object.scale[0] = 0.02
        bpy.context.active_object.scale[1] = 0.02
        bpy.context.active_object.scale[2] = 0.02
        
        bpy.context.active_object.name = str(vertices_amount[0])
        
        vertices_amount[0] += 1
        
        return {'FINISHED'}

class createVerticesFromMesh(Operator):
    bl_idname = 'create.vertices'
    bl_label = 'Create vertices'
    
    def execute(self, context):
        # Change to object mode, then to edit mode.
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')
        
        #mesh_current = bpy.context.selected_objects[0]
        
        for v in bpy.context.active_object.data.vertices:
            print(str(v.index) + ' ' + str(v.select))
            #test = v.matrix_world.translation.x
            
            if (v.select == True): 
                # Get vertex indices and positions.
                mesh_vertices.append(int(v.index))
                mesh_vertices_x.append(float(v.co[0]))
                mesh_vertices_y.append(float(v.co[1]))
                mesh_vertices_z.append(float(v.co[2]))
        
        print(mesh_vertices)
        
        # Change to object mode.
        bpy.ops.object.mode_set(mode='OBJECT')
        
        for i in range(0, len(mesh_vertices)):
            bpy.ops.mesh.primitive_cube_add()
            
            bpy.context.active_object.location[0] = mesh_vertices_x[i]
            bpy.context.active_object.location[1] = mesh_vertices_y[i]
            bpy.context.active_object.location[2] = mesh_vertices_z[i]
            
            bpy.context.active_object.scale[0] = 0.02
            bpy.context.active_object.scale[1] = 0.02
            bpy.context.active_object.scale[2] = 0.02
            
            bpy.context.active_object.name = str(vertices_amount[0])
            
            vertices_amount[0] += 1
        
        # Select all of the vertices.
        # Makes parenting to parent vertex easier.
        for i in range(0, len(mesh_vertices)):
            bpy.data.objects[str(i)].select = True
        
        # Clear all of the data.
        #mesh_current = None
        mesh_vertices.clear()
        mesh_vertices_x.clear()
        mesh_vertices_y.clear()
        mesh_vertices_z.clear()
        
        return {'FINISHED'}

def getVerticesInLoop(index):
    for obj in bpy.data.objects:
        if (obj.name == str(index)):
            vertices_amount[0] += 1

class getVertices(Operator):
    bl_idname = 'get.vertices'
    bl_label = 'Get vertices'
    
    def execute(self, context):
        vertices_amount[0] = 0
        
        for i in range(0, 530):
            getVerticesInLoop(i)
        return {'FINISHED'}

def getVerticesAsObjects(index):
    for obj in bpy.data.objects:
        if (obj.name == str(index)):
            vertices.append(bpy.data.objects[str(index)])

class exportModel(Operator):
    bl_idname = 'export.model'
    bl_label = "Export a model"
    
    def execute(self, context):
        path = 'C:\\Users\\Parker\\Desktop\\Models\\LowPoly\\testModel2.txt'
        
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
        vertices_bones.clear()
        
        vertex_index = 0
        vertices.append(bpy.data.objects[str(0)]) # Append first vertex separately.
        
        # Loop through all vertices, check names, and append them.
        #for obj in bpy.data.objects:
        #    if (obj.name == str(vertex_index)):
        #        vertex_index += 1
        #        vertices.append(bpy.data.objects[str(vertex_index)])
        
        # Unfortunately, each vertex must be checked separately.
        # For-loops generated by external C++ program.
        # However, it is now in a single Python function.
        for i in range(1, 530):
            getVerticesAsObjects(i)
        
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
        
        # Vertices.
        for i in range(0, len(vertices)):
            if (i == 0):
                outfile.write(struct.pack('h', int(vertices[i].matrix_world.to_translation().x * global_scale[0])))
                outfile.write(struct.pack('h', int(vertices[i].matrix_world.to_translation().z * global_scale[0])))
                outfile.write(struct.pack('h', int(vertices[i].matrix_world.to_translation().y * global_scale[0])))
            else:
                outfile.write(struct.pack('h', int((vertices[i].matrix_world.to_translation().x - vertices[i].parent.matrix_world.to_translation().x) * global_scale[0])))
                outfile.write(struct.pack('h', int((vertices[i].matrix_world.to_translation().z - vertices[i].parent.matrix_world.to_translation().z) * global_scale[0])))
                outfile.write(struct.pack('h', int((vertices[i].matrix_world.to_translation().y - vertices[i].parent.matrix_world.to_translation().y) * global_scale[0])))
            
            outfile.write(struct.pack('h', vertices_bones[i]))
        
        # Normals.
        for i in range(0, len(vertices)):
            if (i == 0):
                outfile.write(struct.pack('h', int(vertices[i].matrix_world.to_translation().x * global_scale[0] * 10)))
                outfile.write(struct.pack('h', int(vertices[i].matrix_world.to_translation().z * global_scale[0] * 10)))
                outfile.write(struct.pack('h', int(vertices[i].matrix_world.to_translation().y * global_scale[0] * 10)))
            else:
                outfile.write(struct.pack('h', int((vertices[i].matrix_world.to_translation().x - vertices[i].parent.matrix_world.to_translation().x) * global_scale[0] * 10)))
                outfile.write(struct.pack('h', int((vertices[i].matrix_world.to_translation().z - vertices[i].parent.matrix_world.to_translation().z) * global_scale[0] * 10)))
                outfile.write(struct.pack('h', int((vertices[i].matrix_world.to_translation().y - vertices[i].parent.matrix_world.to_translation().y) * global_scale[0] * 10)))
            
            outfile.write(struct.pack('h', vertices_bones[i]))
        
        #for i in range(0, triangles[0]):
        for i in range(0, triangles[0]+1):
            outfile.write(struct.pack('B', 0x05)) # Material
            outfile.write(struct.pack('B', 0x00)) # Triangle / Quad
            outfile.write(struct.pack('B', 0x01)) # 1 Triangle
            outfile.write(struct.pack('B', 0x00))
            outfile.write(struct.pack('B', 0x14)) # Size In Bytes
            outfile.write(struct.pack('B', 0x00))
            outfile.write(struct.pack('B', 0x00))
            outfile.write(struct.pack('B', 0x00))
            
            outfile.write(struct.pack('h', triangles_y[i])) # Vertex Index 1
            outfile.write(struct.pack('h', triangles_x[i])) # Vertex Index 2
            outfile.write(struct.pack('h', triangles_z[i])) # Vertex Index 3
            outfile.write(struct.pack('h', 0x00))
            outfile.write(struct.pack('B', triangles_color[i])) # Color
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
        
        outfile.seek(NORMALS, 0)
        outfile.write(struct.pack('h', len(vertices)))
        
        outfile.seek(NORMALS_OFFSET, 0)
        outfile.write(struct.pack('h', HEADER + (bones[0] * 8) + (len(vertices) * 8)))
        
        outfile.seek(UNKNOWNS_OFFSET, 0)
        outfile.write(struct.pack('h', HEADER + (bones[0] * 8) + (len(vertices) * 8) + (len(vertices) * 8)))
        
        outfile.seek(POLYGONS, 0)
        outfile.write(struct.pack('h', triangles[0]+1))
        
        outfile.seek(POLYGONS_OFFSET, 0)
        outfile.write(struct.pack('h', HEADER + (bones[0] * 8) + (len(vertices) * 8) + (len(vertices) * 8)))
        
        outfile.seek(LINES_OFFSET, 0)
        outfile.write(struct.pack('h', HEADER + (bones[0] * 8) + (len(vertices) * 8) + (len(vertices) * 8) + ((triangles[0]+1) * 0x14)))
        
        outfile.seek(SPHERES_OFFSET, 0)
        outfile.write(struct.pack('h', HEADER + (bones[0] * 8) + (len(vertices) * 8) + (len(vertices) * 8) + ((triangles[0]+1) * 0x14)))
        
        outfile.seek(TEXTURES_OFFSET, 0)
        outfile.write(struct.pack('h', HEADER + (bones[0] * 8) + (len(vertices) * 8) + (len(vertices) * 8) + ((triangles[0]+1) * 0x14)))
        
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

class scaleUp(Operator):
    bl_idname = 'scale.up'
    bl_label = 'Scale up'
    
    def execute(self, context):
        global_scale[0] += 25
        self.report({'INFO'}, "Global scale set to " + str(global_scale[0]) + ".")
        return {'FINISHED'}

class scaleDown(Operator):
    bl_idname = 'scale.down'
    bl_label = 'Scale down'
    
    def execute(self, context):
        global_scale[0] -= 25
        self.report({'INFO'}, "Global scale set to " + str(global_scale[0]) + ".")
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
        path = 'C:\\Users\\Parker\\Desktop\\Models\\LowPoly\\testBoneSave3.txt'
        
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
        path = 'C:\\Users\\Parker\\Desktop\\Models\\LowPoly\\testBoneSave3.txt'
        
        outfile = open(path, 'rb')
        
        outfile.seek(0, 0)
        tempBones[0] = struct.unpack('h', outfile.read(2))
        
        bones[0] = tempBones[0][0]
        
        for i in range(0, tempBones[0][0]):
            temp_bones_parents[i] = struct.unpack('H', outfile.read(2))
            temp_bones_vertex[i] = struct.unpack('H', outfile.read(2))
            temp_bones_vertices[i] = struct.unpack('H', outfile.read(2))
            temp_bones_types[i] = struct.unpack('H', outfile.read(2))
            
            bones_parents[i] = temp_bones_parents[i][0]
            bones_vertex[i] = temp_bones_vertex[i][0]
            bones_vertices[i] = temp_bones_vertices[i][0]
            bones_types[i] = temp_bones_types[i][0]
            
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
        path = 'C:\\Users\\Parker\\Desktop\\Models\\LowPoly\\testModelSave2.txt'
        
        outfile = open(path, 'wb')
        
        outfile.write(struct.pack('h', triangles[0]+1))
        
        for i in range(0, triangles[0]+1):
            outfile.write(struct.pack('h', triangles_x[i]))
            outfile.write(struct.pack('h', triangles_y[i]))
            outfile.write(struct.pack('h', triangles_z[i]))
            outfile.write(struct.pack('h', triangles_color[i]))
        
        outfile.close()
        outfile = None
        
        return {'FINISHED'}

class loadTriangles(Operator):
    bl_idname = 'load.triangles'
    bl_label = 'Loads triangles'
    
    def execute(self, context):
        path = 'C:\\Users\\Parker\\Desktop\Models\\LowPoly\\testModelSave2.txt'
        
        outfile = open(path, 'rb')
        
        outfile.seek(0, 0)
        tempTriangles[0] = struct.unpack('h', outfile.read(2))
        
        triangles[0] = tempTriangles[0][0]
        
        # We strip a triangle when we load them.
        # This is the case since when we first create a triangle - we add one.
        triangles[0] -= 1
        
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
            temp_triangles_color[i] = struct.unpack('h', outfile.read(2))
            
            triangles_x[i] = temp_x[i][0]
            triangles_y[i] = temp_y[i][0]
            triangles_z[i] = temp_z[i][0]
            triangles_color[i] = temp_triangles_color[i][0]
            
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
            
            mat = bpy.data.materials.get("Material_" + str(i))
            if (mat is None):
                mat = bpy.data.materials.new(name="Material_" + str(i))
            
            if (my_obj.data.materials):
                my_obj.data.materials[0] = mat
            else:
                my_obj.data.materials.append(mat)
            
            # Red
            if (triangles_color[i] == 0x40):
                mat.diffuse_color[0] = 255
                mat.diffuse_color[1] = 0
                mat.diffuse_color[2] = 0
                
            # Green
            if (triangles_color[i] == 0x80):
                mat.diffuse_color[0] = 0
                mat.diffuse_color[1] = 255
                mat.diffuse_color[2] = 0
            
            # Blue
            if (triangles_color[i] == 0xC0):
                mat.diffuse_color[0] = 0
                mat.diffuse_color[1] = 0
                mat.diffuse_color[2] = 255
            
            # Brown
            if (triangles_color[i] == 0x10):
                mat.diffuse_color[0] = 90
                mat.diffuse_color[1] = 64
                mat.diffuse_color[2] = 32
            
            # Tan
            if (triangles_color[i] == 0x20):
                mat.diffuse_color[0] = 190
                mat.diffuse_color[1] = 150
                mat.diffuse_color[2] = 120
            
            # Gray
            if (triangles_color[i] == 0x30):
                mat.diffuse_color[0] = 64
                mat.diffuse_color[1] = 64
                mat.diffuse_color[2] = 64
            
            # Orange
            if (triangles_color[i] == 0x50):
                mat.diffuse_color[0] = 220
                mat.diffuse_color[1] = 120
                mat.diffuse_color[2] = 80
            
            # Yellow
            if (triangles_color[i] == 0x60):
                mat.diffuse_color[0] = 255
                mat.diffuse_color[1] = 255
                mat.diffuse_color[2] = 0
            
            mat.diffuse_intensity = 0.001
        
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
        
        
        
        mat = bpy.data.materials.get("Material_" + str(triangles[0]))
        if (mat is None):
            mat = bpy.data.materials.new(name="Material_" + str(triangles[0]))
        
        if (my_obj.data.materials):
            my_obj.data.materials[0] = mat
        else:
            my_obj.data.materials.append(mat)
        
        #mat = bpy.context.selected_objects[0].data.materials.new(name="Material")
        #mat = bpy.data.materials.new(name="Material")
        #my_obj.data.materials[0] = mat
        
        # If it's black - which it is here - it needs a color assigned to it.
        mat.diffuse_color[0] = 0
        mat.diffuse_color[1] = 0
        mat.diffuse_color[2] = 0
        
        mat.diffuse_intensity = 0.001
        
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
                                bpy.data.objects["triangle" + str(j + 1)].active_material.name = ("Material_" + str(j))
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

class colorTriangle(Operator):
    bl_idname = 'color.triangle'
    bl_label = 'Color triangle'
    
    def execute(self, context):
        #print(pal.colors.active)
        #print(pal.colors[0])
        print(pal.color.active[0])
        return {'FINISHED'}

class colorRed(Operator):
    bl_idname = 'color.red'
    bl_label = 'Color red'
    
    def execute(self, context):
        # Get the triangle name.
        trianglesStr = bpy.context.selected_objects[0].name
        trianglesStr = trianglesStr.lstrip('triangle')
        
        # Color the triangle red.
        triangles_color[int(trianglesStr)] = 0x40
        
        # Color in the 3D viewport.
        bpy.context.selected_objects[0].data.materials[0].diffuse_color[0] = 255
        bpy.context.selected_objects[0].data.materials[0].diffuse_color[1] = 0
        bpy.context.selected_objects[0].data.materials[0].diffuse_color[2] = 0
        
        return {'FINISHED'}

class colorGreen(Operator):
    bl_idname = 'color.green'
    bl_label = 'Color green'
    
    def execute(self, context):
        # Get the triangle name.
        trianglesStr = bpy.context.selected_objects[0].name
        trianglesStr = trianglesStr.lstrip('triangle')
        
        # Color the triangle green.
        triangles_color[int(trianglesStr)] = 0x80
        
        # Color in the 3D viewport.
        bpy.context.selected_objects[0].data.materials[0].diffuse_color[0] = 0
        bpy.context.selected_objects[0].data.materials[0].diffuse_color[1] = 255
        bpy.context.selected_objects[0].data.materials[0].diffuse_color[2] = 0
        
        return {'FINISHED'}

class colorBlue(Operator):
    bl_idname = 'color.blue'
    bl_label = 'Color blue'
    
    def execute(self, context):
        # Get the triangle name.
        trianglesStr = bpy.context.selected_objects[0].name
        trianglesStr = trianglesStr.lstrip('triangle')
        
        # Color the triangle blue.
        triangles_color[int(trianglesStr)] = 0xC0
        
        # Color in the 3D viewport.
        bpy.context.selected_objects[0].data.materials[0].diffuse_color[0] = 0
        bpy.context.selected_objects[0].data.materials[0].diffuse_color[1] = 0
        bpy.context.selected_objects[0].data.materials[0].diffuse_color[2] = 255
        
        return {'FINISHED'}

class colorBrown(Operator):
    bl_idname = 'color.brown'
    bl_label = 'Color brown'
    
    def execute(self, context):
        # Get the triangle name.
        trianglesStr = bpy.context.selected_objects[0].name
        trianglesStr = trianglesStr.lstrip('triangle')
        
        # Color the triangle brown.
        triangles_color[int(trianglesStr)] = 0x10
        
        # Color in the 3D viewport.
        bpy.context.selected_objects[0].data.materials[0].diffuse_color[0] = 90
        bpy.context.selected_objects[0].data.materials[0].diffuse_color[1] = 64
        bpy.context.selected_objects[0].data.materials[0].diffuse_color[2] = 32
        
        return {'FINISHED'}

class colorTan(Operator):
    bl_idname = 'color.tan'
    bl_label = 'Color tan'
    
    def execute(self, context):
        # Get the triangle name.
        trianglesStr = bpy.context.selected_objects[0].name
        trianglesStr = trianglesStr.lstrip('triangle')
        
        # Color the triangle tan.
        triangles_color[int(trianglesStr)] = 0x20
        
        # Color in the 3D viewport.
        bpy.context.selected_objects[0].data.materials[0].diffuse_color[0] = 190
        bpy.context.selected_objects[0].data.materials[0].diffuse_color[1] = 150
        bpy.context.selected_objects[0].data.materials[0].diffuse_color[2] = 120
        
        return {'FINISHED'}

class colorGray(Operator):
    bl_idname = 'color.gray'
    bl_label = 'Color gray'
    
    def execute(self, context):
        # Get the triangle name.
        trianglesStr = bpy.context.selected_objects[0].name
        trianglesStr = trianglesStr.lstrip('triangle')
        
        # Color the triangle gray.
        triangles_color[int(trianglesStr)] = 0x30
        
        # Color in the 3D viewport.
        bpy.context.selected_objects[0].data.materials[0].diffuse_color[0] = 64
        bpy.context.selected_objects[0].data.materials[0].diffuse_color[1] = 64
        bpy.context.selected_objects[0].data.materials[0].diffuse_color[2] = 64
        
        return {'FINISHED'}

class colorOrange(Operator):
    bl_idname = 'color.orange'
    bl_label = 'Color orange'
    
    def execute(self, context):
        # Get the triangle name.
        trianglesStr = bpy.context.selected_objects[0].name
        trianglesStr = trianglesStr.lstrip('triangle')
        
        # Color the triangle orange.
        triangles_color[int(trianglesStr)] = 0x50
        
        # Color in the 3D viewport.
        bpy.context.selected_objects[0].data.materials[0].diffuse_color[0] = 220
        bpy.context.selected_objects[0].data.materials[0].diffuse_color[1] = 120
        bpy.context.selected_objects[0].data.materials[0].diffuse_color[2] = 80
        
        return {'FINISHED'}

class colorYellow(Operator):
    bl_idname = 'color.yellow'
    bl_label = 'Color yellow'
    
    def execute(self, context):
        # Get the triangle name.
        trianglesStr = bpy.context.selected_objects[0].name
        trianglesStr = trianglesStr.lstrip('triangle')
        
        # Color the triangle orange.
        triangles_color[int(trianglesStr)] = 0x60
        
        # Color in the 3D viewport.
        bpy.context.selected_objects[0].data.materials[0].diffuse_color[0] = 255
        bpy.context.selected_objects[0].data.materials[0].diffuse_color[1] = 255
        bpy.context.selected_objects[0].data.materials[0].diffuse_color[2] = 0
        
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

def removeTrianglesAsObjects(index):
    for obj in bpy.data.objects:
        if (obj.name == "triangle" + str(index)):
            bpy.data.objects.remove(bpy.data.objects["triangle" + str(index)], True)

# Doesn't really clear the GL triangles, but sets all their positions to 0 and sets the triangles counter to 0.
# We just use normal triangles in the end anyway.
class clearTriangles(Operator):
    bl_idname = 'clear.triangles'
    bl_label = 'Clears triangles'
    
    def execute(self, context):
        #for i in range(0, triangles[0]):
        for i in range(0, 530):
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
        
        #bpy.data.objects.remove(bpy.data.objects["triangle" + str(i)], True)
        for i in range(0, 530):
            removeTrianglesAsObjects(i)
        
        triangles[0] = -1
        return {'FINISHED'}

class LBA2Panel(bpy.types.Panel):
    bl_label = "LBA2 Panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    
    def draw(self, context):
        layout = self.layout
        
        #button_return_objects = layout.row()
        #button_return_objects.operator('return.objects', text='Return Objects Count')
        
        button_export_model = layout.row()
        button_export_model.alert = True # Shows button as red.
        #button_export_model.prop(context.object.data, "myColor")
        button_export_model.operator('export.model', text='Export Model')
        
        button_export_animation = layout.row()
        button_export_animation.operator('export.animation', text='Export Animation')
        
        button_scale_up_animation = layout.row()
        button_scale_up_animation.operator('scale.up', text='Scale Up')
        
        button_scale_down_animation = layout.row()
        button_scale_down_animation.operator('scale.down', text='Scale Down')
        
        box_vertex_properties = layout.box()
        
        box_vertex_label = box_vertex_properties.row()
        box_vertex_label.label(text='Vertex Properties:')
        
        button_vertex = box_vertex_properties.row()
        button_vertex.operator('create.vertex', text='Create Vertex')
        
        button_vertices_mesh = box_vertex_properties.row()
        button_vertices_mesh.operator('create.vertices', text='Create Vertices From Mesh')
        
        button_vertices_get = box_vertex_properties.row()
        button_vertices_get.operator('get.vertices', text='Get Existing Vertices')
        
        verticesAmount = box_vertex_properties.row()
        verticesAmount.label(text='vertices: ' + str(vertices_amount[0]))
        
        #button_align_cursor_to_vertex = layout.row()
        #button_align_cursor_to_vertex.operator('align.cursor', text='Align Cursor To Vertex')
        
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
        
        #button_color_triangle = box_triangle_properties.row()
        #button_color_triangle.operator('color.triangle', text='Color Triangle')
        
        button_save_triangles = box_triangle_properties.row()
        button_save_triangles.alert = True
        button_save_triangles.operator('save.triangles', text='Save Triangles')
        
        button_load_triangles = box_triangle_properties.row()
        button_load_triangles.operator('load.triangles', text='Load Triangles')
        
        button_update_triangles = box_triangle_properties.row()
        button_update_triangles.operator('update.triangles', text='Update Triangles')
        
        button_clear_triangles = box_triangle_properties.row()
        button_clear_triangles.operator('clear.triangles', text='Clear Triangles')
        
        triangleAmount = box_triangle_properties.row()
        triangleAmount.label(text="triangles: " + str(triangles[0]+1))
        
        for i in range(0, triangles[0]+1):
            amount = box_triangle_properties.row()
            #amount.label(text="v1: %d, v2: %d, v3: %d " % (triangles_x[i], triangles_y[i], triangles_z[i]))
            amount.label(text="v1: %d, v2: %d, v3: %d, color: %d " % (triangles_x[i], triangles_y[i], triangles_z[i], triangles_color[i]))
        
        box_colors = layout.box()
        box_colors_label = box_colors.row()
        box_colors_label.label(text='Color Properties:')
        
        button_color_red = box_colors.row()
        button_color_red.operator('color.red', text='Color Red')
        
        button_color_green = box_colors.row()
        button_color_green.operator('color.green', text='Color Green')
        
        button_color_blue = box_colors.row()
        button_color_blue.operator('color.blue', text='Color Blue')
        
        button_color_brown = box_colors.row()
        button_color_brown.operator('color.brown', text='Color Brown')
        
        button_color_tan = box_colors.row()
        button_color_tan.operator('color.tan', text='Color Tan')
        
        button_color_gray = box_colors.row()
        button_color_gray.operator('color.gray', text='Color Gray')
        
        button_color_orange = box_colors.row()
        button_color_orange.operator('color.orange', text='Color Orange')
        
        button_color_yellow = box_colors.row()
        button_color_yellow.operator('color.yellow', text='Color Yellow')
        
        ts = context.tool_settings
        if ts.image_paint.palette:
            box_colors.template_palette(ts.image_paint, "palette", color=True)
        
        #box_triangles = layout.box()
        
        # Print names of selected objects.
        #if (len(bpy.context.selected_objects) <= 0):
        #    warning = box_triangles.row()
        #    warning.label(text="Please select at least three objects!")
        
        #if (len(bpy.context.selected_objects) == 1):
        #    obj1 = box_triangles.row()
        #    obj1.label(text="v1 = " + str(bpy.context.selected_objects[0].name))
        
        #if (len(bpy.context.selected_objects) == 2):
        #    obj1 = box_triangles.row()
        #    obj1.label(text="v1 = " + str(bpy.context.selected_objects[0].name))
            
        #    obj2 = box_triangles.row()
        #    obj2.label(text="v2 = " + str(bpy.context.selected_objects[1].name))
        
        #if (len(bpy.context.selected_objects) == 3):
        #    obj1 = box_triangles.row()
        #    obj1.label(text="v1 = " + str(bpy.context.selected_objects[0].name))
            
        #    obj2 = box_triangles.row()
        #    obj2.label(text="v2 = " + str(bpy.context.selected_objects[1].name))
            
        #    obj3 = box_triangles.row()
        #    obj3.label(text="v3 = " + str(bpy.context.selected_objects[2].name))
        
        #if (len(bpy.context.selected_objects) >= 4):
        #    warning = box_triangles.row()
        #    warning.label(text="Please select only three objects!")
        
        #box_triangles_amount = layout.box()
        
        #triangleAmount = box_triangles_amount.row()
        #triangleAmount.label(text="triangles: " + str(triangles[0]+1))
        
        #for i in range(0, triangles[0]+1):
            #amount = box_triangles_amount.row()
            #amount.label(text="v1: %d, v2: %d, v3: %d " % (triangles_x[i], triangles_y[i], triangles_z[i]))
            
            # Works with GL commands, but needs to be refreshed somehow.
            # We just disregard it for now.
            #drawTriangle(0, 0, 0, 4, 0, 0, 0, 4, 0)
            #handle = bpy.types.SpaceView3D.draw_handler_add(drawTriangle, (triangles_x1_p[i], triangles_y1_p[i], triangles_z1_p[i], triangles_x2_p[i], triangles_y2_p[i], triangles_z2_p[i], triangles_x3_p[i], triangles_y3_p[i], triangles_z3_p[i]), 'WINDOW', 'POST_VIEW')

def register():
    bpy.utils.register_class(LBA2Panel)
    #bpy.utils.register_class(returnObjects)
    bpy.utils.register_class(exportModel)
    bpy.utils.register_class(exportAnimation)
    bpy.utils.register_class(scaleUp)
    bpy.utils.register_class(scaleDown)
    bpy.utils.register_class(createVertex)
    bpy.utils.register_class(createVerticesFromMesh)
    bpy.utils.register_class(getVertices)
    #bpy.utils.register_class(alignCursor)
    bpy.utils.register_class(setBoneRotation)
    bpy.utils.register_class(setBoneTranslation)
    bpy.utils.register_class(saveBones)
    bpy.utils.register_class(loadBones)
    bpy.utils.register_class(clearBones)
    bpy.utils.register_class(createTriangle)
    bpy.utils.register_class(deleteTriangle)
    bpy.utils.register_class(flipTriangle)
    bpy.utils.register_class(colorTriangle)
    bpy.utils.register_class(saveTriangles)
    bpy.utils.register_class(loadTriangles)
    bpy.utils.register_class(updateTriangles)
    bpy.utils.register_class(clearTriangles)
    bpy.utils.register_class(colorRed)
    bpy.utils.register_class(colorGreen)
    bpy.utils.register_class(colorBlue)
    bpy.utils.register_class(colorBrown)
    bpy.utils.register_class(colorTan)
    bpy.utils.register_class(colorGray)
    bpy.utils.register_class(colorOrange)
    bpy.utils.register_class(colorYellow)

def unregister():
    bpy.utils.unregister_class(LBA2Panel)
    #bpy.utils.unregister_class(returnObjects)
    bpy.utils.unregister_class(exportModel)
    bpy.utils.unregister_class(exportAnimation)
    bpy.utils.unregister_class(scaleUp)
    bpy.utils.unregister_class(scaleDown)
    bpy.utils.unregister_class(createVertex)
    bpy.utils.unregister_class(createVerticesFromMesh)
    bpy.utils.unregister_class(getVertices)
    #bpy.utils.unregister_class(alignCursor)
    bpy.utils.unregister_class(setBoneRotation)
    bpy.utils.unregister_class(setBoneTranslation)
    bpy.utils.unregister_class(saveBones)
    bpy.utils.runegister_class(loadBones)
    bpy.utils.unregister_class(clearBones)
    bpy.utils.unregister_class(createTriangle)
    bpy.utils.unregister_class(deleteTriangle)
    bpy.utils.unregister_class(flipTriangle)
    bpy.utils.unregister_class(colorTriangle)
    bpy.utils.unregister_class(saveTriangles)
    bpy.utils.unregister_class(loadTriangles)
    bpy.utils.unregister_class(updateTriangles)
    bpy.utils.unregister_class(clearTriangles)
    bpy.utils.unregister_class(colorRed)
    bpy.utils.unregister_class(colorGreen)
    bpy.utils.unregister_class(colorBlue)
    bpy.utils.unregister_class(colorBrown)
    bpy.utils.unregister_class(colorTan)
    bpy.utils.unregister_class(colorGray)
    bpy.utils.unregister_class(colorOrange)
    bpy.utils.unregister_class(colorYellow)

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