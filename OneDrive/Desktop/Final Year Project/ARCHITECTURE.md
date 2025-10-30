# 🏗️ System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        IoT SECURITY ECOSYSTEM                        │
│                    Blockchain + Machine Learning                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE LAYER                         │
├─────────────────────────────────────────────────────────────────────┤
│  • Mobile App  • Web Dashboard  • CLI  • API Gateway                │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      SECURITY ORCHESTRATOR                           │
│                    (orchestrator/security_manager.py)                │
├─────────────────────────────────────────────────────────────────────┤
│  • Access Request Processing                                         │
│  • ML Model Coordination                                             │
│  • Alert Management                                                  │
│  • System Monitoring                                                 │
└─────────────────────────────────────────────────────────────────────┘
                    │                              │
                    ▼                              ▼
┌───────────────────────────────┐    ┌───────────────────────────────┐
│     BLOCKCHAIN LAYER          │    │     MACHINE LEARNING LAYER    │
├───────────────────────────────┤    ├───────────────────────────────┤
│                               │    │                               │
│  ┌─────────────────────────┐ │    │  ┌─────────────────────────┐ │
│  │  Blockchain Ledger      │ │    │  │  Anomaly Detection      │ │
│  │  • Blocks & Transactions│ │    │  │  • Isolation Forest     │ │
│  │  • Merkle Trees         │ │    │  │  • LSTM Networks        │ │
│  │  • PoW Consensus        │ │    │  │  • Ensemble Methods     │ │
│  └─────────────────────────┘ │    │  └─────────────────────────┘ │
│                               │    │                               │
│  ┌─────────────────────────┐ │    │  ┌─────────────────────────┐ │
│  │  DID Manager            │ │    │  │  Power Profiling        │ │
│  │  • User DIDs            │ │    │  │  • Autoencoder          │ │
│  │  • Device DIDs          │ │    │  │  • Anomaly Types        │ │
│  │  • Permissions          │ │    │  │  • Baseline Tracking    │ │
│  └─────────────────────────┘ │    │  └─────────────────────────┘ │
│                               │    │                               │
│  ┌─────────────────────────┐ │    │  ┌─────────────────────────┐ │
│  │  Smart Contracts        │ │    │  │  Behavior Prediction    │ │
│  │  • Access Control       │ │    │  │  • Random Forest        │ │
│  │  • Firmware Validation  │ │    │  │  • Pattern Analysis     │ │
│  │  • Activity Logging     │ │    │  │  • Context Awareness    │ │
│  └─────────────────────────┘ │    │  └─────────────────────────┘ │
│                               │    │                               │
└───────────────────────────────┘    └───────────────────────────────┘
                    │                              │
                    └──────────────┬───────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         EDGE DEPLOYMENT LAYER                        │
├─────────────────────────────────────────────────────────────────────┤
│  • Model Optimization (Quantization, Pruning)                        │
│  • TFLite/ONNX Conversion                                            │
│  • Edge Inference Engine                                             │
│  • Lightweight Security Monitor                                      │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          IoT DEVICE LAYER                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ Smart Lock   │  │ Smart Light  │  │ Security Cam │              │
│  │              │  │              │  │              │              │
│  │ • DID        │  │ • DID        │  │ • DID        │              │
│  │ • Firmware   │  │ • Firmware   │  │ • Firmware   │              │
│  │ • Power Mon. │  │ • Power Mon. │  │ • Power Mon. │              │
│  │ • Edge ML    │  │ • Edge ML    │  │ • Edge ML    │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ Smart TV     │  │ Thermostat   │  │ Smart Speaker│              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Architecture

### 1. Access Request Flow

