
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


# -----------------------------------------------------------------------------
# generate id lists for land, bio, prog, mfa, multicountry, multiagency

# load ancillary data
ancillary_01_csv = "{0}/raw_data/ancillary/CD_MFA_CD_projects_sheet.csv".format(repo_dir)
ancillary_02_csv = "{0}/raw_data/ancillary/CD_MFA_MFA_projects_sheet.csv".format(repo_dir)
ancillary_03_csv = "{0}/raw_data/ancillary/GEF_MFA_AidData_Ancillary.csv".format(repo_dir)
ancillary_04_csv = "{0}/raw_data/ancillary/gef_projects_160726.csv".format(repo_dir)
ancillary_05_csv = "{0}/raw_data/ancillary/programmatic_list.csv".format(repo_dir)
ancillary_06_csv = "{0}/raw_data/ancillary/valid_mfa_and_sfa.csv".format(repo_dir)


ancillary_01_df = read_csv(ancillary_01_csv)
ancillary_02_df = read_csv(ancillary_02_csv)
ancillary_03_df = read_csv(ancillary_03_csv)
ancillary_04_df = read_csv(ancillary_04_csv)
ancillary_05_df = read_csv(ancillary_05_csv)
ancillary_06_df = read_csv(ancillary_06_csv)


# -------------------------------------
# build land component list

# # check geocoded land degradation
# land_id_list_00 = list(data_raw_df.loc[data_raw_df['type'] == 'land', 'gef_id'])


# check GEF project records (if any column contains "LD")
cnames_01 = [i for i in list(ancillary_01_df.columns) if i != 'GEF ID']
matches_01 = ['LD' in list(ancillary_01_df.iloc[i])
              for i in range(len(ancillary_01_df))]
land_id_list_01 = list(ancillary_01_df.loc[matches_01, 'GEF ID'].astype('str'))


cnames_02 = [i for i in list(ancillary_02_df.columns) if i != 'GEF ID']
matches_02 = ['LD' in list(ancillary_02_df.iloc[i])
              for i in range(len(ancillary_02_df))]
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
land_partial_id_list = land_id_list_01 + land_id_list_02 + land_id_list_03
land_partial_id_list = list(set(land_partial_id_list))
print 'land partial id count: {0}'.format(len(land_partial_id_list))


# -------------------------------------
# build bio component list

# # check geocoded biodiversity
# bio_id_list_00 = list(data_raw_df.loc[data_raw_df['type'].isin(['bio', 'ext_bio']), 'gef_id'])


# check GEF project records (if any column contains "BD")
cnames_03 = [i for i in list(ancillary_01_df.columns) if i != 'GEF ID']
matches_03 = ['BD' in list(ancillary_01_df.iloc[i])
              for i in range(len(ancillary_01_df))]
bio_id_list_01 = list(ancillary_01_df.loc[matches_01, 'GEF ID'].astype('str'))


cnames_04 = [i for i in list(ancillary_02_df.columns) if i != 'GEF ID']
matches_04 = ['BD' in list(ancillary_02_df.iloc[i])
              for i in range(len(ancillary_02_df))]
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


# combine different bio id lists
bio_partial_id_list = bio_id_list_01 + bio_id_list_02 + bio_id_list_03
bio_partial_id_list = list(set(bio_partial_id_list))
print 'bio partial id count: {0}'.format(len(bio_partial_id_list))


# -------------------------------------
# build project type id lists

# sfa  lists
land_sfa_id_list = list(set(ancillary_06_df['ld'][ancillary_06_df['ld'].notnull()].astype('int').astype('str')))
bio_sfa_id_list = list(set(ancillary_06_df['bio'][ancillary_06_df['bio'].notnull()].astype('int').astype('str')))


# any land/bio lists
land_id_list = list(set(land_sfa_id_list + land_partial_id_list))
bio_id_list = list(set(bio_sfa_id_list + bio_partial_id_list))


