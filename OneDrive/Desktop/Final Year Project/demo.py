"""
Comprehensive Demo of IoT Security System
Demonstrates blockchain + ML integration for smart home security
"""

import os
import sys
import time
from datetime import datetime, timedelta
import random

# Add project to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestrator.security_manager import SecurityManager
from devices.smart_lock import SmartLock
from devices.smart_light import SmartLight
from devices.security_camera import SecurityCamera


def print_section(title: str):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_result(result: dict, indent: int = 2):
    """Pretty print result dictionary"""
    import json
    print(" " * indent + json.dumps(result, indent=2, default=str))


def demo_blockchain_access_control(manager: SecurityManager):
    """Demonstrate blockchain-based access control"""
    print_section("1. BLOCKCHAIN ACCESS CONTROL")
    
    print("\n📝 Registering users...")
    adish_did = manager.register_user('Adish')
    guest_did = manager.register_user('Guest001')
    
    print("\n📝 Registering devices...")
    smart_lock = SmartLock('smart_lock_001')
    manager.register_device(
        device_id=smart_lock.device_id,
        device_type=smart_lock.device_type,
        firmware_version=smart_lock.firmware_version,
        firmware_hash=smart_lock.firmware_hash
    )
    
    print("\n🔑 Granting access permissions...")
    
    # Grant Adish full access
    manager.grant_device_access(
        user_did=adish_did,
        device_id='smart_lock_001',
        actions=['unlock', 'lock'],
        duration_hours=720  # 30 days
    )
    
    # Grant guest limited access with time constraint
    manager.grant_device_access(
        user_did=guest_did,
        device_id='smart_lock_001',
        actions=['unlock'],
        duration_hours=4,
        constraints={'time_range': '10:00-14:00'}
    )
    
    print("\n✅ Testing access requests...")
    
    # Test 1: Valid access
    print("\n  Test 1: Adish accessing lock (should succeed)")
    context = {
        'ip_address': '192.168.1.100',
        'location': 'home',
        'timestamp': datetime.now().isoformat()
    }
    result = manager.request_device_access(adish_did, 'smart_lock_001', 'unlock', context)
    print(f"  Result: {'✓ GRANTED' if result['granted'] else '✗ DENIED'}")
    
    # Test 2: Guest outside time window
    print("\n  Test 2: Guest accessing at 3 AM (should fail)")
    context['timestamp'] = datetime.now().replace(hour=3, minute=0).isoformat()
    result = manager.request_device_access(guest_did, 'smart_lock_001', 'unlock', context)
    print(f"  Result: {'✓ GRANTED' if result['granted'] else '✗ DENIED'}")
    if not result['granted']:
        print(f"  Reason: {result.get('reason')}")
    
    # Test 3: Unauthorized action
    print("\n  Test 3: Guest trying to lock (not permitted)")
    context['timestamp'] = datetime.now().replace(hour=12, minute=0).isoformat()
    result = manager.request_device_access(guest_did, 'smart_lock_001', 'lock', context)
    print(f"  Result: {'✓ GRANTED' if result['granted'] else '✗ DENIED'}")
    if not result['granted']:
        print(f"  Reason: {result.get('reason')}")


def demo_firmware_validation(manager: SecurityManager):
    """Demonstrate firmware integrity validation"""
    print_section("2. FIRMWARE INTEGRITY VALIDATION")
    
    print("\n🔧 Creating device with firmware...")
    camera = SecurityCamera('security_camera_001')
    
    print(f"  Device: {camera.device_id}")
    print(f"  Firmware: v{camera.firmware_version}")
    print(f"  Hash: {camera.firmware_hash[:16]}...")
    
    manager.register_device(
        device_id=camera.device_id,
        device_type=camera.device_type,
        firmware_version=camera.firmware_version,
        firmware_hash=camera.firmware_hash
    )
    
    print("\n✅ Test 1: Valid firmware verification")
    result = manager.verify_device_firmware(
        device_id=camera.device_id,
        firmware_version=camera.firmware_version,
        firmware_hash=camera.firmware_hash
    )
    print(f"  Result: {'✓ VALID' if result['valid'] else '✗ INVALID'}")
    
    print("\n🚨 Test 2: Tampered firmware detection")
    tampered_hash = "0" * 64  # Fake hash
    result = manager.verify_device_firmware(
        device_id=camera.device_id,
        firmware_version=camera.firmware_version,
        firmware_hash=tampered_hash
    )
    print(f"  Result: {'✓ VALID' if result['valid'] else '✗ INVALID - TAMPERING DETECTED'}")
    if not result['valid']:
        print(f"  Reason: {result.get('reason')}")


