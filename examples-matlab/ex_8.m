function ex_8
% DEMO-8: build regional meshes via stereographic projection

    initjig;                            % load jigsaw

%------------------------------------ setup files for JIGSAW

    rootpath = fileparts( ...
        mfilename( 'fullpath' ) ) ;
    rootpath = ...
        fullfile(rootpath, '..') ;

    opts.geom_file = ...                % domain file
        fullfile(rootpath,...
            'cache', 'proj.msh') ;

    opts.jcfg_file = ...                % config file
        fullfile(rootpath,...
            'cache', 'paci.jig') ;

    opts.mesh_file = ...                % output file
        fullfile(rootpath,...
            'cache', 'mesh.msh') ;

    opts.hfun_file = ...                % sizing file
        fullfile(rootpath,...
            'cache', 'spac.msh') ;

%------------------------------------ define JIGSAW geometry

    geom = loadmsh( ...
        fullfile(rootpath, ...
            'files', 'paci.msh')) ;

    xmin = min(geom.point.coord(:,1)) ;
    xmax = max(geom.point.coord(:,1)) ;
    ymin = min(geom.point.coord(:,2)) ;
    ymax = max(geom.point.coord(:,2)) ;

    xlon = linspace(xmin, xmax, 100);
    ylat = linspace(ymin, ymax, 100);

%------------------------------------ define spacing pattern

    hval = 200.;

    hfun.mshID = 'ELLIPSOID-GRID';
    hfun.radii = 6371.E+00;
    hfun.point.coord{1} = xlon * pi/180. ;
    hfun.point.coord{2} = ylat * pi/180. ;
    hfun.value = ...
    hval*ones(length(ylat),length(xlon)) ;

%------------------------------------ do stereographic proj.

    geom.point.coord(:,1:2) = ...
    geom.point.coord(:,1:2) * pi/180. ;

    proj.prjID = 'STEREOGRAPHIC' ;
    proj.radii = 6371.E+00;
    proj.xbase = .5 * ( ...
        min(geom.point.coord(:,1)) ...
      + max(geom.point.coord(:,1))) ;
    proj.ybase = .5 * ( ...
        min(geom.point.coord(:,2)) ...
      + max(geom.point.coord(:,2))) ;

    GEOM = project(geom,proj,'fwd') ;
    HFUN = project(hfun,proj,'fwd') ;

    savemsh (opts.geom_file,GEOM) ;
    savemsh (opts.hfun_file,HFUN) ;

%------------------------------------ build mesh via JIGSAW!

    opts.hfun_scal = 'absolute' ;
    opts.hfun_hmin = +0.0 ;
    opts.hfun_hmax = +inf ;             % null HFUN limits

    opts.mesh_dims = +2 ;               % 2-dim. simplexes

    opts.mesh_eps1 = +1.0E+00 ;         % relax edge error

    opts.optm_iter = +32;
    opts.optm_qtol = +1.0E-05 ;

    MESH = jigsaw(opts) ;

%------------------------------------ transform on to sphere

    mesh = project(MESH,proj,'inv') ;

    radii = 6371. * ones(3,1) ;

    mesh.point.coord(:,1:3) = S2toR3( ...
    radii, mesh.point.coord(:,1:2)) ;

    geom.point.coord(:,1:3) = S2toR3( ...
    radii, geom.point.coord(:,1:2)) ;

%------------------------------------ display JIGSAW outputs

    plotplanar(GEOM,MESH,HFUN) ;

    drawnow ;
    set(figure(1),'units','normalized', ...
    'position',[.05,.50,.25,.30]) ;

    set(figure(2),'units','normalized', ...
    'position',[.30,.50,.25,.30]) ;

    set(figure(4),'units','normalized', ...
    'position',[.05,.10,.25,.30]) ;

    set(figure(3),'units','normalized', ...
    'position',[.30,.10,.25,.30]) ;

    set(figure(5),'units','normalized', ...
    'position',[.55,.10,.25,.30]) ;

    patch( ...
       'faces',mesh.tria3.index(:,1:3), ...
    'vertices',mesh.point.coord(:,1:3), ...
    'facecolor','w', ...
    'edgecolor','k') ;
    hold on; axis image off;
    patch( ...
       'faces',geom.edge2.index(:,1:2), ...
    'vertices',geom.point.coord(:,1:3), ...
    'facecolor','w', ...
    'edgecolor','b') ;
    plot3(+0.,+0.,+0.,'ko');
    set(gca,'clipping','off');

end



