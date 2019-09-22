function ex_7
% DEMO-7: setup simple piecewise linear geometry definitions

    addpath('../jigsaw-matlab') ;

    initjig;                            % load jigsaw

%------------------------------------ setup files for JIGSAW

    rootpath = fileparts( ...
        mfilename( 'fullpath' ) ) ;

    opts.geom_file = ...                % domain file
        fullfile(rootpath,...
        'cache','pslg-geom.msh') ;
    
    opts.jcfg_file = ...                % config file
        fullfile(rootpath,...
        'cache','pslg.jig') ;

    opts.mesh_file = ...                % output file
        fullfile(rootpath,...
        'cache','pslg-mesh.msh') ;
    
%------------------------------------ define JIGSAW geometry

    geom.mshID = 'EUCLIDEAN-MESH' ;

    geom.point.coord = [    % list of xy "node" coordinates
        0, 0, 0             % outer square
        9, 0, 0
        9, 9, 0
        0, 9, 0 
        4, 4, 0             % inner square
        5, 4, 0
        5, 5, 0
        4, 5, 0 ] ;
    
    geom.edge2.index = [    % list of "edges" between nodes
        1, 2, 0             % outer square 
        2, 3, 0
        3, 4, 0
        4, 1, 0 
        5, 6, 0             % inner square
        6, 7, 0
        7, 8, 0
        8, 5, 0 ] ;
    
    savemsh (opts.geom_file,geom) ;
    
%------------------------------------ build mesh via JIGSAW! 
    
    opts.hfun_scal = 'absolute' ;
    opts.hfun_hmin = +0.0 ;
    opts.hfun_hmax = +2.5E-01           % uniform at 0.250
    
    opts.mesh_dims = +2 ;               % 2-dim. simplexes
    
    opts.optm_qlim = +9.5E-01 ;         % tighter opt. tol
    opts.optm_iter = +32;
    opts.optm_qtol = +1.0E-05 ;
    
    mesh = jigsaw(opts) ;
 
%------------------------------------ display JIGSAW outputs
  
    topo = loadmsh( ...
        fullfile(rootpath, ...
            'files', 'topo.msh')) ;
         
    plotplanar(geom,mesh,[]) ;

    drawnow ;        
    set(figure(1),'units','normalized', ...
    'position',[.05,.50,.25,.30]) ;
    
    set(figure(2),'units','normalized', ...
    'position',[.30,.50,.25,.30]) ;

    set(figure(3),'units','normalized', ...
    'position',[.05,.10,.25,.30]) ;

end



