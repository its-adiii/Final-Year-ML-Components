# 🔐 IoT Devices Security using Blockchain and ML

A comprehensive smart home security system combining blockchain-based access control with machine learning anomaly detection.

## 🎯 Features

### Blockchain Components
- **Decentralized Access Control**: DID-based permission management
- **Firmware Integrity Verification**: SHA-256 hash validation on-chain
- **Immutable Activity Logs**: Tamper-proof audit trails

### Machine Learning Models
- **Behavioral Anomaly Detection**: Isolation Forest & LSTM models
- **Power Consumption Profiling**: Autoencoder-based anomaly detection
- **Contextual Device Behavior**: Pattern recognition and prediction
- **Edge ML Deployment**: Lightweight models for IoT devices

## 📁 Project Structure

```
├── blockchain/              # Blockchain integration & smart contracts
│   ├── smart_contracts.py   # Access control & firmware validation
│   ├── blockchain_ledger.py # Transaction management
│   └── did_manager.py       # Decentralized Identity management
├── ml_models/               # Machine Learning models
│   ├── anomaly_detection.py # Isolation Forest & LSTM
│   ├── power_profiling.py   # Autoencoder for power analysis
│   ├── behavior_prediction.py # Contextual behavior models
│   └── model_trainer.py     # Training utilities
├── devices/                 # IoT device simulators
│   ├── smart_lock.py
│   ├── smart_light.py
│   ├── security_camera.py
│   └── base_device.py
├── edge/                    # Edge ML deployment
│   ├── edge_inference.py
│   └── model_optimizer.py
├── orchestrator/            # Main security system
│   ├── security_manager.py
│   └── alert_system.py
├── data/                    # Training data & logs
├── models/                  # Saved ML models
└── tests/                   # Unit tests
```

## 🚀 Installation

```bash
pip install -r requirements.txt
```

## 💡 Usage

### 1. Train ML Models
```bash
python ml_models/model_trainer.py
```

### 2. Start Security System
```bash
python orchestrator/security_manager.py
```

### 3. Run Demo
```bash
python demo.py
```

## 🔬 Technical Stack

- **Blockchain**: Custom implementation with smart contracts
- **ML Framework**: TensorFlow, PyTorch, Scikit-learn
- **Edge ML**: ONNX Runtime for optimized inference
- **Communication**: MQTT protocol
- **Identity**: W3C DID-based authentication

## 📊 ML Models

1. **Isolation Forest**: Unsupervised anomaly detection for device behavior
2. **LSTM**: Time-series analysis for access patterns
3. **Autoencoder**: Power consumption profiling
4. **Random Forest**: Contextual behavior classification

## 🔒 Security Features

- Zero-trust architecture
- End-to-end encryption
- Tamper-proof audit logs
- Real-time threat detection
- Automated incident response

## 📝 License

MIT License
