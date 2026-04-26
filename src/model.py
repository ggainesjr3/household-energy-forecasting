import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

def create_features(df):
    df = df.copy()
    
    # 1. Circular Time Encoding (The "Clock" Fix)
    df['hour_sin'] = np.sin(2 * np.pi * df.index.hour / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df.index.hour / 24)
    
    # 2. Weekend Logic
    df['is_weekend'] = df.index.dayofweek.isin([5, 6]).astype(int)
    
    # 3. Enhanced Lags (Short and Long Term)
    df['target'] = df['Global_active_power']
    df['lag_1h'] = df['target'].shift(1)
    df['lag_2h'] = df['target'].shift(2)
    df['lag_24h'] = df['target'].shift(24)
    
    # 4. Rolling Volatility (The "Bouncer" Logic - watching for trouble)
    df['rolling_std_3h'] = df['target'].rolling(window=3).std()
    
    return df.dropna()

if __name__ == "__main__":
    PATH = 'data/household_power_consumption.txt'
    try:
        # Load and resample
        df_raw = pd.read_csv(PATH, sep=';', parse_dates={'dt': ['Date', 'Time']}, 
                             na_values=['?'], index_col='dt', low_memory=False)
        df_raw = df_raw.ffill().fillna(df_raw.median())
        hourly = df_raw.resample('H').mean()
        
        df = create_features(hourly)

        # Chronological Split
        split_idx = int(len(df) * 0.8)
        train, test = df.iloc[:split_idx], df.iloc[split_idx:]

        cols = ['hour_sin', 'hour_cos', 'is_weekend', 'lag_1h', 'lag_2h', 'lag_24h', 'rolling_std_3h']
        
        # XGBoost with refined parameters
        model = XGBRegressor(
            n_estimators=500,
            learning_rate=0.03,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            n_jobs=-1
        )
        
        print("🚀 Training Refined Energy Engine...")
        model.fit(train[cols], train['target'])

        preds = model.predict(test[cols])
        mae = mean_absolute_error(test['target'], preds)
        rmse = np.sqrt(mean_squared_error(test['target'], preds))

        print(f"\n✅ REFINED PERFORMANCE:")
        print(f"MAE: {mae:.4f} kW | RMSE: {rmse:.4f} kW")

    except Exception as e:
        print(f"❌ Error: {e}")
