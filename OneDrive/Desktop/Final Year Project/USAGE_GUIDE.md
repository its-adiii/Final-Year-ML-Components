# 📖 IoT Security System - Usage Guide

Complete guide for using the IoT Devices Security system with Blockchain and ML.

---

## 🚀 Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Train ML Models

```bash
# Train all ML models with synthetic data
python ml_models/model_trainer.py

# This will create:
# - models/anomaly_detection/ (Isolation Forest + LSTM)
# - models/power_profiles/ (Autoencoder for each device)
# - models/behavior_prediction/ (Random Forest + Pattern Analyzer)
```

### 3. Run Demo

```bash
# Run comprehensive demo
python demo.py
```

### 4. Run Tests

```bash
# Run unit tests
python tests/test_system.py
```

---

## 🔧 System Components

### 1. Blockchain Layer

#### **Blockchain Ledger**
```python
from blockchain.blockchain_ledger import get_blockchain

blockchain = get_blockchain()

# Add transaction
tx_hash = blockchain.add_transaction(
    tx_type='access',
    data={'device_id': 'smart_lock_001', 'action': 'unlock'},
    did='DID:SmartHome:User:Adish'
)

# Mine pending transactions
blockchain.mine_pending_transactions()

# Validate chain
is_valid = blockchain.validate_chain()
```

#### **DID Management**
```python
from blockchain.did_manager import get_did_manager

did_manager = get_did_manager()

# Create DID for user
user_did = did_manager.create_did('User', 'Adish')

# Create DID for device
device_did = did_manager.create_did('Device', 'smart_lock_001')

# Grant permission
permission = did_manager.grant_permission(
    did=user_did.did_string,
    resource='smart_lock_001',
    actions=['unlock', 'lock'],
    duration_hours=24,
    constraints={'time_range': '06:00-22:00'}
)

# Check permission
has_permission = did_manager.check_permission(
    did=user_did.did_string,
    resource='smart_lock_001',
    action='unlock',
    context={'ip_address': '192.168.1.100'}
)
```

#### **Smart Contracts**

**Access Control:**
```python
from blockchain.smart_contracts import get_access_control_contract

access_control = get_access_control_contract()

# Request access
result = access_control.request_access(
    did='DID:SmartHome:User:Adish',
    device_id='smart_lock_001',
    action='unlock',
    context={
        'ip_address': '192.168.1.100',
        'location': 'home',
        'timestamp': '2024-01-01T19:00:00'
    }
)

if result['granted']:
    print("Access granted!")
else:
    print(f"Access denied: {result['reason']}")
```

**Firmware Validation:**
```python
from blockchain.smart_contracts import get_firmware_validation_contract

firmware_contract = get_firmware_validation_contract()

# Register firmware
firmware_contract.register_firmware(
    device_id='smart_lock_001',
    version='1.2.0',
    firmware_hash='abc123...',
    manufacturer_did='DID:Manufacturer:SmartLock'
)

# Validate firmware
result = firmware_contract.validate_firmware(
    device_id='smart_lock_001',
    version='1.2.0',
    firmware_hash='abc123...'
)

if result['valid']:
    print("Firmware verified!")
else:
    print(f"Tampering detected: {result['reason']}")
```

---

### 2. Machine Learning Models

#### **Anomaly Detection**

**Isolation Forest:**
```python
from ml_models.anomaly_detection import IsolationForestDetector

detector = IsolationForestDetector()

# Train with access logs
detector.train(access_logs)

# Predict
access_log = {
    'timestamp': '2024-01-01T03:42:00',
    'device_id': 'smart_lock_001',
    'action': 'unlock',
    'ip_address': '203.45.67.89',
    'location': 'unknown',
    'access_count': 1,
    'time_since_last': 86400,
    'duration': 120,
    'success': True
}

result = detector.predict(access_log)
if result['is_anomaly']:
    print(f"Anomaly detected! Score: {result['anomaly_score']}")
```

**LSTM Detector:**
```python
from ml_models.anomaly_detection import LSTMDetector

lstm = LSTMDetector(sequence_length=10)

# Train with sequential access logs
lstm.train(access_logs, epochs=50)

# Predict on recent sequence
result = lstm.predict(recent_access_logs[-10:])
if result['is_anomaly']:
    print(f"Temporal anomaly! Error: {result['reconstruction_error']}")
```

**Ensemble Detector:**
```python
from ml_models.anomaly_detection import EnsembleAnomalyDetector

ensemble = EnsembleAnomalyDetector()
ensemble.train(access_logs)

# Combined prediction
result = ensemble.predict(access_log)
print(f"Anomaly: {result['is_anomaly']}")
print(f"Confidence: {result['combined_confidence']}")
```

