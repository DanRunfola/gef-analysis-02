
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

def clean_gef_id(val):
    try:
        return str(int(val))
    except:
        return -999

data_raw_df['gef_id'] = data_raw_df['gef_id'].apply(lambda z: clean_gef_id(z))
data_raw_df = data_raw_df.loc[data_raw_df['gef_id'] != -999]


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
print 'land id count: {0}'.format(len(land_id_list))

# -------------------------------------

# check geocoded land degradation
bio_id_list_00 = list(data_df.loc[data_df['type'].isin(['bio', 'ext_bio']), 'gef_id'])


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
print 'bio id count: {0}'.format(len(bio_id_list))

# -------------------------------------

# multi country
multicountry_id_list = list(set(ancillary_04_df.loc[ancillary_04_df["Country"].isin(["Regional", "Global"]), 'GEF_ID'].astype('int').astype('str')))

# multi agency
multiagency_id_list = list(set(ancillary_04_df.loc[~ancillary_04_df["Secondary agency(ies)"].isnull(), 'GEF_ID'].astype('int').astype('str')))


data_df['multicountry'] = [int(i) for i in data_df['gef_id'].isin(multicountry_id_list)]
data_df['multiagency'] = [int(i) for i in data_df['gef_id'].isin(multiagency_id_list)]

data_df.loc[data_df['type'] == 'rand', 'multicountry'] = np.random.randint(2, size=len(data_df['type'] == 'rand'))
data_df.loc[data_df['type'] == 'rand', 'multiagency'] = np.random.randint(2, size=len(data_df['type'] == 'rand'))


# -------------------------------------


prog_id_list = list(set(data_df.loc[data_df['type'] == "prog", 'gef_id']))

mfa_id_list = list(set(data_df.loc[data_df['type'] == "mfa", 'gef_id']))


# -------------------------------------

data_df_out = "{0}/data_prep/analysis_cases/base_data.csv".format(repo_dir)
data_df.to_csv(data_df_out, index=False, encoding='utf-8')


# -----------------------------------------------------------------------------


def build_case(case_id, treatment, control, dry_run=dry_run):
    print "Running {0}".format(str(case_id).upper())
    case_df = data_df.copy(deep=True)
    case_df['treatment'] = -1
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
# Example case
#
# Treatment:  Definitiion of treatment for `case_t`
# Control:    Definitiion of control for `case_c`

# case_name = "example"
# print "Running Prog {0}".format(case_name.upper())
# case_t = (

# )
# case_c = (

# )
# case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
# print case_stats



# =====================================
# programmatic

# -----------------
# Treatment:  Programmatic w/ LD objectives
# Control:    Null Case Comparisons

case_name = "m1"
case_t = (
    (data_df['type'] == 'prog')
    & (data_df['gef_id'].isin(land_id_list))
)
case_c = (
    (data_df['type'] == 'rand')
)
case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
print case_stats


# -----------------
# Treatment:  Programmatic w/ Biodiversity objectives
# Control:    Null Case Comparisons

case_name = "m2"
case_t = (
    (data_df['type'] == 'prog')
    & (data_df['gef_id'].isin(bio_id_list))
)
case_c = (
    (data_df['type'] == 'rand')
)
case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
print case_stats


# -----------------
# Treatment:  Programmatic projects w/ LD objectives
# Control:    Non-Programmatic projects w/ LD objectives

case_name = "m3"
case_t = (
    (data_df['type'] == 'prog')
    & (data_df['gef_id'].isin(land_id_list))
)
case_c = (
    (data_df['type'].isin(['land']))
    & ~(data_df['gef_id'].isin(prog_id_list))
)
case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
print case_stats


# -----------------
# Treatment:  Programmatic projects w/ Bio objectives
# Control:    Non-Programmatic projects w/ Bio objectives

case_name = "m4"
case_t = (
    (data_df['type'] == 'prog')
    & (data_df['gef_id'].isin(bio_id_list))
)
case_c = (
    (data_df['type'].isin(['bio', 'ext_bio']))
    & ~(data_df['gef_id'].isin(prog_id_list))
)
case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
print case_stats


# -----------------
# Treatment:  Programmatic w/ LD objectives
# Control:    MFA w/ LD objectives

case_name = "m5"
case_t = (
    (data_df['type'] == 'prog')
    & (data_df['gef_id'].isin(land_id_list))
)
case_c = (
    (data_df['type'] == 'mfa')
    & (data_df['gef_id'].isin(land_id_list))
    & ~(data_df['gef_id'].isin(prog_id_list))
)
case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
print case_stats


# -----------------
# Treatment:  Programmatic w/ Biodiversity objectives
# Control:    MFA w/ Biodiversity objectives

case_name = "m6"
case_t = (
    (data_df['type'] == 'prog')
    & (data_df['gef_id'].isin(bio_id_list))
)
case_c = (
    (data_df['type'] == 'mfa')
    & (data_df['gef_id'].isin(bio_id_list))
    & ~(data_df['gef_id'].isin(prog_id_list))
)
case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
print case_stats


# -----------------
# Treatment:  Programmatic w/ LD objectives
# Control:    SFA w/ LD objectives (SFA is non prog and non mfa)

