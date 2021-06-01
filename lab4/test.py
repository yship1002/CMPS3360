#!/usr/bin/env/ python
import vtk
a=vtk.vtkColorTransferFunction()
a.AddRGBPoint(0,0,1,0)
a.AddRGBPoint(10,1,0,0)
b=a.GetColor(1)
print(b)