#### **Power Profiling**

```python
from ml_models.power_profiling import PowerProfiler

profiler = PowerProfiler()

# Create device profile
profiler.create_profile('smart_light_001', power_logs)

# Check power consumption
power_data = {
    'device_id': 'smart_light_001',
    'timestamp': '2024-01-01T12:00:00',
    'power_watts': 150.0,  # Abnormally high
    'voltage': 120.0,
    'current_amps': 1.25,
    'cpu_usage': 95,
    'network_activity': 200,
    'temperature': 65
}

result = profiler.check_power_consumption('smart_light_001', power_data)
if result['is_anomaly']:
    print(f"Power anomaly: {result['anomaly_type']}")
    # Types: crypto_mining, botnet_activity, hardware_issue, etc.
```

#### **Behavior Prediction**

```python
from ml_models.behavior_prediction import ContextualBehaviorSystem

behavior_system = ContextualBehaviorSystem()
behavior_system.train(behavior_logs)

# Predict expected behavior
context = {
    'timestamp': '2024-01-01T19:00:00',
    'user_id': 'Adish',
    'device_id': 'smart_tv',
    'previous_state': 'off',
    'is_home': True,
    'ambient_light': 20,
    'temperature': 22
}

result = behavior_system.check_behavior(context, actual_state='on')
if result['is_anomaly']:
    print(f"Unexpected behavior!")
    print(f"Predicted: {result['prediction_based']['predicted_state']}")
    print(f"Actual: {result['prediction_based']['actual_state']}")
```

---

### 3. IoT Devices

#### **Smart Lock**

```python
from devices.smart_lock import SmartLock

lock = SmartLock('smart_lock_001')

# Unlock
result = lock.unlock(
    user_did='DID:SmartHome:User:Adish',
    context={'ip_address': '192.168.1.100'}
)

# Lock
result = lock.lock(user_did='DID:SmartHome:User:Adish')

# Get status
status = lock.get_status()
print(f"Lock state: {status['lock_state']}")

# Get power consumption
power = lock.get_power_consumption()
print(f"Power: {power['power_watts']} W")
```

#### **Smart Light**

```python
from devices.smart_light import SmartLight

light = SmartLight('smart_light_001')

# Turn on with brightness
light.turn_on(brightness=75)

# Set brightness
light.set_brightness(50)

# Set color temperature
light.set_color_temp(3000)  # Warm white

# Turn off
light.turn_off()
```

#### **Security Camera**

```python
from devices.security_camera import SecurityCamera

camera = SecurityCamera('security_camera_001')

# Start recording
camera.start_recording()

# Detect motion
result = camera.detect_motion()
if result['motion_detected']:
    print("Motion detected! Recording started.")

# Set resolution
camera.set_resolution('1080p')

# Stop recording
camera.stop_recording()
```

---

### 4. Security Manager (Main Orchestrator)

```python
from orchestrator.security_manager import SecurityManager

# Initialize
manager = SecurityManager()
manager.load_ml_models('models')

# Register user
user_did = manager.register_user('Adish')

# Register device
manager.register_device(
    device_id='smart_lock_001',
    device_type='smart_lock',
    firmware_version='1.2.0',
    firmware_hash='abc123...'
)

# Grant access
manager.grant_device_access(
    user_did=user_did,
    device_id='smart_lock_001',
    actions=['unlock', 'lock'],
    duration_hours=720,  # 30 days
    constraints={'time_range': '06:00-22:00'}
)

# Request access (full security check)
result = manager.request_device_access(
    user_did=user_did,
    device_id='smart_lock_001',
    action='unlock',
    context={
        'ip_address': '192.168.1.100',
        'location': 'home',
        'timestamp': '2024-01-01T19:00:00'
    }
)

# Check power consumption
manager.check_device_power('smart_lock_001', power_data)

# Verify firmware
manager.verify_device_firmware('smart_lock_001', '1.2.0', 'abc123...')

# Get alerts
alerts = manager.get_alerts(limit=10, severity='high')

# Get system status
status = manager.get_system_status()
```

---

### 5. Edge ML Deployment

```python
from edge.edge_inference import EdgeInferenceEngine, deploy_to_edge

# Deploy model to edge device
deploy_to_edge('models/anomaly_detection/isolation_forest.pkl', 'smart_lock_001')

# Edge inference
engine = EdgeInferenceEngine()
engine.load_model('anomaly', 'models/anomaly_detection/isolation_forest.pkl')

# Run inference on edge
result = engine.predict_anomaly(features, model_name='anomaly')
print(f"Inference time: {result['inference_time_ms']} ms")
```