# prog and mfa lists
# prog_id_list = list(set(data_raw_df.loc[data_raw_df['type'] == "prog", 'gef_id']))
prog_id_list = list(set(ancillary_05_df['Project GEF_ID'].astype('int').astype('str')))

# mfa_id_list = list(set(data_raw_df.loc[data_raw_df['type'] == "mfa", 'gef_id']))
mfa_id_list = list(set(ancillary_06_df['mfa'][ancillary_06_df['mfa'].notnull()].astype('int').astype('str')))


# print prog_id_list
# print mfa_id_list
# print land_id_list
# print bio_id_list
# print len(prog_id_list)
# print len(mfa_id_list)
# print len(land_id_list)
# print len(bio_id_list)
# raise


# -------------------------------------
# build multi country and multi agency lists

multicountry_id_list = list(set(ancillary_04_df.loc[ancillary_04_df["Country"].isin(["Regional", "Global"]), 'GEF_ID'].astype('int').astype('str')))

multiagency_id_list = list(set(ancillary_04_df.loc[~ancillary_04_df["Secondary agency(ies)"].isnull(), 'GEF_ID'].astype('int').astype('str')))


# -----------------------------------------------------------------------------
# prepare new fields

data_df = data_raw_df.copy(deep=True)


# -------------------------------------
# multiagency and multicountry

# add multicountry and multiagency fields
data_df['multicountry'] = [int(i) for i in data_df['gef_id'].isin(multicountry_id_list)]
data_df['multiagency'] = [int(i) for i in data_df['gef_id'].isin(multiagency_id_list)]

# assign random multicountry and multiagency to controls
data_df.loc[data_df['type'] == 'rand', 'multicountry'] = np.random.randint(2, size=len(data_df['type'] == 'rand'))
data_df.loc[data_df['type'] == 'rand', 'multiagency'] = np.random.randint(2, size=len(data_df['type'] == 'rand'))


# -------------------------------------
# implementation year

# assign random year 2002-2013 to controls
import random
data_df.loc[data_df['type'] == 'rand', 'transactions_start_year'] = (
    data_df.loc[data_df['type'] == 'rand'].apply(
        lambda z: random.randint(2002, 2013), axis=1
    )
)


# attempt to find year for non controls

stage_00 = (
    (data_df['type'] != 'rand')
    & (data_df['transactions_start_year'] == ' ')
)
data_df.loc[stage_00, 'transactions_start_year'] = float('nan')

def date_to_year(d):
    partial = d.split('-')[2]
    if int(partial) > 20:
        y = '19'+ str(partial)
    else:
        y = '20' + str(partial)
    return y


stage_01 = (
    (data_df['type'] != 'rand')
    & (data_df['transactions_start_year'].isnull())
    & (~data_df['Actual date of implementation start'].isnull())
)

data_df.loc[stage_01, 'transactions_start_year'] = data_df.loc[stage_01]['Actual date of implementation start'].apply(lambda z: date_to_year(z))


stage_02 = (
    (data_df['type'] != 'rand')
    & (data_df['transactions_start_year'].isnull())
    & (data_df['Type acronym'].isin(['MSP', 'EA']))
    & (~data_df['Date of CEO approval (MSP / EA)'].isnull())
)

data_df.loc[stage_02, 'transactions_start_year'] = data_df.loc[stage_02]['Date of CEO approval (MSP / EA)'].apply(lambda z: date_to_year(z))


stage_03 = (
   (data_df['type'] != 'rand')
    & (data_df['transactions_start_year'].isnull())
    & (data_df['Type acronym'].isin(['FP']))
    & (~data_df['Date of CEO endorsement (FSP)'].isnull())
)

data_df.loc[stage_03, 'transactions_start_year'] = data_df.loc[stage_03]['Date of CEO endorsement (FSP)'].apply(lambda z: date_to_year(z))


stage_04 = (
    (data_df['type'] != 'rand')
    & (data_df['transactions_start_year'].isnull())
    & (~data_df['Date of project approval'].isnull())
)

data_df.loc[stage_04, 'transactions_start_year'] = data_df.loc[stage_04]['Date of project approval'].apply(lambda z: date_to_year(z))


