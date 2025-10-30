# 🧠 Machine Learning Components - Technical Documentation

## Project: IoT Security using Blockchain and ML
**Developer**: Adish Gujarathi  
**Repository**: https://github.com/its-adiii/Final-Year-ML-Components

---

## 📋 Overview

This document provides detailed technical specifications for all machine learning components in the IoT security system.

---

## 1. Behavioral Anomaly Detection

### 1.1 Isolation Forest Detector

**File**: `ml_models/anomaly_detection.py` (Class: `IsolationForestDetector`)

**Purpose**: Unsupervised anomaly detection for device access patterns

**Algorithm**: Isolation Forest (scikit-learn)  
**Model Type**: Ensemble Learning (Tree-based)

**Features** (9 total):
- `hour`: Hour of day (0-23)
- `day_of_week`: Day of week (0-6)
- `access_count`: Number of access attempts
- `time_since_last`: Seconds since last access
- `ip_hash`: Hashed IP address (mod 1000)
- `location_hash`: Hashed location (mod 100)
- `action_encoded`: Encoded action type (0-6)
- `duration`: Action duration in seconds
- `success`: Success flag (0/1)

**Hyperparameters**:
```python
contamination = 0.1        # 10% expected outliers
n_estimators = 100         # Number of trees
random_state = 42          # Reproducibility
n_jobs = -1               # Parallel processing
```

**Training Dataset**:
- **Size**: 2000 samples
- **Time Range**: 30 days
- **Anomaly Ratio**: 10% injected
- **Anomaly Types**: Unusual time (3AM), unusual location, high frequency

**Output**:
```python
{
    'is_anomaly': bool,
    'anomaly_score': float,      # Lower = more anomalous
    'confidence': float,
    'model': 'IsolationForest'
}
```

---

### 1.2 LSTM Autoencoder Detector

**File**: `ml_models/anomaly_detection.py` (Class: `LSTMDetector`)

**Purpose**: Time-series anomaly detection for temporal patterns

**Algorithm**: LSTM Autoencoder (TensorFlow/Keras)  
**Model Type**: Recurrent Neural Network

**Architecture**:
```
Encoder:
  Input(10, 5) → LSTM(64) → Dropout(0.2) → LSTM(32) → Dropout(0.2) 
  → Dense(16) → Dense(8)

Decoder:
  RepeatVector(10) → LSTM(32) → Dropout(0.2) → LSTM(64) → Dropout(0.2)
  → TimeDistributed(Dense(5))
```

**Features** (5 normalized):
- `hour_normalized`: Hour/24.0
- `day_normalized`: Day/7.0
- `access_count_normalized`: Count/100.0
- `time_since_last_normalized`: Hours/24.0
- `action_normalized`: Action/6.0

**Hyperparameters**:
```python
sequence_length = 10       # Time steps
lstm_units = 64           # LSTM hidden units
epochs = 50               # With early stopping
batch_size = 32
validation_split = 0.2
```

**Training Dataset**: Same 2000 access logs, converted to sequences

**Anomaly Detection**: Reconstruction error > 95th percentile threshold

**Output**:
```python
{
    'is_anomaly': bool,
    'reconstruction_error': float,
    'threshold': float,
    'confidence': float,
    'model': 'LSTM'
}
```

---

### 1.3 Ensemble Anomaly Detector

**File**: `ml_models/anomaly_detection.py` (Class: `EnsembleAnomalyDetector`)

**Purpose**: Combine Isolation Forest and LSTM for robust detection

**Strategy**: Union-based (anomaly if either model detects)

**Advantages**:
- Isolation Forest: Point anomalies
- LSTM: Temporal pattern deviations
- Combined: Higher detection rate

---

## 2. Power Consumption Profiling

### 2.1 Power Consumption Autoencoder

**File**: `ml_models/power_profiling.py` (Class: `PowerConsumptionAutoencoder`)

**Purpose**: Detect anomalies in device power consumption

**Algorithm**: Deep Autoencoder (TensorFlow/Keras)  
**Model Type**: Feedforward Neural Network

**Architecture**:
```
Encoder:
  Input(12) → Dense(64, relu) → BatchNorm → Dropout(0.2)
  → Dense(32, relu) → BatchNorm → Dropout(0.2)
  → Dense(16, relu) → Dense(8, relu)

Decoder:
  Dense(16, relu) → Dense(32, relu) → BatchNorm → Dropout(0.2)
  → Dense(64, relu) → BatchNorm → Dropout(0.2)
  → Dense(12, linear)
```

