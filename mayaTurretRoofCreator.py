import maya.cmds as cmds
import math

#Set turret attributes:
numberOfRows = 7
height = 1.5
width = 2.0
depth = width

#Make turret shape:
turret = cmds.polyCube(name="turret", h=height, w=width, d=depth)
cmds.move(0,height/2,0)
cmds.select(turret[0]+'.f[1]')
cmds.scale(0.1,0.1,0, xz=True)
cmds.select(turret[0]+'.f[3]', r=True)
cmds.delete()
cmds.select(turret[0])

#Add rows to turret:
for rowNumber in range(1,numberOfRows):
    cmds.polyCut(rx=90, pcy=rowNumber*height/numberOfRows)

#Add tiles to turret:
for i in range(2):
    for rowNumber in range(numberOfRows):
        for tileNumber in range(1, numberOfRows-rowNumber):
            
            #Create lists of all faces in turret:
            list1 = []
            list2 = []
            numberOfFaces=cmds.polyEvaluate('turret',f=True)
            for faceNumber in range(numberOfFaces):
                list1.append(turret[0]+'.f['+str(faceNumber)+']')
                list2.append(turret[0]+'.f['+str(faceNumber)+']')
            
            #Remove all faces not in the current row from list2:
            y1 = rowNumber*height/numberOfRows
            y2 = (rowNumber+1)*height/numberOfRows
            for face in list1:
                cmds.select(face,r=True)
                yValues = cmds.polyEvaluate(bc=True)[1]
                centre = (yValues[0]+yValues[1])/2
                if centre<=y1 or centre>=y2:
                    list2.remove(face)
            cmds.select(cl=True)
            
            #Cut selected face along varied angles to create tiles
            for face in list2:
                cmds.select(face,add=True)            
            angle = float(numberOfRows-rowNumber-2*tileNumber)/float(numberOfRows-rowNumber)
            cmds.polyCut(ry = i*90 + math.atan(angle)*180.0/math.pi)  
            print i, ' ', rowNumber, ' ', tileNumber, '\n'

#Extrude tiles
cmds.select(turret[0]+'.f[*]', r=True)
cmds.polyExtrudeFacet(kft=False, d=2, lt=[0,0,0.03], off=0.05, ls=[0.8,0.8,0.8])