"""
Smart Contracts for IoT Security
Implements access control and firmware validation logic
"""

import hashlib
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from .blockchain_ledger import get_blockchain, Transaction
from .did_manager import get_did_manager


class AccessControlContract:
    """Smart contract for device access control"""
    
    def __init__(self):
        self.blockchain = get_blockchain()
        self.did_manager = get_did_manager()
    
    def request_access(self, did: str, device_id: str, action: str,
                      context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process access request through smart contract
        
        Args:
            did: Decentralized identifier of requester
            device_id: Target device identifier
            action: Requested action (e.g., 'unlock', 'view', 'control')
            context: Additional context (IP, location, time, etc.)
        
        Returns:
            Access decision with details
        """
        # Check permission on blockchain
        has_permission = self.did_manager.check_permission(
            did=did,
            resource=device_id,
            action=action,
            context=context
        )
        
        # Log access attempt to blockchain
        access_data = {
            'device_id': device_id,
            'action': action,
            'granted': has_permission,
            'context': context,
            'timestamp': datetime.now().isoformat()
        }
        
        tx_hash = self.blockchain.add_transaction(
            tx_type='access',
            data=access_data,
            did=did
        )
        
        result = {
            'granted': has_permission,
            'did': did,
            'device_id': device_id,
            'action': action,
            'tx_hash': tx_hash,
            'timestamp': access_data['timestamp']
        }
        
        if not has_permission:
            result['reason'] = self._get_denial_reason(did, device_id, action, context)
        
        return result
    
    def _get_denial_reason(self, did: str, device_id: str, action: str,
                          context: Dict[str, Any]) -> str:
        """Determine why access was denied"""
        permissions = self.did_manager.get_permissions(did)
        
        if not permissions:
            return "No permissions found for DID"
        
        for perm in permissions:
            if perm['resource'] == device_id:
                if action not in perm['actions']:
                    return f"Action '{action}' not permitted"
                
                if perm['revoked']:
                    return "Permission has been revoked"
                
                valid_from = datetime.fromisoformat(perm['valid_from'])
                valid_until = datetime.fromisoformat(perm['valid_until'])
                now = datetime.now()
                
                if now < valid_from:
                    return "Permission not yet valid"
                if now > valid_until:
                    return "Permission has expired"
                
                return "Contextual constraints not met"
        
        return f"No permission for device '{device_id}'"
    
    def grant_access(self, admin_did: str, target_did: str, device_id: str,
                    actions: List[str], duration_hours: int = 24,
                    constraints: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Grant access permission (requires admin privileges)
        """
        # In production, verify admin_did has admin privileges
        
        permission = self.did_manager.grant_permission(
            did=target_did,
            resource=device_id,
            actions=actions,
            duration_hours=duration_hours,
            constraints=constraints
        )
        
        # Log permission grant to blockchain
        grant_data = {
            'target_did': target_did,
            'device_id': device_id,
            'actions': actions,
            'duration_hours': duration_hours,
            'constraints': constraints,
            'timestamp': datetime.now().isoformat()
        }
        
        tx_hash = self.blockchain.add_transaction(
            tx_type='permission_grant',
            data=grant_data,
            did=admin_did
        )
        
        return {
            'success': True,
            'permission': permission.to_dict(),
            'tx_hash': tx_hash
        }
    
    def revoke_access(self, admin_did: str, target_did: str, device_id: str) -> Dict[str, Any]:
        """Revoke access permission"""
        self.did_manager.revoke_permission(target_did, device_id)
        
        # Log revocation to blockchain
        revoke_data = {
            'target_did': target_did,
            'device_id': device_id,
            'timestamp': datetime.now().isoformat()
        }
        
        tx_hash = self.blockchain.add_transaction(
            tx_type='permission_revoke',
            data=revoke_data,
            did=admin_did
        )
        
        return {
            'success': True,
            'tx_hash': tx_hash
        }


class FirmwareValidationContract:
    """Smart contract for firmware integrity validation"""
    
    def __init__(self):
        self.blockchain = get_blockchain()
        self.firmware_registry: Dict[str, Dict[str, Any]] = {}
    
    def register_firmware(self, device_id: str, version: str,
                         firmware_hash: str, manufacturer_did: str) -> Dict[str, Any]:
        """
        Register verified firmware hash on blockchain
        
        Args:
            device_id: Device identifier
            version: Firmware version
            firmware_hash: SHA-256 hash of firmware
            manufacturer_did: DID of manufacturer
        """
        registry_key = f"{device_id}:{version}"
        
        firmware_data = {
            'device_id': device_id,
            'version': version,
            'firmware_hash': firmware_hash,
            'registered_at': datetime.now().isoformat()
        }
        
        self.firmware_registry[registry_key] = firmware_data
        
        # Log to blockchain
        tx_hash = self.blockchain.add_transaction(
            tx_type='firmware_register',
            data=firmware_data,
            did=manufacturer_did
        )
        
        return {
            'success': True,
            'registry_key': registry_key,
            'tx_hash': tx_hash
        }
    
    def validate_firmware(self, device_id: str, version: str,
                         firmware_hash: str) -> Dict[str, Any]:
        """
        Validate firmware against on-chain hash
        
        Returns:
            Validation result with details
        """
        registry_key = f"{device_id}:{version}"
        
        if registry_key not in self.firmware_registry:
            return {
                'valid': False,
                'reason': 'Firmware version not registered',
                'device_id': device_id,
                'version': version
            }
        
        registered_firmware = self.firmware_registry[registry_key]
        expected_hash = registered_firmware['firmware_hash']
        
        is_valid = firmware_hash == expected_hash
        
        # Log validation attempt to blockchain
        validation_data = {
            'device_id': device_id,
            'version': version,
            'provided_hash': firmware_hash,
            'expected_hash': expected_hash,
            'valid': is_valid,
            'timestamp': datetime.now().isoformat()
        }
        
        tx_hash = self.blockchain.add_transaction(
            tx_type='firmware_validation',
            data=validation_data,
            did=f"DID:SmartHome:Device:{device_id}"
        )
        
        result = {
            'valid': is_valid,
            'device_id': device_id,
            'version': version,
            'tx_hash': tx_hash
        }
        
        if not is_valid:
            result['reason'] = 'Hash mismatch - possible tampering detected'
            result['expected_hash'] = expected_hash
            result['provided_hash'] = firmware_hash
        
        return result
    
    def get_firmware_info(self, device_id: str, version: str) -> Optional[Dict[str, Any]]:
        """Retrieve registered firmware information"""
        registry_key = f"{device_id}:{version}"
        return self.firmware_registry.get(registry_key)


class ActivityLogContract:
    """Smart contract for immutable activity logging"""
    
    def __init__(self):
        self.blockchain = get_blockchain()
    
    def log_activity(self, device_id: str, activity_type: str,
                    details: Dict[str, Any], did: str) -> str:
        """
        Log device activity to blockchain
        
        Args:
            device_id: Device identifier
            activity_type: Type of activity (e.g., 'power_on', 'state_change')
            details: Activity details
            did: DID of entity performing activity
        
        Returns:
            Transaction hash
        """
        activity_data = {
            'device_id': device_id,
            'activity_type': activity_type,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        
        tx_hash = self.blockchain.add_transaction(
            tx_type='activity',
            data=activity_data,
            did=did
        )
        
        return tx_hash
    
    def get_device_history(self, device_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve activity history for a device"""
        all_activities = self.blockchain.get_transactions_by_type('activity')
        
        device_activities = [
            activity for activity in all_activities
            if activity['data'].get('device_id') == device_id
        ]
        
        # Sort by timestamp (most recent first)
        device_activities.sort(
            key=lambda x: x['data']['timestamp'],
            reverse=True
        )
        
        return device_activities[:limit]
    
    def verify_log_integrity(self, tx_hash: str) -> bool:
        """Verify that a log entry hasn't been tampered with"""
        # In a real implementation, this would verify the transaction
        # exists in the blockchain and the chain is valid
        return self.blockchain.validate_chain()


# Singleton instances
_access_control_instance = None
_firmware_validation_instance = None
_activity_log_instance = None

def get_access_control_contract() -> AccessControlContract:
    """Get access control contract singleton"""
    global _access_control_instance
    if _access_control_instance is None:
        _access_control_instance = AccessControlContract()
    return _access_control_instance

def get_firmware_validation_contract() -> FirmwareValidationContract:
    """Get firmware validation contract singleton"""
    global _firmware_validation_instance
    if _firmware_validation_instance is None:
        _firmware_validation_instance = FirmwareValidationContract()
    return _firmware_validation_instance

def get_activity_log_contract() -> ActivityLogContract:
    """Get activity log contract singleton"""
    global _activity_log_instance
    if _activity_log_instance is None:
        _activity_log_instance = ActivityLogContract()
    return _activity_log_instance