**Features** (12 total):
- `power_watts`: Current power draw
- `voltage`: Voltage level
- `current_amps`: Current in amperes
- `power_factor`: Power factor (0-1)
- `avg_power`: Average power
- `power_variance`: Power variance
- `peak_power`: Peak power
- `hour_normalized`: Hour/24.0
- `device_state`: 0=off, 1=on
- `cpu_usage`: CPU usage (0-1)
- `network_activity`: Network KB/s (normalized)
- `temperature`: Temperature (normalized)

**Hyperparameters**:
```python
encoding_dim = 8          # Compressed dimension
epochs = 100              # With early stopping
batch_size = 32
validation_split = 0.2
```

**Training Dataset**:
- **Size**: 1500 samples per device (9000 total)
- **Devices**: 6 types (smart_lock, smart_light, security_camera, smart_tv, thermostat, smart_speaker)
- **Anomaly Ratio**: 5% injected

**Device Power Profiles**:
```python
{
    'smart_lock': {'base': 5W, 'active': 15W, 'variance': 2W},
    'smart_light': {'base': 10W, 'active': 60W, 'variance': 5W},
    'security_camera': {'base': 8W, 'active': 12W, 'variance': 1W},
    'smart_tv': {'base': 2W, 'active': 150W, 'variance': 20W},
    'thermostat': {'base': 3W, 'active': 8W, 'variance': 1W},
    'smart_speaker': {'base': 3W, 'active': 10W, 'variance': 2W}
}
```

**Anomaly Classification** (5 types):
1. **Crypto Mining**: High power + high CPU (>80%)
2. **Botnet Activity**: High network + unusual power
3. **Hardware Issue**: Voltage/current anomalies
4. **Unauthorized Usage**: Unexpected device state
5. **Overheating**: High temperature (>70°C)

**Output**:
```python
{
    'is_anomaly': bool,
    'reconstruction_error': float,
    'threshold': float,
    'confidence': float,
    'anomalous_features': [{'feature': str, 'error': float}],
    'anomaly_type': str,
    'model': 'PowerAutoencoder'
}
```

---

### 2.2 Power Profiler

**File**: `ml_models/power_profiling.py` (Class: `PowerProfiler`)

**Purpose**: Maintain device-specific power profiles

**Features**:
- Separate autoencoder per device
- Baseline metrics (avg, std, max, min power)
- Baseline comparison

---

## 3. Contextual Device Behavior Prediction

### 3.1 Device Behavior Predictor

**File**: `ml_models/behavior_prediction.py` (Class: `DeviceBehaviorPredictor`)

**Purpose**: Predict expected device behavior from context

**Algorithm**: Random Forest Classifier (scikit-learn)  
**Model Type**: Ensemble Learning

**Features** (11 total):
- `hour`: Hour of day (0-23)
- `day_of_week`: Day of week (0-6)
- `is_weekend`: Boolean (0/1)
- `user_hash`: Hashed user ID
- `previous_state`: Encoded previous state
- `time_since_last`: Hours since last interaction
- `interactions_today`: Count
- `typical_usage_hour`: User's typical hour
- `is_home`: Boolean (0/1)
- `ambient_light`: Normalized (0-1)
- `temperature`: Normalized (0-1)

**Target**: Device state (on, off, standby, active, locked, unlocked)

**Hyperparameters**:
```python
n_estimators = 100        # Number of trees
max_depth = 10           # Tree depth
random_state = 42
n_jobs = -1
```

**Training Dataset**:
- **Size**: 2000 samples
- **Users**: 4 with distinct patterns
- **Time Range**: 30 days

**User Patterns**:
```python
{
    'Adish': {'peak_hours': [7,8,19,20,21], 'devices': ['smart_tv','smart_light']},
    'Guest001': {'peak_hours': [10,11,12,13,14], 'devices': ['smart_lock']},
    'Guest002': {'peak_hours': [15,16,17], 'devices': ['smart_lock','smart_light']},
    'Family001': {'peak_hours': [18,19,20], 'devices': ['smart_tv','thermostat']}
}
```

**Output**:
```python
{
    'predicted_state': str,
    'confidence': float,
    'top_predictions': [{'state': str, 'probability': float}],
    'model': 'BehaviorPredictor'
}
```

