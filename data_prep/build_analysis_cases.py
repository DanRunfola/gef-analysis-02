
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


def build_case(case_id, treatment, control):
    print "Running {0}".format(str(case_id).upper())
    case_df = data_df.copy(deep=True)
    case_df['treatment'] = -1
    case_df.loc[treatment, 'treatment'] = 1
    case_df.loc[control, 'treatment'] = 0
    case_df = case_df.loc[case_df['treatment'] != -1]
    stats = {}
    stats['treatment_count'] = sum(treatment)
    stats['control_count'] = sum(control)
    stats['total_count'] = len(case_df)
    return case_df, stats


def output_case(case_id, case_out, dry_run=dry_run):
    print "Outputting {0}".format(str(case_id).upper())
    case_out = "{0}/data_prep/analysis_cases/{1}_data.csv".format(repo_dir, case_id)
    if not dry_run:
        case_df.to_csv(case_out, index=False, encoding='utf-8')


# -----------------------------------------------------------------------------


data_path = "{0}/data_prep/analysis_cases/base_data.csv".format(repo_dir)
data_df = read_csv(data_path)


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
# case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
# print case_stats


# =============================================================================
# programmatic


# -----------------------------------------------------------------------------
# Treatment:  Programmatic w/ LD objectives
# Control:    Null Case Comparisons

# -------------------------------------
case_name = "m1a"
case_t = (
    (data_df['type'] == 'prog')
    & (data_df['gef_id'].isin(land_id_list))
)
case_c = (
    (data_df['type'] == 'rand')
)
case_df, case_stats = build_case(case_name, case_t, case_c)

# modify
#

output_case(case_name, case_df, dry_run=dry_run)
print case_stats

# -------------------------------------

case_name = "m1b"
case_t = (
    (data_df['type'] == 'prog')
    & (data_df['gef_id'].isin(land_id_list))
)
case_c = (
    (data_df['type'] == 'rand')
)
case_df, case_stats = build_case(case_name, case_t, case_c)

# modify
#

output_case(case_name, case_df, dry_run=dry_run)
print case_stats


# -----------------------------------------------------------------------------
# Treatment:  Programmatic w/ Biodiversity objectives
# Control:    Null Case Comparisons

# -------------------------------------
case_name = "m2a"
case_t = (
    (data_df['type'] == 'prog')
    & (data_df['gef_id'].isin(bio_id_list))
)
case_c = (
    (data_df['type'] == 'rand')
)
case_df, case_stats = build_case(case_name, case_t, case_c)

# modify
#

output_case(case_name, case_df, dry_run=dry_run)
print case_stats


# -------------------------------------
case_name = "m2b"
case_t = (
    (data_df['type'] == 'prog')
    & (data_df['gef_id'].isin(bio_id_list))
)
case_c = (
    (data_df['type'] == 'rand')
)
case_df, case_stats = build_case(case_name, case_t, case_c)

# modify
#

output_case(case_name, case_df, dry_run=dry_run)
print case_stats


# -------------------------------------
case_name = "m2c"
case_t = (
    (data_df['type'] == 'prog')
    & (data_df['gef_id'].isin(bio_id_list))
)
case_c = (
    (data_df['type'] == 'rand')
)
case_df, case_stats = build_case(case_name, case_t, case_c)

# modify
#

output_case(case_name, case_df, dry_run=dry_run)
print case_stats

# -----------------------------------------------------------------------------
# Treatment:  Programmatic projects w/ LD objectives
# Control:    Non-Programmatic projects w/ LD objectives

# -------------------------------------
case_name = "m3a"
case_t = (
    (data_df['type'] == 'prog')
    & (data_df['gef_id'].isin(land_id_list))
)
case_c = (
    (data_df['type'].isin(['land']))
    & ~(data_df['gef_id'].isin(prog_id_list))
)
case_df, case_stats = build_case(case_name, case_t, case_c)

# modify
#

output_case(case_name, case_df, dry_run=dry_run)
print case_stats

# -------------------------------------
case_name = "m3b"
case_t = (
    (data_df['type'] == 'prog')
    & (data_df['gef_id'].isin(land_id_list))
)
case_c = (
    (data_df['type'].isin(['land']))
    & ~(data_df['gef_id'].isin(prog_id_list))
)
case_df, case_stats = build_case(case_name, case_t, case_c)