```
┌─────────┐
│  User   │
└────┬────┘
     │ 1. Request Access
     ▼
┌─────────────────────┐
│ Security Manager    │
└────┬────────────────┘
     │
     ├─► 2. Check Blockchain Permission
     │   ┌──────────────────────┐
     │   │ Smart Contract       │
     │   │ • Validate DID       │
     │   │ • Check constraints  │
     │   │ • Time/Location      │
     │   └──────────────────────┘
     │
     ├─► 3. ML Anomaly Detection
     │   ┌──────────────────────┐
     │   │ Ensemble Detector    │
     │   │ • Isolation Forest   │
     │   │ • LSTM Analysis      │
     │   │ • Confidence Score   │
     │   └──────────────────────┘
     │
     ├─► 4. Behavior Check
     │   ┌──────────────────────┐
     │   │ Behavior Predictor   │
     │   │ • Expected state     │
     │   │ • Pattern match      │
     │   │ • Context analysis   │
     │   └──────────────────────┘
     │
     └─► 5. Decision & Logging
         ┌──────────────────────┐
         │ Blockchain Logger    │
         │ • Create transaction │
         │ • Mine block         │
         │ • Immutable record   │
         └──────────────────────┘
              │
              ▼
         ┌─────────┐
         │ GRANTED │  or  │ DENIED │
         └─────────┘      └────────┘
```

---

### 2. Power Anomaly Detection Flow

```
┌──────────────┐
│ IoT Device   │
└──────┬───────┘
       │ Continuous monitoring
       ▼
┌─────────────────────┐
│ Power Sensor        │
│ • Voltage           │
│ • Current           │
│ • Power (W)         │
│ • CPU usage         │
│ • Network activity  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Edge ML Inference   │
│ (On-device)         │
│ • Quick check       │
│ • Threshold-based   │
└──────┬──────────────┘
       │
       ├─► Normal ──► Continue
       │
       └─► Anomaly detected
           │
           ▼
    ┌──────────────────────┐
    │ Cloud ML Analysis    │
    │ • Autoencoder        │
    │ • Feature analysis   │
    │ • Anomaly type       │
    └──────┬───────────────┘
           │
           ▼
    ┌──────────────────────┐
    │ Alert & Log          │
    │ • Blockchain log     │
    │ • Notify owner       │
    │ • Quarantine device  │
    └──────────────────────┘
```

---

### 3. Firmware Validation Flow

```
┌──────────────┐
│ Device Boot  │
└──────┬───────┘
       │
       ▼
┌─────────────────────┐
│ Calculate Hash      │
│ SHA-256(firmware)   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Query Blockchain    │
│ Get expected hash   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Compare Hashes      │
└──────┬──────────────┘
       │
       ├─► Match ──► Boot normally
       │
       └─► Mismatch
           │
           ▼
    ┌──────────────────────┐
    │ TAMPERING DETECTED   │
    │ • Block device       │
    │ • Alert owner        │
    │ • Log to blockchain  │
    │ • Forensic mode      │
    └──────────────────────┘
```

---

## Component Interaction Matrix

```
┌────────────────┬──────────┬──────────┬──────────┬──────────┐
│                │Blockchain│    ML    │  Edge    │ Devices  │
├────────────────┼──────────┼──────────┼──────────┼──────────┤
│ Blockchain     │    -     │  Logs    │  Verify  │  Audit   │
├────────────────┼──────────┼──────────┼──────────┼──────────┤
│ ML Models      │  Query   │    -     │  Deploy  │  Monitor │
├────────────────┼──────────┼──────────┼──────────┼──────────┤
│ Edge Layer     │  Sync    │  Infer   │    -     │  Control │
├────────────────┼──────────┼──────────┼──────────┼──────────┤
│ Devices        │  Report  │  Data    │  Execute │    -     │
└────────────────┴──────────┴──────────┴──────────┴──────────┘
```

---

