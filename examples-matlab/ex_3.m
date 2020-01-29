function ex_3
% DEMO-3: generate a grid based on the "HR" spacing pattern,
% developed by the FESOM team at AWI.

    initjig;                            % load jigsaw

%------------------------------------ setup files for JIGSAW

    rootpath = fileparts( ...
        mfilename( 'fullpath' )) ;
    rootpath = ...
        fullfile(rootpath, '..') ;

    opts.geom_file = ...                % domain file
        fullfile(rootpath,...
            'cache', 'eSPH.msh') ;
    
    opts.jcfg_file = ...                % config file
        fullfile(rootpath,...
            'cache', 'eSPH.jig') ;
    
    opts.hfun_file = ...                % sizing file
        fullfile(rootpath,...
            'cache', 'spac.msh') ;

    opts.mesh_file = ...                % output file
        fullfile(rootpath,...
            'cache', 'mesh.msh') ;
    
%------------------------------------ define JIGSAW geometry

    geom.mshID = 'ELLIPSOID-MESH' ;
    geom.radii = 6371 * ones(3,1) ;
    
    savemsh (opts.geom_file,geom) ;

%------------------------------------ define spacing pattern

    hfun = loadmsh( ...
        fullfile(rootpath, ...
            'files', 'f_hr.msh')) ;
   
    hfun.value = +3. * hfun.value ;     % for fast example

    savemsh (opts.hfun_file,hfun) ;
    
%------------------------------------ build mesh via JIGSAW! 
    
    opts.hfun_scal = 'absolute' ;
    opts.hfun_hmin = +0.0 ;
    opts.hfun_hmax = +inf ;             % null HFUN limits
    
    opts.mesh_dims = +2 ;               % 2-dim. simplexes
    
    opts.optm_qlim = +9.5E-01 ;         % tighter opt. tol
    opts.optm_iter = +32;
    opts.optm_qtol = +1.0E-05 ;
    
    mesh = jigsaw(opts) ;
 
%------------------------------------ display JIGSAW outputs
  
    topo = loadmsh( ...
        fullfile(rootpath, ...
            'files', 'topo.msh')) ;
         
    plotsphere(geom,mesh,hfun,topo) ;

    drawnow ;        
    set(figure(2),'units','normalized', ...
    'position',[.05,.50,.25,.30]) ;
    
    set(figure(3),'units','normalized', ...
    'position',[.05,.10,.25,.30]) ;

    set(figure(1),'units','normalized', ...
    'position',[.30,.50,.25,.30]) ;
    
end



