
import sys
import os
import pandas as pd
import numpy as np

dry_run = False
if len(sys.argv) == 2:
    if sys.argv[1] in [1, "1", "True", "true", "T", "t", "yes", "Y", "Yes"]:
        dry_run = True
        print "Running dry run..."


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


# load main data
data_csv = "{0}/data_prep/merged_data.csv".format(repo_dir)
data_raw_df = read_csv(data_csv)

# initialize treatment field as -1
# for each case:
#   actual treatments will be set to 1
#   actual controls will be set to 0
# then all remaining (-1) can be dropped
data_raw_df['treatment'] = -1

# add gef_id of -1 to random control points
# so we can match on field without nan errors
data_raw_df.loc[data_raw_df['type'] == 'rand', 'gef_id'] = -1
data_raw_df['gef_id'] = data_raw_df['gef_id'].astype('int').astype('str')


# load ancillary data
ancillary_01_csv = "{0}/raw_data/ancillary/CD_MFA_CD_projects_sheet.csv".format(repo_dir)
ancillary_02_csv = "{0}/raw_data/ancillary/CD_MFA_MFA_projects_sheet.csv".format(repo_dir)
ancillary_03_csv = "{0}/raw_data/ancillary/GEF_MFA_AidData_Ancillary.csv".format(repo_dir)
ancillary_04_csv = "{0}/raw_data/ancillary/gef_projects_160726.csv".format(repo_dir)

ancillary_01_df = read_csv(ancillary_01_csv)
ancillary_02_df = read_csv(ancillary_02_csv)
ancillary_03_df = read_csv(ancillary_03_csv)
ancillary_04_df = read_csv(ancillary_04_csv)


# merge project data from ancillary_04 with main data

ancillary_04_df['GEF_ID'] = ancillary_04_df['GEF_ID'].astype('int').astype('str')

data_df = data_raw_df.copy(deep=True)
data_df = data_df.merge(ancillary_04_df,
                        left_on='gef_id', right_on='GEF_ID',
                        how='left')

# -------------------------------------

land_id_list_00 = list(data_df.loc[data_df['type'] == 'land', 'gef_id'])


# check GEF project records (if any column contains "LD")
cnames_01 = [i for i in list(ancillary_01_df.columns) if i != 'GEF ID']
matches_01 = ['LD' in list(ancillary_01_df.iloc[i])
              for i in range(len(ancillary_01_df))]
land_id_list_01 = list(ancillary_01_df.loc[matches_01, 'GEF ID'].astype('str'))


cnames_02 = [i for i in list(ancillary_02_df.columns) if i != 'GEF ID']
matches_02 = ['LD' in list(ancillary_01_df.iloc[i])
              for i in range(len(ancillary_01_df))]
land_id_list_02 = list(ancillary_02_df.loc[matches_02, 'GEF ID'].astype('str'))


# check aiddata ancillary ("Sub-Foci" column)
land_keywords = ["LD", "Sustainable", "SFM", "REDD", "LULUCF",
                 "Land", "Degradation", "Degredation", "Sustainable"]

raw_land_matches = ancillary_03_df['Sub-Foci'].str.contains('|'.join(land_keywords))
clean_land_matches = [
    False if np.isnan(x) else x
    for x in raw_land_matches
]
land_id_list_03 = list(ancillary_03_df.loc[clean_land_matches, 'GEF_ID']
    .astype('int').astype('str'))


# combine different land id lists
land_id_list = land_id_list_00 + land_id_list_01 + land_id_list_02 + land_id_list_03
land_id_list = list(set(land_id_list))

# -------------------------------------

# check geocoded land degradation
bio_id_list_00 = list(data_df.loc[data_df['type'] == 'bio', 'gef_id'])


# check GEF project records (if any column contains "BD")
cnames_03 = [i for i in list(ancillary_01_df.columns) if i != 'GEF ID']
matches_03 = ['BD' in list(ancillary_01_df.iloc[i])
              for i in range(len(ancillary_01_df))]
bio_id_list_01 = list(ancillary_01_df.loc[matches_01, 'GEF ID'].astype('str'))


cnames_04 = [i for i in list(ancillary_02_df.columns) if i != 'GEF ID']
matches_04 = ['BD' in list(ancillary_01_df.iloc[i])
              for i in range(len(ancillary_01_df))]
bio_id_list_02 = list(ancillary_02_df.loc[matches_02, 'GEF ID'].astype('str'))


# check aiddata ancillary ("Sub-Foci" column)
bio_keywords = ["BD", "Biodiversity"]

