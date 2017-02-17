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


# -------------------------------------
# load data

# treatments extract data
treatments_csv = "{0}/raw_data/merge_gef_treatments.csv".format(repo_dir)
treatments_df = read_csv(treatments_csv)
treatments_df['gef_id'] = treatments_df['gef_id'].astype('int').astype('str')
data_df = treatments_df.copy(deep=True)


# get project location id by matching shapefile generated id
treatments_location_id_csv = "{0}/raw_data/treatments_location_id.csv".format(repo_dir)
treatments_location_id_df = read_csv(treatments_location_id_csv)
treatments_location_id_df = treatments_location_id_df[['id', 'project_location_id']]
data_df = data_df.merge(treatments_location_id_df, on='id')


# get round from project ancillary table
projects_ancillary_csv = "{0}/raw_data/aiddata/GlobalEnvironmentFacility_GeocodedResearchRelease_Level1_v1.0/data/projects_ancillary.csv".format(repo_dir)
projects_ancillary_df = read_csv(projects_ancillary_csv)
projects_ancillary_df = projects_ancillary_df[['gef_id', 'round']]
projects_ancillary_df['gef_id'] = projects_ancillary_df['gef_id'].astype('int').astype('str')
data_df = data_df.merge(projects_ancillary_df, on='gef_id', how='left')


# get location type code from locations table
locations_csv = "{0}/raw_data/aiddata/GlobalEnvironmentFacility_GeocodedResearchRelease_Level1_v1.0/data/locations.csv".format(repo_dir)
locations_df = read_csv(locations_csv)
locations_df = locations_df[['project_location_id', 'project_id', 'location_type_code']]
data_df = data_df.merge(locations_df, on='project_location_id', how='left')

# get year info from projects table
projects_csv = "{0}/raw_data/aiddata/GlobalEnvironmentFacility_GeocodedResearchRelease_Level1_v1.0/data/projects.csv".format(repo_dir)
projects_df = read_csv(projects_csv)
projects_df = projects_df[['project_id', 'transactions_start_year', 'transactions_end_year']]
data_df = data_df.merge(projects_df, on='project_id', how='left')


# gef project info
master_gef_projects_csv = "{0}/raw_data/ancillary/master_gef_projects.csv".format(repo_dir)
master_gef_projects_df = read_csv(master_gef_projects_csv)
master_gef_projects_df['gef_id'] = master_gef_projects_df['GEF_ID'].astype('int').astype('str')
data_df = data_df.merge(master_gef_projects_df, on='gef_id', how='left')


# mfa funding info
funding_csv = "{0}/raw_data/ancillary/mfa_funding_breakdown.csv".format(repo_dir)
funding_df = read_csv(funding_csv)
funding_df['gef_id'] = funding_df['GEF ID'].astype('int').astype('str')
data_df = data_df.merge(funding_df, on='gef_id', how='left')


# data_df.to_csv(
#     "{0}/data_prep/debug.csv".format(repo_dir),
#     index=False, encoding='utf-8')
# raise


# assign types
data_df.loc[data_df['round'] == "Programmatic", 'type'] = 'prog'
data_df.loc[data_df['round'] == "MFA", 'type'] = 'mfa'
data_df.loc[data_df['round'] == "Biodiversity", 'type'] = 'bio'
data_df.loc[data_df['round'] == "Land Degradation", 'type'] = 'land'
data_df.loc[data_df['project_location_id'].isnull(), 'type'] = 'ext_bio'


# controls
controls_csv = "{0}/raw_data/merge_gef_controls.csv".format(repo_dir)
controls_df = read_csv(controls_csv)
controls_df['type'] = 'rand'


# concat all data
merged_df = pd.concat([data_df, controls_df])



col_first = ['gef_id', 'project_location_id', 'type', 'id', 'longitude', 'latitude']
col_mid = sorted(list(set(list(treatments_df.columns)) - set(col_first)))
col_last = [i for i in list(data_df.columns) if i not in col_first + col_mid]
merged_df = merged_df[col_first + col_mid + col_last]


# -------------------------------------


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
merged_gdf['iba_year'] = -1

iba_distance = []
iba_statescore = []
iba_area = []
iba_year = []

for i in range(len(merged_gdf)):
    # run distance check
    distance_vals = iba_gdf.geometry.distance(merged_gdf.iloc[i].geometry)
    distance_vals.sort_values(inplace=True)
    # get vals
    ix = distance_vals.index[0]
    distance = distance_vals.iloc[0]
    score = iba_gdf.loc[ix]['StateScore']
    area = iba_gdf.loc[ix]['Area']
    year = iba_gdf.loc[ix]['MonitoringYear']
    # append
    iba_distance.append(distance)
    iba_statescore.append(score)
    iba_area.append(area)
    iba_year.append(year)


merged_gdf['iba_distance'] = iba_distance
merged_gdf['iba_statescore'] = iba_statescore
merged_gdf['iba_area'] = iba_area
merged_gdf['iba_year'] = iba_year


merged_out = pd.DataFrame(merged_gdf)

# output data
out_path = "{0}/data_prep/merged_data.csv".format(repo_dir)
merged_out.to_csv(out_path, index=False, encoding='utf-8')

