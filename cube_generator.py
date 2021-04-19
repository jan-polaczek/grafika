import sys
from point import Point3D
from triangle import Triangle3D 


x_start = float(sys.argv[1])
y_start = float(sys.argv[2])
z_start = float(sys.argv[3])
edge_len = float(sys.argv[4])

vertices = []

vertices.append(Point3D(x_start, y_start, z_start))
vertices.append(Point3D(x_start + edge_len, y_start, z_start))
vertices.append(Point3D(x_start + edge_len, y_start, z_start + edge_len))
vertices.append(Point3D(x_start, y_start, z_start + edge_len))

for i in range(4):
    bottom_v = vertices[i]
    top_v = Point3D(
        bottom_v.x,
        bottom_v.y + edge_len,
        bottom_v.z
    )
    vertices.append(top_v)

triangles = []
#podstawa dolna
triangles.append(Triangle3D([vertices[0], vertices[1], vertices[2]]))
triangles.append(Triangle3D([vertices[2], vertices[3], vertices[0]]))
#podstawa górna
triangles.append(Triangle3D([vertices[4], vertices[5], vertices[6]]))
triangles.append(Triangle3D([vertices[6], vertices[7], vertices[4]]))
#przednia ściana
triangles.append(Triangle3D([vertices[0], vertices[1], vertices[5]]))
triangles.append(Triangle3D([vertices[5], vertices[4], vertices[0]]))
#tylna ściana
triangles.append(Triangle3D([vertices[3], vertices[2], vertices[6]]))
triangles.append(Triangle3D([vertices[6], vertices[7], vertices[3]]))
#lewa ściana 
triangles.append(Triangle3D([vertices[3], vertices[0], vertices[4]]))
triangles.append(Triangle3D([vertices[4], vertices[7], vertices[3]]))
#prawa ściana
triangles.append(Triangle3D([vertices[2], vertices[1], vertices[5]]))
triangles.append(Triangle3D([vertices[5], vertices[6], vertices[2]]))

for t in triangles:
    print(str(t))