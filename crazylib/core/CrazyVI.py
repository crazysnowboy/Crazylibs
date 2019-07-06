
import os
import numpy as np


from .pyCrazyCPP import *
from . import pyCrazyCPP

from . import dirs
class PyPangolin():

    def __init__(self,button_list=[]):

        self.conf = config_parameters()
        self.conf.WithPanel=True

        self.cross_datum = CrossDatum()

        for button_name in button_list:
            self.conf.SetGUI_BUTTON(button_name)
            self.cross_datum.InsertButton(button_name,False)

        self.crazy_gui = CrazyGUI(self.conf)

    def run(self):

        while(self.SholudExit()==False):
            pass

    def SholudExit(self):
        res = self.crazy_gui.ShouldExit()
        return res

    def PreCall(self):
        self.crazy_gui.Precall()
    def PostCall(self):
        self.crazy_gui.PostCall()

    def ProcessEvent(self):
        self.crazy_gui.ProcessEvent(tDatum=self.cross_datum)

    def GetView(self):
        return self.crazy_gui.GetViewMatrix()
    def GetDrawMode(self):
        return self.conf.GetDrawMode()

    def CheckButton(self,btn_name):
        return self.cross_datum.CheckButton(btn_name)


class PyRender():

    def __init__(self):
        this_path = dirs.get_file_dir(__file__)
        shader_root=os.path.join(this_path,"shader")
        vert_file=os.path.join("TransformVertexShader.vert")
        frag_file=os.path.join("TextureFragmentShader.frag")
        shader_program = loadProgramFromFile(vert_file,frag_file,shader_root)
        self.render = pyCrazyCPP.CrazyRender(shader_program)

    def Upload(self,all_mesh):
        self.render.Update(all_mesh)

    def rendering(self,view_matrix,draw_mode):

        self.render.Rendering(view_matrix,draw_mode)

    def UploadGe(self,mesh_ge):
        self.render.UpdateGe(mesh_ge)


def ReadObjMesh(root_path,obj_name):
    obj_mesh = Mesh()
    TinyLoadOBJ(obj_mesh, os.path.join(root_path,obj_name))
    LoadTexture(root_path, obj_mesh)
    return obj_mesh

def CrazyVI_Test():



    gui = PyPangolin(button_list=["next","pre"])
    render = PyRender()

    rendering_mesh = ReadObjMesh("packages/CrazyCPPs/data","face_mesh.obj")
    pyCrazyCPP.BaseOperator__Compute_Face_Vertices_Normals(rendering_mesh)
    pyCrazyCPP.BaseOperator__NormalizeVertices(rendering_mesh)
    render.Upload(rendering_mesh)


    while (gui.SholudExit() == False):
        gui.PreCall()

        gui.ProcessEvent()

        if gui.CheckButton("next"):
            print("next")
        if gui.CheckButton("pre"):
            print("pre")


        render.rendering(gui.GetView(), gui.GetDrawMode())

        gui.PostCall()


