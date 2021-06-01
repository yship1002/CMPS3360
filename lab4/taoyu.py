#!/usr/bin/env python
# coding: utf-8

# In[2]:


#!/usr/bin/env python
from __future__ import print_function

import vtk

#Interactor style that handles mouse and keyboard events
isovalue=0.125
class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self,parent=None):
        self.parent = vtk.vtkRenderWindowInteractor()
        if(parent is not None):
          self.parent = parent
        self.AddObserver("KeyPressEvent",self.keyPress)
    
    def keyPress(self,obj,event):
      key = self.parent.GetKeySym()
      global isovalue;
      if(key == "Up"):
        #TODO: have this increase the isovalue
        isovalue+=0.1
        isosurface.SetValue(0, isovalue);
        isosurface.Modified();
        isosurface.Update()
        txt.SetInput("Isovalue: "+str(isovalue))
        renwin.Render();
        print("Up")
      if(key == "Down"):
        #TODO: have this decrease the isovalue
        isovalue-=0.1
        isosurface.SetValue(0, isovalue);
        isosurface.Modified();
        isosurface.Update()
        txt.SetInput("Isovalue: "+str(isovalue))
        renwin.Render();
        print("Down")


#Loader for our structured dataset
imageReader = vtk.vtkStructuredPointsReader()
imageReader.SetFileName("./data/hydrogen.vtk")
imageReader.Update()

#Print dimensions and range of the 3d image
dims = imageReader.GetOutput().GetDimensions()
print("Dimensions of image: " + str(dims[0]) + " x "
      + str(dims[1]) + " x " + str(dims[2]))
range = imageReader.GetOutput().GetScalarRange();
print("Range of image: " + str(range[0]) + " to " +  str(range[1]))

#create an outline that shows the bounds of our dataset
outline = vtk.vtkOutlineFilter();
outline.SetInputConnection(imageReader.GetOutputPort());
#mapper to push the outline geometry to the graphics library
outlineMapper = vtk.vtkPolyDataMapper();
outlineMapper.SetInputConnection(outline.GetOutputPort());
#actor for the outline to add to our renderer
outlineActor = vtk.vtkActor();
outlineActor.SetMapper(outlineMapper);
outlineActor.GetProperty().SetLineWidth(2);

#TODO:
#
#Insert isosurfacing, scalebar, and text code here
#
color = vtk.vtkColorTransferFunction()
color.SetColorSpaceToRGB()
color.SetScaleToLinear()
color.AddRGBPoint(0.0, 0.085, 0.932, 0.201)
color.AddRGBPoint(1.0, 1,1,1)

output = imageReader.GetOutput()
scalar_range = output.GetScalarRange()
lut = vtk.vtkLookupTable()
lut.Build()
outlineMapper.SetScalarRange(scalar_range)
outlineMapper.SetLookupTable(lut)

isosurface = vtk.vtkMarchingCubes();
isosurface.SetInputData(output);
isosurface.ComputeNormalsOn();
isosurface.ComputeGradientsOn();
isosurface.SetValue(0, isovalue);
isosurface.Update();

isosurfaceMapper = vtk.vtkPolyDataMapper()
isosurfaceMapper.SetInputConnection(isosurface.GetOutputPort())
isosurfaceActor = vtk.vtkActor();
isosurfaceMapper.SetLookupTable(color)
isosurfaceActor.SetMapper(isosurfaceMapper);
isosurfaceActor.GetProperty().SetLineWidth(2.0);

txt = vtk.vtkTextActor()
txt.SetInput("Isovalue: "+str(isovalue))
txtprop=txt.GetTextProperty()
txtprop.SetFontFamilyToArial()
txtprop.SetFontSize(10)
txtprop.SetColor(1,1,1)
txt.SetDisplayPosition(0,0)

#A renderer that renders our geometry into the render window
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.1, 0.1, 0.2)

#Add actors to our renderer
renderer.AddActor(outlineActor)
#TODO: You'll probably need to add additional actors to the scene
renderer.AddActor(isosurfaceActor)
renderer.AddActor(txt)

#The render window
renwin = vtk.vtkRenderWindow()
renwin.SetSize(512, 512);
renwin.AddRenderer(renderer)

#Interactor to handle mouse and keyboard events
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetInteractorStyle(MyInteractorStyle(parent = interactor))
interactor.SetRenderWindow(renwin)

# create the scalar_bar
scalar_bar = vtk.vtkScalarBarActor()
scalar_bar.SetOrientationToHorizontal()
scalar_bar.SetLookupTable(lut)


scalar_bar.SetLookupTable(color)

# create the scalar_bar_widget
scalar_bar_widget = vtk.vtkScalarBarWidget()
scalar_bar_widget.SetInteractor(interactor)
scalar_bar_widget.SetScalarBarActor(scalar_bar)
scalar_bar_widget.On()

interactor.Initialize()
interactor.Start()

