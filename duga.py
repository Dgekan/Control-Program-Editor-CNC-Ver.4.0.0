import sys
import ezdxf
import numpy as np

try:
    doc = ezdxf.readfile("duga.dxf")
except IOError:
    print(f'Not a DXF file or a generic I/O error.')
    sys.exit(1)
except ezdxf.DXFStructureError:
    print(f'Invalid or corrupted DXF file.')
    sys.exit(2)

def print_entity(e):
   # print("LINE on layer: %s" % e.dxf.layer)
    print(e,"start point: %s" % e.dxf.start)
   # print(e,"end point: %s" % e.dxf.end) 

def print_entit(e):
    print(e,"center: %s" % e.dxf.center)
    print(e,"radius: %s" % e.dxf.radius)
    print(e,"start point: %s" % e.start_point)
    print(e,"end point: %s" % e.end_point) 
    print(e)

msp = doc.modelspace()
print(len(msp))
lisx=[]
lisy=[]
for e in msp:
    if e.dxftype() == 'ARC':
       # print(e,e.start_point)
       # print(e,e.end_point)
        lisx.append(e.start_point)
       # lisy.append(e.start_point[1])
        lisx.append(e.end_point)
       # lisy.append(e.end_point[1])

    elif e.dxftype() == 'LINE':
       # print(e,e.dxf.start)
       # print(e,e.dxf.end)
        lisx.append(e.dxf.start)
       # lisy.append(e.dxf.start[1])
        lisx.append(e.dxf.end)
       # lisy.append(e.dxf.end[1])
   # elif e.dxftype() == 'SPLINE':    
    #    print(e,e.dxf.n_control_points)
    #    print(e,e.control_points)

#print(lisx,lisy)
x=np.array(lisx)
print(x)
c=np.msort(x)
#y=np.array(lisy)
#y.sort()
print(c)


# entity query for all LINE entities in modelspace
#for e in msp.query('ARC'):
  #  print_entity(e)

   