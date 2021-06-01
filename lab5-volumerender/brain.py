#!/usr/bin/env python
#https://github.com/Beastmaster/itk-python-example/blob/master/vtkMarchingCubes.py
#https://lorensen.github.io/VTKExamples/site/Cxx/Modelling/MarchingCubes/#code


from __future__ import print_function

import vtk

#Interactor style that handles mouse
class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self,parent=None):
        self.parent = vtk.vtkRenderWindowInteractor()
        if(parent is not None):
          self.parent = parent

#Loader for our structured dataset
imageReader = vtk.vtkStructuredPointsReader()
imageReader.SetFileName("./data/brain.vtk")
imageReader.Update()
im=imageReader.GetOutput();

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
outlineActor.GetProperty().SetLineWidth(2.0);

#TODO:
#
#Insert isosurfacing, scalebar, and text code here
#
color = vtk.vtkColorTransferFunction()
color.SetColorSpaceToRGB()
color.SetScaleToLinear()
color.AddRGBPoint(-2.34454, 1, 0, 0.0156863)
color.AddRGBPoint(101.074, 0.0823529,0.0196078,1)
color.AddRGBPoint(255, 1,1,1)
output = imageReader.GetOutput()
scalar_range = output.GetScalarRange()
lut = vtk.vtkLookupTable()
lut.Build()
outlineMapper.SetScalarRange(scalar_range)
outlineMapper.SetLookupTable(lut)

#define a piecewise function
opacityFunction = vtk.vtkPiecewiseFunction()
opacityFunction.AddPoint(-2.34454, 0.0)
opacityFunction.AddPoint(18.4996, 0.0)
opacityFunction.AddPoint(74.6183, 0.0384615)
opacityFunction.AddPoint(190.063, 0.371795)
opacityFunction.AddPoint(255, 1)

volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetScalarOpacity(opacityFunction)
volumeProperty.SetColor(color)
volumeProperty.ShadeOff()
volumeProperty.SetInterpolationTypeToLinear()
volumeMapper = vtk.vtkSmartVolumeMapper()
volumeMapper.SetInputData(output)
volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)


#A renderer that renders our geometry into the render window
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.1, 0.1, 0.2)

#Add actors to our renderer
renderer.AddActor(outlineActor)
#TODO: You'll probably need to add additional actors to the scene
renderer.AddVolume(volume)

#The render window
renwin = vtk.vtkRenderWindow()
renwin.SetSize(512, 512);
renwin.AddRenderer(renderer)

#Interactor to handle mouse and keyboard events
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetInteractorStyle(MyInteractorStyle(parent = interactor))
interactor.SetRenderWindow(renwin)

plane = vtk.vtkPlane()
clipper = vtk.vtkCutter()
clipper.SetInputConnection(imageReader.GetOutputPort())
clipper.SetCutFunction(plane)

selectMapper = vtk.vtkPolyDataMapper()
selectMapper.SetInputConnection(clipper.GetOutputPort())
selectMapper.SetScalarModeToUsePointFieldData()
selectMapper.SetColorModeToMapScalars()
selectMapper.ScalarVisibilityOn()
selectMapper.SetScalarRange(imageReader.GetOutputDataObject(0).GetPointData().GetScalars().GetRange())
selectMapper.SelectColorArray('RTData')

selectActor = vtk.vtkLODActor()
selectActor.SetMapper(selectMapper)
selectActor.VisibilityOn()
selectActor.SetScale(1, 1, 1)

# The callback function
def callback(obj, event):
    global plane
    obj.GetRepresentation().GetPlane(plane)
    selectActor.VisibilityOn()

# Create the representation and widget
planeRep = vtk.vtkImplicitPlaneRepresentation()
planeRep.SetPlaceFactor(1)
planeRep.PlaceWidget(imageReader.GetOutput().GetBounds())
planeRep.VisibilityOn()
planeRep.SetNormal(1,1,1)
planeRep.GetPlane(plane)

planeWidget = vtk.vtkImplicitPlaneWidget2()
planeWidget.SetInteractor(interactor)
planeWidget.SetRepresentation(planeRep)
planeWidget.SetEnabled(1)
planeWidget.AddObserver("InteractionEvent", callback)

interactor.Initialize()
interactor.Start()