## Security Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    LAYER 7: USER INTERFACE                   │
│  Security: Authentication, Session Management                │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                LAYER 6: ORCHESTRATION LAYER                  │
│  Security: Authorization, Rate Limiting, Input Validation    │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                  LAYER 5: BLOCKCHAIN LAYER                   │
│  Security: Immutability, Consensus, Cryptographic Proofs     │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                LAYER 4: MACHINE LEARNING LAYER               │
│  Security: Anomaly Detection, Threat Intelligence            │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                   LAYER 3: EDGE LAYER                        │
│  Security: Local Inference, Quick Response                   │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                 LAYER 2: COMMUNICATION LAYER                 │
│  Security: TLS/SSL, MQTT Auth, Message Encryption           │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                   LAYER 1: DEVICE LAYER                      │
│  Security: Firmware Integrity, Secure Boot, TPM              │
└─────────────────────────────────────────────────────────────┘
```

---

## Threat Detection Pipeline

```
┌────────────────────────────────────────────────────────────────┐
│                    THREAT DETECTION PIPELINE                    │
└────────────────────────────────────────────────────────────────┘

Input: Device Activity / Access Request / Power Data
  │
  ▼
┌─────────────────────┐
│ Data Collection     │
│ • Timestamp         │
│ • Context           │
│ • Metrics           │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Feature Extraction  │
│ • Normalize         │
│ • Encode            │
│ • Scale             │
└──────┬──────────────┘
       │
       ├──────────────────────┬──────────────────────┐
       ▼                      ▼                      ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│ Isolation   │      │    LSTM     │      │ Behavior    │
│ Forest      │      │  Temporal   │      │ Predictor   │
│ Detection   │      │  Analysis   │      │ Contextual  │
└──────┬──────┘      └──────┬──────┘      └──────┬──────┘
       │                    │                    │
       └────────────┬───────┴────────────────────┘
                    ▼
           ┌─────────────────┐
           │ Ensemble Fusion │
           │ • Vote          │
           │ • Confidence    │
           └────────┬────────┘
                    │
                    ▼
           ┌─────────────────┐
           │ Threat Scoring  │
           │ • Severity      │
           │ • Type          │
           └────────┬────────┘
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
   Normal      Suspicious    Critical
     │             │             │
     └─────────────┴─────────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ Response Action │
          │ • Allow         │
          │ • Alert         │
          │ • Block         │
          │ • Quarantine    │
          └─────────────────┘
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLOUD LAYER                           │
│  • Security Manager                                          │
│  • Blockchain Nodes                                          │
│  • ML Training Pipeline                                      │
│  • Model Registry                                            │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │   Internet/5G     │
                    └─────────┬─────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                        EDGE LAYER                            │
│  • Home Gateway / Raspberry Pi                               │
│  • Local Blockchain Node                                     │
│  • Edge ML Inference                                         │
│  • MQTT Broker                                               │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │   Local Network   │
                    │   (WiFi/Zigbee)   │
                    └─────────┬─────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                       DEVICE LAYER                           │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐          │
│  │Lock  │  │Light │  │Camera│  │ TV   │  │Sensor│          │
│  └──────┘  └──────┘  └──────┘  └──────┘  └──────┘          │
└─────────────────────────────────────────────────────────────┘
```

---

## Technology Stack Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│  Python 3.8+  │  Flask  │  CLI  │  REST API                 │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                    BLOCKCHAIN LAYER                          │
│  Custom PoW  │  SHA-256  │  Merkle Trees  │  Smart Contracts│
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                  MACHINE LEARNING LAYER                      │
│  TensorFlow  │  PyTorch  │  Scikit-learn  │  Keras          │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                    EDGE/OPTIMIZATION                         │
│  ONNX  │  TensorFlow Lite  │  Model Quantization            │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                   COMMUNICATION LAYER                        │
│  MQTT  │  CoAP  │  HTTP/HTTPS  │  WebSocket                 │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER                              │
│  Pickle  │  JSON  │  YAML  │  IPFS (optional)               │
└─────────────────────────────────────────────────────────────┘
```

---

This architecture provides:
- ✅ **Scalability**: Supports 100+ devices
- ✅ **Security**: Multi-layer defense
- ✅ **Performance**: <10ms edge inference
- ✅ **Reliability**: Blockchain immutability
- ✅ **Flexibility**: Modular components
- ✅ **Maintainability**: Clean separation of concerns