# add year = 2012 to non control still missing year
stage_05 = (
    (data_df['type'] != 'rand')
    & (data_df['transactions_start_year'].isnull())
)

data_df.loc[stage_05, 'transactions_start_year'] = 2012


# drop location type = PCLI PCLD CONT
data_df = data_df.loc[~data_df['location_type_code'].isin(['PCLI', 'PCLD', 'CONT'])]

# drop start year > 2013
data_df['transactions_start_year'] = data_df['transactions_start_year'].astype('int')
data_df = data_df.loc[data_df['transactions_start_year'] <= 2013]


# -------------------------------------
# years since implementation

current_year = 2013
data_df['years_since_implementation'] = current_year - data_df['transactions_start_year']

# -------------------------------------
# ndvi pre-post difference


def calc_ndvi_period_average(row, period):
    total = 0
    count = 0
    start_year = int(row['transactions_start_year'])

    if period == "pre":
        years = range(start_year, 2014)
    elif period == "post":
        years = range(2000, start_year)
    else:
        raise Exception("Invalid ndvi period (use `pre` or `post`)")

    for year in years:
        cname = "ltdr_yearly_ndvi_mean.{0}.mean".format(year)
        try:
            total += float(row[cname])
            count += 1
        except:
            pass

    if count > 0:
        return total / float(count)
    else:
        return float('nan')


# average ndvi 2000:implementation (not including implmentation)
data_df['ndvi_pre_average'] = data_df.apply(lambda z: calc_ndvi_period_average(z, period="pre"), axis=1)

# average ndvi implementation:2013 (including 2013)
data_df['ndvi_post_average'] = data_df.apply(lambda z: calc_ndvi_period_average(z, period="post"), axis=1)

# difference
data_df['ndvi_pre_post_diff'] = data_df['ndvi_pre_average'] - data_df['ndvi_post_average']


# -------------------------------------
# forest cover change

lossyr25_cols = [i for i in list(data_df.columns)
                 if i.startswith('lossyr25.na.categorical_')
                 and not i.endswith(('_count', '_noloss'))]

data_df['lossyr25_sum'] = data_df[lossyr25_cols].sum(axis=1)

data_df['chg.forest.km.outcome'] = (data_df['lossyr25_sum'] / data_df['lossyr25.na.categorical_count']) *  (np.pi * 10**2)


# -------------------------------------
# iba year filter

data_df['iba_start_diff'] = data_df['iba_year'] - data_df['transactions_start_year']


# -------------------------------------
# GEF phase

data_df['gef_phase_3'] = map(int, data_df["GEF replenishment phase"] == "GEF - 3")
data_df['gef_phase_4'] = map(int, data_df["GEF replenishment phase"] == "GEF - 4")
data_df['gef_phase_5'] = map(int, data_df["GEF replenishment phase"] == "GEF - 5")
data_df['gef_phase_6'] = map(int, data_df["GEF replenishment phase"] == "GEF - 6")
data_df['gef_phase_other'] = map(int, data_df["GEF replenishment phase"].isnull())

# -------------------------------------
# valid projects

# drop projects that are not true prog, mfa, sfa land, sfa bio
total_valid = list(set(prog_id_list + mfa_id_list + land_sfa_id_list + bio_sfa_id_list))

data_df = data_df.loc[
    (data_df['type'].isin(['rand']))
    | (data_df['gef_id'].isin(total_valid))
]



# -----------------------------------------------------------------------------
# output

data_df_out = "{0}/data_prep/analysis_cases/base_data.csv".format(repo_dir)
data_df.to_csv(data_df_out, index=False, encoding='utf-8')


# -----------------------------------------------------------------------------


def build_case(case_id, treatment, control):
    print "Running {0}".format(str(case_id).upper())
    case_df = data_df.copy(deep=True)
    case_df['treatment'] = -1
    case_df.loc[treatment, 'treatment'] = 1
    case_df.loc[control, 'treatment'] = 0
    case_df = case_df.loc[case_df['treatment'] != -1]
    return case_df


