
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

