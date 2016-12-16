# merge raw data into single file

import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point


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


# biodiversity (treatment)
bio_csv = "{0}/raw_data/biodiversity_treatment.csv".format(repo_dir)
bio_df = read_csv(bio_csv)
bio_df['type'] = 'bio'


# land degradation (treatment)
land_csv = "{0}/raw_data/landdegradation_treatment.csv".format(repo_dir)
land_df = read_csv(land_csv)
land_df['type'] = 'land'


# multi focal area (treatment)
mfa_csv = "{0}/raw_data/multifocalarea_treatment.csv".format(repo_dir)
mfa_df = read_csv(mfa_csv)
mfa_df['type'] = 'mfa'


# programmatic (treatment)
prog_csv = "{0}/raw_data/programmatic_treatment.csv".format(repo_dir)
prog_df = read_csv(prog_csv)
prog_df['type'] = 'prog'

prog_coord_csv = "{0}/raw_data/programmatic_treatments_coords.csv".format(repo_dir)
prog_coord_df = read_csv(prog_coord_csv)

prog_df = prog_df.merge(prog_coord_df[['id', 'latitude', 'longitude']], on='id')


# programmatic (control)
rand_csv = "{0}/raw_data/programmatic_control.csv".format(repo_dir)
rand_df = read_csv(rand_csv)
rand_df['type'] = 'rand'

rand_coord_csv = "{0}/raw_data/programmatic_controls_coords.csv".format(repo_dir)
rand_coord_df = read_csv(rand_coord_csv)

rand_df = rand_df.merge(rand_coord_df[['id', 'latitude', 'longitude']], on='id')



# concat all data
merged_df = pd.concat([bio_df, land_df, mfa_df, prog_df, rand_df])


# add iba field
merged_gdf = gpd.GeoDataFrame(merged_df)
merged_gdf.geometry = merged_gdf.apply(lambda z: Point(z.longitude, z.latitude), axis=1)


iba_csv = "{0}/raw_data/iba/IBA monitoring data 4 Nov 2015.csv".format(repo_dir)
iba_raw_df = read_csv(iba_csv)

# drop statescore 5 (areas that were not assessed) and
# sort by year and only keep last one
# to get rid of multiples for each site
iba_df = iba_raw_df.copy(deep=True)

iba_df = iba_df.loc[(iba_df['StateScore'] != 5)]
iba_df = iba_df.sort_values(by='MonitoringYear', ascending=1)
iba_df = iba_df.groupby('SiteID').last()

# convert to geodataframe
iba_gdf = gpd.GeoDataFrame(iba_df)
iba_gdf.geometry = iba_gdf.apply(lambda z: Point(z.Longitude, z.Latitude), axis=1)


# actual values for assessed areas are 0-3
merged_gdf['iba_statescore'] = -1
merged_gdf['iba_distance'] = -1
merged_gdf['iba_area'] = -1

iba_distance = []
iba_statescore = []
iba_area = []

for i in range(len(merged_gdf)):
    distance_vals = iba_gdf.geometry.distance(merged_gdf.iloc[i].geometry)
    distance_vals.sort_values(inplace=True)

    ix = distance_vals.index[0]

    distance = distance_vals.iloc[0]
    score = iba_gdf.loc[ix]['StateScore']
    area = iba_gdf.loc[ix]['Area']

    iba_distance.append(distance)
    iba_statescore.append(score)
    iba_area.append(area)


merged_gdf['iba_distance'] = iba_distance
merged_gdf['iba_statescore'] = iba_statescore
merged_gdf['iba_area'] = iba_area


merged_out = pd.DataFrame(merged_gdf)

# output data
out_path = "{0}/data_prep/merged_data.csv".format(repo_dir)
merged_out.to_csv(out_path, index=False, encoding='utf-8')