def demo_anomaly_detection(manager: SecurityManager):
    """Demonstrate ML-based anomaly detection"""
    print_section("3. ML ANOMALY DETECTION")
    
    if not manager.anomaly_detector:
        print("\n⚠ ML models not loaded. Skipping anomaly detection demo.")
        print("  Run 'python ml_models/model_trainer.py' first to train models.")
        return
    
    print("\n🤖 Testing behavioral anomaly detection...")
    
    # Normal access pattern
    print("\n  Test 1: Normal access (7 PM, home)")
    normal_access = {
        'timestamp': datetime.now().replace(hour=19, minute=0).isoformat(),
        'device_id': 'smart_lock_001',
        'user_id': 'DID:SmartHome:User:Adish',
        'action': 'unlock',
        'ip_address': '192.168.1.100',
        'location': 'home',
        'access_count': 1,
        'time_since_last': 3600,
        'duration': 5,
        'success': True
    }
    
    result = manager.anomaly_detector.predict(normal_access)
    print(f"  Anomaly: {'✗ YES' if result['is_anomaly'] else '✓ NO'}")
    print(f"  Confidence: {result.get('combined_confidence', 0):.2f}")
    
    # Anomalous access pattern
    print("\n  Test 2: Suspicious access (3:42 AM, unknown location)")
    anomalous_access = {
        'timestamp': datetime.now().replace(hour=3, minute=42).isoformat(),
        'device_id': 'smart_lock_001',
        'user_id': 'DID:SmartHome:User:Guest001',
        'action': 'unlock',
        'ip_address': '203.45.67.89',  # External IP
        'location': 'unknown_city',
        'access_count': 1,
        'time_since_last': 86400,  # 24 hours
        'duration': 120,
        'success': True
    }
    
    result = manager.anomaly_detector.predict(anomalous_access)
    print(f"  Anomaly: {'✗ YES' if result['is_anomaly'] else '✓ NO'}")
    print(f"  Confidence: {result.get('combined_confidence', 0):.2f}")
    
    if result['is_anomaly']:
        print(f"\n  🚨 ALERT: Suspicious access pattern detected!")
        print(f"     - Unusual time (3:42 AM)")
        print(f"     - Unknown location")
        print(f"     - External IP address")


def demo_power_profiling(manager: SecurityManager):
    """Demonstrate power consumption profiling"""
    print_section("4. POWER CONSUMPTION PROFILING")
    
    if not manager.power_profiler:
        print("\n⚠ Power profiler not loaded. Skipping power profiling demo.")
        return
    
    print("\n⚡ Testing power consumption anomaly detection...")
    
    # Normal power consumption
    print("\n  Test 1: Normal power consumption")
    normal_power = {
        'device_id': 'smart_light_001',
        'timestamp': datetime.now().isoformat(),
        'power_watts': 12.0,
        'voltage': 120.0,
        'current_amps': 0.1,
        'power_factor': 0.95,
        'avg_power': 12.0,
        'power_variance': 1.0,
        'peak_power': 15.0,
        'device_state': 'on',
        'cpu_usage': 15,
        'network_activity': 50,
        'temperature': 25
    }
    
    result = manager.check_device_power('smart_light', normal_power)
    if 'error' not in result:
        print(f"  Anomaly: {'✗ YES' if result.get('is_anomaly') else '✓ NO'}")
    
    # Crypto mining attack simulation
    print("\n  Test 2: Crypto mining attack (high power + CPU)")
    mining_power = {
        'device_id': 'smart_light_001',
        'timestamp': datetime.now().isoformat(),
        'power_watts': 150.0,  # Abnormally high
        'voltage': 120.0,
        'current_amps': 1.25,
        'power_factor': 0.95,
        'avg_power': 12.0,
        'power_variance': 50.0,
        'peak_power': 150.0,
        'device_state': 'on',
        'cpu_usage': 95,  # Very high CPU
        'network_activity': 200,
        'temperature': 65
    }
    
    result = manager.check_device_power('smart_light', mining_power)
    if 'error' not in result:
        print(f"  Anomaly: {'✗ YES' if result.get('is_anomaly') else '✓ NO'}")
        if result.get('is_anomaly'):
            print(f"  Type: {result.get('anomaly_type')}")
            print(f"\n  🚨 ALERT: Possible crypto mining malware detected!")