case_name = "m7"
case_t = (
    (data_df['type'] == 'prog')
    & (data_df['gef_id'].isin(land_id_list))
)
case_c = (
    (data_df['type'].isin(['bio', 'ext_bio', 'land']))
    & ~(data_df['gef_id'].isin(prog_id_list + mfa_id_list))
    & (data_df['gef_id'].isin(land_id_list))
)
case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
print case_stats


# -----------------
# Treatment:  Programmatic w/ Bio objectives
# Control:    SFA w/ Bio objectives (SFA is non prog and non mfa)

case_name = "m8"
case_t = (
    (data_df['type'] == 'prog')
    & (data_df['gef_id'].isin(bio_id_list))
)
case_c = (
    (data_df['type'].isin(['bio', 'ext_bio', 'land']))
    & ~(data_df['gef_id'].isin(prog_id_list + mfa_id_list))
    & (data_df['gef_id'].isin(bio_id_list))
)
case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
print case_stats


# -----------------
# Treatment:  Programmatic multi-country w/ Biodiversity objectives
# Control:    Non-programmatic single-country w/ Biodiversity objectives
#             (aka: Biodiversity single-country)

case_name = "m9"
case_t = (
    (data_df['type'] == 'prog')
    & (data_df['gef_id'].isin(bio_id_list))
    & (data_df['gef_id'].isin(multicountry_id_list))
)
case_c = (
    (data_df['type'].isin(['bio', 'ext_bio']))
    & ~(data_df['gef_id'].isin(prog_id_list))
    & ~(data_df['gef_id'].isin(multicountry_id_list))
)
case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
print case_stats


# -----------------
# Treatment:  Programmatic w/ LD objectives
# Control:    Null Case Comparisons with random multicountry binary

case_name = "m10"
case_t = (
    (data_df['type'] == 'prog')
    & (data_df['gef_id'].isin(land_id_list))
)
case_c = (
    (data_df['type'] == 'rand')
)
case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
print case_stats


# -----------------
# Treatment:  Programmatic multi-country w/ Biodiversity objectives
# Control:    Programmatic single-country w/ Biodiversity objectives

case_name = "m11"
case_t = (
    (data_df['type'] == 'prog')
    & (data_df['gef_id'].isin(bio_id_list))
    & (data_df['gef_id'].isin(multicountry_id_list))
)
case_c = (
    (data_df['type'] == 'prog')
    & (data_df['gef_id'].isin(bio_id_list))
    & ~(data_df['gef_id'].isin(multicountry_id_list))
)
case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
print case_stats


# -----------------
# Treatment:  Programmatic multi-country w/ Bio objectives
# Control:    Stand-alone Bio (MFA + SFA) w/ multi-country designation.


case_name = "m12"
case_t = (
    (data_df['type'] == 'prog')
    & (data_df['gef_id'].isin(bio_id_list))
    & (data_df['gef_id'].isin(multicountry_id_list))
)
case_c = (
    (data_df['type'].isin(['bio', 'ext_bio']))
    & ~(data_df['gef_id'].isin(prog_id_list))
    & (data_df['gef_id'].isin(multicountry_id_list))
)
case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
print case_stats



# =====================================
# biodiversity

# -----------------
# Treatment:  Biodiversity projects
# Control:    Null Case Comparisons

case_name = "bm1"
case_t = (
    (data_df['type'].isin(['bio', 'ext_bio']))
)
case_c = (
    (data_df['type'] == 'rand')
)
case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
print case_stats


# -----------------
# Treatment:  Biodiversity projects
# Control:    Land degradation projects

case_name = "bm2"
case_t = (
    (data_df['type'].isin(['bio', 'ext_bio']))
)
case_c = (
    (data_df['type'] == 'land')
    & ~(data_df['gef_id'].isin(prog_id_list))
)
case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
print case_stats


# -----------------
# Treatment:  Biodiversity projects
# Control:    Null Case Comparisons

case_name = "bm3"
case_t = (
    (data_df['type'].isin(['bio', 'ext_bio']))
)
case_c = (
    (data_df['type'] == 'rand')
)
case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
print case_stats


# =====================================
# multifocal areas

# -----------------
# Treatment:  Land degradation projects
# Control:    Null Case Comparisons

case_name = "mm1"
case_t = (
    (data_df['type'].isin(['land']))
)
case_c = (
    (data_df['type'] == 'rand')
)
case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
print case_stats


# -----------------
# Treatment:  MFA projects
# Control:    Null Case Comparisons

case_name = "mm2"
case_t = (
    (data_df['type'].isin(['mfa']))
)
case_c = (
    (data_df['type'] == 'rand')
)
case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
print case_stats


# -----------------
# Treatment:  MFA projects
# Control:    Single Focal Bio

case_name = "mm3"
case_t = (
    (data_df['type'].isin(['mfa']))
    & (data_df['gef_id'].isin(bio_id_list))
)
case_c = (
    (data_df['type'].isin(['bio', 'ext_bio']))
    & ~(data_df['gef_id'].isin(prog_id_list + mfa_id_list))
)
case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
print case_stats


# -----------------
# Treatment:  MFA projects w/ Bio
# Control:    Null Case Comparisons

case_name = "mm4"
case_t = (
    (data_df['type'].isin(['mfa']))
    & (data_df['gef_id'].isin(bio_id_list))
)
case_c = (
    (data_df['type'] == 'rand')
)
case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
print case_stats