# modify
#

output_case(case_name, case_df, dry_run=dry_run)
print case_stats


# -----------------------------------------------------------------------------
# Treatment:  Programmatic projects w/ Bio objectives
# Control:    Non-Programmatic projects w/ Bio objectives

# -------------------------------------
case_name = "m4"
case_t = (
    (data_df['type'] == 'prog')
    & (data_df['gef_id'].isin(bio_id_list))
)
case_c = (
    (data_df['type'].isin(['bio', 'ext_bio']))
    & ~(data_df['gef_id'].isin(prog_id_list))
)
case_df, case_stats = build_case(case_name, case_t, case_c)

# modify
#

output_case(case_name, case_df, dry_run=dry_run)
print case_stats











# -----------------------------------------------------------------------------
# # Treatment:  Programmatic w/ LD objectives
# # Control:    MFA w/ LD objectives

# case_name = "m5"
# case_t = (
#     (data_df['type'] == 'prog')
#     & (data_df['gef_id'].isin(land_id_list))
# )
# case_c = (
#     (data_df['type'] == 'mfa')
#     & (data_df['gef_id'].isin(land_id_list))
#     & ~(data_df['gef_id'].isin(prog_id_list))
# )
# case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
# print case_stats


# -----------------------------------------------------------------------------
# # Treatment:  Programmatic w/ Biodiversity objectives
# # Control:    MFA w/ Biodiversity objectives

# case_name = "m6"
# case_t = (
#     (data_df['type'] == 'prog')
#     & (data_df['gef_id'].isin(bio_id_list))
# )
# case_c = (
#     (data_df['type'] == 'mfa')
#     & (data_df['gef_id'].isin(bio_id_list))
#     & ~(data_df['gef_id'].isin(prog_id_list))
# )
# case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
# print case_stats


# -----------------------------------------------------------------------------
# # Treatment:  Programmatic w/ LD objectives
# # Control:    SFA w/ LD objectives (SFA is non prog and non mfa)

# case_name = "m7"
# case_t = (
#     (data_df['type'] == 'prog')
#     & (data_df['gef_id'].isin(land_id_list))
# )
# case_c = (
#     (data_df['type'].isin(['bio', 'ext_bio', 'land']))
#     & ~(data_df['gef_id'].isin(prog_id_list + mfa_id_list))
#     & (data_df['gef_id'].isin(land_id_list))
# )
# case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
# print case_stats


# -----------------------------------------------------------------------------
# # Treatment:  Programmatic w/ Bio objectives
# # Control:    SFA w/ Bio objectives (SFA is non prog and non mfa)

# case_name = "m8"
# case_t = (
#     (data_df['type'] == 'prog')
#     & (data_df['gef_id'].isin(bio_id_list))
# )
# case_c = (
#     (data_df['type'].isin(['bio', 'ext_bio', 'land']))
#     & ~(data_df['gef_id'].isin(prog_id_list + mfa_id_list))
#     & (data_df['gef_id'].isin(bio_id_list))
# )
# case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
# print case_stats


# -----------------------------------------------------------------------------
# # Treatment:  Programmatic multi-country w/ Biodiversity objectives
# # Control:    Non-programmatic single-country w/ Biodiversity objectives
# #             (aka: Biodiversity single-country)

# case_name = "m9"
# case_t = (
#     (data_df['type'] == 'prog')
#     & (data_df['gef_id'].isin(bio_id_list))
#     & (data_df['gef_id'].isin(multicountry_id_list))
# )
# case_c = (
#     (data_df['type'].isin(['bio', 'ext_bio']))
#     & ~(data_df['gef_id'].isin(prog_id_list))
#     & ~(data_df['gef_id'].isin(multicountry_id_list))
# )
# case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
# print case_stats


# -----------------------------------------------------------------------------
# # Treatment:  Programmatic w/ LD objectives
# # Control:    Null Case Comparisons with random multicountry binary

# case_name = "m10"
# case_t = (
#     (data_df['type'] == 'prog')
#     & (data_df['gef_id'].isin(land_id_list))
# )
# case_c = (
#     (data_df['type'] == 'rand')
# )
# case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
# print case_stats