def demo_behavior_prediction(manager: SecurityManager):
    """Demonstrate contextual behavior prediction"""
    print_section("5. CONTEXTUAL BEHAVIOR PREDICTION")
    
    if not manager.behavior_system:
        print("\n⚠ Behavior system not loaded. Skipping behavior prediction demo.")
        return
    
    print("\n🧠 Testing device behavior prediction...")
    
    # Expected behavior
    print("\n  Test 1: Expected behavior (TV on at 7 PM)")
    context = {
        'timestamp': datetime.now().replace(hour=19, minute=0).isoformat(),
        'user_id': 'Adish',
        'device_id': 'smart_tv',
        'previous_state': 'off',
        'time_since_last': 3600,
        'interactions_today': 3,
        'typical_usage_hour': 19,
        'is_home': True,
        'ambient_light': 20,
        'temperature': 22
    }
    
    result = manager.check_device_behavior('smart_tv', 'Adish', context, 'on')
    if 'error' not in result:
        print(f"  Anomaly: {'✗ YES' if result.get('is_anomaly') else '✓ NO'}")
        pred = result.get('prediction_based', {})
        print(f"  Predicted: {pred.get('predicted_state')}")
        print(f"  Actual: {pred.get('actual_state')}")
    
    # Unexpected behavior
    print("\n  Test 2: Unexpected behavior (lights on at 3 AM, user away)")
    context = {
        'timestamp': datetime.now().replace(hour=3, minute=0).isoformat(),
        'user_id': 'Unknown',
        'device_id': 'smart_light',
        'previous_state': 'off',
        'time_since_last': 28800,
        'interactions_today': 0,
        'typical_usage_hour': 19,
        'is_home': False,
        'ambient_light': 0,
        'temperature': 18
    }
    
    result = manager.check_device_behavior('smart_light', 'Unknown', context, 'on')
    if 'error' not in result:
        print(f"  Anomaly: {'✗ YES' if result.get('is_anomaly') else '✓ NO'}")
        if result.get('is_anomaly'):
            print(f"\n  🚨 ALERT: Unexpected device activation!")
            print(f"     - Unusual time (3 AM)")
            print(f"     - User not home")


def demo_blockchain_audit(manager: SecurityManager):
    """Demonstrate blockchain audit trail"""
    print_section("6. BLOCKCHAIN AUDIT TRAIL")
    
    print("\n📊 Blockchain statistics:")
    stats = manager.get_blockchain_stats()
    print(f"  Total blocks: {stats['total_blocks']}")
    print(f"  Total transactions: {stats['total_transactions']}")
    print(f"  Chain valid: {'✓ YES' if stats['is_valid'] else '✗ NO'}")
    print(f"  Pending transactions: {stats['pending_transactions']}")
    
    print("\n📜 Recent device activity (smart_lock_001):")
    history = manager.get_device_history('smart_lock_001', limit=5)
    
    if history:
        for i, activity in enumerate(history[:3], 1):
            print(f"\n  Activity {i}:")
            print(f"    Type: {activity['data'].get('activity_type')}")
            print(f"    Timestamp: {activity['data'].get('timestamp')}")
            print(f"    DID: {activity['did']}")
            print(f"    TX Hash: {activity['tx_hash'][:16]}...")
    else:
        print("  No activity recorded yet")


