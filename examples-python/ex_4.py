
import os
import numpy as np
from scipy import interpolate

import jigsawpy


def ex_4():

# DEMO-4: generate a grid based on the "HR" spacing pattern,
# developed by the FESOM team at AWI -- use the "multilevel"
# meshing strategy: "TETRIS".

    dst_path = \
        os.path.abspath(
            os.path.dirname(__file__))

    src_path = \
        os.path.join(dst_path, "..", "files")
    dst_path = \
        os.path.join(dst_path, "..", "cache")


    opts = jigsawpy.jigsaw_jig_t()

    topo = jigsawpy.jigsaw_msh_t()

    geom = jigsawpy.jigsaw_msh_t()
    hfun = jigsawpy.jigsaw_msh_t()
    mesh = jigsawpy.jigsaw_msh_t()

#------------------------------------ setup files for JIGSAW

    opts.geom_file = \
        os.path.join(src_path, "eSPH.msh")

    opts.jcfg_file = \
        os.path.join(dst_path, "eSPH.jig")

    opts.mesh_file = \
        os.path.join(dst_path, "mesh.msh")

    opts.hfun_file = \
        os.path.join(dst_path, "spac.msh")

#------------------------------------ define JIGSAW geometry

    geom.mshID = "ellipsoid-mesh"
    geom.radii = np.full(
        3, 6.371E+003, dtype=geom.REALS_t)

    jigsawpy.savemsh(opts.geom_file, geom)

#------------------------------------ define spacing pattern

    jigsawpy.loadmsh(os.path.join(
        src_path, "f_hr.msh"), hfun)

    hfun.value = +3. * hfun.value       # for fast example

    jigsawpy.savemsh(opts.hfun_file, hfun)

#------------------------------------ make mesh using JIGSAW

    opts.hfun_scal = "absolute"
    opts.hfun_hmax = float("inf")       # null HFUN limits
    opts.hfun_hmin = float(+0.00)

    opts.mesh_dims = +2                 # 2-dim. simplexes

    opts.optm_qlim = +9.5E-01           # tighter opt. tol
    opts.optm_iter = +32
    opts.optm_qtol = +1.0E-05

    jigsawpy.cmd.tetris(opts, 3, mesh)

#------------------------------------ save mesh for Paraview

    jigsawpy.loadmsh(os.path.join(
        src_path, "topo.msh"), topo)

#------------------------------------ a very rough land mask

    apos = jigsawpy.R3toS2(
        geom.radii, mesh.point["coord"][:])

    apos = apos * 180. / np.pi

    zfun = interpolate.RectBivariateSpline(
        topo.ygrid, topo.xgrid, topo.value)

    mesh.value = zfun(
        apos[:, 1], apos[:, 0], grid=False)

    cell = mesh.tria3["index"]

    zmsk = \
        mesh.value[cell[:, 0]] + \
        mesh.value[cell[:, 1]] + \
        mesh.value[cell[:, 2]]
    zmsk = zmsk / +3.0

    mesh.tria3 = mesh.tria3[zmsk < +0.]

    print("Saving to ../cache/case_4a.vtk")

    jigsawpy.savevtk(os.path.join(
        dst_path, "case_4a.vtk"), mesh)

    print("Saving to ../cache/case_4b.vtk")

    jigsawpy.savevtk(os.path.join(
        dst_path, "case_4b.vtk"), hfun)

    return


if (__name__ == "__main__"): ex_4()