# -----------------------------------------------------------------------------
# # Treatment:  Programmatic multi-country w/ Biodiversity objectives
# # Control:    Programmatic single-country w/ Biodiversity objectives

# case_name = "m11"
# case_t = (
#     (data_df['type'] == 'prog')
#     & (data_df['gef_id'].isin(bio_id_list))
#     & (data_df['gef_id'].isin(multicountry_id_list))
# )
# case_c = (
#     (data_df['type'] == 'prog')
#     & (data_df['gef_id'].isin(bio_id_list))
#     & ~(data_df['gef_id'].isin(multicountry_id_list))
# )
# case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
# print case_stats


# -----------------------------------------------------------------------------
# # Treatment:  Programmatic multi-country w/ Bio objectives
# # Control:    Stand-alone Bio (MFA + SFA) w/ multi-country designation.


# case_name = "m12"
# case_t = (
#     (data_df['type'] == 'prog')
#     & (data_df['gef_id'].isin(bio_id_list))
#     & (data_df['gef_id'].isin(multicountry_id_list))
# )
# case_c = (
#     (data_df['type'].isin(['bio', 'ext_bio']))
#     & ~(data_df['gef_id'].isin(prog_id_list))
#     & (data_df['gef_id'].isin(multicountry_id_list))
# )
# case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
# print case_stats



# # =============================================================================
# # biodiversity

# -----------------------------------------------------------------------------
# # Treatment:  Biodiversity projects
# # Control:    Null Case Comparisons

# case_name = "bm1"
# case_t = (
#     (data_df['type'].isin(['bio', 'ext_bio']))
# )
# case_c = (
#     (data_df['type'] == 'rand')
# )
# case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
# print case_stats


# -----------------------------------------------------------------------------
# # Treatment:  Biodiversity projects
# # Control:    Land degradation projects

# case_name = "bm2"
# case_t = (
#     (data_df['type'].isin(['bio', 'ext_bio']))
# )
# case_c = (
#     (data_df['type'] == 'land')
#     & ~(data_df['gef_id'].isin(prog_id_list))
# )
# case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
# print case_stats


# -----------------------------------------------------------------------------
# # Treatment:  Biodiversity projects
# # Control:    Null Case Comparisons

# case_name = "bm3"
# case_t = (
#     (data_df['type'].isin(['bio', 'ext_bio']))
# )
# case_c = (
#     (data_df['type'] == 'rand')
# )
# case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
# print case_stats


# # =============================================================================
# # multifocal areas

# -----------------------------------------------------------------------------
# # Treatment:  Land degradation projects
# # Control:    Null Case Comparisons

# case_name = "mm1"
# case_t = (
#     (data_df['type'].isin(['land']))
# )
# case_c = (
#     (data_df['type'] == 'rand')
# )
# case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
# print case_stats


# -----------------------------------------------------------------------------
# # Treatment:  MFA projects
# # Control:    Null Case Comparisons

# case_name = "mm2"
# case_t = (
#     (data_df['type'].isin(['mfa']))
# )
# case_c = (
#     (data_df['type'] == 'rand')
# )
# case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
# print case_stats


# -----------------------------------------------------------------------------
# # Treatment:  MFA projects
# # Control:    Single Focal Bio

# case_name = "mm3"
# case_t = (
#     (data_df['type'].isin(['mfa']))
#     & (data_df['gef_id'].isin(bio_id_list))
# )
# case_c = (
#     (data_df['type'].isin(['bio', 'ext_bio']))
#     & ~(data_df['gef_id'].isin(prog_id_list + mfa_id_list))
# )
# case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
# print case_stats


# -----------------------------------------------------------------------------
# # Treatment:  MFA projects w/ Bio
# # Control:    Null Case Comparisons

# case_name = "mm4"
# case_t = (
#     (data_df['type'].isin(['mfa']))
#     & (data_df['gef_id'].isin(bio_id_list))
# )
# case_c = (
#     (data_df['type'] == 'rand')
# )
# case_stats = build_case(case_name, case_t, case_c, dry_run=dry_run)
# print case_stats

