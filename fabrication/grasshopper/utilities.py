from __future__ import print_function

import rhinoscriptsyntax as rs
import ghpythonlib.components as ghcomp
from compas.datastructures.mesh import Mesh


def mesh_from_guid(guid, **kwargs):
    """Creates an instance of a compAS mesh class from an identifier
    in Rhino/Grasshopper.

    This function is almost identical to ``mesh_from_guid`` in the core
    framework, but there were some import issues when used from within
    Grasshopper, but eventually, it should be migrated into the core.
    """
    trimesh = ghcomp.Triangulate(rs.coercemesh(guid))[0]
    vertices = [map(float, vertex) for vertex in rs.MeshVertices(trimesh)]
    faces = map(list, rs.MeshFaceVertices(trimesh))
    faces = [face[: -1] if face[-2] == face[-1] else face for face in faces]
    mesh = Mesh.from_vertices_and_faces(vertices, faces)
    mesh.attributes.update(kwargs)
    return mesh


def vrep_pose_from_plane(plane):
    """Creates a vrep-compatible pose from a Rhino/Grasshopper plane.

    This function might need rework as the source of the 90-deg Y rotation
    need is not entirely clear to me (related to the RFL model mismatch).
    """
    translation_matrix = rs.XformTranslation(((plane[0][0]), (plane[0][1]), plane[0][2]))
    plane_start = rs.PlaneFromFrame(rs.AddPoint(0, 0, 0), rs.AddPoint(1, 0, 0), rs.AddPoint(0, 1, 0))
    plane_end = rs.PlaneFromFrame(rs.AddPoint(0, 0, 0), rs.AddPoint(plane[1][0], (plane[1][1]), plane[1][2]), rs.AddPoint(plane[2][0], plane[2][1], plane[2][2]))
    rotation_matrix = rs.XformRotation1(plane_start, plane_end)
    matrix = rs.XformMultiply(translation_matrix, rotation_matrix)
    return [matrix.M00, matrix.M01, matrix.M02, matrix.M03,
            matrix.M10, matrix.M11, matrix.M12, matrix.M13,
            matrix.M20, matrix.M21, matrix.M22, matrix.M23]