raw_bio_matches = ancillary_03_df['Sub-Foci'].str.contains('|'.join(bio_keywords))
clean_bio_matches = [
    False if np.isnan(x) else x
    for x in raw_bio_matches
]
bio_id_list_03 = list(ancillary_03_df.loc[clean_bio_matches, 'GEF_ID']
    .astype('int').astype('str'))


# combine different land id lists
bio_id_list = bio_id_list_00 + bio_id_list_01 + bio_id_list_02 + bio_id_list_03
bio_id_list = list(set(bio_id_list))

# -------------------------------------

# multi country
multicountry_id_list = list(set(ancillary_04_df.loc[ancillary_04_df["Country"].isin(["Regional", "Global"]), 'GEF_ID'].astype('int').astype('str')))

# multi agency
multiagency_id_list = list(set(ancillary_04_df.loc[~ancillary_04_df["Secondary agency(ies)"].isnull(), 'GEF_ID'].astype('int').astype('str')))


data_df['multicountry'] = [int(i) for i in data_df['gef_id'].isin(multicountry_id_list)]
data_df['multiagency'] = [int(i) for i in data_df['gef_id'].isin(multiagency_id_list)]

# -------------------------------------

data_df_out = "{0}/data_prep/analysis_cases/base_data.csv".format(repo_dir)
data_df.to_csv(data_df_out, index=False, encoding='utf-8')


# -----------------------------------------------------------------------------


def build_case(case_id, treatment, control, dry_run=False):
    case_df = data_df.copy(deep=True)

    case_df.loc[treatment, 'treatment'] = 1
    case_df.loc[control, 'treatment'] = 0

    case_df = case_df.loc[case_df['treatment'] != -1]

    case_out = "{0}/data_prep/analysis_cases/{1}_data.csv".format(repo_dir, case_id)
    if not dry_run:
        case_df.to_csv(case_out, index=False, encoding='utf-8')

    stats = {}
    stats['treatment_count'] = sum(treatment)
    stats['control_count'] = sum(control)
    stats['total_count'] = len(case_df)

    return stats


# -----------------
# (M1)
#   Treatment:  Programmatic w/ LD objectives
#   Control:    Null Case Comparisons

print "Running M1"
m1t = (data_df['type'] == 'prog') & (data_df['gef_id'].isin(land_id_list))
m1c = (data_df['type'] == 'rand')
m1_stats = build_case('m1', m1t, m1c, dry_run=dry_run)
print m1_stats


# -----------------
# (M2)
#   Treatment:  Programmatic w/ Biodiversity objectives
#   Control:    Null Case Comparisons

print "Running M2"
m2t = (data_df['type'] == 'prog') & (data_df['gef_id'].isin(bio_id_list))
m2c = (data_df['type'] == 'rand')
m2_stats = build_case('m2', m2t, m2c, dry_run=dry_run)
print m2_stats


# -----------------
# (M3)
#   Treatment:  Programmatic w/ LD objectives
#   Control:    MFA w/ LD objectives

print "Running M3"
m3t = (data_df['type'] == 'prog') & (data_df['gef_id'].isin(land_id_list))
m3c = (data_df['type'] == 'mfa') & (data_df['gef_id'].isin(land_id_list))
m3_stats = build_case('m3', m3t, m3c, dry_run=dry_run)
print m3_stats


# -----------------
# (M4)
#   Treatment:  Programmatic w/ Biodiversity objectives
#   Control:    MFA w/ Biodiversity objectives

print "Running M4"
m4t = (data_df['type'] == 'prog') & (data_df['gef_id'].isin(bio_id_list))
m4c = (data_df['type'] == 'mfa') & (data_df['gef_id'].isin(bio_id_list))
m4_stats = build_case('m4', m4t, m4c, dry_run=dry_run)
print m4_stats


# -----------------
# (M5)
#   Treatment:  Programmatic multi-country w/ LD objectives
#   Control:    Non-programmatic single-country w/ LD objectives
#               (aka: LD single-country)

print "Running M5"
m5t = ((data_df['type'] == 'prog')
       & (data_df['gef_id'].isin(land_id_list))
       & (data_df['gef_id'].isin(multicountry_id_list)))
m5c = ((data_df['type'] == 'land')
       & ~(data_df['gef_id'].isin(list(set(data_df.loc[data_df['type'] == "prog", 'gef_id']))))
       & ~(data_df['gef_id'].isin(multicountry_id_list)))
m5_stats = build_case('m5', m5t, m5c, dry_run=dry_run)
print m5_stats


# -----------------
# (M6)
#   Treatment:  Programmatic multi-country w/ Biodiversity objectives
#   Control:    Non-programmatic single-country w/ Biodiversity objectives
#               (aka: Biodiversity single-country)

