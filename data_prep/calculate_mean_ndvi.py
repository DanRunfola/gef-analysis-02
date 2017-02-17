# calculate mean ndvi
# average NDVI from 2000 until year before project implementation -
# average after implementation (inc. iimplementation year)

#from pandas import DataFrame as df
import pandas as pd
import numpy

infile = r"/Users/mirandalv/Documents/AidData/github/GEF_Programmatic/data_prep/merged_data.csv"

dta = pd.read_csv(infile, encoding='utf-8', sep=',')

ndvi_year = list(range(2000,2014))

def get_ndvi_mean(row):
    pre_value = 0
    pre_count = 0
    after_value = 0
    after_count = 0
    for year in ndvi_year:
        y = dta['transactions_start_year'][0]
        if y > year:
            ndvinm = "ltdr_yearly_ndvi_mean."+ str(year)+".mean"
            if numpy.isnan(row[ndvinm][0])==False:
                t=row[ndvinm][0]
                pre_count += 1
                pre_value += row[ndvinm]
        else:
            ndvinm = "ltdr_yearly_ndvi_mean." + str(year) + ".mean"
            if numpy.isnan(row[ndvinm][0])==False:
                after_count = after_count + 1
                after_value += row[ndvinm]
    pre_mean_ndvi = pre_value / float(pre_count)
    after_mean_ndvi = after_value / float(after_count)
    ndvi_mean = pre_mean_ndvi - after_mean_ndvi
    return ndvi_mean


dta['ndvi_value'] = get_ndvi_mean(dta)
