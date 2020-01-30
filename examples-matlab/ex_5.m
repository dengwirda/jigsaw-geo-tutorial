function ex_5
% DEMO-5: generate multi-resolution spacing, via local refi-
% nement along coastlines and shallow ridges. Global grid
% resolution is 150KM, background resolution is 99KM and the
% min. adaptive resolution is 33KM.

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

    hfun = +hfn0*ones(size(zlev)) ;

    htop = sqrt(max(-zlev(:),eps))/1. ;
    htop = max(htop,hfn2);
    htop = min(htop,hfn3);
    htop(zlev>0.) = hfn0 ;

    hfun(YPOS>=40.) = htop(YPOS>=40.) ;

%------------------------------------ set HFUN grad.-limiter

    dhdx = +.025;                       % max. gradients
   %dhdx = +0.05;

    hraw.mshID = 'ELLIPSOID-GRID' ;
    hraw.radii = geom.radii ;
    hraw.point.coord{1} = xpos*pi/180 ;
    hraw.point.coord{2} = ypos*pi/180 ;
    hraw.value = single(hfun) ;
    hraw.slope = dhdx*ones(size(hfun));

    savemsh (opts.hfun_file,hraw) ;

%------------------------------------ set HFUN grad.-limiter

    hlim = marche(opts) ;

    plotsphere(geom,[],hraw,topo) ;
    plotsphere(geom,[],hlim,topo) ;

    drawnow ;
    set(figure(1),'units','normalized', ...
    'position',[.05,.50,.25,.30]) ;
    title('H(x): raw data');

    set(figure(2),'units','normalized', ...
    'position',[.30,.50,.25,.30]) ;
    title('H(x): smoothed');

end



