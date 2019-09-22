
from pathlib import Path
import os
import numpy as np
from scipy import interpolate

import jigsawpy

def ex_9():

# DEMO-9: generate a 2-dim. grid for the Australian coastal 
# region, using topography as a mesh-spacing indicator. A
# local stereographic projection is employed.

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
        str(Path(dst_path)/"aust-proj.msh") # GEOM file
        
    opts.jcfg_file = \
        str(Path(dst_path)/"aust.jig")      # JCFG file
    
    opts.hfun_file = \
        str(Path(dst_path)/"aust-hfun.msh") # HFUN file

    opts.mesh_file = \
        str(Path(dst_path)/"aust-mesh.msh") # MESH file

#------------------------------------ define JIGSAW geometry

    jigsawpy.loadmsh(
        str(Path(src_path)/"aust.msh"), geom)

    jigsawpy.loadmsh(
        str(Path(src_path)/"topo.msh"), topo)

    xmin = np.min(geom.point["coord"][:,0])
    xmax = np.max(geom.point["coord"][:,0])
    ymin = np.min(geom.point["coord"][:,1])
    ymax = np.max(geom.point["coord"][:,1])
    
    xmsk = np.logical_and(topo.xgrid >= xmin, 
                          topo.xgrid <= xmax)
    ymsk = np.logical_and(topo.ygrid >= ymin, 
                          topo.ygrid <= ymax)

    zlev = topo.value
    zlev = zlev[:,xmsk]; zlev = zlev[ymsk,:]

#------------------------------------ define spacing pattern

    hfun.mshID = "ellipsoid-grid"
    hfun.radii = np.full(3, 6371., 
        dtype=jigsawpy.jigsaw_msh_t.REALS_t)
    hfun.xgrid = \
        topo.xgrid[xmsk] * np.pi / 180.
    hfun.ygrid = \
        topo.ygrid[ymsk] * np.pi / 180.
    
    hmin = +1.0E+01; hmax = +1.0E+02

    hfun.value = \
        np.sqrt(np.maximum(-zlev, 0.)) / .5

    hfun.value = \
        np.maximum(hfun.value, hmin)
    hfun.value = \
        np.minimum(hfun.value, hmax) 

    hfun.slope = np.full(
        hfun.value.shape, +.1750, 
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

#------------------------------------ set HFUN grad.-limiter
    
    jigsawpy.cmd.marche(opts, hfun)

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
    
    print("Writing ex_i.vtk file.")

    jigsawpy.savevtk(
        str(Path(dst_path)/"sp_i.vtk"), hfun)

    jigsawpy.savevtk(
        str(Path(dst_path)/"ex_i.vtk"), mesh)

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
        str(Path(dst_path)/"ex_I.vtk"), mesh)


    return


if (__name__ == "__main__"): ex_9()



