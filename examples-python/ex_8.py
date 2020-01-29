
import os
import copy
import numpy as np

import jigsawpy


def ex_8():

# DEMO-8: build regional meshes via stereographic projection

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
    msph = jigsawpy.jigsaw_msh_t()

    proj = jigsawpy.jigsaw_prj_t()

#------------------------------------ setup files for JIGSAW

    opts.geom_file = \
        os.path.join(dst_path, "proj.msh")

    opts.jcfg_file = \
        os.path.join(dst_path, "paci.jig")

    opts.mesh_file = \
        os.path.join(dst_path, "mesh.msh")

    opts.hfun_file = \
        os.path.join(dst_path, "spac.msh")

#------------------------------------ define JIGSAW geometry

    jigsawpy.loadmsh(os.path.join(
        src_path, "paci.msh"), geom)

    jigsawpy.loadmsh(os.path.join(
        src_path, "topo.msh"), topo)

    xmin = np.min(geom.point["coord"][:, 0])
    xmax = np.max(geom.point["coord"][:, 0])

    xlon = np.linspace(xmin, xmax, 100)

    ymin = np.min(geom.point["coord"][:, 1])
    ymax = np.max(geom.point["coord"][:, 1])

    ylat = np.linspace(ymin, ymax, 100)

#------------------------------------ define spacing pattern

    hfun.mshID = "ellipsoid-grid"
    hfun.radii = np.full(
        +3, 6.371E+003,
        dtype=jigsawpy.jigsaw_msh_t.REALS_t)

    hfun.xgrid = xlon * np.pi / 180.
    hfun.ygrid = ylat * np.pi / 180.

    hfun.value = np.full(
        (ylat.size, xlon.size), 200.,
        dtype=jigsawpy.jigsaw_msh_t.REALS_t)

#------------------------------------ do stereographic proj.

    geom.point["coord"][:, :] *= np.pi / 180.

    proj.prjID = 'stereographic'
    proj.radii = +6.371E+003
    proj.xbase = \
        +0.500 * (xmin + xmax) * np.pi / 180.
    proj.ybase = \
        +0.500 * (ymin + ymax) * np.pi / 180.

    jigsawpy.project(geom, proj, "fwd")
    jigsawpy.project(hfun, proj, "fwd")

    jigsawpy.savemsh(opts.geom_file, geom)
    jigsawpy.savemsh(opts.hfun_file, hfun)

#------------------------------------ make mesh using JIGSAW

    opts.hfun_scal = "absolute"
    opts.hfun_hmax = float("inf")   # null HFUN limits
    opts.hfun_hmin = float(+0.00)

    opts.mesh_dims = +2             # 2-dim. simplexes

    opts.mesh_eps1 = +1.0E+00       # relax edge error

    opts.optm_iter = +32
    opts.optm_qtol = +1.0E-05

    jigsawpy.cmd.jigsaw(opts, mesh)

#------------------------------------ do stereographic proj.

    msph = copy.copy(mesh)

    jigsawpy.project(msph, proj, "inv")

#------------------------------------ save mesh for Paraview

    print("Saving to ../cache/case_8a.vtk")

    jigsawpy.savevtk(os.path.join(
        dst_path, "case_8a.vtk"), mesh)

    print("Saving to ../cache/case_8b.vtk")

    jigsawpy.savevtk(os.path.join(
        dst_path, "case_8b.vtk"), hfun)

    print("Saving to ../cache/case_8c.vtk")

    jigsawpy.savevtk(os.path.join(
        dst_path, "case_8c.vtk"), msph)

    return


if (__name__ == "__main__"): ex_8()