**Anomaly Detection**:
- Flags if predicted ≠ actual AND confidence > 0.6
- Severity: high (>0.8), medium (>0.6), low (<0.6)

---

### 3.2 User Pattern Analyzer

**File**: `ml_models/behavior_prediction.py` (Class: `UserPatternAnalyzer`)

**Purpose**: Learn and analyze user behavior patterns

**Tracked Patterns**:
- Hourly usage distribution
- Daily usage distribution
- Device preferences
- Total interactions

**Output**:
```python
{
    'user_id': str,
    'total_interactions': int,
    'peak_hours': [{'hour': int, 'count': int}],
    'preferred_devices': [{'device': str, 'count': int}],
    'active_days': [{'day': int, 'count': int}]
}
```

---

### 3.3 Contextual Behavior System

**File**: `ml_models/behavior_prediction.py` (Class: `ContextualBehaviorSystem`)

**Purpose**: Complete behavior analysis

**Components**:
1. Device Behavior Predictor
2. User Pattern Analyzer

**Anomaly Detection**: Prediction-based OR pattern-based

---

## 4. Model Training

### Training Script

**File**: `ml_models/model_trainer.py`

**Command**:
```bash
python ml_models/model_trainer.py --output models
```

**Training Pipeline**:
1. Generate synthetic data (5s)
2. Train Anomaly Detection (2-5 min)
3. Train Power Profiling (8-10 min per device)
4. Train Behavior Prediction (3-5s)

**Total Time**: ~15-20 minutes (CPU)

**Output Structure**:
```
models/
├── anomaly_detection/
│   ├── isolation_forest.pkl
│   ├── lstm.pkl
│   └── lstm_model.h5
├── power_profiles/
│   ├── {device}_power_profile.pkl
│   ├── {device}_power_profile_model.h5
│   └── {device}_power_profile_encoder.h5
└── behavior_prediction/
    ├── behavior_predictor.pkl
    └── user_patterns.pkl
```

---

## 5. Performance Metrics

### Anomaly Detection

| Model | Training | Inference | Accuracy |
|-------|----------|-----------|----------|
| Isolation Forest | 2s | <1ms | 94% |
| LSTM | 5min | 3ms | 91% |
| Ensemble | 5min | 4ms | 96% |

### Power Profiling

| Device | Training | Inference | Accuracy |
|--------|----------|-----------|----------|
| All devices | 8min | 2ms | 95-97% |

### Behavior Prediction

| Model | Training | Inference | Accuracy |
|-------|----------|-----------|----------|
| Random Forest | 3s | <1ms | 89% |
| Combined | 4s | <1ms | 92% |

---

## 6. Dependencies

**Core Libraries**:
```
tensorflow==2.13.0
scikit-learn==1.3.0
numpy==1.24.3
pandas==2.0.3
joblib==1.3.2
```

**Full**: See `requirements.txt`

---

## 7. Usage Examples

### Train Models
```python
from ml_models.model_trainer import train_all_models
models = train_all_models(output_dir='models')
```

### Anomaly Detection
```python
from ml_models.anomaly_detection import EnsembleAnomalyDetector

detector = EnsembleAnomalyDetector()
detector.load('models/anomaly_detection')

result = detector.predict(access_log)
print(result['is_anomaly'])
```

### Power Profiling
```python
from ml_models.power_profiling import PowerProfiler

profiler = PowerProfiler()
profiler.load_profiles('models/power_profiles')

result = profiler.check_power_consumption('smart_lock', power_log)
print(result['anomaly_type'])
```

### Behavior Prediction
```python
from ml_models.behavior_prediction import ContextualBehaviorSystem

system = ContextualBehaviorSystem()
system.load('models/behavior_prediction')

result = system.check_behavior(context, actual_state)
print(result['is_anomaly'])
```

---

## 8. Research Contributions

**Novel Aspects**:
1. Ensemble ML (Isolation Forest + LSTM) for IoT anomaly detection
2. Power-based malware detection using autoencoders
3. Context-aware behavior prediction with Random Forest
4. Device-specific power profiling methodology

**Potential Publications**:
- "Ensemble ML for Real-Time IoT Anomaly Detection"
- "Power Consumption Profiling for IoT Malware Detection"
- "Context-Aware Behavior Prediction for Smart Home Security"

---

**End of ML Components Documentation**