---

## 🎯 Use Cases

### Use Case 1: Guest Access with Time Constraints

```python
# Grant guest access from 10 AM to 2 PM
manager.grant_device_access(
    user_did='DID:SmartHome:User:Guest001',
    device_id='smart_lock_001',
    actions=['unlock'],
    duration_hours=4,
    constraints={
        'time_range': '10:00-14:00',
        'allowed_ips': ['192.168.1.0/24']
    }
)

# Guest tries to access at 3 AM (denied)
result = manager.request_device_access(
    user_did='DID:SmartHome:User:Guest001',
    device_id='smart_lock_001',
    action='unlock',
    context={'timestamp': '2024-01-01T03:00:00'}
)
# Result: Access denied - outside time window
```

### Use Case 2: Detecting Crypto Mining Malware

```python
# Normal power consumption
normal_power = {'power_watts': 12.0, 'cpu_usage': 15}

# Crypto mining detected
mining_power = {'power_watts': 150.0, 'cpu_usage': 95}

result = manager.check_device_power('smart_light_001', mining_power)
# Result: Anomaly detected - possible_crypto_mining
```

### Use Case 3: Firmware Tampering Detection

```python
# Device boots with tampered firmware
result = manager.verify_device_firmware(
    device_id='smart_lock_001',
    firmware_version='1.2.0',
    firmware_hash='wrong_hash_indicating_tampering'
)
# Result: CRITICAL - Firmware tampering detected
# Action: Device blocked, alert sent, logged to blockchain
```

---

## 📊 Monitoring & Alerts

### Get System Status

```python
status = manager.get_system_status()
print(f"Devices: {status['devices']}")
print(f"Users: {status['users']}")
print(f"Alerts: {status['alerts']['total']}")
print(f"Blockchain valid: {status['blockchain']['is_valid']}")
```

### Register Alert Handler

```python
def alert_handler(alert):
    print(f"🚨 ALERT: {alert['alert_type']}")
    print(f"   Severity: {alert['severity']}")
    # Send email, SMS, webhook, etc.

manager.register_alert_handler(alert_handler)
```

### Blockchain Audit

```python
# Get device history
history = manager.get_device_history('smart_lock_001', limit=100)

for activity in history:
    print(f"Time: {activity['data']['timestamp']}")
    print(f"Action: {activity['data']['activity_type']}")
    print(f"User: {activity['did']}")
    print(f"TX Hash: {activity['tx_hash']}")
```

---

## 🔬 Research & Development

### Training Custom Models

```python
from ml_models.model_trainer import SyntheticDataGenerator

# Generate custom training data
generator = SyntheticDataGenerator()
access_logs = generator.generate_access_logs(num_samples=5000)
power_logs = generator.generate_power_logs('smart_lock', num_samples=3000)

# Train models
from ml_models.anomaly_detection import EnsembleAnomalyDetector
detector = EnsembleAnomalyDetector()
detector.train(access_logs)
detector.save('models/custom_anomaly_detection')
```

### Model Optimization for Edge

```python
from edge.edge_inference import TinyMLOptimizer

optimizer = TinyMLOptimizer()

# Quantize model
quantized_model = optimizer.quantize_model(model, bits=8)

# Prune model
pruned_model = optimizer.prune_model(model, sparsity=0.5)

# Convert to TFLite
optimizer.convert_to_tflite('model.h5', 'model.tflite')
```

---

## 🛠️ Troubleshooting

### Models Not Loading

```bash
# Train models first
python ml_models/model_trainer.py --output models

# Then run demo
python demo.py
```

### Import Errors

```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Check Python version (3.8+)
python --version
```

### Blockchain Validation Fails

```python
# Reset blockchain
from blockchain.blockchain_ledger import BlockchainLedger
blockchain = BlockchainLedger()  # Creates new chain

# Or load from backup
blockchain = BlockchainLedger.load_from_file('data/blockchain_backup.pkl')
```

---

## 📚 Additional Resources

- **Research Paper**: See `docs/research_paper.pdf`
- **API Documentation**: See `docs/api_reference.md`
- **Architecture Diagram**: See `docs/architecture.png`
- **Performance Benchmarks**: See `docs/benchmarks.md`

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Submit pull request

---

## 📄 License

MIT License - See LICENSE file for details
