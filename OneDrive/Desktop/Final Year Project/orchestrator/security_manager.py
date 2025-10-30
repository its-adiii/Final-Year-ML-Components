"""
Security Manager - Main Orchestrator
Integrates blockchain, ML models, and IoT devices for comprehensive security
"""

import os
import sys
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from blockchain.blockchain_ledger import get_blockchain
from blockchain.did_manager import get_did_manager
from blockchain.smart_contracts import (
    get_access_control_contract,
    get_firmware_validation_contract,
    get_activity_log_contract
)


class SecurityManager:
    """
    Main security orchestrator for IoT ecosystem
    Combines blockchain and ML for comprehensive security
    """
    
    def __init__(self):
        # Blockchain components
        self.blockchain = get_blockchain()
        self.did_manager = get_did_manager()
        self.access_control = get_access_control_contract()
        self.firmware_validation = get_firmware_validation_contract()
        self.activity_log = get_activity_log_contract()
        
        # ML models (loaded on demand)
        self.anomaly_detector = None
        self.power_profiler = None
        self.behavior_system = None
        
        # Device registry
        self.devices = {}
        
        # Alert system
        self.alerts = []
        self.alert_handlers = []
        
        print("✓ Security Manager initialized")
    
    def load_ml_models(self, models_dir: str = 'models'):
        """Load trained ML models"""
        print("\n📊 Loading ML models...")
        
        try:
            from ml_models.anomaly_detection import EnsembleAnomalyDetector
            from ml_models.power_profiling import PowerProfiler
            from ml_models.behavior_prediction import ContextualBehaviorSystem
            
            # Load anomaly detector
            if os.path.exists(os.path.join(models_dir, 'anomaly_detection')):
                self.anomaly_detector = EnsembleAnomalyDetector()
                self.anomaly_detector.load(os.path.join(models_dir, 'anomaly_detection'))
                print("  ✓ Anomaly detector loaded")
            
            # Load power profiler
            if os.path.exists(os.path.join(models_dir, 'power_profiles')):
                self.power_profiler = PowerProfiler()
                self.power_profiler.load_profiles(os.path.join(models_dir, 'power_profiles'))
                print("  ✓ Power profiler loaded")
            
            # Load behavior system
            if os.path.exists(os.path.join(models_dir, 'behavior_prediction')):
                self.behavior_system = ContextualBehaviorSystem()
                self.behavior_system.load(os.path.join(models_dir, 'behavior_prediction'))
                print("  ✓ Behavior system loaded")
            
            print("✓ All ML models loaded successfully")
            return True
        
        except Exception as e:
            print(f"⚠ Warning: Could not load ML models: {e}")
            print("  System will operate with blockchain-only security")
            return False
    
    def register_device(self, device_id: str, device_type: str, 
                       firmware_version: str, firmware_hash: str):
        """
        Register a new IoT device
        
        Args:
            device_id: Unique device identifier
            device_type: Type of device (e.g., 'smart_lock')
            firmware_version: Current firmware version
            firmware_hash: SHA-256 hash of firmware
        """
        # Create DID for device
        device_did = self.did_manager.create_did('Device', device_id)
        
        # Register firmware on blockchain
        self.firmware_validation.register_firmware(
            device_id=device_id,
            version=firmware_version,
            firmware_hash=firmware_hash,
            manufacturer_did='DID:SmartHome:System:Core'
        )
        
        # Store device info
        self.devices[device_id] = {
            'device_id': device_id,
            'device_type': device_type,
            'did': device_did.did_string,
            'firmware_version': firmware_version,
            'firmware_hash': firmware_hash,
            'registered_at': datetime.now().isoformat()
        }
        
        print(f"✓ Device registered: {device_id} ({device_type})")
        return device_did
    
    def register_user(self, user_id: str, public_key: str = None) -> str:
        """Register a new user and return their DID"""
        user_did = self.did_manager.create_did('User', user_id, public_key)
        print(f"✓ User registered: {user_id}")
        return user_did.did_string
    
    def grant_device_access(self, user_did: str, device_id: str, 
                           actions: List[str], duration_hours: int = 24,
                           constraints: Dict[str, Any] = None):
        """
        Grant user access to a device
        
        Args:
            user_did: User's decentralized identifier
            device_id: Target device
            actions: Allowed actions (e.g., ['unlock', 'lock'])
            duration_hours: Permission duration
            constraints: Additional constraints (time, location, etc.)
        """
        result = self.access_control.grant_access(
            admin_did='DID:SmartHome:System:Core',
            target_did=user_did,
            device_id=device_id,
            actions=actions,
            duration_hours=duration_hours,
            constraints=constraints
        )
        
        print(f"✓ Access granted: {user_did} → {device_id}")
        return result
    
    def request_device_access(self, user_did: str, device_id: str, 
                             action: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process device access request with full security checks
        
        This is the main security workflow combining blockchain + ML
        """
        print(f"\n🔐 Processing access request...")
        print(f"   User: {user_did}")
        print(f"   Device: {device_id}")
        print(f"   Action: {action}")
        
        # Step 1: Blockchain access control check
        access_result = self.access_control.request_access(
            did=user_did,
            device_id=device_id,
            action=action,
            context=context
        )
        
        if not access_result['granted']:
            print(f"   ✗ Access denied: {access_result.get('reason')}")
            self._create_alert('access_denied', access_result)
            return access_result
        
        print(f"   ✓ Blockchain permission verified")
        
        # Step 2: ML anomaly detection (if available)
        if self.anomaly_detector:
            access_log = {
                'timestamp': context.get('timestamp', datetime.now().isoformat()),
                'device_id': device_id,
                'user_id': user_did,
                'action': action,
                'ip_address': context.get('ip_address', '192.168.1.1'),
                'location': context.get('location', 'home'),
                'access_count': context.get('access_count', 1),
                'time_since_last': context.get('time_since_last', 0),
                'duration': context.get('duration', 0),
                'success': True
            }
            
            anomaly_result = self.anomaly_detector.predict(access_log)
            
            if anomaly_result['is_anomaly']:
                print(f"   ⚠ ML anomaly detected!")
                print(f"      Confidence: {anomaly_result.get('combined_confidence', 0):.2f}")
                
                # High confidence anomaly = block access
                if anomaly_result.get('combined_confidence', 0) > 0.8:
                    print(f"   ✗ Access blocked due to high-confidence anomaly")
                    access_result['granted'] = False
                    access_result['reason'] = 'ML anomaly detection: suspicious pattern'
                    access_result['anomaly_details'] = anomaly_result
                    self._create_alert('ml_anomaly_blocked', access_result)
                    return access_result
                else:
                    # Low confidence = allow but alert
                    print(f"   ⚠ Access allowed but flagged for review")
                    self._create_alert('ml_anomaly_warning', {
                        'access_result': access_result,
                        'anomaly_result': anomaly_result
                    })
        
        # Step 3: Log to blockchain
        self.activity_log.log_activity(
            device_id=device_id,
            activity_type='access_granted',
            details={'action': action, 'context': context},
            did=user_did
        )
        
        print(f"   ✓ Access granted and logged to blockchain")
        
        # Mine pending transactions
        self.blockchain.mine_pending_transactions()
        
        return access_result
    
    def check_device_power(self, device_id: str, power_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check device power consumption for anomalies
        """
        if not self.power_profiler:
            return {'error': 'Power profiler not loaded'}
        
        result = self.power_profiler.check_power_consumption(device_id, power_data)
        
        if result.get('is_anomaly'):
            print(f"⚠ Power anomaly detected on {device_id}")
            print(f"   Type: {result.get('anomaly_type')}")
            
            # Log to blockchain
            self.activity_log.log_activity(
                device_id=device_id,
                activity_type='power_anomaly',
                details=result,
                did=f'DID:SmartHome:Device:{device_id}'
            )
            
            self._create_alert('power_anomaly', result)
        
        return result
    
    def check_device_behavior(self, device_id: str, user_id: str,
                             context: Dict[str, Any], actual_state: str) -> Dict[str, Any]:
        """
        Check if device behavior matches expected patterns
        """
        if not self.behavior_system:
            return {'error': 'Behavior system not loaded'}
        
        context['user_id'] = user_id
        context['device_id'] = device_id
        
        result = self.behavior_system.check_behavior(context, actual_state)
        
        if result.get('is_anomaly'):
            print(f"⚠ Behavioral anomaly detected")
            print(f"   Device: {device_id}")
            print(f"   User: {user_id}")
            
            self._create_alert('behavior_anomaly', result)
        
        return result
    
    def verify_device_firmware(self, device_id: str, firmware_version: str,
                              firmware_hash: str) -> Dict[str, Any]:
        """
        Verify device firmware integrity against blockchain
        """
        result = self.firmware_validation.validate_firmware(
            device_id=device_id,
            version=firmware_version,
            firmware_hash=firmware_hash
        )
        
        if not result['valid']:
            print(f"🚨 CRITICAL: Firmware tampering detected on {device_id}!")
            print(f"   Expected: {result.get('expected_hash')}")
            print(f"   Provided: {result.get('provided_hash')}")
            
            self._create_alert('firmware_tampering', result, severity='critical')
        
        return result
    
    def _create_alert(self, alert_type: str, details: Dict[str, Any], 
                     severity: str = 'medium'):
        """Create and store security alert"""
        alert = {
            'alert_type': alert_type,
            'severity': severity,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        
        self.alerts.append(alert)
        
        # Call alert handlers
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                print(f"Alert handler error: {e}")
        
        # Log critical alerts to blockchain
        if severity == 'critical':
            self.blockchain.add_transaction(
                tx_type='security_alert',
                data=alert,
                did='DID:SmartHome:System:Core'
            )
            self.blockchain.mine_pending_transactions()
    
    def register_alert_handler(self, handler):
        """Register a callback for security alerts"""
        self.alert_handlers.append(handler)
    
    def get_alerts(self, limit: int = 50, severity: str = None) -> List[Dict[str, Any]]:
        """Get recent security alerts"""
        alerts = self.alerts[-limit:]
        
        if severity:
            alerts = [a for a in alerts if a['severity'] == severity]
        
        return alerts
    
    def get_device_history(self, device_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get device activity history from blockchain"""
        return self.activity_log.get_device_history(device_id, limit)
    
    def get_blockchain_stats(self) -> Dict[str, Any]:
        """Get blockchain statistics"""
        return self.blockchain.get_chain_info()
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            'blockchain': self.get_blockchain_stats(),
            'devices': len(self.devices),
            'users': len(self.did_manager.list_all_dids()),
            'alerts': {
                'total': len(self.alerts),
                'critical': len([a for a in self.alerts if a['severity'] == 'critical']),
                'high': len([a for a in self.alerts if a['severity'] == 'high']),
                'medium': len([a for a in self.alerts if a['severity'] == 'medium'])
            },
            'ml_models': {
                'anomaly_detector': self.anomaly_detector is not None,
                'power_profiler': self.power_profiler is not None,
                'behavior_system': self.behavior_system is not None
            }
        }


def main():
    """Main entry point for security manager"""
    print("=" * 60)
    print("IoT Security Manager - Blockchain + ML")
    print("=" * 60)
    
    # Initialize security manager
    manager = SecurityManager()
    
    # Try to load ML models
    manager.load_ml_models()
    
    print("\n" + "=" * 60)
    print("System Status")
    print("=" * 60)
    
    status = manager.get_system_status()
    print(f"\nBlockchain:")
    print(f"  Blocks: {status['blockchain']['total_blocks']}")
    print(f"  Transactions: {status['blockchain']['total_transactions']}")
    print(f"  Valid: {status['blockchain']['is_valid']}")
    
    print(f"\nML Models:")
    print(f"  Anomaly Detector: {'✓' if status['ml_models']['anomaly_detector'] else '✗'}")
    print(f"  Power Profiler: {'✓' if status['ml_models']['power_profiler'] else '✗'}")
    print(f"  Behavior System: {'✓' if status['ml_models']['behavior_system'] else '✗'}")
    
    print("\n✓ Security Manager ready")
    
    return manager


if __name__ == '__main__':
    main()
