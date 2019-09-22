
from pathlib import Path
import os, copy
import numpy as np
from scipy import interpolate

import jigsawpy

def ex_5():

# DEMO-5: generate multi-resolution spacing, via local refi-
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

    hraw = jigsawpy.jigsaw_msh_t()
    hlim = jigsawpy.jigsaw_msh_t()
    
#------------------------------------ setup files for JIGSAW

    opts.geom_file = \
        str(Path(dst_path)/"earth.msh") # GEOM file
        
    opts.jcfg_file = \
        str(Path(dst_path)/"globe.jig") # JCFG file
    
    opts.hfun_file = \
        str(Path(dst_path)/"space.msh") # HFUN file

#------------------------------------ define JIGSAW geometry

    geom.mshID = "ellipsoid-mesh"
    geom.radii = np.full(3, 6371., 
        dtype=jigsawpy.jigsaw_msh_t.REALS_t)
    
    jigsawpy.savemsh(opts.geom_file, geom)

#------------------------------------ define spacing pattern

    jigsawpy.loadmsh(
        str(Path(src_path)/"topo.msh"), topo)

    hraw.mshID = "ellipsoid-grid"
    hraw.radii = geom.radii

    hraw.xgrid = topo.xgrid * np.pi/180.
    hraw.ygrid = topo.ygrid * np.pi/180.
   
    hfn0 = +150.                    # global spacing
    hfn2 = + 33.                    # adapt. spacing
    hfn3 = + 99.                    # arctic spacing
       
    hraw.value = np.sqrt(
        np.maximum(-topo.value, +0.0))

    hraw.value = \
        np.maximum(hraw.value, hfn2)
    hraw.value = \
        np.minimum(hraw.value, hfn3)

    hraw.value[hraw.ygrid < 30.*np.pi/180.] = hfn0
  
#------------------------------------ set HFUN grad.-limiter

    hlim = copy.copy(hraw)

    dhdx = +.025

    hlim.slope = np.full(
        topo.value.shape, dhdx, 
        dtype=jigsawpy.jigsaw_msh_t.REALS_t)

    jigsawpy.savemsh(opts.hfun_file, hlim)

    jigsawpy.cmd.marche(opts, hlim)

#------------------------------------ save mesh for Paraview

    xpos, ypos = \
        np.meshgrid(topo.xgrid, topo.ygrid)

    zval = topo.value

    xpos = np.reshape(xpos, (xpos.size))
    ypos = np.reshape(ypos, (ypos.size))
    zval = np.reshape(zval, (zval.size))


    print("Writing ex_e.vtk file.")

    jigsawpy.savevtk(
        str(Path(dst_path)/"sp_e_1.vtk"), hraw)

    jigsawpy.savevtk(
        str(Path(dst_path)/"sp_e_2.vtk"), hlim)


    return


if (__name__ == "__main__"): ex_5()



