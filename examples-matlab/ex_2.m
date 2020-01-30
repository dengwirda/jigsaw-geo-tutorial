function ex_2
% DEMO-2: generate a regionally-refined global grid with a
% high-resolution "patch" embedded in a uniform background
% grid.

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

    hfun.mshID = 'ELLIPSOID-GRID' ;
    hfun.radii = geom.radii;

    hfun.point.coord{1} = linspace( ...
        -1.*pi, +1.*pi, 720) ;

    hfun.point.coord{2} = linspace( ...
        -.5*pi, +.5*pi, 360) ;

   [xmat, ymat] = meshgrid ( ...
        hfun.point.coord{1}, ...
        hfun.point.coord{2}) ;

    hfun.value = +150. - 100. * exp( -( ...
        +1.5 * (xmat + 1.0).^2 ...
        +1.5 * (ymat - 0.5).^2).^4) ;

   %hfun.value = ...
   %    +150.0 - 100.0 * sin(ymat).^2 ;

    savemsh (opts.hfun_file,hfun) ;

%------------------------------------ build mesh via JIGSAW!

    opts.hfun_scal = 'absolute' ;
    opts.hfun_hmin = +0.0 ;
    opts.hfun_hmax = +inf ;             % null HFUN limits

    opts.mesh_dims = +2 ;               % 2-dim. simplexes

    opts.optm_qlim = +9.5E-01 ;         % tighter opt. tol
    opts.optm_iter = +32;
    opts.optm_qtol = +1.0E-05 ;

    mesh = tetris(opts, +3) ;

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



