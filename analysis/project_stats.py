
import sys
import os
import json
import pandas as pd
import numpy as np
from collections import OrderedDict

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
data_csv = "{0}/data_prep/analysis_cases/base_data.csv".format(repo_dir)
data_df = read_csv(data_csv)
data_df = data_df.loc[data_df['type'] != 'rand']



def build_case(case_id, dry_run=dry_run):
    print "Running {0}".format(str(case_id).upper())
    case_df = data_df.copy(deep=True)

    case_id_list = [case_id]
    if case_id == 'bio':
        case_id_list.append('ext_bio')

    case_df = case_df.loc[data_df['type'].isin(case_id_list)]

    case_df = case_df[['gef_id', 'iba_area']]

    case_result_df = case_df.groupby("gef_id")['iba_area'].agg({"location_count": 'size'}).join(case_df.groupby('gef_id')['iba_area'].sum())

    case_result_df['gef_id'] = case_result_df.index
    case_result_df = case_result_df[['gef_id', 'location_count', 'iba_area']]

    case_out = "{0}/results/{1}_project_stats.csv".format(repo_dir, case_id)
    if not dry_run:
        case_result_df.to_csv(case_out, index=False, encoding='utf-8')


    stats = OrderedDict()

    stats['location_count_min'] = case_result_df['location_count'].min()
    stats['location_count_max'] = case_result_df['location_count'].max()
    stats['location_count_mean'] = case_result_df['location_count'].mean()
    stats['location_count_median'] = case_result_df['location_count'].median()

    stats['iba_area_min'] = case_result_df['iba_area'].min()
    stats['iba_area_max'] = case_result_df['iba_area'].max()
    stats['iba_area_mean'] = case_result_df['iba_area'].mean()
    stats['iba_area_median'] = case_result_df['iba_area'].median()

    return stats


# -------------------------------------


# case_name = "prog"
# case_stats = build_case(case_name, dry_run=dry_run)
# print json.dumps(case_stats, indent=4)


case_name = "mfa"
case_stats = build_case(case_name, dry_run=dry_run)
print json.dumps(case_stats, indent=4)


case_name = "land"
case_stats = build_case(case_name, dry_run=dry_run)
print json.dumps(case_stats, indent=4)


case_name = "bio"
case_stats = build_case(case_name, dry_run=dry_run)
print json.dumps(case_stats, indent=4)


# case_name = "ext_bio"
# case_stats = build_case(case_name, dry_run=dry_run)
# print json.dumps(case_stats, indent=4)

