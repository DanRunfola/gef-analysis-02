
import os
import pandas as pd
import numpy as np

repo_dir = os.path.dirname(
    os.path.dirname(os.path.realpath(__file__)))


def read_csv(path):
    '''read csv using pandas
    '''
    return pd.read_csv(path, quotechar='\"',
                       na_values='', keep_default_na=False,
                       encoding='utf-8')


# load main data
data_csv = "{0}/data_prep/merged_data.csv".format(repo_dir)
data_df = read_csv(data_csv)

# initialize treatment field as -1
# for each case:
#   actual treatments will be set to 1
#   actual controls will be set to 0
# then all remaining (-1) can be dropped
data_df['treatment'] = -1

# add gef_id of -1 to random control points
# so we can match on field without nan errors
data_df.loc[data_df['type'] == 'rand', 'gef_id'] = -1
data_df['gef_id'] = data_df['gef_id'].astype('int').astype('str')


# load ancillary data
ancillary_01_csv = "{0}/raw_data/ancillary/CD_MFA_CD_projects_sheet.csv".format(repo_dir)
ancillary_02_csv = "{0}/raw_data/ancillary/CD_MFA_MFA_projects_sheet.csv".format(repo_dir)
ancillary_03_csv = "{0}/raw_data/ancillary/GEF_MFA_AidData_Ancillary.csv".format(repo_dir)
ancillary_04_csv = "{0}/raw_data/ancillary/gef_projects_160726.csv".format(repo_dir)

ancillary_01_df = read_csv(ancillary_01_csv)
ancillary_02_df = read_csv(ancillary_02_csv)
ancillary_03_df = read_csv(ancillary_03_csv)
ancillary_04_df = read_csv(ancillary_04_csv)

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

raw_matches = ancillary_03_df['Sub-Foci'].str.contains('|'.join(land_keywords))
clean_matches = [
    False if np.isnan(x) else x
    for x in raw_matches
]
land_id_list_03 = list(ancillary_03_df.loc[clean_matches, 'GEF_ID']
    .astype('int').astype('str'))


# combine different land id lists
land_id_list = land_id_list_00 + land_id_list_01 + land_id_list_02 + land_id_list_03
land_id_list = list(set(land_id_list))

# -------------------------------------

# check geocoded land degradation
# bio_id_list = list(data_df.loc[data_df['type'] == 'bio', 'gef_id'])


# # check GEF project records (if any column contains "BD")
# cnames_01 = [i for i in list(ancillary_01_df.columns) if i != 'GEF ID']
# matches_01 = ['BD' in list(ancillary_01_df.iloc[i])
#               for i in range(len(ancillary_01_df))]
# land_id_list_01 = list(ancillary_01_df.loc[matches_01, 'GEF ID'].astype('str'))


# cnames_02 = [i for i in list(ancillary_02_df.columns) if i != 'GEF ID']
# matches_02 = ['BD' in list(ancillary_01_df.iloc[i])
#               for i in range(len(ancillary_01_df))]
# land_id_list_02 = list(ancillary_02_df.loc[matches_02, 'GEF ID'].astype('str'))


# # check aiddata ancillary ("Sub-Foci" column)
# bio_keywords = ["BD", "Biodiversity"]


# -----------------------------------------------------------------------------


# (M1)
#   Treatment:  Programmatic w/ LD objectives
#   Control:    Null Case Comparisons

m1_df = data_df.copy(deep=True)

m1_df.loc[(m1_df['type'] == 'prog') & (m1_df['gef_id'].isin(land_id_list)), 'treatment'] = 1
m1_df.loc[(m1_df['type'] == 'rand'), 'treatment'] = 0

m1_df = m1_df.loc[m1_df['treatment'] != -1]

m1_out = "{0}/data_prep/analysis_cases/m1_data.csv".format(repo_dir)
m1_df.to_csv(m1_out, index=False, encoding='utf-8')


# (M2)
#   Treatment:  Programmatic w/ Biodiversity objectives
#   Control:    Null Case Comparisons



# (M3)
#   Treatment:  Programmatic w/ LD objectives
#   Control:    MFA w/ LD objectives

m3_df = data_df.copy(deep=True)

m3_df.loc[(m3_df['type'] == 'prog') & (m3_df['gef_id'].isin(land_id_list)), 'treatment'] = 1
m3_df.loc[(m3_df['type'] == 'mfa') & (m3_df['gef_id'].isin(land_id_list)), 'treatment'] = 0

m3_df = m3_df.loc[m3_df['treatment'] != -1]

m3_out = "{0}/data_prep/analysis_cases/m3_data.csv".format(repo_dir)
m3_df.to_csv(m3_out, index=False, encoding='utf-8')


# (M4)
#   Treatment:  Programmatic w/ Biodiversity objectives
#   Control:    MFA w/ Biodiversity objectives



# (M5)
#   Treatment:  Programmatic multi-country w/ LD objectives
#   Control:    Non-programmatic single-country w/ LD objectives



# (M6)
#   Treatment:  Programmatic multi-country w/ Biodiversity objectives
#   Control:    Non-programmatic single-country w/ Biodiversity objectives



# (M7)
#   Treatment:  Programmatic multi-agency w/ LD objectives
#   Control:    Non-programmatic single-agency w/ LD objectives



# (M8)
#   Treatment:  Programmatic multi-agency w/ Biodiversity objectives
#   Control:    Non-programmatic single-agency w/ Biodiversity objectives



# (M9)
#   Treatment:  Programmatic multi-country w/ LD objectives
#   Control:    Programmatic single-country w/ LD objectives



# (M10)
#   Treatment:  Programmatic multi-country w/ Biodiversity objectives
#   Control:    Programmatic single-country w/ Biodiversity objectives



# (M11)
#   Treatment:  Programmatic multi-agency w/ LD objectives
#   Control:    Programmatic single-agency w/ LD objectives



# (M12)
#   Treatment:  Programmatic multi-agency w/ Biodiversity objectives
#   Control:    Programmatic single-agency w/ Biodiversity objectives



