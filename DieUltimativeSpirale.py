import numpy as np
from scipy.special import fresnel
import gmsh
import sys
import math
import os
import matplotlib.pyplot as plt
from sympy import *

#Phase 0

askShowcase = input("Showcase? (J/N) ")
if askShowcase == "J":
    showcase = True
else: 
    showcase = False


askmodification = input("KSS an? (J/N) ")
if askmodification == "J":
    modification = np.sqrt
    modiBool = True
else: 
    modiBool = False

asktime = input("Wie viel Uhr? (0-4) ")
phase = float(asktime)
"""
askthick = input("Spandicke? (Empfehlung: 0.1) ")
thick = float(askthick)
"""
thick = 0.1



askquantity = input("Wie viele Elemente auf Hauptspline? Jeder weitere Spline jeweils plus 1 Element (Empfehlung: 50) ")
quantity = int(askquantity)

#Endgeometrie
if (phase > 3):
        
    Spandau = gmsh.model.occ
    gmsh.initialize()
    #gmsh.merge('./Spanraum.geo')


    radiusCurrent = 2
    thickTransfi = 0.1
    yFloor = -2.375
    xStart = 0.09
    wide = 1.25
    Spandau.addCylinder(xStart - radiusCurrent , yFloor+radiusCurrent, 0, 0, 0, wide, radiusCurrent, tag=101010, angle=2*pi)
    Spandau.addCylinder(xStart - radiusCurrent , yFloor+radiusCurrent, 0, 0, 0, wide, radiusCurrent-thickTransfi, tag=202020, angle=2*pi)
    Spandau.addCylinder(xStart - radiusCurrent , yFloor+radiusCurrent, 0, 0, 0, wide, radiusCurrent, tag=303030, angle=pi)
    Spandau.addCylinder(xStart - radiusCurrent , yFloor+radiusCurrent, 0, 0, 0, wide, radiusCurrent-thickTransfi, tag=404040, angle=pi)
    Spandau.cut([(3,101010)],[(3,202020)],tag=505050)
    Spandau.cut([(3,303030)],[(3,404040)],tag=606060)
    Spandau.cut([(3,505050)],[(3,606060)],tag=707070)


    Spandau.addCylinder(xStart - radiusCurrent , yFloor+radiusCurrent, 0, 0, 0, wide, radiusCurrent, tag=808080, angle=pi)
    Spandau.addCylinder(xStart - radiusCurrent , yFloor+radiusCurrent, 0, 0, 0, wide, radiusCurrent-thickTransfi, tag=909090, angle=pi)
    Spandau.cut([(3,808080)],[(3,909090)],tag=1010101)





    Spandau.synchronize()





    gmsh.model.mesh.setTransfiniteCurve(2, 50)
    gmsh.model.mesh.setTransfiniteCurve(2, 50)
    gmsh.model.mesh.setTransfiniteCurve(4, 50)
    gmsh.model.mesh.setTransfiniteCurve(9, 50)
    gmsh.model.mesh.setTransfiniteCurve(12, 50)
    gmsh.model.mesh.setTransfiniteCurve(13, 50)
    gmsh.model.mesh.setTransfiniteCurve(15, 50)
    gmsh.model.mesh.setTransfiniteCurve(18, 50)
    gmsh.model.mesh.setTransfiniteCurve(23, 50)

    gmsh.model.mesh.setTransfiniteCurve(1, 20)
    gmsh.model.mesh.setTransfiniteCurve(5, 20)
    gmsh.model.mesh.setTransfiniteCurve(11, 20)
    gmsh.model.mesh.setTransfiniteCurve(3, 20)
    gmsh.model.mesh.setTransfiniteCurve(14, 20)
    gmsh.model.mesh.setTransfiniteCurve(16, 20)
    gmsh.model.mesh.setTransfiniteCurve(21, 20)
    gmsh.model.mesh.setTransfiniteCurve(24, 20)


    gmsh.model.mesh.setTransfiniteCurve(7, 3)
    gmsh.model.mesh.setTransfiniteCurve(6, 3)
    gmsh.model.mesh.setTransfiniteCurve(10, 3)
    gmsh.model.mesh.setTransfiniteCurve(8, 3)
    gmsh.model.mesh.setTransfiniteCurve(17, 3)
    gmsh.model.mesh.setTransfiniteCurve(19, 3)
    gmsh.model.mesh.setTransfiniteCurve(20, 3)
    gmsh.model.mesh.setTransfiniteCurve(22, 3)





    gmsh.model.mesh.setTransfiniteSurface(1)

    gmsh.model.mesh.setTransfiniteSurface(2)

    gmsh.model.mesh.setTransfiniteSurface(3)

    gmsh.model.mesh.setTransfiniteSurface(4)

    gmsh.model.mesh.setTransfiniteSurface(5)

    gmsh.model.mesh.setTransfiniteSurface(6)

    gmsh.model.mesh.setTransfiniteSurface(7)

    gmsh.model.mesh.setTransfiniteSurface(8)

    gmsh.model.mesh.setTransfiniteSurface(9)

    gmsh.model.mesh.setTransfiniteSurface(10)

    gmsh.model.mesh.setTransfiniteSurface(11)

    gmsh.model.mesh.setTransfiniteSurface(12)


    gmsh.model.mesh.setTransfiniteVolume(1010101)
    gmsh.model.mesh.setTransfiniteVolume(707070)


    gmsh.model.mesh.generate(3)
    gmsh.write("Spirale.msh")
    gmsh.write("Spirale.stl")
    gmsh.fltk.run()
    gmsh.clear()
    gmsh.finalize()





