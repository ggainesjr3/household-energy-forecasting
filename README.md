# 📂 SYSTEM_ARCH: HOUSEHOLD_ENERGY_FORECASTER_V1
# STATUS: [OPERATIONAL] | MAE: [0.1974 kW] | ENVIRONMENT: [ROSENCRANTZ]
# DEVELOPER: GARY EDWARD GAINES, JR.

---

## 🛠 TACTICAL OVERVIEW
A high-frequency time-series regression engine designed to forecast household power consumption. Developed using **XGBoost Regressor**, this system specializes in capturing cyclical usage patterns and sudden load surges.

### 🧠 REFINED LOGIC (TIME-SERIES MATH)
Achieving a sub-0.20 MAE required moving beyond linear time logic:
* **[CIRCULAR_ENCODING]:** Utilized Sine/Cosine transformations for hourly data. This forces the model to recognize that 23:00 and 00:00 are adjacent points, preventing "Midnight Jumps" in prediction.
* **[VOLATILITY_MONITOR]:** Implemented a 3-hour Rolling Standard Deviation feature. This acts as a "Early Warning System" for high-variance periods (e.g., heavy appliance usage).
* **[LAG_INJECTION]:** Features 1h, 2h, and 24h lag states to provide the model with "Short-Term Memory" and "Daily Rhythm" context.

### 🛡 DEFENSIVE PATTERNS
* **CHRONO_SPLIT:** Training/Validation is split strictly by time. The model is never allowed to "peek" into the future during training.
* **SENSOR_RECOVERY:** Implemented Forward-Fill (`ffill`) logic to maintain time-series continuity during sensor dropouts or "dirty data" events.
* **STOCHASTIC_REGRESSION:** Tuned XGBoost with a 0.03 learning rate and 80% subsampling to ensure the model learns trends rather than memorizing noise.

---

## 🚀 DEPLOYMENT_LOGS

### INSTALL_DEPENDS
```bash
pip install xgboost pandas numpy scikit-learn

EXECUTE_TRAIN
Bash

# Processes 2M+ rows, resamples to hourly, and trains XGBoost
python3 src/model.py

🎙 PHILOSOPHY

    "Predicting energy is like managing a bar tab: the past hour usually tells you exactly what the next ten minutes will look like. It's about spotting the surge before it hits the meter."

👤 DEVELOPER_INFO

    Lead Engineer: Gary Edward Gaines, Jr.

    Focus: Time-Series Forecasting, ML Ops

    Location: Philadelphia, PA / Southern NJ Area

    Host_Machine: rosencrantz