
from pathlib import Path
import os
import numpy as np
from scipy import interpolate

import jigsawpy

def ex_6():

# DEMO-6: generate a multi-resolution grid, with local refi-
# nement along coastlines and shallow ridges. Global grid 
# resolution is 150KM, background resolution is 99KM and the 
# min. adaptive resolution is 33KM.

    src_path = os.path.join(
        os.path.abspath(
        os.path.dirname(__file__)),"files")

    dst_path = os.path.join(
        os.path.abspath(
        os.path.dirname(__file__)),"cache")


    opts = jigsawpy.jigsaw_jig_t()

    topo = jigsawpy.jigsaw_msh_t()
    
    geom = jigsawpy.jigsaw_msh_t()
    hfun = jigsawpy.jigsaw_msh_t()
    mesh = jigsawpy.jigsaw_msh_t()

#------------------------------------ setup files for JIGSAW

    opts.geom_file = \
        str(Path(dst_path)/"earth.msh") # GEOM file
        
    opts.jcfg_file = \
        str(Path(dst_path)/"globe.jig") # JCFG file
    
    opts.hfun_file = \
        str(Path(dst_path)/"space.msh") # HFUN file

    opts.mesh_file = \
        str(Path(dst_path)/"globe.msh") # MESH file

#------------------------------------ define JIGSAW geometry

    geom.mshID = "ellipsoid-mesh"
    geom.radii = np.full(3, 6371., 
        dtype=jigsawpy.jigsaw_msh_t.REALS_t)
    
    jigsawpy.savemsh(opts.geom_file, geom)

#------------------------------------ define spacing pattern

    jigsawpy.loadmsh(
        str(Path(src_path)/"topo.msh"), topo)

    hfun.mshID = "ellipsoid-grid"
    hfun.radii = geom.radii

    hfun.xgrid = topo.xgrid * np.pi/180.
    hfun.ygrid = topo.ygrid * np.pi/180.
   
    dhdx = +.05

    hfun.slope = np.full(
        topo.value.shape, dhdx, 
        dtype=jigsawpy.jigsaw_msh_t.REALS_t)

    hfn0 = +150.                    # global spacing
    hfn2 = + 33.                    # adapt. spacing
    hfn3 = + 99.                    # arctic spacing
       
    hfun.value = np.sqrt(
        np.maximum(-topo.value, +0.0))

    hfun.value = \
        np.maximum(hfun.value, hfn2)
    hfun.value = \
        np.minimum(hfun.value, hfn3)

    hfun.value[hfun.ygrid < 45.*np.pi/180.] = hfn0
  
    jigsawpy.savemsh(opts.hfun_file, hfun)

#------------------------------------ set HFUN grad.-limiter

    jigsawpy.cmd.marche(opts, hfun)

#------------------------------------ make mesh using JIGSAW 
    
    opts.hfun_scal = "absolute"
    opts.hfun_hmax = float("inf")   # null HFUN limits
    opts.hfun_hmin = float(+0.00)
    
    opts.mesh_dims = +2             # 2-dim. simplexes
    
    opts.optm_qlim = +9.5E-01       # tighter opt. tol
    opts.optm_iter = +32    
    opts.optm_qtol = +1.0E-05

    jigsawpy.cmd.tetris(opts, 2, mesh)

#------------------------------------ save mesh for Paraview

    apos = jigsawpy.R3toS2(
        geom.radii, mesh.point["coord"][:])

    apos = apos * 180./np.pi

    zfun = interpolate.RectBivariateSpline(
        topo.ygrid, topo.xgrid, topo.value)

    mesh.value = zfun(
        apos[:, 1], apos[:, 0], grid=False)

    zmsk = \
    mesh.value[mesh.tria3["index"][:,0]] + \
    mesh.value[mesh.tria3["index"][:,1]] + \
    mesh.value[mesh.tria3["index"][:,2]]
    zmsk = zmsk / +3.0

    mesh.tria3 = mesh.tria3[zmsk < +0.]

    
    print("Writing ex_f.vtk file.")

    jigsawpy.savevtk(
        str(Path(dst_path)/"sp_f.vtk"), hfun)

    jigsawpy.savevtk(
        str(Path(dst_path)/"ex_f.vtk"), mesh)


    return


if (__name__ == "__main__"): ex_6()



