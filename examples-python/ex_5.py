
import os
import copy
import numpy as np

import jigsawpy


def ex_5():

# DEMO-5: generate multi-resolution spacing, via local refi-
# nement along coastlines and shallow ridges. Global grid
# resolution is 150KM, background resolution is 99KM and the
# min. adaptive resolution is 33KM.

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

    hraw = jigsawpy.jigsaw_msh_t()
    hlim = jigsawpy.jigsaw_msh_t()

#------------------------------------ setup files for JIGSAW

    opts.geom_file = \
        os.path.join(src_path, "eSPH.msh")

    opts.jcfg_file = \
        os.path.join(dst_path, "eSPH.jig")

    opts.hfun_file = \
        os.path.join(dst_path, "spac.msh")

#------------------------------------ define JIGSAW geometry

    geom.mshID = "ellipsoid-mesh"
    geom.radii = np.full(
        3, 6.371E+003, dtype=geom.REALS_t)

    jigsawpy.savemsh(opts.geom_file, geom)

#------------------------------------ define spacing pattern

    jigsawpy.loadmsh(os.path.join(
        src_path, "topo.msh"), topo)

    hraw.mshID = "ellipsoid-grid"
    hraw.radii = geom.radii

    hraw.xgrid = topo.xgrid * np.pi / 180.
    hraw.ygrid = topo.ygrid * np.pi / 180.

    hfn0 = +150.                        # global spacing
    hfn2 = +33.                         # adapt. spacing
    hfn3 = +99.                         # arctic spacing

    hraw.value = np.sqrt(
        np.maximum(-topo.value, 0.0))

    hraw.value = \
        np.maximum(hraw.value, hfn2)
    hraw.value = \
        np.minimum(hraw.value, hfn3)

    mask = hraw.ygrid < 40. * np.pi / 180.

    hraw.value[mask] = hfn0

#------------------------------------ set HFUN grad.-limiter

    hlim = copy.copy(hraw)

    hlim.slope = np.full(               # |dH/dx| limits
        topo.value.shape,
        +0.050, dtype=hlim.REALS_t)

    jigsawpy.savemsh(opts.hfun_file, hlim)

    jigsawpy.cmd.marche(opts, hlim)

#------------------------------------ save mesh for Paraview

    print("Saving to ../cache/case_5a.vtk")

    jigsawpy.savevtk(os.path.join(
        dst_path, "case_5a.vtk"), hraw)

    print("Saving to ../cache/case_5b.vtk")

    jigsawpy.savevtk(os.path.join(
        dst_path, "case_5b.vtk"), hlim)

    return


if (__name__ == "__main__"): ex_5()
