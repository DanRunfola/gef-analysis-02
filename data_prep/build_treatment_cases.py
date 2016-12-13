
import os
import pandas as pd

repo_dir = os.path.dirname(
    os.path.dirname(os.path.realpath(__file__)))



# (M1) Programmatic w/ LD objectives;  Null Case Comparisons

m1_csv = "{0}/raw_data/programmatic_control.csv".format(repo_dir)
m1_df = pd.read_csv(m1_csv, quotechar='\"',
                    na_values='', keep_default_na=False,
                    encoding='utf-8')

m1_df['treatment'] = 0

m1_out = "{0}/data_prep/analysis_cases/m1_data.csv".format(repo_dir)
m1_df.to_csv(m1_out, index=False, encoding='utf-8')



# (M2) Programmatic w/ Biodiversity objectives; Null Case Comparisons



# (M3) Programmatic w/ LD objectives;  MFA w/ LD objectives



# (M4) Programmatic w/ Biodiversity objectives; MFA w/ Biodiversity objectives



# (M5) Programmatic multi-country w/ LD objectives;  Non-programmatic single-country w/ LD objectives



# (M6) Programmatic multi-country w/ Biodiversity objectives; Non-programmatic single-country w/ Biodiversity objectives



# (M7) Programmatic multi-agency w/ LD objectives;  Non-programmatic single-agency w/ LD objectives



# (M8) Programmatic multi-agency w/ Biodiversity objectives; Non-programmatic single-agency w/ Biodiversity objectives



# (M9) Programmatic multi-country w/ LD objectives;  Programmatic single-country w/ LD objectives



# (M10) Programmatic multi-country w/ Biodiversity objectives; Programmatic single-country w/ Biodiversity objectives



# (M11) Programmatic multi-agency w/ LD objectives;  Programmatic single-agency w/ LD objectives



# (M12) Programmatic multi-agency w/ Biodiversity objectives; Programmatic single-agency w/ Biodiversity objectives



