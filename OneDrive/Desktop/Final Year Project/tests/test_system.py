"""
Unit tests for IoT Security System
Tests blockchain, ML models, and integration
"""

import unittest
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from blockchain.blockchain_ledger import BlockchainLedger, Transaction, Block
from blockchain.did_manager import DIDManager, DID
from blockchain.smart_contracts import AccessControlContract, FirmwareValidationContract
from devices.smart_lock import SmartLock
from devices.smart_light import SmartLight
from devices.security_camera import SecurityCamera


class TestBlockchain(unittest.TestCase):
    """Test blockchain functionality"""
    
    def setUp(self):
        self.blockchain = BlockchainLedger()
    
    def test_genesis_block(self):
        """Test genesis block creation"""
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(self.blockchain.chain[0].index, 0)
    
    def test_add_transaction(self):
        """Test adding transactions"""
        tx_hash = self.blockchain.add_transaction(
            tx_type='test',
            data={'message': 'test transaction'},
            did='DID:Test:001'
        )
        self.assertIsNotNone(tx_hash)
        self.assertEqual(len(self.blockchain.pending_transactions), 1)
    
    def test_mine_block(self):
        """Test mining blocks"""
        self.blockchain.add_transaction(
            tx_type='test',
            data={'message': 'test'},
            did='DID:Test:001'
        )
        
        block = self.blockchain.mine_pending_transactions()
        self.assertIsNotNone(block)
        self.assertEqual(len(self.blockchain.chain), 2)
        self.assertEqual(len(self.blockchain.pending_transactions), 0)
    
    def test_chain_validation(self):
        """Test blockchain validation"""
        self.blockchain.add_transaction('test', {'data': 'test'}, 'DID:Test:001')
        self.blockchain.mine_pending_transactions()
        
        self.assertTrue(self.blockchain.validate_chain())
    
    def test_merkle_root(self):
        """Test Merkle root calculation"""
        self.blockchain.add_transaction('test1', {'data': 'test1'}, 'DID:Test:001')
        self.blockchain.add_transaction('test2', {'data': 'test2'}, 'DID:Test:002')
        
        block = self.blockchain.mine_pending_transactions()
        self.assertIsNotNone(block.merkle_root)
        self.assertEqual(len(block.merkle_root), 64)  # SHA-256 hex length


class TestDIDManager(unittest.TestCase):
    """Test DID management"""
    
    def setUp(self):
        self.did_manager = DIDManager()
    
    def test_create_did(self):
        """Test DID creation"""
        did = self.did_manager.create_did('User', 'TestUser')
        self.assertIsNotNone(did)
        self.assertEqual(did.entity_type, 'User')
        self.assertEqual(did.entity_id, 'TestUser')
    
    def test_grant_permission(self):
        """Test permission granting"""
        did = self.did_manager.create_did('User', 'TestUser')
        
        permission = self.did_manager.grant_permission(
            did=did.did_string,
            resource='smart_lock',
            actions=['unlock'],
            duration_hours=24
        )
        
        self.assertIsNotNone(permission)
        self.assertTrue(permission.is_valid())
    
    def test_check_permission(self):
        """Test permission checking"""
        did = self.did_manager.create_did('User', 'TestUser')
        
        self.did_manager.grant_permission(
            did=did.did_string,
            resource='smart_lock',
            actions=['unlock', 'lock'],
            duration_hours=24
        )
        
        # Should have permission
        self.assertTrue(
            self.did_manager.check_permission(
                did=did.did_string,
                resource='smart_lock',
                action='unlock'
            )
        )
        
        # Should not have permission for different action
        self.assertFalse(
            self.did_manager.check_permission(
                did=did.did_string,
                resource='smart_lock',
                action='delete'
            )
        )


