"""Herzlich Willkommen zum Dokovic'en Kringel"""

import numpy as np
from scipy.special import fresnel
import gmsh
import sys
import math
import os
"""Was wirkt wie ein einfacher schlechter Witz ist tatsächlich sehr wichtig... Es gibt in PyGMSH zwei Möglichkeiten Geometrien zu erstellen: mit dem GEO und dem OCC Kern. Entschließt man sich ein davon zu nehmen kann man nicht mehr tauschen bzw zwischendrin einfach wechseln denn die Geometrien wären sonst unvollständig. Da hier für den Spanraum eine STEP Datei eingelesen wird müssen wir den OCC Kern von GMSH verwenden. Um keine Fehler zu machen kürze ich das hier einmal ab. Der Name allerdings ist tatsächlich nur ein schlechter Witz. 
Als nächstes wird gmsh gestartet und der Spanraum eingelesen."""

Spandau = gmsh.model.occ
gmsh.initialize()
gmsh.merge('./Stroemungsgebiet_Symmetrisch_3.STEP')
"""Im folgenden erzeugen wir den Kringel mithilfe der Fresnel-Integrale sowie bereits einige Parameter des Spans"""


zoom = 70 #Größe des Kringels
quantity = 50 #Anzahl der Punkte des Kringels
start = 0.38 #Startpunkt des Kringels
end = 3 #Endpunkt des Kringels
xShift = -7.47 #Verschiebung in X-Richtung
yShift = -38 #Verschiebung in Y-Richtung
zShift = 0 #Verschiebung in Z-Richtung
wide = 12 #Breite des Spans
thick = 1 #Dicke des Spans
lc = -5.0 #Netzdichte an den Punkten des Kringels

t = np.linspace(start, end, quantity+1) #Erzeugt die gewünschte Anzahl an Punkten zwischen Start und Endpunkt (+1 da die ableitung für die Normalenvektoren und dadurch das +1. Element genutzt wird)
function = fresnel
modification = np.sqrt
sin, cos = modification(function(t)) #Erzeugt das Fresnelintegral
x = ((sin)*zoom) + xShift #Fügt alle Parameter für X und Y zusammen und erzeugt die X und Y Koordinaten
y = ((cos)*zoom) + yShift
z = t * 0 + zShift #Lage der Symmatrieachse
b = z + wide #Breite des Kringels

"""Um dem Span eine Dicke zu geben benötigt man einen zweiten Kringel der in jedem Punkt parallel ist zum Original. Damit der Abstand verstellbar ist und auch sicher gewährleistet ist das der zweite Kringel immer parallel ist wird für jeden Punkt des Originalen Kringels der Einheitsnormalenvekotor errechnet und mit der gewünschten Dicke multipliziert. Abschließend wird der jeweilige Vekotor auf den jeweiligen Punkt addiert um die Koordinaten des parallelen Kringels zu erhalten."""

#Funktion für die Normalenvektoren

def normal(xValue, yValue, xList, yList):
    for idx in range(len(x)-1):
        x0, y0, x1, y1 = xValue[idx], yValue[idx], xValue[idx+1], yValue[idx+1]
        dx = x1-x0 #Ableitungen
        dy = y1-y0
        norm = math.hypot(dx, dy) * 1/thick #Normierung
        dx /= norm
        dy /= norm
        xc = x0-dy #Vekotor+Original
        yc = y0+dx
        xList.append(xc)#Einfügen in die Arrays
        yList.append(yc)
        
resultdx = [] #Arrays für die Koordinaten der Normalenvektoren, müssen global sein (also außerhalb der funktion deklariert) um in jedem Punkt des Programms darauf zugreifen zu können
resultdy = []

normal(x, y, resultdx, resultdy)#Normalenvektoren für den originalen Kringel werden erstellt

"""die Anzahl der Elemente wird in einer einfachen Liste erfasst, über jedes Element wird rüber iteriert und in einem Array gespeichert"""

coordsx = (x)
resultx = []
for x in coordsx:
    resultx.append(x)
        
coordsy = (y)
resulty = []
for y in coordsy:
    resulty.append(y)
        
coordsz = (z)
resultz = []
for z in coordsz:
    resultz.append(z)

coordsb = (b)
resultb =[]
for b in coordsb:
    resultb.append(b) 
    
"""die einzelnen Koordinaten werden hier zusammengefügt. Von 1D Koordinaten zu 3D Koordinaten. Da der Span nicht nur in der z=0 Ebene entwickelt wird werden Span und Normalenkoordinaten auf die z=b Ebene projeziert. Also insgesamt erhalten wir am ende 4 Kringel. Original und Paralleler jeweils auf den zwei Ebenen."""

