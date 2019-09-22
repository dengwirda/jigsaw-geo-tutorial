
from pathlib import Path
import os
import numpy as np
from scipy import interpolate

import jigsawpy

def ex_8():

# DEMO-8: build regional meshes via stereographic projection

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

    proj = jigsawpy.jigsaw_prj_t()

#------------------------------------ setup files for JIGSAW

    opts.geom_file = \
        str(Path(dst_path)/"paci-proj.msh") # GEOM file
        
    opts.jcfg_file = \
        str(Path(dst_path)/"paci.jig")      # JCFG file
    
    opts.hfun_file = \
        str(Path(dst_path)/"paci-hfun.msh") # HFUN file

    opts.mesh_file = \
        str(Path(dst_path)/"paci-mesh.msh") # MESH file

#------------------------------------ define JIGSAW geometry

    jigsawpy.loadmsh(
        str(Path(src_path)/"paci.msh"), geom)

    jigsawpy.loadmsh(
        str(Path(src_path)/"topo.msh"), topo)

    xmin = np.min(geom.point["coord"][:,0])
    xmax = np.max(geom.point["coord"][:,0])
    
    xlon = np.linspace(xmin, xmax, 100)

    ymin = np.min(geom.point["coord"][:,1])
    ymax = np.max(geom.point["coord"][:,1])

    ylat = np.linspace(ymin, ymax, 100)
    
#------------------------------------ define spacing pattern

    hval = 200.

    hfun.mshID = "ellipsoid-grid"
    hfun.radii = np.full(3, 6371., 
        dtype=jigsawpy.jigsaw_msh_t.REALS_t)
    hfun.xgrid = xlon * np.pi / 180.
    hfun.ygrid = ylat * np.pi / 180.
    
    hfun.value = np.full(
        (ylat.size, xlon.size), hval, 
        dtype=jigsawpy.jigsaw_msh_t.REALS_t)

#------------------------------------ do stereographic proj.    
 
    geom.point["coord"][:,:] *= np.pi/180.

    proj.prjID  = 'stereographic'
    proj.radii  = +6371.E+00
    proj.xbase  = \
        +0.50 * (xmin + xmax) * np.pi/180.
    proj.ybase  = \
        +0.50 * (ymin + ymax) * np.pi/180.
  
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
    
   #opts.optm_qlim = +9.5E-01       # tighter opt. tol
    opts.optm_iter = +32
    opts.optm_qtol = +1.0E-05

    jigsawpy.cmd.jigsaw(opts, mesh)

#------------------------------------ save mesh for Paraview
    
    print("Writing ex_h.vtk file.")

    jigsawpy.savevtk(
        str(Path(dst_path)/"sp_h.vtk"), hfun)

    jigsawpy.savevtk(
        str(Path(dst_path)/"ex_h.vtk"), mesh)

#------------------------------------ transform on to sphere 

    jigsawpy.project(mesh, proj, "inv")

    radii = np.full(3, +6371., 
        dtype=jigsawpy.jigsaw_msh_t.REALS_t)

    mesh.vert3 = np.zeros(mesh.vert2.size, 
        dtype=jigsawpy.jigsaw_msh_t.VERT3_t)

    mesh.vert3["coord"] = jigsawpy.S2toR3(
        radii, mesh.vert2["coord"])

    mesh.vert2 = None
    
    jigsawpy.savevtk(
        str(Path(dst_path)/"ex_H.vtk"), mesh)


    return


if (__name__ == "__main__"): ex_8()



