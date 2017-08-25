#Author-Sterling Crispin
#Description-see https://www.instructables.com/id/Parametric-Modeling-With-Fusion-360-API/

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

        splineSegments = 10
        tubeCount = 15
        tubeLength = 10
        xstep = 0
        for j in range(tubeCount):
            radius = j/(tubeCount) + 0.1
            xstep += (radius * 2)
            for i in range(splineSegments):
                # from 0 to TWOPI radians as i increases 
                p = (i/splineSegments) * math.pi * 2
                # scaled in intensity by each tube
                p = p * (j/tubeCount) 
                taper = (j*i*0.05)
                length = ((tubeLength * j/tubeCount) / splineSegments) + 0.1
                points.add(adsk.core.Point3D.create( math.cos(p) + xstep , math.sin(p) - taper , length * i  ))
                
            # Create a spline along those points
            spline = sketch.sketchCurves.sketchFittedSplines.add(points)
            
            # Create a circle at the beginning of the spline
            circles = sketch.sketchCurves.sketchCircles
            circle1 = circles.addByCenterRadius(points[0], radius)
            
            # Create a sweep input
            # there's probably a better way of getting the profile of the Circle but I don't know it
            prof = sketch.profiles.item(j)
            path = rootComp.features.createPath(spline)
            sweeps = rootComp.features.sweepFeatures
            sweepInput = sweeps.createInput(prof,path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

            # Create the sweep.
            sweep = sweeps.add(sweepInput)
             #delete any old points
            points = adsk.core.ObjectCollection.create()


    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))