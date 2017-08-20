#Author-Sterling Crispin
#Description-directly adapted from http://help.autodesk.com/view/fusion360/ENU/?guid=GUID-c3d4a306-fade-11e4-8e56-3417ebd3d5be


import adsk.core, adsk.fusion, traceback
import math

def run(context):
    ui = None
    try: 
        app = adsk.core.Application.get()
        ui = app.userInterface

        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

        # Get the root component of the active design.
        rootComp = design.rootComponent

        # Create a new sketch on the xy plane.
        sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)

        # Create an object collection for the points.
        points = adsk.core.ObjectCollection.create()

        
        # Define the points the spline with fit through.
        for i in range(10):
            p = (i/9) * math.pi * 2;
            points.add(adsk.core.Point3D.create( math.cos(p), math.sin(p), i))

        # Create the spline.
        sketch.sketchCurves.sketchFittedSplines.add(points)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))