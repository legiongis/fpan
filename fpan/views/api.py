from psycopg2 import sql
from django.core.cache import cache
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.db import transaction, connection
from arches.app.models import models
from arches.app.views.api import APIBase
from arches.app.models.system_settings import settings
from fpan.utils.permission_backend import get_allowed_resource_ids

class MVT(APIBase):
    EARTHCIRCUM = 40075016.6856
    PIXELSPERTILE = 256

    def get(self, request, nodeid, zoom, x, y):
        if hasattr(request.user, "userprofile") is not True:
            models.UserProfile.objects.create(user=request.user)
        viewable_nodegroups = request.user.userprofile.viewable_nodegroups
        try:
            node = models.Node.objects.get(nodeid=nodeid, nodegroup_id__in=viewable_nodegroups)
        except models.Node.DoesNotExist:
            raise Http404()
        config = node.config
        cache_key = f"mvt_{nodeid}_{zoom}_{x}_{y}"
        tile = cache.get(cache_key)

        res_access = get_allowed_resource_ids(request.user, str(node.graph_id))

        if res_access["access_level"] == "no_access":
            return HttpResponseForbidden()
        elif res_access["access_level"] == "full_access":
            resid_where = f"NULL IS NULL"
        else:
            ids = "','".join(res_access["id_list"])
            resid_where = f"resourceinstanceid IN ('{ids}')"

        if tile is None:
            with connection.cursor() as cursor:

                query_params = {
                    'nodeid': nodeid,
                    'zoom': zoom,
                    'x': x,
                    'y': y,
                    'resid_where': resid_where,
                }

                # TODO: when we upgrade to PostGIS 3, we can get feature state
                # working by adding the feature_id_name arg:
                # https://github.com/postgis/postgis/pull/303

                if int(zoom) <= int(config["clusterMaxZoom"]):
                    arc = self.EARTHCIRCUM / ((1 << int(zoom)) * self.PIXELSPERTILE)
                    distance = arc * int(config["clusterDistance"])
                    min_points = int(config["clusterMinPoints"])

                    query_params['distance'] = distance
                    query_params['min_points'] = min_points

                    cursor.execute(
                        """WITH clusters(tileid, resourceinstanceid, nodeid, geom, cid)
                        AS (
                            SELECT m.*,
                            ST_ClusterDBSCAN(geom, eps := {distance}, minpoints := {min_points}) over () AS cid
                            FROM (
                                SELECT tileid,
                                    resourceinstanceid,
                                    nodeid,
                                    geom
                                FROM mv_geojson_geoms
                                WHERE nodeid = '{nodeid}' AND {resid_where}
                            ) m
                        )

                        SELECT ST_AsMVT(
                            tile,
                             '{nodeid}',
                            4096,
                            'geom',
                            'id'
                        ) FROM (
                            SELECT resourceinstanceid::text,
                                row_number() over () as id,
                                1 as total,
                                ST_AsMVTGeom(
                                    geom,
                                    TileBBox({zoom}, {x}, {y}, 3857)
                                ) AS geom,
                                '' AS extent
                            FROM clusters
                            WHERE cid is NULL
                            UNION
                            SELECT NULL as resourceinstanceid,
                                row_number() over () as id,
                                count(*) as total,
                                ST_AsMVTGeom(
                                    ST_Centroid(
                                        ST_Collect(geom)
                                    ),
                                    TileBBox({zoom}, {x}, {y}, 3857)
                                ) AS geom,
                                ST_AsGeoJSON(
                                    ST_Extent(geom)
                                ) AS extent
                            FROM clusters
                            WHERE cid IS NOT NULL
                            GROUP BY cid
                        ) as tile;""".format(**query_params)
                    )
                else:
                    cursor.execute(
                        """SELECT ST_AsMVT(tile, '{nodeid}', 4096, 'geom', 'id') FROM (SELECT tileid,
                            row_number() over () as id,
                            resourceinstanceid,
                            nodeid,
                            ST_AsMVTGeom(
                                geom,
                                TileBBox({zoom}, {x}, {y}, 3857)
                            ) AS geom,
                            1 AS total
                        FROM mv_geojson_geoms
                        WHERE nodeid = '{nodeid}' AND {resid_where}) AS tile;""".format(**query_params)
                    )
                tile = bytes(cursor.fetchone()[0])
                cache.set(cache_key, tile, settings.TILE_CACHE_TIMEOUT)

        if not len(tile):
            raise Http404()
        return HttpResponse(tile, content_type="application/x-protobuf")