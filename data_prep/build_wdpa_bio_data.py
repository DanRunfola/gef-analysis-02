"""
input are two sets of data where each row has a gef id and between 1 and 4
wdpa ids.

wdpa polygons are then used to build a dataframe where each row has a wdpa id
and the longitude and latitude of the wdpa polygon centroid.

we then iterate over the concatenation of the original two data sets and
check for any match between their wdpa ids and the wdpa centroid lookup.
the first match found for the given wdpa ids becomes the "geocoded" coordinates
associated with that gef id project instance

result is saved as a geojson
"""



import os
import re
import json
import pandas as pd
import geopandas as gpd
import numpy as np
import fiona
from shapely.geometry import shape, Point


if os.environ.get('USER') == "vagrant":
    repo_dir = os.path.dirname(
        os.path.dirname(os.path.realpath(__file__)))
else:
    repo_dir = os.path.realpath(".")


def read_csv(path):
    '''read csv using pandas
    '''
    return pd.read_csv(path, quotechar='\"',
                       na_values='', keep_default_na=False,
                       encoding='utf-8')




gef_wdpa_2014_csv = "{0}/raw_data/wdpa/IUCN GEF Project and PA Database 24Oct (2014).csv".format(repo_dir)
gef_wdpa_2015_csv = "{0}/raw_data/wdpa/PAsList (from Najeeb - 28 JUL 2015).csv".format(repo_dir)

gef_wdpa_2014_df = read_csv(gef_wdpa_2014_csv)
gef_wdpa_2015_df = read_csv(gef_wdpa_2015_csv)


gef_wdpa_2014_df = gef_wdpa_2014_df.loc[gef_wdpa_2014_df['Found on PP?'] == 'Y']
gef_wdpa_2014_df = gef_wdpa_2014_df[['PMIS GEF ID', 'WDPA ID1', 'WDPA ID2', 'WDPA ID3', 'WDPA ID4']]
gef_wdpa_2014_df.columns = ['gef_id', 'wdpa01', 'wdpa02', 'wdpa03', 'wdpa04']

gef_wdpa_2015_df = gef_wdpa_2015_df.loc[~gef_wdpa_2015_df['WDPA ID'].isnull() | ~gef_wdpa_2015_df['Other WDPA IDs'].isnull()]
gef_wdpa_2015_df = gef_wdpa_2015_df[['gef_id', 'WDPA ID', 'Other WDPA IDs']]
gef_wdpa_2015_df.columns = ['gef_id', 'wdpa01', 'wdpa02']


gef_wdpa_df = pd.concat([gef_wdpa_2014_df, gef_wdpa_2015_df])


gef_wdpa_df['wdpa01'] = gef_wdpa_df['wdpa01'].astype(int).astype(str)
gef_wdpa_df['wdpa02'] = gef_wdpa_df['wdpa02'].astype(int).astype(str)
gef_wdpa_df['wdpa03'] = gef_wdpa_df['wdpa03'].astype(int).astype(str)
gef_wdpa_df['wdpa04'] = gef_wdpa_df['wdpa04'].astype(int).astype(str)


gef_wdpa_df['longitude'] = -999
gef_wdpa_df['latitude'] = -999

wdpa_id_list_raw = (list(gef_wdpa_df.loc[~gef_wdpa_df['wdpa01'].isnull(), 'wdpa01']) +
                    list(gef_wdpa_df.loc[~gef_wdpa_df['wdpa02'].isnull(), 'wdpa02']) +
                    list(gef_wdpa_df.loc[~gef_wdpa_df['wdpa03'].isnull(), 'wdpa03']) +
                    list(gef_wdpa_df.loc[~gef_wdpa_df['wdpa04'].isnull(), 'wdpa04']))


wdpa_id_list_raw = list(set(wdpa_id_list_raw))

wdpa_id_list = []
for i in wdpa_id_list_raw:
    try:
        wdpa_id_list.append(int(i))
    except:
        val_list = re.split('\W+', i)
        for j in val_list:
            try:
                wdpa_id_list.append(int(j))
            except:
                pass

wdpa_id_list = list(set(wdpa_id_list))


# -----------------------------------------------------------------------------

# this is just polygon features from WDPA export
# which have been simplified
# excess attribute fields may have been removed as well
wdpa_shp_path = "{0}/raw_data/wdpa/shps/WDPA_Dec2016_poly_simp.shp".format(repo_dir)
wdpa_shp = fiona.open(wdpa_shp_path)

wdpa_centroid_lookup = pd.DataFrame(columns=['index', 'wdpa_id', 'longitude', 'latitide'])

tmp_wdpa_id = []
tmp_wdpa_lon = []
tmp_wdpa_lat = []
for feat in wdpa_shp:
    wdpa_id = feat['properties']['WDPA_PID']
    try:
        centroid = shape(feat['geometry']).centroid
        tmp_wdpa_id.append(wdpa_id)
        tmp_wdpa_lon.append(centroid.x)
        tmp_wdpa_lat.append(centroid.y)
    except:
        print "Invalid feature ({0})".format(wdpa_id)


wdpa_centroid_lookup['index'] = tmp_wdpa_id
wdpa_centroid_lookup['wdpa_id'] = tmp_wdpa_id
wdpa_centroid_lookup['longitude'] = tmp_wdpa_lon
wdpa_centroid_lookup['latitude'] = tmp_wdpa_lat

wdpa_centroid_lookup['index'] = wdpa_centroid_lookup['index'].astype('str')
wdpa_centroid_lookup.set_index('index', inplace=True)



def get_wdpa_coords(row):
    valid = False
    for i in range(1,5):
        f = 'wdpa0{0}'.format(i)
        test_id = str(row[f])
        if isinstance(test_id, unicode):
            test_id = str(test_id)
        if not isinstance(test_id, str) and np.isnan(test_id):
            continue
        try:
            test_id = str(int(float(str(test_id))))
            match = wdpa_centroid_lookup.loc[test_id]
            lon = match['longitude']
            lat = match['latitude']
            valid = True
            break
        except Exception as e:
            continue
    if not valid:
        lat = -999
        lon = -999
    return pd.Series({'longitude':lon, 'latitude': lat})


coord_results =  gef_wdpa_df.apply(
    lambda z: get_wdpa_coords(z),
    axis=1)


gef_wdpa_df['longitude'] = coord_results['longitude']
gef_wdpa_df['latitude'] = coord_results['latitude']

out_gef_wdpa_df = gef_wdpa_df.copy(deep=True)

out_gef_wdpa_df = out_gef_wdpa_df[(out_gef_wdpa_df['longitude'] != -999) & (out_gef_wdpa_df['latitude'] != -999)]


out_gef_wdpa_gdf = gpd.GeoDataFrame(out_gef_wdpa_df)
out_gef_wdpa_gdf.geometry = out_gef_wdpa_gdf.apply(lambda z: Point(z.longitude, z.latitude), axis=1)


geo_json = out_gef_wdpa_gdf.to_json()
geo_path = "{0}/raw_data/external_bio.geojson".format(repo_dir)
geo_file = open(geo_path, "w")
json.dump(json.loads(geo_json), geo_file, indent=4)
geo_file.close()
