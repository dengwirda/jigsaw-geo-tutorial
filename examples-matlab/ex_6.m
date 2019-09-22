function ex_6
% DEMO-6: generate a multi-resolution grid, with local refi-
% nement along coastlines and shallow ridges. Global grid 
% resolution is 150KM, background resolution is 99KM and the 
% min. adaptive resolution is 33KM.

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
    
    opts.hfun_file = ...                % sizing file
        fullfile(rootpath,...
        'cache','globe-hfun.msh') ;

    opts.mesh_file = ...                % output file
        fullfile(rootpath,...
        'cache','globe-mesh.msh') ;
    
%------------------------------------ define JIGSAW geometry

    geom.mshID = 'ELLIPSOID-MESH' ;
    geom.radii = 6371 * ones(3,1) ;
    
    savemsh (opts.geom_file,geom) ;

%------------------------------------ define spacing pattern

    topo = loadmsh( ...
        fullfile(rootpath, ...
            'files', 'topo.msh')) ;
   
    xpos = topo.point.coord{1};
    ypos = topo.point.coord{2};
    zlev = topo.value;
    
   [XPOS,YPOS] = meshgrid (xpos,ypos) ;
      
    hfn0 = +150. ;                      % global spacing
    hfn2 = +33.;                        % adapt. spacing
    hfn3 = +99.;                        % arctic spacing
    
    hmat = +hfn0*ones(size(zlev)) ;
    
    htop = sqrt(max(-zlev(:),eps))/1. ;
    htop = max(htop,hfn2);
    htop = min(htop,hfn3);
    htop(zlev>0.) = hfn0 ;
    
    hmat(YPOS>=45.) = htop(YPOS>=45.) ;

%------------------------------------ set HFUN grad.-limiter
    
    dhdx = +.050;                       % max. gradients
       
    hfun.mshID = 'ELLIPSOID-GRID' ;
    hfun.radii = geom.radii ;
    hfun.point.coord{1} = xpos*pi/180 ;
    hfun.point.coord{2} = ypos*pi/180 ;
    hfun.value = single(hmat) ;
    hfun.slope = dhdx*ones(size(hmat));
    
    savemsh (opts.hfun_file,hfun) ;
 
%------------------------------------ set HFUN grad.-limiter

    hfun = marche(opts) ;
    
%------------------------------------ build mesh via JIGSAW! 
    
    opts.hfun_scal = 'absolute' ;
    opts.hfun_hmin = +0.0 ;
    opts.hfun_hmax = +inf ;             % null HFUN limits
    
    opts.mesh_dims = +2 ;               % 2-dim. simplexes
    
    opts.optm_qlim = +9.5E-01 ;         % tighter opt. tol
    opts.optm_iter = +32;
    opts.optm_qtol = +1.0E-05 ;
    
    mesh = tetris(opts, +2) ;
 
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



