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
        for j in range(10):
            for i in range(10):
                # from 0 to TWOPI radians as i increases 
                p = (i/10-1) * math.pi * 2
                # scaled in intensity by each tube
                p = p * (j/10-1) 
                # so the tubes aren't ontop of one another
                xstep = j * 2
                points.add(adsk.core.Point3D.create( math.cos(p) + xstep , math.sin(p) , i ))
                
            # Create a spline along those points
            spline = sketch.sketchCurves.sketchFittedSplines.add(points)
            
             #delete any old points
            points = adsk.core.ObjectCollection.create()
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))