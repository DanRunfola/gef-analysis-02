


import os
import pandas as pd


def read_csv(path):
    '''read csv using pandas
    '''
    path = os.path.expanduser(path)
    return pd.read_csv(path, quotechar='\"',
                       na_values='', keep_default_na=False,
                       encoding='utf-8')


def clean_id(z):
    try:
        return str(int(z))
    except:
        return str(z)

# -------------------------------------
# complete level 1
projects = read_csv('~/git/GEF_Programmatic/gef_ids/GlobalEnvironmentFacility_GeocodedResearchRelease_Level1_v1.0/data/projects.csv')
locations = read_csv('~/git/GEF_Programmatic/gef_ids/GlobalEnvironmentFacility_GeocodedResearchRelease_Level1_v1.0/data/locations.csv')
ancillary = read_csv('~/git/GEF_Programmatic/gef_ids/GlobalEnvironmentFacility_GeocodedResearchRelease_Level1_v1.0/data/projects_ancillary.csv')
ancillary['gef_id'] = ancillary['gef_id'].apply(lambda z: clean_id(z))

all_ids = list(set(ancillary['gef_id']))
prog_ids = list(set(ancillary.loc[ancillary['round'].isin(['Programmatic'])]['gef_id']))


# -------------------------------------
# # extracts
# active = read_csv('~/git/GEF_Programmatic/gef_ids/merged_data.csv')
# active = active.loc[~active['type'].isin(['rand'])]
# active['gef_id'] = active['gef_id'].apply(lambda z: clean_id(z))

# prog = list(set(active.loc[active['type'].isin(['prog'])]['gef_id']))
# mfa = list(set(active.loc[active['type'].isin(['mfa'])]['gef_id']))
# land = list(set(active.loc[active['type'].isin(['land'])]['gef_id']))
# bio = list(set(active.loc[active['type'].isin(['bio', 'ext_bio'])]['gef_id']))


# # LD level 1
# LD = read_csv('~/git/GEF_Programmatic/gef_ids/LD_projects_ancillary.csv')
# LD['gef_id'] = LD['gef_id'].apply(lambda z: clean_id(z))
# land_alt = list(set(LD['gef_id']))


# -------------------------------------
# gef spreadsheets

# this is csv combining MFA+LD SFA sheet and BD SFA sheet
gef_valid = read_csv('~/git/GEF_Programmatic/gef_ids/valid_mfa_and_sfa.csv')

mfa_valid = list(set(gef_valid['mfa'][gef_valid['mfa'].notnull()].astype('int').astype('str')))
ld_valid = list(set(gef_valid['ld'][gef_valid['ld'].notnull()].astype('int').astype('str')))
# combo_valid = list(set(gef_valid['combo'][gef_valid['combo'].notnull()].astype('int').astype('str')))
bio_valid = list(set(gef_valid['bio'][gef_valid['bio'].notnull()].astype('int').astype('str')))

total_valid = mfa_valid + ld_valid + bio_valid

# initial full missing sheet
not_geocoded_plus_missing = read_csv('~/git/GEF_Programmatic/gef_ids/not_geocoded_plus_missing.csv')
not_geocoded_plus_missing['gef_id'] = not_geocoded_plus_missing['GEF ID'].apply(lambda z: clean_id(z))
not_geocoded_plus_missing_list =  list(set(not_geocoded_plus_missing['gef_id']))

# missing sheet after projects that were not geocoded were removed
missing = read_csv('~/git/GEF_Programmatic/gef_ids/missing.csv')
missing['gef_id'] = missing['GEF ID'].apply(lambda z: clean_id(z))
missing_list =  list(set(missing['gef_id']))

not_geocoded_list = [i for i in not_geocoded_plus_missing_list if i not in missing_list]


# -------------------------------------
# checks

keep = list(set(total_valid) - set(not_geocoded_list)) + prog_ids

# cur = prog + mfa + bio + land + land_alt
cur = all_ids

out = [i for i in list(cur) if i in keep]


ancillary['is_valid'] = ancillary['gef_id'].isin(out).astype(int)

ancillary.to_csv(
    '~/git/GEF_Programmatic/gef_ids/checked_projects_ancillary.csv',
    index=False, encoding='utf-8')


projects_merge = ancillary.merge(projects[['project_id', 'project_title']], left_on="AidData Project ID", right_on="project_id")
projects_merge = projects_merge.loc[projects_merge['is_valid'] == 1]
projects_merge.to_csv(
    '~/git/GEF_Programmatic/gef_ids/final_projects_merge.csv',
    index=False, encoding='utf-8')


locations_merge = projects_merge.merge(locations, on="project_id")

# -------------------------------------


print "Programmatic Projects: {0}".format(
    len(projects_merge.loc[projects_merge['round'] == 'Programmatic']))

print "MFA Projects: {0}".format(
    len(projects_merge.loc[projects_merge['round'] == 'MFA']))

print "Biodiversity Projects: {0}".format(
    len(projects_merge.loc[projects_merge['round'] == 'Biodiversity']))

print "Land Degradation Projects: {0}".format(
    len(projects_merge.loc[projects_merge['round'] == 'Land Degradation']))




print "Programmatic Locations: {0}".format(
    len(locations_merge.loc[locations_merge['round'] == 'Programmatic']))

print "MFA Locations: {0}".format(
    len(locations_merge.loc[locations_merge['round'] == 'MFA']))

print "Biodiversity Locations: {0}".format(
    len(locations_merge.loc[locations_merge['round'] == 'Biodiversity']))

print "Land Degradation Locations: {0}".format(
    len(locations_merge.loc[locations_merge['round'] == 'Land Degradation']))



# Programmatic Projects: 47
# MFA Projects: 84
# Biodiversity Projects: 185
# Land Degradation Projects: 154


# Programmatic Locations: 400
# MFA Locations: 586
# Biodiversity Locations: 1067
# Land Degradation Locations: 1538
