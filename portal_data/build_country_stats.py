

import os
import json
import fiona
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point, shape


def read_csv(path):
    '''read csv using pandas
    '''
    return pd.read_csv(path, quotechar='\"',
                       na_values='', keep_default_na=False,
                       encoding='utf-8')


iso_key = 'iso_a3'
# iso_key = 'ISO'

# deleted usa, canada, greenland, antarctica
adm0_path = os.path.expanduser(
    "~/Desktop/gef_portal_data/countries.geojson")
    # "~/Desktop/gef_portal_data/gadm28_adm0_mod.shp")

adm0_shp = fiona.open(adm0_path, 'r')

adm0_gdf = gpd.GeoDataFrame.from_file(adm0_path)
adm0_gdf['index'] = adm0_gdf[iso_key]
adm0_gdf.set_index('index', inplace=True)



# -----------------------------------------------------------------------------


fc_path = os.path.expanduser(
    "~/Desktop/gef_portal_data/output_website_fc.csv")

fc_out = os.path.expanduser(
    "~/Desktop/gef_portal_data/fc_country.csv")

fc_geojson = os.path.expanduser(
    "~/Desktop/gef_portal_data/fc_country.geojson")


fc_df = read_csv(fc_path)
fc_df['geometry'] = fc_df.apply(lambda z: Point(z.longitude, z.latitude), axis=1)
fc_gdf = gpd.GeoDataFrame(fc_df)

fc_gdf['country_iso'] = -1
for feat in adm0_shp:
    iso = feat['properties'][iso_key]
    print iso
    shp = shape(feat['geometry'])#.simplify(0.001)
    fc_gdf['contains'] = -1
    try:
        fc_gdf['contains'] = fc_gdf['geometry'].within(shp)
    except:
        try:
            fc_gdf['contains'] = fc_gdf['geometry'].within(shp.buffer(0))
        except:
            print "WARNING - {0} has invalid shape".format(iso)
    fc_gdf.loc[fc_gdf['contains'] == 1, 'country_iso'] = iso


fc_matched = fc_gdf.loc[fc_gdf['country_iso'] != -1].copy(deep=True)
fc_country = fc_matched.groupby('country_iso')['tree.pred'].agg([np.mean, np.std, 'count'])

fc_country.to_csv(fc_out, index=True, encoding='utf-8')


fc_country_gdf = adm0_gdf.copy(deep=True)
fc_country_gdf = fc_country_gdf.loc[fc_country_gdf[iso_key].isin(list(fc_country.index))]
fc_country_gdf = fc_country_gdf.merge(fc_country, left_index=True, right_index=True)


fc_json = fc_country_gdf.to_json()
fc_file = open(fc_geojson, "w")
json.dump(json.loads(fc_json), fc_file)
fc_file.close()


# -----------------------------------------------------------------------------


ndvi_path = os.path.expanduser(
    "~/Desktop/gef_portal_data/output_website_ndvi.csv")

ndvi_out = os.path.expanduser(
    "~/Desktop/gef_portal_data/ndvi_country.csv")

ndvi_geojson = os.path.expanduser(
    "~/Desktop/gef_portal_data/ndvi_country.geojson")


ndvi_df = read_csv(ndvi_path)
ndvi_df['geometry'] = ndvi_df.apply(lambda z: Point(z.longitude, z.latitude), axis=1)
ndvi_gdf = gpd.GeoDataFrame(ndvi_df)

ndvi_gdf['country_iso'] = -1
for feat in adm0_shp:
    iso = feat['properties'][iso_key]
    print iso
    shp = shape(feat['geometry']).simplify(0.001)
    ndvi_gdf['contains'] = -1
    try:
        ndvi_gdf['contains'] = ndvi_gdf['geometry'].within(shp)
    except:
        try:
            ndvi_gdf['contains'] = ndvi_gdf['geometry'].within(shp.buffer(0))
        except:
            print "WARNING - {0} has invalid shape".format(iso)
    ndvi_gdf.loc[ndvi_gdf['contains'] == 1, 'country_iso'] = iso


ndvi_matched = ndvi_gdf.loc[ndvi_gdf['country_iso'] != -1].copy(deep=True)
ndvi_country = ndvi_matched.groupby(['country_iso'])['tree.pred'].agg([np.mean, np.std, 'count'])


ndvi_country.to_csv(ndvi_out, index=True, encoding='utf-8')


ndvi_country_gdf = adm0_gdf.copy(deep=True)
ndvi_country_gdf = ndvi_country_gdf.loc[ndvi_country_gdf[iso_key].isin(list(ndvi_country.index))]
ndvi_country_gdf = ndvi_country_gdf.merge(ndvi_country, left_index=True, right_index=True)


ndvi_json = ndvi_country_gdf.to_json()
ndvi_file = open(ndvi_geojson, "w")
json.dump(json.loads(ndvi_json), ndvi_file)
ndvi_file.close()