coords1 = list(zip(resultx, resulty, resultz)) #Kringel
coords1n = list(zip(resultdx, resultdy, resultz)) #Paralleler Kringel
coords2 = list(zip(resultx, resulty, resultb))
coords2n = list(zip(resultdx, resultdy, resultb))

"""Um jede einzelne Koordinate auch in GMSH wieder gefunden werden kann, wird hier für jeden Punkt ein Index festgelegt. Zumindest wird hier die Dimension des Index festgelegt. Indexe dürfen niemals doppelt vergeben werden. Um eine möglichst hohe Flexibilität der Punkte zu haben beginnen die Punktindexe im tausender Bereich. nicht vergessen: Der Spanraum wurde natürlich durch GMSH schon mit netsprechenden Punkten, Splines, Geometrien etc. versehen. Diese Geometrien haben natürlich auch schon Tags die nicht doppelt vergeben werden dürfen. Zusätzlich werden alle Punktindexe in einem jeweiligen Array gespeichert. Dies hat auf den ersten Blick keinen weiteren Nutzen, jedoch kann man so immer Kontrollieren wo der Fehler liegt falls es einen gibt. Das ist auch der Hauptgrund warum von jeder bisherigen Koordinate ein array angelegt wurde. Entsteht ein Fehler oder wird etwas faslch eingetragen, soist durch print(gewünschteListe) eine genaue nachverfolgung von GMSH tag bis 1D Koordinate möglich.für die gewünschte Kontrolle einfach die folgende Zeile einkommentieren"""

#print(coords1)

index1 = 1000 #Original Kringel
index1list=[]
index2 = 2000 #1. Normalenvektor
index2list=[]
index3 = 3000 #Projektion des Kringels
index3list=[]
index4 = 4000 #2. Normalenvektor
index4list=[]

#über jede Koordinatenpackung iterieren und in GMSH eintragen

for [x,y,z] in (coords1[:-1]):
        Spandau.addPoint(x, y, z, lc, index1)
        index1list.append(index1)
        index1+=1

for [x,y,b] in (coords2[:-1]):
        Spandau.addPoint(x, y, b, lc, index3)
        index3list.append(index3)
        index3+=1

for [xc,yc,z] in coords1n:
        Spandau.addPoint(xc, yc, z, lc, index2)
        index2list.append(index2)
        index2+=1

for [xc,yc,b] in coords2n:
        Spandau.addPoint(xc, yc, b, lc, index4)
        index4list.append(index4)
        index4+=1
 
#Die vier endpunkte werden hier durch BSplines zu einer Vierecksform verbunden. Splines erhalten wie Punkte in GMSH natürlich auch einen Tag. 

Spandau.addBSpline([index2-1,index1-1], degree=1, tag=6000) #verbindet Original mit Normale (kurz)
Spandau.addBSpline([index2-1,index4-1], degree=1, tag=6001) #verbindet Normale mit Normale (lang)
Spandau.addBSpline([index4-1,index3-1], degree=1, tag=6002) #verbindet Projektion mit Normale (kurz)
Spandau.addBSpline([index3-1,index1-1], degree=1, tag=6003) #verbindet Original mit Projektion (lang)

"""Die Kringelgeometrie wurde nun erstellt es gilt nun den Kringel mit dem Werkzeug zu verbinden. Ganz zu Beginn verläuft der Span direkt am Werkzeug entlang, dieser Teil ist fest und ohne Abstnad am Werkzeug gelegen. Um natürlich auch diesem festen Span die Entsprechende dicke zu geben wurden auch hier die Einheitsnormalenvektoren errechnet allerdings ein einziges mal von Hand und nicht durch Code. Diese Koordinaten werden nur ein mal festgelegt"""

"""Der Spanbeginn (Viereck wie das Ende) besteht aus den Punkten 90,91,92,28"""
Spandau.addPoint(thick,0,z,lc,90)
Spandau.addPoint(thick,0,b,lc,91)
Spandau.addPoint(0,0,b,lc,92)
Spandau.addPoint(1,2.5,b,lc,93)


Spandau.addPoint(1,2.5,z,lc,210)
Spandau.addPoint(0,0,z,lc,211)
Spandau.addBSpline([211,210], tag = 9999)
Spandau.addBSpline([210,93],tag=9010)
Spandau.addBSpline([211,210],tag=9011)


Spandau.addBSpline([90,91], degree=1, tag=6004) #verbindet Original mit Projektion (lang)
Spandau.addBSpline([92,91], degree=1, tag=6005) #verbindet Projektion mit Normale (kurz)
Spandau.addBSpline([92,211], degree=1, tag=6006)
Spandau.addBSpline([211,90], degree=1, tag=6007)