#Spanbildungsgeometrie
if (phase <= 3):
    thickTransfi = 0.1

    VerschiebungY = 2.37469
    VerschiebungX = 4.25

    start = int(0)#Startpunkt des Kringels
    end = int(2) #Endpunkt des Kringels
    definition = 1000000
    quantityCalc = int(end * definition) #Anzahl der Punkte des Kringels
    u = np.linspace(start, end, quantityCalc) #Erzeugt die gewünschte Anzahl an Punkten zwischen Start und Endpunkt (+1 da die ableitung für die Normalenvektoren und dadurch das +1. Element genutzt wird)
    function = fresnel


    if modiBool == True:
        sin, cos = modification(function(u)) #Erzeugt das Fresnelintegral #modification(function(u))
        
    else:
        sin, cos = (function(u))
        

    x = sin 
    y = cos 
    xShift = 0
    yShift = 0
    zShift = 0 #Verschiebung in Z-Richtung
    zoom = 1.5 #Größe des Kringels
    plt.plot(x, y, 'red')
    #plt.savefig('foo.png')

    #Die Kooridnaten werden in Arrays abgepackt
    coordsXCalc = (x)
    resultXCalc = []

    coordsYCalc = (y)
    resultYCalc = []

    def getInArray(xList, xArray , yList, yArray):
        for x in xList:
            xArray.append(x)
            
        for y in yList:
            yArray.append(y)         
    getInArray(coordsXCalc, resultXCalc, coordsYCalc, resultYCalc)

    #Löscht jeden Eintrag aus den Koordinaten-Arrays
    def resetCoords (xList,yList):
        del xList[:]
        del yList[:]

    #Y-Koordinatenwert nach 180°
    def getYValuePi(xList, yList):
        xPosition = np.where(xList == np.amax(xList))
        xPositionArray = xPosition[0]#Y-Koordinatenwert nach 90°zoom = 10 #Größe des Kringels
        xPositionInt = xPositionArray[0]
        yValuePi = yList[xPositionInt]
        return yValuePi
    #print(getYValuePi(resultXCalc, resultYCalc))

    #X-Koordinatenwert nach 180°
    def getXValuePi(xList, yList):
        xPosition = np.where(xList == np.amax(xList))
        xPositionArray = xPosition[0]
        xPositionInt = xPositionArray[0]
        xValuePi = xList[xPositionInt]
        return xValuePi
    #print(getXValuePi(resultXCalc, resultYCalc))

    #Arrayindex für die Koordinaten bei 180°
    def getIndexPi(xList, yList):    
        xPosition = np.where(xList == np.amax(xList))
        xPositionArray = xPosition[0]#Y-Koordinatenwert nach 90°
        xPositionInt = xPositionArray[0]
        return xPositionInt
    #print(getIndexPi(resultXCalc, resultYCalc))

    #Y-Koordinatenwert nach 90°
    def getYValuePiHalf(xList, yList):    
        yPosition = np.where(yList == np.amax(yList))
        yPositionArray = yPosition[0]
        yPositionInt = yPositionArray[0]
        yValuePiHalf = yList[yPositionInt]
        return yValuePiHalf
    #print(getYValuePiHalf(resultXCalc,resultYCalc))

    #Arrayindex für die Koordinaten bei 90°
    def getYIndexPiHalf(xList, yList):    
        yPosition = np.where(yList == np.amax(yList))
        yPositionArray = yPosition[0]
        yIndexPiHalf = yPositionArray[0]
        return yIndexPiHalf
    #print(getYIndexPiHalf(resultXCalc,resultYCalc))

    #Arrayindex für die Koordinaten bei 270°
    def getYIndex3PiHalf(xList, yList):
        xPosition = np.where(xList == np.amax(xList))
        xPositionArray = xPosition[0]
        xPositionInt = xPositionArray[0]
        cutList = yList[xPositionInt:]
        minPosition = np.where(cutList == np.amin(cutList))
        minPositionArray = minPosition[0]
        yIndex3PiHalf = minPositionArray[0]+xPositionInt
        return yIndex3PiHalf
    #print(getYIndex3PiHalf(resultXCalc,resultYCalc))

    #Y-Koordinatenwert nach 270°
    def getYValue3PiHalf(xList, yList):
        
        xPosition = np.where(xList == np.amax(xList))
        xPositionArray = xPosition[0]
        xPositionInt = xPositionArray[0]
        cutList = yList[xPositionInt:]
        yValue3PiHalf = np.amin(cutList)
        return yValue3PiHalf
    #print(getYValue3PiHalf(resultXCalc,resultYCalc))


    def getYIndexZero(xList, yList):
        yIndexZero = next(x[0] for x in enumerate(yList) if x[1] > -0.000000000000001)
        return yIndexZero
    #print(getYIndexZero(resultXCalc,resultYCalc))

    def getYValueZero(xList, yList):
        yIndexZero = next(x[0] for x in enumerate(yList) if x[1] > -0.000000000000001)
        yValueZero = yList[yIndexZero]
        return(yValueZero)
    #print(getYValueZero(resultXCalc, resultYCalc))

    def getXValueZero(xList, yList):
        yIndexZero = next(y[0] for y in enumerate(yList) if y[1] >= 0)
        xValueZero = xList[yIndexZero]
        return(xValueZero)
    #print(getXValueZero(resultXCalc,resultYCalc))

    #Erstellung der Normalenvektoren
    def normal(xValue, yValue, xList, yList):
        for idx in range(len(x)-1):
            x0, y0, x1, y1 = xValue[idx], yValue[idx], xValue[idx+1], yValue[idx+1]
            dx = x1-x0 #Ableitungen
            dy = y1-y0
            norm = math.hypot(dx, dy) * 1/(thick+thickTransfi+thick) #Normierung
            dx /= norm
            dy /= norm
            xc = x0-dy #Vekotor+Original
            xc = round(xc,3)
            yc = y0+dx
            yc = round(yc,3)
            xList.append(xc)#Einfügen in die Arrays
            yList.append(yc)

    #Erstellung der Normalenvektoren für die Netzschicht in die 1. Richtung
    def normalTransfi(xValue, yValue, xList, yList):
        for idx in range(len(x)-1):
            x0, y0, x1, y1 = xValue[idx], yValue[idx], xValue[idx+1], yValue[idx+1]
            dx = x1-x0 #Ableitungen
            dy = y1-y0
            norm = math.hypot(dx, dy) * 1/(thickTransfi) #Normierung
            dx /= norm
            dy /= norm
            xc = x0-dy #Vekotor+Original
            xc = round(xc,3)
            yc = y0+dx
            yc = round(yc,3)
            xList.append(xc)#Einfügen in die Arrays
            yList.append(yc)

    #Erstellung der Normalenvektoren für die Netzschicht in die 2. Richtung
    def normalTransfi2(xValue, yValue, xList, yList):
        for idx in range(len(x)-1):
            x0, y0, x1, y1 = xValue[idx], yValue[idx], xValue[idx+1], yValue[idx+1]
            dx = x1-x0 #Ableitungen
            dy = y1-y0
            norm = math.hypot(dx, dy) * 1/(thick+thickTransfi) #Normierung
            dx /= norm
            dy /= norm
            xc = x0-dy #Vekotor+Original
            xc = round(xc,3)
            yc = y0+dx
            yc = round(yc,3)
            xList.append(xc)#Einfügen in die Arrays
            yList.append(yc)


    #phase 1
    finalList = []


    #Berechnung des Endpunkts und der Position für die entsprechenden Phasen

    def phase1(phaseList, status):
        del phaseList[:]
        spiralProgress = status

        yShift = getYValuePi(resultXCalc,resultYCalc)
        xShift = 0
        resetCoords(resultXCalc, resultYCalc)
        x = sin + xShift
        y = cos - yShift
        coordsXPhase = (x)
        coordsYPhase = (y)
        getInArray(coordsXPhase, resultXCalc, coordsYPhase, resultYCalc)
        yShift1 = getYValueZero(resultXCalc,resultYCalc)
        xShift1 = getXValueZero(resultXCalc, resultYCalc)
        resetCoords(resultXCalc, resultYCalc)
        
        x = sin - xShift1
        y = cos - yShift - yShift1
        coordsXPhase01 = (x)
        coordsYPhase01 = (y)
        getInArray(coordsXPhase01, resultXCalc, coordsYPhase01, resultYCalc)
        IndexPi = getIndexPi(resultXCalc, resultYCalc)
        IndexZero = getYIndexZero(resultXCalc, resultYCalc)
        startPhase = (1/definition) * (IndexZero+1)
        

        spiralProgress < 0.1
        percent = spiralProgress * 10
        endPhaseSpan = ((1/definition) * (IndexPi+1)) * percent
        endPhase = (1/definition) * (IndexPi+1)
        zoomPhase = zoom
        
        finalXShift = -xShift1
        finalYShift = -(yShift + yShift1)
    
        
        phaseList.insert(0,startPhase)
        phaseList.insert(1,endPhaseSpan)
        phaseList.insert(2,finalXShift)
        phaseList.insert(3,finalYShift)
        phaseList.insert(4,zoomPhase)
        
    if (phase < 0.1):
        phase1(finalList, phase)


    def phase11(phase1List, status):
        del phase1List[:]
        spiralProgress = status

        yShift = getYValuePi(resultXCalc,resultYCalc)
        xShift = 0
        resetCoords(resultXCalc, resultYCalc)
        x = sin + xShift
        y = cos - yShift
        coordsXPhase1 = (x)
        coordsYPhase1 = (y)
        getInArray(coordsXPhase1, resultXCalc, coordsYPhase1, resultYCalc)
        yShift1 = getYValueZero(resultXCalc,resultYCalc)
        xShift1 = getXValueZero(resultXCalc, resultYCalc)
        resetCoords(resultXCalc, resultYCalc)
        
        x = sin - xShift1
        y = cos - yShift - yShift1
        coordsXPhase11 = (x)
        coordsYPhase11 = (y)
        getInArray(coordsXPhase11, resultXCalc, coordsYPhase11, resultYCalc)
        IndexPi = getIndexPi(resultXCalc, resultYCalc)
        IndexZero = getYIndexZero(resultXCalc, resultYCalc)
        startPhase1 = (1/definition) * (IndexZero+1)
        
        endPhase1 = (1/definition) * (IndexPi+1)
        zoomPhase1 = zoom + (zoom*spiralProgress)

        finalXShift1 = -xShift1
        finalYShift1 = -(yShift + yShift1)
    
        
        phase1List.insert(0,startPhase1)
        phase1List.insert(1,endPhase1)
        phase1List.insert(2,finalXShift1)
        phase1List.insert(3,finalYShift1)
        phase1List.insert(4,zoomPhase1)


    if (phase <= 1 and phase >=0.1):
        phase11(finalList, phase)


    def phase2(phase2List, status):
        
        zoomPhase1 = 2*zoom
        
        
        del phase2List[:]
        spiralProgress = status-1
        
        
        endPhase1Index = getIndexPi(resultXCalc, resultYCalc)
        endPahse2Index = getYIndex3PiHalf(resultXCalc,resultYCalc)
        PhaseDiff = endPahse2Index-endPhase1Index
        currentIndex = PhaseDiff*spiralProgress
        currentIndexInt = int(currentIndex) +endPhase1Index
        
        if spiralProgress <= 0.5:
            extraShiftInY = 0.1*(spiralProgress*2) 
        else:
            extraShiftInY = 0.1
        
        
        yShift = resultYCalc[currentIndexInt]-extraShiftInY
        xCheck = resultXCalc[currentIndexInt]
        xShift = 0
        resetCoords(resultXCalc, resultYCalc)
        x = sin + xShift
        y = cos - yShift
        coordsXPhase2 = (x)
        coordsYPhase2 = (y)
        getInArray(coordsXPhase2, resultXCalc, coordsYPhase2, resultYCalc)
        yShift1 = getYValueZero(resultXCalc,resultYCalc)
        xShift1 = getXValueZero(resultXCalc, resultYCalc)
        resetCoords(resultXCalc, resultYCalc)
        
        x = sin - xShift1
        y = cos - yShift - yShift1
        coordsXPhase21 = (x)
        coordsYPhase21 = (y)
        getInArray(coordsXPhase21, resultXCalc, coordsYPhase21, resultYCalc)
        IndexZero = getYIndexZero(resultXCalc, resultYCalc)
        startPhase1 = (1/definition) * (IndexZero+1)
    
        endPhase1 = (1/definition) * (currentIndexInt+1)
        

        finalXShift1 = -xShift1
        finalYShift1 = -(yShift + yShift1)
    
        
        phase2List.insert(0,startPhase1)
        phase2List.insert(1,endPhase1)
        phase2List.insert(2,finalXShift1)
        phase2List.insert(3,finalYShift1)
        phase2List.insert(4,zoomPhase1)


    if (phase > 1 and phase <= 2):
        phase2(finalList, phase)



    def phase3(phase3List, status):
        del phase3List[:]
        spiralProgress = status-2
        extraShiftInY = spiralProgress*0.025

        yShift = getYValue3PiHalf(resultXCalc,resultYCalc)-(0.1 - extraShiftInY)
        
        xShift = 0
        resetCoords(resultXCalc, resultYCalc)
        x = sin + xShift
        y = cos - yShift
        coordsXPhase3 = (x)
        coordsYPhase3 = (y)
        getInArray(coordsXPhase3, resultXCalc, coordsYPhase3, resultYCalc)
        yShift3 = getYValueZero(resultXCalc,resultYCalc)
        xShift3 = getXValueZero(resultXCalc, resultYCalc)
        resetCoords(resultXCalc, resultYCalc)
        
        x = sin - xShift3
        y = cos - yShift - yShift3
        coordsXPhase31 = (x)
        coordsYPhase31 = (y)
        getInArray(coordsXPhase31, resultXCalc, coordsYPhase31, resultYCalc)
        Index3PiHalf = getYIndex3PiHalf(resultXCalc, resultYCalc)
        IndexZero = getYIndexZero(resultXCalc, resultYCalc)
        startPhase3 = (1/definition) * (IndexZero+1)
        
        endPhase3 = (1/definition) * (Index3PiHalf+1)
        zoomPhase3 = 2*zoom + spiralProgress

        finalXShift3 = -xShift3
        finalYShift3 = -(yShift + yShift3)
    
        height = getYValue3PiHalf(resultXCalc, resultYCalc)

        
        phase3List.insert(0,startPhase3)
        phase3List.insert(1,endPhase3)
        phase3List.insert(2,finalXShift3)
        phase3List.insert(3,finalYShift3)
        phase3List.insert(4,zoomPhase3)
        phase3List.insert(5,height)
        phase3List.insert(6,spiralProgress)


    if (phase > 2 and phase <= 3):
        phase3(finalList, phase)


    end = finalList[1]
    start = finalList[0]
    xShift = finalList[2]
    yShift = finalList[3]
    zoom = finalList[4]


    Spandau = gmsh.model.occ
    gmsh.initialize()
    if (showcase == True):
        gmsh.merge('./Spanraum.geo')

    #quantity = 50 #Anzahl der Punkte des Kringels
    wide = 1.25 #Breite des Spans
    lc = -1.0 #Netzdichte an den Punkten des Kringels


    t = np.linspace(start, end, quantity) #Erzeugt die gewünschte Anzahl an Punkten zwischen Start und Endpunkt (+1 da die ableitung für die Normalenvektoren und dadurch das +1. Element genutzt wird)
    tTransfi = np.linspace(start, end, quantity)

    if modiBool == True:
        sin, cos = modification(function(t)) #Erzeugt das Fresnelintegral #modification(function(u))
        sinTransfi, cosTransfi = modification(function(tTransfi))
    else:
        sin, cos = (function(t))
        sinTransfi, cosTransfi = (function(tTransfi)) 

    #Fügt alle Parameter für X und Y zusammen und erzeugt die X und Y Koordinaten

    x = ((sin)*zoom) + (xShift*zoom) - VerschiebungX 
    xTransfi = ((sinTransfi)*zoom) + (xShift*zoom) - VerschiebungX

    y = ((cos)*zoom) + (yShift*zoom) - VerschiebungY
    yTransfi = ((cosTransfi)*zoom) + (yShift*zoom) - VerschiebungY

    z = t * 0 + zShift #Lage der Symmatrieachse
    b = z + wide #Breite des Kringels

            
    resultdx = [] #Arrays für die Koordinaten der Normalenvektoren, müssen global sein (also außerhalb der funktion deklariert) um in jedem Punkt des Programms darauf zugreifen zu können
    resultdy = []

    resultdxTransfi = []
    resultdyTransfi = []

    resultdxTransfi2 = []
    resultdyTransfi2 = []

    #Normalenvektoren für den originalen Kringel werden erstellt
    normal(x, y, resultdx, resultdy)
    normalTransfi(xTransfi, yTransfi, resultdxTransfi, resultdyTransfi)
    normalTransfi2(xTransfi, yTransfi, resultdxTransfi2, resultdyTransfi2)

    #Die Endpunkte der Normalenvektoren sind aufgrund der art der Errechnung der Normalenvektoren wird ein Punkt "zu wenig" errechnet daher für den letzten Punkt hier noch eine einzelne Berechnung eines Noramlenvekors
    tChipEnd = np.linspace(end, end+0.01 , quantity)
    tChipEndTransfi = np.linspace(end, end+0.01, quantity)




    if modiBool == True:
        sinChipEnd, cosChipEnd = modification(function(tChipEnd)) #Erzeugt das Fresnelintegral
        sinChipEndTransfi, cosChipEndTransfi = modification(function(tChipEndTransfi))
    else:
        sinChipEnd, cosChipEnd = (function(tChipEnd))
        sinChipEndTransfi, cosChipEndTransfi = (function(tChipEndTransfi))




    xChipEnd = ((sinChipEnd)*zoom) + (xShift*zoom) - VerschiebungX#Fügt alle Parameter für X und Y zusammen und erzeugt die X und Y Koordinaten
    xChipEndTransfi = ((sinChipEndTransfi)*zoom) + (xShift*zoom) - VerschiebungX

    yChipEnd = ((cosChipEnd)*zoom) + (yShift*zoom) - VerschiebungY
    yChipEndTransfi = ((cosChipEndTransfi)*zoom) + (yShift*zoom) - VerschiebungY

    #Letztes Normalenelement wird erstellt
    normal(xChipEnd, yChipEnd, resultdx, resultdy)
    normalTransfi(xChipEndTransfi, yChipEndTransfi, resultdxTransfi, resultdyTransfi)
    normalTransfi2(xChipEndTransfi, yChipEndTransfi, resultdxTransfi2, resultdyTransfi2)

    coordsx = (x)
    resultx = []
    for x in coordsx:
        x = round(x,3)
        resultx.append(x)
            
    coordsy = (y)
    resulty = []
    for y in coordsy:
        y = round(y,3)
        resulty.append(y)
            
    coordsz = (z)
    resultz = []
    for z in coordsz:
        resultz.append(z)
        
    coordsb = (b)
    resultb =[]
    for b in coordsb:
        resultb.append(b) 
        
    coords1 = list(zip(resultx, resulty, resultz)) #Kringel
    coords1n = list(zip(resultdx, resultdy, resultz)) #Paralleler Kringel
    coords2 = list(zip(resultx, resulty, resultb))
    coords2n = list(zip(resultdx, resultdy, resultb))
    coords3n = list(zip(resultdxTransfi, resultdyTransfi, resultz)) #Kringel
    coords3nb = list(zip(resultdxTransfi, resultdyTransfi, resultb))
    coords4n = list(zip(resultdxTransfi2, resultdyTransfi2, resultz)) #Paralleler Kringel
    coords4nb = list(zip(resultdxTransfi2, resultdyTransfi2, resultb))

    #print(coords2n)

    index1 = 1000 #Original Kringel
    index1list=[]
    index2 = 2000 #1. Normalenvektor
    index2list=[]
    index3 = 3000 #Projektion des Kringels
    index3list=[]
    index4 = 4000 #2. Normalenvektor
    index4list=[]
    index5 = 5000 
    index5list=[]
    index6 = 6000 
    index6list=[]
    index7 = 7000 
    index7list=[]
    index8 = 8000 
    index8list=[]

    verschiebungAnfang = 0

    for [x,y,z] in coords1:
            Spandau.addPoint(x, y, z, lc, index1)
            index1list.append(index1)
            index1+=1

    for [x,y,b] in coords2:
            Spandau.addPoint(x, y, b, lc, index3)
            index3list.append(index3)
            index3+=1


    coords1n.insert(0,(-thick-thickTransfi-thickTransfi-verschiebungAnfang - VerschiebungX, 0 - VerschiebungY, 0))

    for [xc,yc,z] in coords1n:
            Spandau.addPoint(xc, yc, z, lc, index2)
            index2list.append(index2)
            index2+=1


    coords2n.insert(0,(-thick-thickTransfi-thickTransfi-verschiebungAnfang - VerschiebungX, 0 - VerschiebungY, wide))

    for [xc,yc,b] in coords2n:
            Spandau.addPoint(xc, yc, b, lc, index4)
            index4list.append(index4)
            index4+=1
            

    coords3n.insert(0,(-thickTransfi - VerschiebungX, 0 - VerschiebungY, 0))

    for [xc,yc,z] in coords3n:
            Spandau.addPoint(xc, yc, z, lc, index5)
            index5list.append(index5)
            index5+=1
            
    coords3nb.insert(0,(-thickTransfi - VerschiebungX, 0 - VerschiebungY, wide))

    for [xc,yc,z] in coords3nb:
            Spandau.addPoint(xc, yc, z, lc, index6)
            index6list.append(index6)
            index6+=1

    coords4n.insert(0,(-thickTransfi-thick-verschiebungAnfang - VerschiebungX, 0 - VerschiebungY, 0))

    for [xc,yc,z] in coords4n:
            Spandau.addPoint(xc, yc, z, lc, index7)
            index7list.append(index7)
            index7+=1
            
    coords4nb.insert(0,(-thickTransfi-thick-verschiebungAnfang - VerschiebungX, 0 - VerschiebungY, wide))

    for [xc,yc,z] in coords4nb:
            Spandau.addPoint(xc, yc, z, lc, index8)
            index8list.append(index8)
            index8+=1

    #Die vier Anfangspunkte werden hier (jeweils 2) durch BSplines verbunden. Splines erhalten wie Punkte in GMSH natürlich auch einen Tag. 
    if (phase <= 3 and phase >0):
        Spandau.addBSpline([(index5)-(quantity+1), (index1)-quantity], degree=1, tag=5000) #verbindet Original mit Normale (kurz)
        Spandau.addBSpline([(index6)-(quantity+1), (index3)-quantity], degree=1, tag=5001) #verbindet Projektion mit Normale (kurz)

        Spandau.addBSpline([(index8)-(quantity+1), (index6)-(quantity+1)], degree=1, tag=5002) #verbindet Original mit Normale (kurz)
        Spandau.addBSpline([(index7)-(quantity+1), (index5)-(quantity+1)], degree=1, tag=5003) #verbindet Projektion mit Normale (kurz)

        Spandau.addBSpline([(index7)-(quantity+1), (index2)-(quantity+1)], degree=1, tag=5004) #verbindet Original mit Normale (kurz)
        Spandau.addBSpline([(index8)-(quantity+1), (index4)-(quantity+1)], degree=1, tag=5005) #verbindet Projektion mit Normale (kurz)

        #Die vier endpunkte werden hier (jeweils 2) durch BSplines verbunden. Splines erhalten wie Punkte in GMSH natürlich auch einen Tag. 
        Spandau.addBSpline([index1-1,index5-1], degree=1, tag=6000) #verbindet Original mit Normale (kurz)
        Spandau.addBSpline([index3-1,index6-1], degree=1, tag=6001) #verbindet Projektion mit Normale (kurz)

        Spandau.addBSpline([index6-1,index8-1], degree=1, tag=6002) #verbindet Original mit Normale (kurz)
        Spandau.addBSpline([index5-1,index7-1], degree=1, tag=6003) #verbindet Projektion mit Normale (kurz)

        Spandau.addBSpline([index4-1,index8-1], degree=1, tag=6004) #verbindet Original mit Normale (kurz)
        Spandau.addBSpline([index2-1,index7-1], degree=1, tag=6005) #verbindet Projektion mit Normale (kurz)


        Spandau.addBSpline(index1list, degree=3, tag=10000) #OriginalKringel
        Spandau.addBSpline(index3list, degree=3, tag=30000) #Projektion des Kringels
        Spandau.addBSpline(index2list[::-1], degree=3, tag=20000) #1.Normalenvektor
        Spandau.addBSpline(index4list[::-1], degree=3, tag=40000) #2.Normalenvektor


        Spandau.addBSpline(index5list[::-1], degree=3, tag=50000) #OriginalKringel
        Spandau.addBSpline(index7list, degree=3, tag=70000) #Projektion des Kringels
        Spandau.addBSpline(index6list[::-1], degree=3, tag=60000) #1.Normalenvektor
        Spandau.addBSpline(index8list, degree=3, tag=80000) #2.Normalenvektor


        
        if (showcase == False):
            #Volumen vom echten Kringel
            Spandau.addCurveLoop([5002, 60000, 6002, 80000], tag = 80000)
            Spandau.addCurveLoop([5003, 50000, 6003, 70000], tag = 80001)

            Spandau.addCurveLoop([5005, 5002, 5001, 30000, 6001, 6002, 6004, 40000], tag = 80002)
            Spandau.addCurveLoop([5004, 5003, 5000, 10000, 6000, 6003, 6005, 20000], tag = 80003)


            Spandau.addThruSections([80000, 80001],2)
            Spandau.addThruSections([80002, 80003],1)

            Spandau.cut([(3,1)],[(3,2)],tag=-1)
        

    """
    tooMuchSplines= (Spandau.getEntitiesInBoundingBox(-100, -100, -100, 100, 0, 100, dim=1))
    Spandau.remove(tooMuchSplines, recursive=False)

    tooMuchPoints= (Spandau.getEntitiesInBoundingBox(-100, -100, -100, 100, 0, 100, dim=0))
    Spandau.remove(tooMuchPoints, recursive=False)
    """

    if (phase < 0.1 and phase >0 and showcase == False):
        
        EntitiesInWide = Spandau.getEntitiesInBoundingBox(-1000, -0.01 - VerschiebungY, wide - 0.01 , 1000, 1000, wide + 0.01) # Kurzen Splines und Punkte auf z = wide Ebene
        EntitiesInZero = Spandau.getEntitiesInBoundingBox(-1000, -0.01 - VerschiebungY, -0.01 , 1000, 1000, 0.01)
        
        EntitiesOnGround = Spandau.getEntitiesInBoundingBox(-1000, -0.01 - VerschiebungY, -0.01, 1000, 0.01 - VerschiebungY, wide + 0.01)
        
        EntitiesInAir = Spandau.getEntitiesInBoundingBox(-1000, 0.01 - VerschiebungY, -0.01, 1000, 1000, wide + 0.01)
        
        
        
        SplinesInWide = []
        SplinesInZero = []
        AllSplinesOnGround = []
        AllSplinesInAir = []
        
        for(x,y) in EntitiesOnGround:
            if x==1:
                AllSplinesOnGround.append(y)

        for (x,y) in EntitiesInWide:
            if x==1:
                SplinesInWide.append(y)
                
        for (x,y) in EntitiesInZero:
            if x==1:
                SplinesInZero.append(y)

        for (x,y) in EntitiesInAir:
            if x==1:
                AllSplinesInAir.append(y)

        AllSmallAndMediumSplines = AllSplinesOnGround+AllSplinesInAir
        AllSmallSplines = []

        for i in AllSmallAndMediumSplines:
            if i in SplinesInWide:
                AllSmallSplines.append(i)
                
        for i in AllSmallAndMediumSplines:
                if i in SplinesInZero:
                    AllSmallSplines.append(i)

        AllMediumSplines = []        
        
        for i in AllSmallAndMediumSplines:
            if i not in AllSmallSplines:
                AllMediumSplines.append(i)

        AllEntities = Spandau.getEntities()
        AllSplines= []


        for (x,y) in AllEntities:
            if x==1:
                AllSplines.append(y)
        
        
        AllBigSplines = []

        for i in AllSplines:
            if i not in AllSmallAndMediumSplines:
                AllBigSplines.append(i)

        

    if (phase <= 1 and phase >=0.1 and showcase == False):
        EntitiesInWide = Spandau.getEntitiesInBoundingBox(-1000 - VerschiebungX, -1 - VerschiebungY, wide - 0.01 , 1000- VerschiebungX, 1 - VerschiebungY, wide + 0.01) # Kurzen Splines und Punkte auf z = wide Ebene
        EntitiesInZero = Spandau.getEntitiesInBoundingBox(-1000, -0.01 - VerschiebungY, -0.01 , 1000, 0.01 - VerschiebungY, 0.01)

        EntitiesOnGround = Spandau.getEntitiesInBoundingBox(-1000- VerschiebungX, -0.01 - VerschiebungY, -0.01, 1000- VerschiebungX, 0.01 - VerschiebungY, wide + 0.01)


        SplinesInWide = []
        SplinesInZero = []
        AllSplinesOnGround = []


        for(x,y) in EntitiesOnGround:
            if x==1:
                AllSplinesOnGround.append(y)

        for (x,y) in EntitiesInWide:
            if x==1:
                SplinesInWide.append(y)
                
        for (x,y) in EntitiesInZero:
            if x==1:
                SplinesInZero.append(y)

        AllSmallSplines = SplinesInWide + SplinesInZero


        AllMediumSplines = []

        for i in AllSplinesOnGround:
            if i not in AllSmallSplines:
                AllMediumSplines.append(i)


        AllEntities = Spandau.getEntities()
        AllSplines= []


        for (x,y) in AllEntities:
            if x==1:
                AllSplines.append(y)

        AllBigSplines = []

        for i in AllSplines:
            if i not in AllSplinesOnGround:
                AllBigSplines.append(i)


    if (phase <= 2 and phase >1 and showcase == False):
        EntitiesInWide = Spandau.getEntitiesInBoundingBox(-1000, -1 - VerschiebungY, wide - 0.01 , 1000, 1 - VerschiebungY, wide + 0.01) # Kurzen Splines und Punkte auf z = wide Ebene
        EntitiesInZero = Spandau.getEntitiesInBoundingBox(-1000 - VerschiebungX, -1 - VerschiebungY, -0.01 , 1000 - VerschiebungX, 1 - VerschiebungY, 0.01)

        EntitiesInXZero = Spandau.getEntitiesInBoundingBox(-1000, -0.01 - VerschiebungY, -0.01, 1- VerschiebungX, 1000 - VerschiebungY, wide + 0.01)
        EntitiesInXWide = Spandau.getEntitiesInBoundingBox(1 - VerschiebungX, -0.01 - VerschiebungY, -0.01, 1000, 1000 - VerschiebungY, wide + 0.01)

        SplinesInWide = []
        SplinesInZero = []
        AllSplinesInXZero = []
        AllSplinesInXWide = []

        for(x,y) in EntitiesInXZero:
            if x==1:
                AllSplinesInXZero.append(y)
                
        for(x,y) in EntitiesInXWide:
            if x==1:
                AllSplinesInXWide.append(y)

        for (x,y) in EntitiesInWide:
            if x==1:
                SplinesInWide.append(y)
                
        for (x,y) in EntitiesInZero:
            if x==1:
                SplinesInZero.append(y)

        AllSmallAndMediumSplines = AllSplinesInXWide+AllSplinesInXZero
        AllSmallSplines = []

        for i in AllSmallAndMediumSplines:
            if i in SplinesInWide:
                AllSmallSplines.append(i)
                
        for i in AllSmallAndMediumSplines:
                if i in SplinesInZero:
                    AllSmallSplines.append(i)

        AllMediumSplines = []        
        
        for i in AllSmallAndMediumSplines:
            if i not in AllSmallSplines:
                AllMediumSplines.append(i)

        AllEntities = Spandau.getEntities()
        AllSplines= []


        for (x,y) in AllEntities:
            if x==1:
                AllSplines.append(y)
        
        
        AllBigSplines = []

        for i in AllSplines:
            if i not in AllSmallAndMediumSplines:
                AllBigSplines.append(i)

        
    if (phase <= 3 and phase >2 and showcase == False):
        EntitiesInWide = Spandau.getEntitiesInBoundingBox(-1000, -0.01 - VerschiebungY, wide - 0.01 , 1000, 0.01 - VerschiebungY, wide + 0.01) # Kurzen Splines und Punkte auf z = wide Ebene
        EntitiesInZero = Spandau.getEntitiesInBoundingBox(-1000, -0.01 - VerschiebungY, -0.01 , 1000, 0.01 - VerschiebungY, 0.01)

        EntitiesInXZero = Spandau.getEntitiesInBoundingBox(-1000, -0.01 - VerschiebungY, -0.01, 0.01 - VerschiebungX, 1000, wide + 0.01)
        EntitiesInXWide = Spandau.getEntitiesInBoundingBox(0.01 - VerschiebungX, -0.01 - VerschiebungY, -0.01, 1000, 1000, wide + 0.01)

        SplinesInWide = []
        SplinesInZero = []
        AllSplinesInXZero = []
        AllSplinesInXWide = []

        for(x,y) in EntitiesInXZero:
            if x==1:
                AllSplinesInXZero.append(y)
                
        for(x,y) in EntitiesInXWide:
            if x==1:
                AllSplinesInXWide.append(y)

        for (x,y) in EntitiesInWide:
            if x==1:
                SplinesInWide.append(y)
                
        for (x,y) in EntitiesInZero:
            if x==1:
                SplinesInZero.append(y)

        AllSmallAndMediumSplines = AllSplinesInXWide+AllSplinesInXZero
        AllSmallSplines = []

        for i in AllSmallAndMediumSplines:
            if i in SplinesInWide:
                AllSmallSplines.append(i)
                
        for i in AllSmallAndMediumSplines:
                if i in SplinesInZero:
                    AllSmallSplines.append(i)

        AllMediumSplines = []        
        
        for i in AllSmallAndMediumSplines:
            if i not in AllSmallSplines:
                AllMediumSplines.append(i)
        print(AllMediumSplines)
        AllEntities = Spandau.getEntities()
        AllSplines= []


        for (x,y) in AllEntities:
            if x==1:
                AllSplines.append(y)
        
        
        AllBigSplines = []

        for i in AllSplines:
            if i not in AllSmallAndMediumSplines:
                AllBigSplines.append(i)


        
        radiusProgress = finalList[6]
        radiusMin = (thick+thickTransfi+thickTransfi)
        radiusMax = radiusMin*2
        radiusCurrent = radiusMin+(radiusProgress*radiusMin)
        yFloor = -2.375
        xStart = resultx[-1]
        

        radiusProgress = finalList[6]
        radiusMin = (thick+thickTransfi+thickTransfi)
        radiusMax = radiusMin*2
        radiusCurrent = radiusMin+(radiusProgress*radiusMin)

        Spandau.addCylinder(xStart - radiusCurrent , yFloor+radiusCurrent, 0, 0, 0, wide, radiusCurrent, tag=101010, angle=2*pi)
        Spandau.addCylinder(xStart - radiusCurrent , yFloor+radiusCurrent, 0, 0, 0, wide, radiusCurrent-thickTransfi, tag=202020, angle=2*pi)
        Spandau.addCylinder(xStart - radiusCurrent , yFloor+radiusCurrent, 0, 0, 0, wide, radiusCurrent, tag=303030, angle=pi)
        Spandau.addCylinder(xStart - radiusCurrent , yFloor+radiusCurrent, 0, 0, 0, wide, radiusCurrent-thickTransfi, tag=404040, angle=pi)
        Spandau.cut([(3,101010)],[(3,202020)],tag=505050)
        Spandau.cut([(3,303030)],[(3,404040)],tag=606060)
        Spandau.cut([(3,505050)],[(3,606060)],tag=707070)


        Spandau.addCylinder(xStart - radiusCurrent , yFloor+radiusCurrent, 0, 0, 0, wide, radiusCurrent, tag=808080, angle=pi)
        Spandau.addCylinder(xStart - radiusCurrent , yFloor+radiusCurrent, 0, 0, 0, wide, radiusCurrent-thickTransfi, tag=909090, angle=pi)
        Spandau.cut([(3,808080)],[(3,909090)],tag=1010101)
    
        AllEntitiesCyl = Spandau.getEntities()
        AllSplinesCyl= []


        for (x,y) in AllEntitiesCyl:
            if x==1:
                AllSplinesCyl.append(y)
        
        AllSplinesOnlyCyl = []        
        
        for i in AllSplinesCyl:
            if i not in AllSplines:
                AllSplinesOnlyCyl.append(i)


    
        
    Spandau.synchronize()



    if (showcase == False):
        for y in AllSmallSplines:
                gmsh.model.mesh.setTransfiniteCurve(y, 3)

        for y in AllMediumSplines:
                gmsh.model.mesh.setTransfiniteCurve(y, 20)

        for y in AllBigSplines:
                gmsh.model.mesh.setTransfiniteCurve(y, 50)


        AllSurfaces = []

        for (x,y) in AllEntities:
            if x==2:
                AllSurfaces.append(y)
                
        for i in AllSurfaces:
            gmsh.model.mesh.setTransfiniteSurface(i)

        gmsh.model.mesh.setTransfiniteVolume(1)
        gmsh.model.mesh.setTransfiniteVolume(2)
        
        if (phase <= 3 and phase >2):
            for y in AllSplinesOnlyCyl:
                gmsh.model.mesh.setTransfiniteCurve(y, 20)
            
            gmsh.model.mesh.setTransfiniteAutomatic()
            """
            gmsh.model.mesh.setTransfiniteSurface(13)
            gmsh.model.mesh.setTransfiniteSurface(14)
            gmsh.model.mesh.setTransfiniteSurface(15)
            gmsh.model.mesh.setTransfiniteSurface(16)
                
            gmsh.model.mesh.setTransfiniteVolume(303030)
            """

    if (showcase == False):
        OriginalKringelList = np.array(coords1)
        file = open("OriginalKringelCoords", "w+")
        content = str(OriginalKringelList)
        content = content.replace("[","")
        content = content.replace("]","")
        file.write(content)
        file.close()

        OriginalKringelInZList = np.array(coords2)
        file = open("OriginalKringelCoordsInZ", "w+")
        content2 = str(OriginalKringelInZList)
        content2 = content2.replace("[","")
        content2 = content2.replace("]","")
        file.write(content2)
        file.close()

        FirstNormalList = np.array(coords3n)
        file = open("FirstNormalCoords", "w+")
        content3 = str(FirstNormalList)
        content3 = content3.replace("[","")
        content3 = content3.replace("]","")
        file.write(content3)
        file.close()

        FirstNormalInZList = np.array(coords3nb)
        file = open("FirstNormalCoordsInZ", "w+")
        content4 = str(FirstNormalInZList)
        content4 = content4.replace("[","")
        content4 = content4.replace("]","")
        file.write(content4)
        file.close()

        ScndNormalList = np.array(coords4n)
        file = open("ScndNormalCoords", "w+")
        content5 = str(ScndNormalList)
        content5 = content5.replace("[","")
        content5 = content5.replace("]","")
        file.write(content5)
        file.close()

        ScndNormalInZList = np.array(coords4nb)
        file = open("ScndNormalCoordsInZ", "w+")
        content6 = str(ScndNormalInZList)
        content6 = content6.replace("[","")
        content6 = content6.replace("]","")
        file.write(content6)
        file.close()

        ThirdNormalList = np.array(coords1n)
        file = open("ThirdNormalCoords", "w+")
        content7 = str(ThirdNormalList)
        content7 = content7.replace("[","")
        content7 = content7.replace("]","")
        file.write(content7)
        file.close()    

        ThirdNormalInZList = np.array(coords2n)
        file = open("ThirdNormalCoordsInZ", "w+")
        content8 = str(ThirdNormalInZList)
        content8 = content8.replace("[","")
        content8 = content8.replace("]","")
        file.write(content8)
        file.close()


    if (showcase == True or (phase <= 3 and phase >2)):
        gmsh.model.mesh.generate(1)
    else:
        gmsh.model.mesh.generate(3)
        
    if (showcase == False):
        gmsh.write("Spirale.msh")
        gmsh.write("Spirale.stl")

        
    gmsh.fltk.run()
    gmsh.clear()
    gmsh.finalize()