def output_case(case_id, case_out, dry_run=dry_run):
    print "Outputting {0}".format(str(case_id).upper())
    case_path = "{0}/data_prep/analysis_cases/{1}_data.csv".format(repo_dir, case_id)
    stats = {}
    stats['treatment_count'] = sum(case_out['treatment'] == 1)
    stats['control_count'] = sum(case_out['treatment'] == 0)
    stats['total_count'] = len(case_out)
    if not dry_run:
        case_out.to_csv(case_path, index=False, encoding='utf-8')
    return stats


# =============================================================================
# =============================================================================
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
# case_df = build_case(case_name, case_t, case_c)

# Modify
#

# case_stats = output_case(case_name, case_df, dry_run=dry_run)
# print case_stats


# =============================================================================
# =============================================================================
# programmatic


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Treatment:  Programmatic w/ LD objectives
# Control:    Null Case Comparisons

# -------------------------------------
case_name = "m1vout"
case_t = (
    (data_df['gef_id'].isin(prog_id_list))
    & (data_df['gef_id'].isin(land_id_list))
)
case_c = (
    (data_df['type'] == 'rand')
)
case_df = build_case(case_name, case_t, case_c)

# drop rows without ndvi diff outcome values
case_df = case_df.loc[~case_df['ndvi_pre_post_diff'].isnull()]
# start year >= 2008
case_df = case_df.loc[(case_df['transactions_start_year'] >= 2008)]

case_stats = output_case(case_name, case_df, dry_run=dry_run)
print case_stats


# -------------------------------------

case_name = "m1fout"
case_t = (
    (data_df['gef_id'].isin(prog_id_list))
    & (data_df['gef_id'].isin(land_id_list))
)
case_c = (
    (data_df['type'] == 'rand')
)
case_df = build_case(case_name, case_t, case_c)

# start year >= 2008
case_df = case_df.loc[(case_df['transactions_start_year'] >= 2008)]

case_stats = output_case(case_name, case_df, dry_run=dry_run)
print case_stats


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Treatment:  Programmatic w/ Biodiversity objectives
# Control:    Null Case Comparisons

# -------------------------------------
case_name = "m2vout"
case_t = (
    (data_df['gef_id'].isin(prog_id_list))
    & (data_df['gef_id'].isin(bio_id_list))
)
case_c = (
    (data_df['type'] == 'rand')
)
case_df = build_case(case_name, case_t, case_c)

# drop rows without ndvi diff outcome values
case_df = case_df.loc[~case_df['ndvi_pre_post_diff'].isnull()]
# start year >= 2008
case_df = case_df.loc[(case_df['transactions_start_year'] >= 2008)]

case_stats = output_case(case_name, case_df, dry_run=dry_run)
print case_stats


# -------------------------------------
case_name = "m2fout"
case_t = (
    (data_df['gef_id'].isin(prog_id_list))
    & (data_df['gef_id'].isin(bio_id_list))
)
case_c = (
    (data_df['type'] == 'rand')
)
case_df = build_case(case_name, case_t, case_c)

# start year >= 2008
case_df = case_df.loc[(case_df['transactions_start_year'] >= 2008)]

case_stats = output_case(case_name, case_df, dry_run=dry_run)
print case_stats


# # -------------------------------------
# case_name = "m2iout"
# case_t = (
#     (data_df['gef_id'].isin(prog_id_list))
#     & (data_df['gef_id'].isin(bio_id_list))
# )
# case_c = (
#     (data_df['type'] == 'rand')
# )
# case_df = build_case(case_name, case_t, case_c)

# # filter any units of observation that have a year of implementation > the last state score measurement
# case_df = case_df.loc[(case_df['transactions_start_year'] > case_df['iba_year'])]
# # start year >= 2008
# case_df = case_df.loc[(case_df['transactions_start_year'] >= 2008)]

