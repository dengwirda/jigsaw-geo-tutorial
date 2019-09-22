function ex_1
% DEMO-1: generate a uniform resolution (150KM) global grid.

    addpath('../jigsaw-matlab') ;

    initjig;                            % load jigsaw

%------------------------------------ setup files for JIGSAW

    rootpath = fileparts( ...
        mfilename( 'fullpath' ) ) ;

    opts.geom_file = ...                % domain file
        fullfile(rootpath,...
        'cache','globe-geom.msh') ;
    
    opts.jcfg_file = ...                % config file
        fullfile(rootpath,...
        'cache','globe.jig') ;
    
    opts.mesh_file = ...                % output file
        fullfile(rootpath,...
        'cache','globe-mesh.msh') ;
    
%------------------------------------ define JIGSAW geometry

    geom.mshID = 'ELLIPSOID-MESH' ;
    geom.radii = 6371 * ones(3,1) ;
    
    savemsh (opts.geom_file,geom) ;
    
%------------------------------------ build mesh via JIGSAW! 
    
    opts.hfun_scal = 'absolute';
    opts.hfun_hmax = +150. ;            % uniform at 150km
    
    opts.mesh_dims = +2 ;               % 2-dim. simplexes
    
    opts.optm_qlim = +9.5E-01 ;         % tighter opt. tol
    opts.optm_iter = +32;
    opts.optm_qtol = +1.0E-05 ;
    
    mesh = jigsaw(opts) ;
 
%------------------------------------ display JIGSAW outputs
  
    topo = loadmsh( ...
        fullfile(rootpath, ...
            'files', 'topo.msh')) ;
         
    plotsphere(geom,mesh,[],topo) ;

    drawnow ;        
    set(figure(1),'units','normalized', ...
    'position',[.05,.50,.25,.30]) ;
    
    set(figure(2),'units','normalized', ...
    'position',[.05,.10,.25,.30]) ;
    
end



