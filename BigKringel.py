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



gmsh.initialize()


zoom = 70 #Größe des Kringels
quantity = 45 #Anzahl der Punkte des Kringels
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
    resultb.append(b) #Normalenvektor
    
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

Spandau.addBSpline([index1-1,index2-1], degree=1, tag=6000) #verbindet Original mit Normale (kurz)

Spandau.addBSpline([index3-1,index4-1], degree=1, tag=6002) #verbindet Projektion mit Normale (kurz)


"""Die Kringelgeometrie wurde nun erstellt es gilt nun den Kringel mit dem Werkzeug zu verbinden. Ganz zu Beginn verläuft der Span direkt am Werkzeug entlang, dieser Teil ist fest und ohne Abstnad am Werkzeug gelegen. Um natürlich auch diesem festen Span die Entsprechende dicke zu geben wurden auch hier die Einheitsnormalenvektoren errechnet allerdings ein einziges mal von Hand und nicht durch Code. Diese Koordinaten werden nur ein mal festgelegt"""
Spandau.addPoint(thick,0,z,lc,90)
Spandau.addPoint(thick,0,b,lc,91)
Spandau.addPoint(0,0,b,lc,92)
Spandau.addPoint(1,2.5,b,lc,93)
Spandau.addPoint(1,2.5,z,lc,210)




distanceNormal = 0.01
"""
#Vom Span aus Rückwärts
distanceNormal = 0.01
tSpan1 = start - distanceNormal
sinSpan1, cosSpan1 = modification(function(tSpan1)) #fresnelintegral erzeugen
xSpan1 = ((sinSpan1)*zoom)+xShift
ySpan1 = ((cosSpan1)*zoom)+yShift
Spandau.addPoint(xSpan1,ySpan1,z,lc,80)
Spandau.addPoint(xSpan1,ySpan1,b,lc,81)
"""

"""Hier werden die Hilfspunkte für einen stetigen Übergang errechnet. Dabei wird sowohl vom Kringel aus Rückwärts so wie vom festen Span aus entgegengekommen für ein besonders stetigen Übergang. Ist hier hinfällig, da die Transfinite Geometire keinen stetigen Übergang erlaubt. Bei Bedarf alles Auskommentierte zwischen den Zeilen 160-208  wieder einkommentieren."""
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
    #Spandau.addPoint(xcSpan,ycSpan,z,lc,82)
    #Spandau.addPoint(xcSpan,ycSpan,b,lc,83)


norm2 = 1/np.sqrt(1+np.square(2.5))
Spanx = thick * (-2.5*norm2)
Spany = thick * (1*norm2)
Spandau.addPoint(1-Spanx,2.5-Spany,z,lc,94)
Spandau.addPoint(1-Spanx,2.5-Spany,b,lc,95)

abstand = (np.sqrt(np.square(xcSpan-1)+np.square(ycSpan-2.5)))
vektorx = norm2*(abstand/5)
vektory = norm2*(abstand/5)*2.5
#Spandau.addPoint(1+vektorx, 2.5+vektory,z,lc,96)
#Spandau.addPoint(1+vektorx, 2.5+vektory,b,lc,97)
#Spandau.addPoint((1+vektorx)-Spanx, (2.5+vektory)-Spany,z,lc,98)
#Spandau.addPoint((1+vektorx)-Spanx, (2.5+vektory)-Spany,b,lc,99)


"""Alle Hilfspunkte werden zum Kringel hinzugefügt"""
#index1list.insert(0, 98)
index1list.insert(0, 94)



#index3list.insert(0, 99)
index3list.insert(0, 95)


#index2list.insert(0, 82)
#index2list.insert(0, 96)
index2list.insert(0, 210)


#index4list.insert(0, 83)
#index4list.insert(0, 97)
index4list.insert(0, 93)


"""Finale Zusammenführung aller Punkte zu Splines!!!"""
Spandau.addBSpline(index1list, degree=3, tag=10000) #OriginalKringel
Spandau.addBSpline(index3list, degree=3, tag=30000) #Projektion des Kringels
Spandau.addBSpline(index2list[::-1], degree=3, tag=20000) #1.Normalenvektor
Spandau.addBSpline(index4list[::-1], degree=3, tag=40000) #2.Normalenvektor