# case_stats = output_case(case_name, case_df, dry_run=dry_run)
# print case_stats


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Treatment:  Programmatic projects w/ LD objectives
# Control:    Non-Programmatic projects w/ LD objectives

# -------------------------------------
case_name = "m3vout"
case_t = (
    (data_df['gef_id'].isin(prog_id_list))
    & (data_df['gef_id'].isin(land_id_list))
)
case_c = (
    (data_df['gef_id'].isin(land_id_list))
    & ~(data_df['gef_id'].isin(prog_id_list))
)
case_df = build_case(case_name, case_t, case_c)

# drop rows without ndvi diff outcome values
case_df = case_df.loc[~case_df['ndvi_pre_post_diff'].isnull()]
# start year >= 2008
case_df = case_df.loc[(case_df['transactions_start_year'] >= 2008)]

case_stats = output_case(case_name, case_df, dry_run=dry_run)
print case_stats


# -------------------------------------
case_name = "m3fout"
case_t = (
    (data_df['gef_id'].isin(prog_id_list))
    & (data_df['gef_id'].isin(land_id_list))
)
case_c = (
    (data_df['gef_id'].isin(land_id_list))
    & ~(data_df['gef_id'].isin(prog_id_list))
)
case_df = build_case(case_name, case_t, case_c)

# start year >= 2008
case_df = case_df.loc[(case_df['transactions_start_year'] >= 2008)]

case_stats = output_case(case_name, case_df, dry_run=dry_run)
print case_stats


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Treatment:  Programmatic projects w/ Bio objectives
# Control:    Non-Programmatic projects w/ Bio objectives


# -------------------------------------
case_name = "m4vout"
case_t = (
    (data_df['gef_id'].isin(prog_id_list))
    & (data_df['gef_id'].isin(bio_id_list))
)
case_c = (
    (data_df['gef_id'].isin(bio_id_list))
    & ~(data_df['gef_id'].isin(prog_id_list))
)
case_df = build_case(case_name, case_t, case_c)

# drop rows without ndvi diff outcome values
case_df = case_df.loc[~case_df['ndvi_pre_post_diff'].isnull()]
# start year >= 2008
case_df = case_df.loc[(case_df['transactions_start_year'] >= 2008)]
# filter any units of observation that have a year of implementation > the last state score measurement
# case_df = case_df.loc[(data_df['iba_start_diff'] > 0)]
# iba dist less than 2 decimal degrees or ~200km
# case_df = case_df.loc[(case_df['iba_distance'] < 2)]

case_stats = output_case(case_name, case_df, dry_run=dry_run)
print case_stats


# -------------------------------------
case_name = "m4fout"
case_t = (
    (data_df['gef_id'].isin(prog_id_list))
    & (data_df['gef_id'].isin(bio_id_list))
)
case_c = (
    (data_df['gef_id'].isin(bio_id_list))
    & ~(data_df['gef_id'].isin(prog_id_list))
)
case_df = build_case(case_name, case_t, case_c)

# start year >= 2008
case_df = case_df.loc[(case_df['transactions_start_year'] >= 2008)]

case_stats = output_case(case_name, case_df, dry_run=dry_run)
print case_stats


# # -------------------------------------
# case_name = "m4iout"
# case_t = (
#    (data_df['gef_id'].isin(prog_id_list))
#     & (data_df['gef_id'].isin(bio_id_list))
# )
# case_c = (
#    (data_df['gef_id'].isin(bio_id_list))
#     & ~(data_df['gef_id'].isin(prog_id_list))
# )
# case_df = build_case(case_name, case_t, case_c)

# # start year >= 2008
# case_df = case_df.loc[(case_df['transactions_start_year'] >= 2008)]
# # filter any units of observation that have a year of implementation > the last state score measurement
# # case_df = case_df.loc[(data_df['iba_start_diff'] > 0)]
# # iba dist less than 2 decimal degrees or ~200km
# # case_df = case_df.loc[(case_df['iba_distance'] < 2)]

# case_stats = output_case(case_name, case_df, dry_run=dry_run)
# print case_stats



