
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
        self.PreCall()
        self.ProcessEvent()

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


def ReadObjMesh(root_path="",obj_name=""):
    this_path = dirs.get_file_dir(__file__)
    obj_root_path = os.path.join(this_path, "data")
    if root_path=="":
        root_path=obj_root_path
        obj_name="face_mesh.obj"

    obj_mesh = Mesh()
    TinyLoadOBJ(obj_mesh, os.path.join(root_path,obj_name))
    LoadTexture(root_path, obj_mesh)
    return obj_mesh

def CrazyVI_Test():



    gui = PyPangolin(button_list=["next","pre"])
    render = PyRender()

    rendering_mesh = ReadObjMesh()
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


class BaseGUIManager():
    def __init__(self):
        self.conf = pyCrazyCPP.config_parameters()
        self.cross_datum = pyCrazyCPP.CrossDatum()
        self.basic_tool = pyCrazyCPP.BaseOperator()

        self.conf.WithPanel = True

        self.crazy_gui = pyCrazyCPP.CrazyGUI(self.conf)
        
        
        this_path = dirs.get_file_dir(__file__)
        shader_root=os.path.join(this_path,"shader")
        vert_file=os.path.join("TransformVertexShader.vert")
        frag_file=os.path.join("TextureFragmentShader.frag")
        shader_program = loadProgramFromFile(vert_file,frag_file,shader_root)
        self.renderer = pyCrazyCPP.CrazyRender(shader_program)


    def add_box(self,name,state):
        self.conf.SetGUI_CHECKBOX(name,state)
        self.cross_datum.InsertBox(name, state)

    def add_button(self,name,state):
        self.conf.SetGUI_BUTTON(name)
        self.cross_datum.InsertButton(name, state)

    def add_databar(self,name, s, m, e):

        self.conf.SetGUI_DataBar(name,s,m,e)
        self.cross_datum.InsertData(name, 0.0)
    def update_gui(self):

        self.crazy_gui.UpdateUI(self.conf)

    def CheckBox(self,controller):
        return  self.cross_datum.CheckBox(controller)

    def CheckMouseButton(self,name):
        return  self.cross_datum.CheckMouseButton(name)

    def GetMouse(self,name):
        return  self.cross_datum.GetMousePosition(name)


    def CheckSwitch(self,name):
        return  self.cross_datum.CheckSwitch(name)

    def CheckSwitchBox(self,name,bool):
        return  self.cross_datum.CheckSwitchBox(name,bool)



    def CheckButton(self,controller):
        return  self.cross_datum.CheckButton(controller)

    def Update(self,mesh,flag="mesh"):

        if flag=="ge":
            self.renderer.UpdateGe(mesh)
        elif flag =="mesh":
            self.renderer.Update(mesh)


    def PostProcess(self,draw_axis=False,scale =1.0):

        if(draw_axis==True):
            lines = [
                np.array([[0, 0, -1.0], [0, 0, 1.0]]),
                np.array([[0, -1.0, 0], [0, 1.0, 0]]),
                np.array([[-1.0, 0, 0], [1.0, 0, 0]]),
            ]
            for line in lines:
                src_pts = line[0,:]*scale
                dst_pts = line[1,:]*scale
                self.basic_tool.DrawLine(float(src_pts[0]), float(src_pts[1]), float(src_pts[2]),
                                     float(dst_pts[0]), float(dst_pts[1]), float(dst_pts[2]),
                                     0.0, 1.0, 0.0)

        self.renderer.Rendering(self.crazy_gui.GetViewMatrix(), self.conf.GetDrawMode())
        self.crazy_gui.PostCall()

    def ShouldExit(self):
        res = self.crazy_gui.ShouldExit()
        self.crazy_gui.Precall()
        self.crazy_gui.ProcessEvent(self.cross_datum)


        return res

