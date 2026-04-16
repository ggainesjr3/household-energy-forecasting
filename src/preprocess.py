import pandas as pd
import numpy as np

def load_and_clean_data(filepath):
    """
    Step 1: The 'Opening Shift'
    Loads the data and fixes the European date format (DD/MM/YYYY).
    """
    print(f"--- Loading: {filepath} ---")
    
    # dayfirst=True is the 'fix' for the UCI dataset's European date format
    df = pd.read_csv(
        filepath, 
        sep=';', 
        parse_dates={'dt': ['Date', 'Time']}, 
        dayfirst=True, 
        low_memory=False, 
        na_values=['?'], 
        index_col='dt'
    )

    # Use Forward Fill to maintain continuity (the 'Slope' of usage)
    df.ffill(inplace=True)
    
    # float32 saves memory on your Linux machine
    return df.astype('float32')

def engineer_features(df):
    """
    Step 2: The 'Context'
    Resamples data to hourly and creates the 'Past' features.
    """
    print("--- Resampling and Engineering features ---")
    
    # Resample to Hourly chunks (Integrating the minutes)
    df = df.resample('H').mean()
    
    # Lag Features: Looking back 1 hour and 24 hours
    df['lag_1h'] = df['Global_active_power'].shift(1)
    df['lag_24h'] = df['Global_active_power'].shift(24)
    
    # Rolling Window: The average momentum of the last 6 hours
    df['rolling_6h_mean'] = df['Global_active_power'].rolling(window=6).mean()
    
    # Cyclical Encoding: Mapping hours to a circle (The 'Trig' trick)
    hour = df.index.hour
    df['hour_sin'] = np.sin(2 * np.pi * hour / 24)
    df['hour_cos'] = np.cos(2 * np.pi * hour / 24)
    
    # Drop rows that don't have enough history to fill the lags
    df.dropna(inplace=True)
    return df

def train_test_split_time_series(df, target='Global_active_power'):
    """
    Step 3: The 'Clean Cut'
    Splits data chronologically (No 'Time Travel' allowed).
    """
    split_point = int(len(df) * 0.8) # 80% for training
    
    train = df.iloc[:split_point]
    test = df.iloc[split_point:]
    
    X_train, y_train = train.drop(columns=[target]), train[target]
    X_test, y_test = test.drop(columns=[target]), test[target]
    
    return X_train, X_test, y_train, y_test