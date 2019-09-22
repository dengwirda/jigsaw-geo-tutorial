
from pathlib import Path
import os
import numpy as np
from scipy import interpolate

import jigsawpy

def ex_7():

# DEMO-7: setup simple piecewise linear geometry definitions

    src_path = os.path.join(
        os.path.abspath(
        os.path.dirname(__file__)),"files")

    dst_path = os.path.join(
        os.path.abspath(
        os.path.dirname(__file__)),"cache")


    opts = jigsawpy.jigsaw_jig_t()

    geom = jigsawpy.jigsaw_msh_t()
    mesh = jigsawpy.jigsaw_msh_t()

#------------------------------------ setup files for JIGSAW

    opts.geom_file = \
        str(Path(dst_path)/"test.msh")  # GEOM file
        
    opts.jcfg_file = \
        str(Path(dst_path)/"test.jig")  # JCFG file
    
    opts.mesh_file = \
        str(Path(dst_path)/"mesh.msh")  # MESH file

#------------------------------------ define JIGSAW geometry

    geom.mshID = "euclidean-mesh"
    geom.ndims = +2
    geom.vert2 = np.array([ # list of xy "node" coordinate
      ((0, 0), 0),          # outer square
      ((9, 0), 0),
      ((9, 9), 0),
      ((0, 9), 0),
      ((4, 4), 0),          # inner square
      ((5, 4), 0),
      ((5, 5), 0),
      ((4, 5), 0)] ,
    dtype=jigsawpy.jigsaw_msh_t.VERT2_t)

    geom.edge2 = np.array([ # list of "edges" between vert
      ((0, 1), 0),          # outer square 
      ((1, 2), 0),
      ((2, 3), 0),
      ((3, 0), 0),
      ((4, 5), 0),          # inner square
      ((5, 6), 0),
      ((6, 7), 0),
      ((7, 4), 0)] ,
    dtype=jigsawpy.jigsaw_msh_t.EDGE2_t)

    jigsawpy.savemsh(opts.geom_file, geom)

#------------------------------------ make mesh using JIGSAW 
    
    opts.hfun_scal = "absolute"
    opts.hfun_hmax = +2.5E-01       # uniform at 0.250
    
    opts.mesh_dims = +2             # 2-dim. simplexes
    
   #opts.geom_feat = True           # do sharp feature
   #opts.mesh_top1 = True           # preserve 1-topo.

    opts.optm_qlim = +9.5E-01       # tighter opt. tol
    opts.optm_iter = +32    
    opts.optm_qtol = +1.0E-05

    jigsawpy.cmd.jigsaw(opts, mesh)

#------------------------------------ save mesh for Paraview

    print("Writing ex_g.vtk file.")

    jigsawpy.savevtk(
        str(Path(dst_path)/"ex_g.vtk"), mesh)


    return


if (__name__ == "__main__"): ex_7()