class TestSmartContracts(unittest.TestCase):
    """Test smart contracts"""
    
    def setUp(self):
        self.access_control = AccessControlContract()
        self.firmware_validation = FirmwareValidationContract()
    
    def test_access_control(self):
        """Test access control contract"""
        # Grant permission
        did = 'DID:SmartHome:User:TestUser'
        self.access_control.did_manager.create_did('User', 'TestUser')
        
        self.access_control.grant_access(
            admin_did='DID:SmartHome:System:Core',
            target_did=did,
            device_id='test_device',
            actions=['unlock'],
            duration_hours=24
        )
        
        # Request access
        result = self.access_control.request_access(
            did=did,
            device_id='test_device',
            action='unlock',
            context={'ip_address': '192.168.1.1'}
        )
        
        self.assertTrue(result['granted'])
    
    def test_firmware_validation(self):
        """Test firmware validation contract"""
        # Register firmware
        device_id = 'test_device'
        version = '1.0.0'
        firmware_hash = 'abc123' * 10  # Dummy hash
        
        self.firmware_validation.register_firmware(
            device_id=device_id,
            version=version,
            firmware_hash=firmware_hash,
            manufacturer_did='DID:Manufacturer:Test'
        )
        
        # Validate correct firmware
        result = self.firmware_validation.validate_firmware(
            device_id=device_id,
            version=version,
            firmware_hash=firmware_hash
        )
        
        self.assertTrue(result['valid'])
        
        # Validate tampered firmware
        result = self.firmware_validation.validate_firmware(
            device_id=device_id,
            version=version,
            firmware_hash='wrong_hash'
        )
        
        self.assertFalse(result['valid'])


class TestDevices(unittest.TestCase):
    """Test IoT device simulators"""
    
    def test_smart_lock(self):
        """Test smart lock functionality"""
        lock = SmartLock('test_lock')
        
        # Test unlock
        result = lock.unlock('DID:User:Test')
        self.assertTrue(result['success'])
        self.assertEqual(lock.lock_state, 'unlocked')
        
        # Test lock
        result = lock.lock('DID:User:Test')
        self.assertTrue(result['success'])
        self.assertEqual(lock.lock_state, 'locked')
    
    def test_smart_light(self):
        """Test smart light functionality"""
        light = SmartLight('test_light')
        
        # Test turn on
        result = light.turn_on(brightness=75)
        self.assertTrue(result['success'])
        self.assertEqual(light.state, 'on')
        self.assertEqual(light.brightness, 75)
        
        # Test brightness change
        result = light.set_brightness(50)
        self.assertTrue(result['success'])
        self.assertEqual(light.brightness, 50)
    
    def test_security_camera(self):
        """Test security camera functionality"""
        camera = SecurityCamera('test_camera')
        
        # Test recording
        result = camera.start_recording()
        self.assertTrue(result['success'])
        self.assertTrue(camera.recording)
        
        # Test motion detection
        result = camera.detect_motion()
        self.assertTrue(result['motion_detected'])
    
    def test_power_consumption(self):
        """Test device power consumption"""
        light = SmartLight('test_light')
        
        # Off state
        power = light.get_power_consumption()
        self.assertLess(power['power_watts'], 5)
        
        # On state
        light.turn_on(brightness=100)
        power = light.get_power_consumption()
        self.assertGreater(power['power_watts'], 10)


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_full_access_workflow(self):
        """Test complete access control workflow"""
        from orchestrator.security_manager import SecurityManager
        
        manager = SecurityManager()
        
        # Register user
        user_did = manager.register_user('TestUser')
        
        # Register device
        lock = SmartLock('test_lock')
        manager.register_device(
            device_id=lock.device_id,
            device_type=lock.device_type,
            firmware_version=lock.firmware_version,
            firmware_hash=lock.firmware_hash
        )
        
        # Grant access
        manager.grant_device_access(
            user_did=user_did,
            device_id=lock.device_id,
            actions=['unlock', 'lock'],
            duration_hours=24
        )
        
        # Request access
        result = manager.request_device_access(
            user_did=user_did,
            device_id=lock.device_id,
            action='unlock',
            context={'ip_address': '192.168.1.1', 'timestamp': datetime.now().isoformat()}
        )
        
        self.assertTrue(result['granted'])
        
        # Verify blockchain logging
        stats = manager.get_blockchain_stats()
        self.assertGreater(stats['total_transactions'], 0)


def run_tests():
    """Run all tests"""
    print("=" * 70)
    print("  IoT Security System - Unit Tests")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestBlockchain))
    suite.addTests(loader.loadTestsFromTestCase(TestDIDManager))
    suite.addTests(loader.loadTestsFromTestCase(TestSmartContracts))
    suite.addTests(loader.loadTestsFromTestCase(TestDevices))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 70)
    print("  Test Summary")
    print("=" * 70)
    print(f"  Tests run: {result.testsRun}")
    print(f"  Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  Failures: {len(result.failures)}")
    print(f"  Errors: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
