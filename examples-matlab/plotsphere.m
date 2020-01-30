function plotsphere(geom,mesh,hfun,topo)
%PLOT-SPHERE draw JIGSAW output for meshes on sphere.

    if (~isempty(topo))
        xpos = topo.point.coord{1};
        ypos = topo.point.coord{2};
        zlev = reshape( ...
        topo.value,length(ypos),length(xpos));
    else
        zlev = [] ;
    end

    if (~isempty(hfun))
    switch (upper(hfun.mshID))
        case{'EUCLIDEAN-GRID', ...
             'ELLIPSOID-GRID'}
%------------------------------------ disp. 'grid' functions
        hfun.value = reshape(hfun.value, ...
            length(hfun.point.coord{2}), ...
            length(hfun.point.coord{1})  ...
            ) ;
        if (all(size(hfun.value)==size(zlev)))
            vals = hfun.value ;
            vals(zlev>0.) = inf ;
        else
            vals = hfun.value ;
        end
        figure('color','w');
        surf(hfun.point.coord{1}*180/pi, ...
             hfun.point.coord{2}*180/pi, ...
             vals) ;
        view(2); axis image; hold on ;
        shading interp;
        title('JIGSAW HFUN data') ;
    end
    end

    if (~isempty(mesh))
%------------------------------------ draw unstructured mesh
    if (~isempty(topo))
        tlev = findalt( ...
            geom,mesh,xpos,ypos,zlev);
        W   = tlev <= +0. ;
        D   = tlev >  +0. ;
        figure('color','w') ;
        patch ('faces',mesh.tria3.index(W,1:3), ...
            'vertices',mesh.point.coord(:,1:3), ...
            'facevertexcdata',tlev(W), ...
            'facecolor','flat', ...
            'edgecolor','k') ;
        hold on; axis image off;
        patch ('faces',mesh.tria3.index(D,1:3), ...
            'vertices',mesh.point.coord(:,1:3), ...
            'facecolor','w', ...
            'edgecolor','none');
        set(gca,'clipping','off') ;
        caxis([min(zlev(:))*9./8., +0.]);
        brighten(+0.75);
    else
        figure('color','w') ;
        patch ('faces',mesh.tria3.index(:,1:3), ...
            'vertices',mesh.point.coord(:,1:3), ...
            'facecolor','w', ...
            'edgecolor','k') ;
        hold on; axis image off;
        set(gca,'clipping','off') ;
    end
    drawcost(mesh, hfun) ;
    end

end

function [zlev] = ...
    findalt(geom,mesh,alon,alat,topo)
%FINDALT calc. an "altitude" for each tria-cell in the mesh.

    xsph = R3toS2( ...
        geom.radii, mesh.point.coord(:, 1:3));

    xlat = xsph(:,2) * 180 / pi;
    xlon = xsph(:,1) * 180 / pi;

    xlev = interp2 (alon,alat,topo,xlon,xlat);

    zlev = xlev (mesh.tria3.index(:,1)) ...
         + xlev (mesh.tria3.index(:,2)) ...
         + xlev (mesh.tria3.index(:,3)) ;
    zlev = zlev / +3.0 ;

end



