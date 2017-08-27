#Author-Sterling Crispin
#Description-see https://www.instructables.com/id/Parametric-Modeling-With-Fusion-360-API/

import adsk.core, adsk.fusion, traceback
import math

def sweepNormalToSpline(spline,radius,rootComp):    
    path = rootComp.features.createPath(spline)
    # create construction plane normal to the spline
    planes = rootComp.constructionPlanes
    planeInput = planes.createInput()
    planeInput.setByDistanceOnPath(path, adsk.core.ValueInput.createByReal(0))
    plane = planes.add(planeInput)
    
    sketches = rootComp.sketches
    sketch = sketches.add(plane)
    
    center = plane.geometry.origin
    center = sketch.modelToSketchSpace(center)
    sketch.sketchCurves.sketchCircles.addByCenterRadius(center, radius)
    profile = sketch.profiles[0]
    
    # Create a sweep input
    sweeps = rootComp.features.sweepFeatures
    sweepInput = sweeps.createInput(profile,path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    sweepInput.orientation = adsk.fusion.SweepOrientationTypes.PerpendicularOrientationType
    
    # Create the sweep.
    sweep = sweeps.add(sweepInput)
    return sweep

def chamferSweep(sweep,chamferDistance,rootComp):
    #prepare chamfer
    faces = sweep.faces
    edges  = adsk.core.ObjectCollection.create()
    for f in range(faces.count):
        for e in range(faces.item(f).edges.count):
            edges.add(faces.item(f).edges.item(e))
        
    chamfers = rootComp.features.chamferFeatures
    
    chamferInput = chamfers.createInput(edges,False)
    chamferInput.setToEqualDistance(adsk.core.ValueInput.createByReal(chamferDistance))
    
    chamfer = chamfers.add(chamferInput)

def run(context):
    ui = None
    try: 
        app = adsk.core.Application.get()
        ui = app.userInterface

        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct
        # This changes the model so it's no longer capturing the parametric history.
        # increases speed and declutters history
        design.designType = adsk.fusion.DesignTypes.DirectDesignType

        # Get the root component of the active design.
        rootComp = design.rootComponent

        # Create a new sketch on the xy plane.
        sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
        
        # Create an object collection for the points.
        pointsA = adsk.core.ObjectCollection.create()
        pointsB = adsk.core.ObjectCollection.create()
        
        pointsTemp = adsk.core.ObjectCollection.create()
        
        splineSegments = 5
        tubeCount = 10
        tubeLength = 10
        xstep = 0
        minLength = tubeLength * 0.05
        maxRadius = 0.5
        for j in range(tubeCount):
            radius = (j/tubeCount) * maxRadius + 0.1
            xstep += (radius * 3)
            for i in range(splineSegments):
                # from 0 to TWOPI radians as i increases 
                p = (i/splineSegments) * math.pi * 2
                # scaled in intensity by each tube
                p = p * (j/tubeCount) 
                taper = (j*i*0.05)
                length = ((tubeLength * j/tubeCount) / splineSegments) + minLength
                x = math.cos(p) + xstep
                y = math.sin(p) + taper
                z = length * i 
                pointsTemp.add(adsk.core.Point3D.create( x , y , z ))
                #these are kept for later
                pointsA.add(adsk.core.Point3D.create( x , y , z ))

            # Create a spline along points
            spline = sketch.sketchCurves.sketchFittedSplines.add(pointsTemp)

            #   call our handy functions
            sweep = sweepNormalToSpline(spline,radius,rootComp)
            chamferDistance = radius * 0.5
            chamferSweep(sweep,chamferDistance,rootComp)
            
             #delete any old points
            pointsTemp = adsk.core.ObjectCollection.create()
         
        # Create a new sketch on the yZ plane.
        sketch2 = rootComp.sketches.add(rootComp.yZConstructionPlane)
        
        radius =  (minLength / splineSegments) * 1.8
        # now we're going across the prior form connecting each tube
        for j in range(splineSegments):
            for i in range(tubeCount):
                index =  i  * splineSegments + j
                # points appear to be in relationship to their construction plane requiring a transformation here
                x = pointsA.item(index).z * -1
                y = pointsA.item(index).y
                z = pointsA.item(index).x 
                pointsB.add(adsk.core.Point3D.create(x,y,z))
            
            # Create a spline along points
            spline = sketch2.sketchCurves.sketchFittedSplines.add(pointsB)
            
            #   call our handy function
            sweep = sweepNormalToSpline(spline,radius,rootComp)
            chamferDistance = radius * 0.5
            chamferSweep(sweep,chamferDistance,rootComp)

             #delete any old points
            pointsB = adsk.core.ObjectCollection.create()
            
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))