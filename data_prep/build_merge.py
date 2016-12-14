# merge raw data into single file

import os
import pandas as pd

repo_dir = os.path.dirname(
    os.path.dirname(os.path.realpath(__file__)))

# land degradation (treatment)
land_csv = "{0}/raw_data/landdegradation_treatment.csv".format(repo_dir)
land_df = pd.read_csv(land_csv, quotechar='\"',
                    na_values='', keep_default_na=False,
                    encoding='utf-8')
land_df['type'] = 'land'

# multi focal area (treatment)
mfa_csv = "{0}/raw_data/multifocalarea_treatment.csv".format(repo_dir)
mfa_df = pd.read_csv(mfa_csv, quotechar='\"',
                     na_values='', keep_default_na=False,
                     encoding='utf-8')
mfa_df['type'] = 'mfa'

# programmatic (treatment)
prog_csv = "{0}/raw_data/programmatic_treatment.csv".format(repo_dir)
prog_df = pd.read_csv(prog_csv, quotechar='\"',
                      na_values='', keep_default_na=False,
                      encoding='utf-8')
prog_df['type'] = 'prog'

prog_coord_csv = "{0}/raw_data/programmatic_treatments_coords.csv".format(repo_dir)
prog_coord_df = pd.read_csv(prog_coord_csv, quotechar='\"',
                            na_values='', keep_default_na=False,
                            encoding='utf-8')

prog_df = prog_df.merge(prog_coord_df[['id', 'latitude', 'longitude']], on='id')


# programmatic (control)
rand_csv = "{0}/raw_data/programmatic_control.csv".format(repo_dir)
rand_df = pd.read_csv(rand_csv, quotechar='\"',
                      na_values='', keep_default_na=False,
                      encoding='utf-8')
rand_df['type'] = 'rand'

rand_coord_csv = "{0}/raw_data/programmatic_controls_coords.csv".format(repo_dir)
rand_coord_df = pd.read_csv(rand_coord_csv, quotechar='\"',
                            na_values='', keep_default_na=False,
                            encoding='utf-8')

rand_df = rand_df.merge(rand_coord_df[['id', 'latitude', 'longitude']], on='id')


merged_df = pd.concat([land_df, mfa_df, prog_df, rand_df])
merged_df['treatment'] = 0

out_path = "{0}/data_prep/merged_data.csv".format(repo_dir)
merged_df.to_csv(out_path, index=False, encoding='utf-8')

