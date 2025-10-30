"""
Quick Start Script
Minimal example to get started with the IoT Security System
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestrator.security_manager import SecurityManager
from devices.smart_lock import SmartLock
from devices.smart_light import SmartLight
from datetime import datetime


def main():
    print("\n" + "=" * 60)
    print("  IoT Security System - Quick Start")
    print("=" * 60)
    
    # Step 1: Initialize Security Manager
    print("\n1️⃣  Initializing Security Manager...")
    manager = SecurityManager()
    
    # Step 2: Register a user
    print("\n2️⃣  Registering user 'Adish'...")
    user_did = manager.register_user('Adish')
    print(f"   ✓ User DID: {user_did}")
    
    # Step 3: Register a smart lock device
    print("\n3️⃣  Registering smart lock device...")
    smart_lock = SmartLock('smart_lock_001')
    manager.register_device(
        device_id=smart_lock.device_id,
        device_type=smart_lock.device_type,
        firmware_version=smart_lock.firmware_version,
        firmware_hash=smart_lock.firmware_hash
    )
    print(f"   ✓ Device registered: {smart_lock.device_id}")
    
    # Step 4: Grant access permission
    print("\n4️⃣  Granting access permission...")
    manager.grant_device_access(
        user_did=user_did,
        device_id='smart_lock_001',
        actions=['unlock', 'lock'],
        duration_hours=24
    )
    print(f"   ✓ Permission granted for 24 hours")
    
    # Step 5: Request access (blockchain verification)
    print("\n5️⃣  Requesting device access...")
    context = {
        'ip_address': '192.168.1.100',
        'location': 'home',
        'timestamp': datetime.now().isoformat()
    }
    
    result = manager.request_device_access(
        user_did=user_did,
        device_id='smart_lock_001',
        action='unlock',
        context=context
    )
    
    if result['granted']:
        print(f"   ✓ Access GRANTED")
        print(f"   Transaction hash: {result['tx_hash'][:16]}...")
    else:
        print(f"   ✗ Access DENIED: {result.get('reason')}")
    
    # Step 6: Verify firmware integrity
    print("\n6️⃣  Verifying firmware integrity...")
    firmware_result = manager.verify_device_firmware(
        device_id='smart_lock_001',
        firmware_version=smart_lock.firmware_version,
        firmware_hash=smart_lock.firmware_hash
    )
    
    if firmware_result['valid']:
        print(f"   ✓ Firmware verified - no tampering detected")
    else:
        print(f"   ✗ Firmware tampering detected!")
    
    # Step 7: Check system status
    print("\n7️⃣  System status:")
    status = manager.get_system_status()
    print(f"   Blockchain blocks: {status['blockchain']['total_blocks']}")
    print(f"   Total transactions: {status['blockchain']['total_transactions']}")
    print(f"   Registered devices: {status['devices']}")
    print(f"   Registered users: {status['users']}")
    print(f"   Security alerts: {status['alerts']['total']}")
    
    # Summary
    print("\n" + "=" * 60)
    print("  ✅ Quick Start Complete!")
    print("=" * 60)
    print("\n🎯 What you just did:")
    print("   • Created a blockchain-secured IoT ecosystem")
    print("   • Registered users with decentralized identities (DIDs)")
    print("   • Implemented access control with smart contracts")
    print("   • Verified firmware integrity on-chain")
    print("   • Logged all activities to immutable blockchain")
    
    print("\n📚 Next steps:")
    print("   • Train ML models: python ml_models/model_trainer.py")
    print("   • Run full demo: python demo.py")
    print("   • Run tests: python tests/test_system.py")
    print("   • Read usage guide: USAGE_GUIDE.md")
    
    print("\n" + "=" * 60 + "\n")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