"""Das feste spanstück wird hier erstellt. Sowohl die zugehörigen Punkte als auch Flächen und Volumen"""
Spandau.addBSpline([93,95], tag = 50013)
Spandau.addBSpline([210,94], tag = 50014)

Spandau.addBSpline([95,91], tag = 50015)
Spandau.addBSpline([91,92], tag = 50016)
Spandau.addBSpline([92,93], tag = 50017)

Spandau.addCurveLoop([50013, 50015, 50016, 50017], tag = 80001)

Spandau.addPoint(0,0,0,lc,212)
Spandau.addBSpline([94,90], tag = 50018)
Spandau.addBSpline([90,212], tag = 50019)
Spandau.addBSpline([212,210], tag = 50020)

Spandau.addCurveLoop([50014, 50018, 50019, 50020], tag = 80002)

Spandau.addThruSections([80001, 80002])



"""Aus Kringel wird hier nun Span. Die Punkte und Splines sind bereits fertig hier wird nur noch das Volumen difiniert"""

#Flächen links und rechts (dicke) des Spans
Spandau.addCurveLoop([50014,10000,6000,20000], tag = 70001)
Spandau.addCurveLoop([50013,30000,6002,40000], tag = 70002)

Spandau.addThruSections([70002,70001])




"""Fester Span und Kringel-Span werden aus dem Spanraum "rausgeschnitten"."""
gmsh.model.occ.cut([(3,1)],[(3,2)])
gmsh.model.occ.cut([(3,1)],[(3,3)])

"""Geometrie wird final in GMSH synchronisiert"""
Spandau.synchronize()



""" Physical groups werden festgelegt: 1. beinhaltet das finale Volumen, 2. beinhaltet alle Oberflächen"""
gmsh.model.addPhysicalGroup(3, [3], 1) #1 Volumen 

surfaces = []
for i in range(37,74):
    t = i
    surfaces.append(t)
gmsh.model.addPhysicalGroup(2, surfaces,2) #Alle Oberflächen


"""Alle Kringelspan zugehörigen Geometrien bis auf das Gesamtvolumen werden transfinit gesetzt."""
#Spline lang
gmsh.model.mesh.setTransfiniteCurve(17, 30)
gmsh.model.mesh.setTransfiniteCurve(19, 30)
gmsh.model.mesh.setTransfiniteCurve(20, 30)
gmsh.model.mesh.setTransfiniteCurve(62, 30)


#Spline mittel
gmsh.model.mesh.setTransfiniteCurve(2, 5)
gmsh.model.mesh.setTransfiniteCurve(21, 5)
gmsh.model.mesh.setTransfiniteCurve(61, 5)
gmsh.model.mesh.setTransfiniteCurve(63, 5)

#Spline kurz
gmsh.model.mesh.setTransfiniteCurve(18, 2)
gmsh.model.mesh.setTransfiniteCurve(64, 2)
gmsh.model.mesh.setTransfiniteCurve(65, 2)


#Flächen lang breit
gmsh.model.mesh.setTransfiniteSurface(3)
gmsh.model.mesh.setTransfiniteSurface(17)

#Fläche kurz schmal
gmsh.model.mesh.setTransfiniteSurface(18)

#Fläche lang dünn
gmsh.model.mesh.setTransfiniteSurface(19)


"""Alle Fest-Span zugehörigen Geometrien bis auf das Gesamtvolumen werden transfinit gesetzt."""
#Spline mittel breit
#Spline lang
gmsh.model.mesh.setTransfiniteCurve(56, 5)

#Splines mittelkurz
gmsh.model.mesh.setTransfiniteCurve(22, 3)
gmsh.model.mesh.setTransfiniteCurve(60, 3)
gmsh.model.mesh.setTransfiniteCurve(16, 3)

#Splines kurz
gmsh.model.mesh.setTransfiniteCurve(65, 2)
gmsh.model.mesh.setTransfiniteCurve(57, 2)

#Fläche breit 
gmsh.model.mesh.setTransfiniteSurface(16)

#Fläche kurz 
gmsh.model.mesh.setTransfiniteSurface(20)


gmsh.model.mesh.generate(3)
gmsh.write("BigKringel.msh")
gmsh.fltk.run()
gmsh.clear()
gmsh.finalize()