#Vom Span aus Rückwärts
distanceNormal = 0.01
tSpan1 = start - distanceNormal
sinSpan1, cosSpan1 = modification(function(tSpan1)) #fresnelintegral erzeugen
xSpan1 = ((sinSpan1)*zoom)+xShift
ySpan1 = ((cosSpan1)*zoom)+yShift
Spandau.addPoint(xSpan1,ySpan1,z,lc,80)
Spandau.addPoint(xSpan1,ySpan1,b,lc,81)

#Normalenvektor

tSpan = np.linspace(start - distanceNormal, start, 2)
sinSpan, cosSpan = modification(function(tSpan)) #fresnelintegral erzeugen
xSpan = ((sinSpan)*zoom)+xShift
ySpan = ((cosSpan)*zoom)+yShift

for idx in range(len(xSpan)-1):
    x0Span, y0Span, x1Span, y1Span = xSpan[idx], ySpan[idx], xSpan[idx+1], ySpan[idx+1]
    dxSpan = x1Span-x0Span
    dySpan = y1Span-y0Span
    normSpan = math.hypot(dxSpan, dySpan) * 1/thick
    dxSpan /= normSpan
    dySpan /= normSpan
    xcSpan = x0Span-dySpan
    ycSpan = y0Span+dxSpan
    Spandau.addPoint(xcSpan,ycSpan,z,lc,82)
    Spandau.addPoint(xcSpan,ycSpan,b,lc,83)


norm2 = 1/np.sqrt(1+np.square(2.5))
Spanx = thick * (-2.5*norm2)
Spany = thick * (1*norm2)
Spandau.addPoint(1-Spanx,2.5-Spany,z,lc,94)
Spandau.addPoint(1-Spanx,2.5-Spany,b,lc,95)

abstand = (np.sqrt(np.square(xcSpan-1)+np.square(ycSpan-2.5)))
vektorx = norm2*(abstand/5)
vektory = norm2*(abstand/5)*2.5
Spandau.addPoint(1+vektorx, 2.5+vektory,z,lc,96)
Spandau.addPoint(1+vektorx, 2.5+vektory,b,lc,97)
Spandau.addPoint((1+vektorx)-Spanx, (2.5+vektory)-Spany,z,lc,98)
Spandau.addPoint((1+vektorx)-Spanx, (2.5+vektory)-Spany,b,lc,99)


Spandau.addBSpline([92,93],tag=50000)



index1list.insert(0, 80)
index1list.insert(0, 98)
index1list.insert(0, 94)
index1list.insert(0, 90)

index3list.insert(0, 81)
index3list.insert(0, 99)
index3list.insert(0, 95)
index3list.insert(0, 91)

index2list.insert(0, 82)
index2list.insert(0, 96)
index2list.insert(0, 210)


index4list.insert(0, 83)
index4list.insert(0, 97)
index4list.insert(0, 93)



Spandau.addBSpline(index1list, degree=3, tag=10000) #OriginalKringel
Spandau.addBSpline(index3list, degree=3, tag=30000) #Projektion des Kringels
Spandau.addBSpline(index2list, degree=3, tag=20000) #1.Normalenvektor
Spandau.addBSpline(index4list, degree=3, tag=40000) #2.Normalenvektor



#Flächen

#Flächen links und rechts (dicke) des Spans
Spandau.addCurveLoop([-6007,10000,-6000,-20000,-9999], tag = 70001)#50002 [2]
Spandau.addCurveLoop([-6005,30000,-6002,40000,-50000], tag = 70002)#-50001[letzte]

#Flächen an Anfang und Ende des Spans
Spandau.addCurveLoop([-6007,-6006,-6005,-6004], tag = 80005)
Spandau.addCurveLoop([6000,6001,6002,6003], tag = 80006)#Span ende Fläche 

#Flächen oben und unten vom Span
Spandau.addCurveLoop([6006,50000,40000,6001,20000,9999], tag = 90003)
Spandau.addCurveLoop([6004,30000,6003,-10000], tag = 90004) #50001 [1]-50002[letzte]

Spandau.addThruSections([70001,70002])

Spandau.addPlaneSurface([70001])
Spandau.addPlaneSurface([70002])
Spandau.addPlaneSurface([80005])
Spandau.addPlaneSurface([80006])


gmsh.model.occ.cut([(3,1)],[(3,2)],3)

Spandau.synchronize()


gmsh.model.addPhysicalGroup(3, [3], 1) #1 Volumen 

surfaces = []
for i in range(37,74):
    t = i
    surfaces.append(t)
gmsh.model.addPhysicalGroup(2, surfaces,2) #Alle Oberflächen



gmsh.model.mesh.generate(3)
gmsh.write("Kringel.msh")
gmsh.fltk.run()
gmsh.clear()
gmsh.finalize()
