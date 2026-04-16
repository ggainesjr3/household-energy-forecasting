import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import firebase_admin
from firebase_admin import credentials, firestore

# 1. FIREBASE INITIALIZATION
if not firebase_admin._apps:
    cred = credentials.Certificate('/home/gary/household-energy-forecasting/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

# 2. LOAD DATA
data_path = '/home/gary/household-energy-forecasting/data/household_power_consumption.txt'
data = pd.read_csv(data_path, sep=';', low_memory=False, na_values=['?'])
data = data.rename(columns={'Global_active_power': 'actual'})
data['actual'] = pd.to_numeric(data['actual'])
data = data.dropna(subset=['actual'])
data = data.tail(10000).reset_index(drop=True)

# 3. FEATURE ENGINEERING (Baseline & Rolling)
data['baseline_pred'] = data['actual'].shift(24)
data['rolling_mean_3h'] = data['actual'].rolling(window=3).mean()
data['rolling_std_3h'] = data['actual'].rolling(window=3).std()

# 4. PREPROCESSING
data = data.dropna().reset_index(drop=True)

# Generate Time Features
data['hour'] = pd.to_datetime(data['Time']).dt.hour
data['day_of_week'] = pd.to_datetime(data['Date'], dayfirst=True).dt.dayofweek

# Updated Feature Set
X = data[['hour', 'day_of_week', 'baseline_pred', 'rolling_mean_3h', 'rolling_std_3h']]
y = data['actual']

# Split
split_idx = len(data) - 48
X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

# 5. MODEL TRAINING
model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100)
model.fit(X_train, y_train)
xg_preds = model.predict(X_test)

# 6. METRICS
xg_rmse = np.sqrt(mean_squared_error(y_test, xg_preds))
base_rmse = np.sqrt(mean_squared_error(y_test, X_test['baseline_pred']))

print(f"XGBoost RMSE: {xg_rmse:.4f}")
print(f"Baseline RMSE: {base_rmse:.4f}")

# 7. FIRESTORE PAYLOAD
forecast_data = []
for i in range(len(y_test)):
    forecast_data.append({
        "hour": int(X_test.iloc[i]['hour']),
        "actual": float(y_test.iloc[i]),
        "predicted": float(xg_preds[i]),
        "baseline": float(X_test.iloc[i]['baseline_pred'])
    })

# Update Firestore
doc_ref = db.collection('forecasts').document('latest')
doc_ref.set({
    'data': forecast_data,
    'xg_rmse': float(xg_rmse),
    'base_rmse': float(base_rmse),
    'updatedAt': firestore.SERVER_TIMESTAMP
})

print("Success: Pipeline updated with Rolling Statistics.")