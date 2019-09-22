
from pathlib import Path
import os
import numpy as np
from scipy import interpolate

import jigsawpy

def ex_4():

# DEMO-4: per ex_3 - but using the multi-level scheme TETRIS

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
    str(Path(src_path)/"f_hr.msh") , hfun)
   
    hfun.value = +3. * hfun.value   # for fast example

    jigsawpy.savemsh(opts.hfun_file, hfun)

#------------------------------------ make mesh using JIGSAW 
    
    opts.hfun_scal = "absolute"
    opts.hfun_hmax = float("inf")   # null HFUN limits
    opts.hfun_hmin = float(+0.00)
    
    opts.mesh_dims = +2             # 2-dim. simplexes
    
    opts.optm_qlim = +9.5E-01       # tighter opt. tol
    opts.optm_iter = +32    
    opts.optm_qtol = +1.0E-05

    jigsawpy.cmd.tetris(opts, 2, mesh)

#------------------------------------ calc. mesh cost stats.

    deg2 = jigsawpy.trideg2(
        mesh.point["coord"], 
            mesh.tria3["index"])

    num6 = np.sum(deg2 == +6)

    print("Degree-6 nodes: " + 
        str(100. * num6 / deg2.size) + "%\n")

#------------------------------------ save mesh for Paraview

    jigsawpy.loadmsh(
        str(Path(src_path)/"topo.msh"), topo)
   
#------------------------------------ a very rough land mask

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

    
    print("Writing ex_d.vtk file.")

    jigsawpy.savevtk(
        str(Path(dst_path)/"ex_d.vtk"), mesh)


    return


if (__name__ == "__main__"): ex_4()



