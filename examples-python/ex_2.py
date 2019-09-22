
from pathlib import Path
import os
import numpy as np
from scipy import interpolate

import jigsawpy

def ex_2():

# DEMO-2: generate a regionally-refined global grid with a 
# high-resolution "patch" embedded in a uniform background 
# grid.

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

    hfun.mshID = "ellipsoid-grid"
    hfun.radii = geom.radii

    hfun.xgrid = np.linspace( 
        -1.*np.pi, +1.*np.pi, 180)
                    
    hfun.ygrid = np.linspace(
        -.5*np.pi, +.5*np.pi, 90 )

    xmat, ymat = \
        np.meshgrid(hfun.xgrid, hfun.ygrid)

    hfun.value = +150. - 100. * np.exp(
        -1.5*((xmat+1.)**2+(ymat-.5)**2)**2
              )
   
    jigsawpy.savemsh(opts.hfun_file, hfun)

#------------------------------------ make mesh using JIGSAW 
    
    opts.hfun_scal = "absolute"
    opts.hfun_hmax = float("inf")   # null HFUN limits
    opts.hfun_hmin = float(+0.00)
    
    opts.mesh_dims = +2             # 2-dim. simplexes
    
    opts.optm_qlim = +9.5E-01       # tighter opt. tol
    opts.optm_iter = +32    
    opts.optm_qtol = +1.0E-05
    
    jigsawpy.cmd.jigsaw(opts, mesh)

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

    
    print("Writing ex_b.vtk file.")

    jigsawpy.savevtk(
        str(Path(dst_path)/"sp_b.vtk"), hfun)

    jigsawpy.savevtk(
        str(Path(dst_path)/"ex_b.vtk"), mesh)


    return


if (__name__ == "__main__"): ex_2()