print "Running M6"
m6t = ((data_df['type'] == 'prog')
       & (data_df['gef_id'].isin(bio_id_list))
       & (data_df['gef_id'].isin(multicountry_id_list)))
m6c = ((data_df['type'] == 'bio')
       & ~(data_df['gef_id'].isin(list(set(data_df.loc[data_df['type'] == "prog", 'gef_id']))))
       & ~(data_df['gef_id'].isin(multicountry_id_list)))
m6_stats = build_case('m6', m6t, m6c, dry_run=dry_run)
print m6_stats


# -----------------
# (M7)
#   Treatment:  Programmatic multi-agency w/ LD objectives
#   Control:    Non-programmatic single-agency w/ LD objectives
#               (aka: LD single-agency)

print "Running M7"
m7t = ((data_df['type'] == 'prog')
       & (data_df['gef_id'].isin(land_id_list))
       & (data_df['gef_id'].isin(multiagency_id_list)))
m7c = ((data_df['type'] == 'land')
       & ~(data_df['gef_id'].isin(list(set(data_df.loc[data_df['type'] == "prog", 'gef_id']))))
       & ~(data_df['gef_id'].isin(multiagency_id_list)))
m7_stats = build_case('m7', m7t, m7c, dry_run=dry_run)
print m7_stats


# -----------------
# (M8)
#   Treatment:  Programmatic multi-agency w/ Biodiversity objectives
#   Control:    Non-programmatic single-agency w/ Biodiversity objectives
#               (aka: Biodiversity single-agency)

print "Running M8"
m8t = ((data_df['type'] == 'prog')
       & (data_df['gef_id'].isin(bio_id_list))
       & (data_df['gef_id'].isin(multiagency_id_list)))
m8c = ((data_df['type'] == 'bio')
       & ~(data_df['gef_id'].isin(list(set(data_df.loc[data_df['type'] == "prog", 'gef_id']))))
       & ~(data_df['gef_id'].isin(multiagency_id_list)))
m8_stats = build_case('m8', m8t, m8c, dry_run=dry_run)
print m8_stats


# -----------------
# (M9)
#   Treatment:  Programmatic multi-country w/ LD objectives
#   Control:    Programmatic single-country w/ LD objectives

print "Running M9"
m9t = ((data_df['type'] == 'prog')
       & (data_df['gef_id'].isin(land_id_list))
       & (data_df['gef_id'].isin(multicountry_id_list)))
m9c = ((data_df['type'] == 'prog')
       & (data_df['gef_id'].isin(land_id_list))
       & ~(data_df['gef_id'].isin(multicountry_id_list)))
m9_stats = build_case('m9', m9t, m9c, dry_run=dry_run)
print m9_stats


# -----------------
# (M10)
#   Treatment:  Programmatic multi-country w/ Biodiversity objectives
#   Control:    Programmatic single-country w/ Biodiversity objectives

print "Running M10"
m10t = ((data_df['type'] == 'prog')
        & (data_df['gef_id'].isin(bio_id_list))
        & (data_df['gef_id'].isin(multicountry_id_list)))
m10c = ((data_df['type'] == 'prog')
        & (data_df['gef_id'].isin(bio_id_list))
        & ~(data_df['gef_id'].isin(multicountry_id_list)))
m10_stats = build_case('m10', m10t, m10c, dry_run=dry_run)
print m10_stats


# -----------------
# (M11)
#   Treatment:  Programmatic multi-agency w/ LD objectives
#   Control:    Programmatic single-agency w/ LD objectives

print "Running M11"
m11t = ((data_df['type'] == 'prog')
        & (data_df['gef_id'].isin(land_id_list))
        & (data_df['gef_id'].isin(multiagency_id_list)))
m11c = ((data_df['type'] == 'prog')
        & (data_df['gef_id'].isin(land_id_list))
        & ~(data_df['gef_id'].isin(multiagency_id_list)))
m11_stats = build_case('m11', m11t, m11c, dry_run=dry_run)
print m11_stats


# -----------------
# (M12)
#   Treatment:  Programmatic multi-agency w/ Biodiversity objectives
#   Control:    Programmatic single-agency w/ Biodiversity objectives

print "Running M12"
m12t = ((data_df['type'] == 'prog')
        & (data_df['gef_id'].isin(bio_id_list))
        & (data_df['gef_id'].isin(multiagency_id_list)))
m12c = ((data_df['type'] == 'prog')
        & (data_df['gef_id'].isin(bio_id_list))
        & ~(data_df['gef_id'].isin(multiagency_id_list)))
m12_stats = build_case('m12', m12t, m12c, dry_run=dry_run)
print m12_stats

