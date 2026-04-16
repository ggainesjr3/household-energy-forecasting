import pandas as pd
import numpy as np

def load_and_clean_data(filepath):
    # 1. Load data: We tell pandas about the semicolons and the '?' marks
    df = pd.read_csv(filepath, sep=';', 
                     parse_dates={'dt' : ['Date', 'Time']}, 
                     infer_datetime_format=True, 
                     low_memory=False, 
                     na_values=['?'], 
                     index_index='dt')

    # 2. Handling Nulls: Since this is time-series, we use 'Forward Fill'
    # This assumes the power usage right now is likely similar to 1 minute ago.
    df.ffill(inplace=True)
    
    # 3. Convert all columns to float (they often load as objects/strings)
    return df.astype(float)

# Usage
# df = load_and_clean_data('data/household_power_consumption.txt')
# print(df.head())