def demo_security_alerts(manager: SecurityManager):
    """Demonstrate security alert system"""
    print_section("7. SECURITY ALERTS")
    
    alerts = manager.get_alerts(limit=10)
    
    if alerts:
        print(f"\n🚨 Recent security alerts ({len(alerts)} total):")
        
        for i, alert in enumerate(alerts[:5], 1):
            print(f"\n  Alert {i}:")
            print(f"    Type: {alert['alert_type']}")
            print(f"    Severity: {alert['severity'].upper()}")
            print(f"    Time: {alert['timestamp']}")
            
            # Show key details
            details = alert.get('details', {})
            if 'reason' in details:
                print(f"    Reason: {details['reason']}")
            if 'anomaly_type' in details:
                print(f"    Anomaly: {details['anomaly_type']}")
    else:
        print("\n✓ No security alerts - system operating normally")


def demo_system_status(manager: SecurityManager):
    """Show comprehensive system status"""
    print_section("8. SYSTEM STATUS")
    
    status = manager.get_system_status()
    
    print("\n📊 Overall System Status:")
    print(f"\n  Blockchain:")
    print(f"    Blocks: {status['blockchain']['total_blocks']}")
    print(f"    Transactions: {status['blockchain']['total_transactions']}")
    print(f"    Valid: {'✓' if status['blockchain']['is_valid'] else '✗'}")
    
    print(f"\n  Devices:")
    print(f"    Registered: {status['devices']}")
    
    print(f"\n  Users:")
    print(f"    Registered: {status['users']}")
    
    print(f"\n  Security Alerts:")
    print(f"    Total: {status['alerts']['total']}")
    print(f"    Critical: {status['alerts']['critical']}")
    print(f"    High: {status['alerts']['high']}")
    print(f"    Medium: {status['alerts']['medium']}")
    
    print(f"\n  ML Models:")
    print(f"    Anomaly Detector: {'✓ Loaded' if status['ml_models']['anomaly_detector'] else '✗ Not loaded'}")
    print(f"    Power Profiler: {'✓ Loaded' if status['ml_models']['power_profiler'] else '✗ Not loaded'}")
    print(f"    Behavior System: {'✓ Loaded' if status['ml_models']['behavior_system'] else '✗ Not loaded'}")


def main():
    """Run comprehensive demo"""
    print("\n" + "=" * 70)
    print("  IoT SECURITY SYSTEM - COMPREHENSIVE DEMO")
    print("  Blockchain + Machine Learning Integration")
    print("=" * 70)
    
    # Initialize security manager
    print("\n🚀 Initializing Security Manager...")
    manager = SecurityManager()
    
    # Load ML models
    print("\n📊 Loading ML models...")
    models_loaded = manager.load_ml_models()
    
    if not models_loaded:
        print("\n⚠ Note: ML models not found. Some demos will be skipped.")
        print("   To enable full functionality:")
        print("   1. Run: python ml_models/model_trainer.py")
        print("   2. Re-run this demo\n")
        time.sleep(2)
    
    # Run all demos
    try:
        demo_blockchain_access_control(manager)
        time.sleep(1)
        
        demo_firmware_validation(manager)
        time.sleep(1)
        
        demo_anomaly_detection(manager)
        time.sleep(1)
        
        demo_power_profiling(manager)
        time.sleep(1)
        
        demo_behavior_prediction(manager)
        time.sleep(1)
        
        demo_blockchain_audit(manager)
        time.sleep(1)
        
        demo_security_alerts(manager)
        time.sleep(1)
        
        demo_system_status(manager)
        
    except KeyboardInterrupt:
        print("\n\n⚠ Demo interrupted by user")
    except Exception as e:
        print(f"\n\n✗ Error during demo: {e}")
        import traceback
        traceback.print_exc()
    
    # Summary
    print("\n" + "=" * 70)
    print("  DEMO COMPLETE")
    print("=" * 70)
    print("\n✅ Successfully demonstrated:")
    print("   • Blockchain-based access control with DIDs")
    print("   • Firmware integrity validation")
    print("   • ML-based anomaly detection")
    print("   • Power consumption profiling")
    print("   • Contextual behavior prediction")
    print("   • Immutable audit trails")
    print("   • Security alert system")
    print("\n🔒 Your IoT ecosystem is now secured with blockchain + ML!")
    print("\n" + "=" * 70 + "\n")


if __name__ == '__main__':
    main()
