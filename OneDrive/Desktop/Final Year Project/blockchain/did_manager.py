"""
Decentralized Identity (DID) Manager
Manages W3C DID-based identities for users and devices
"""

import hashlib
import json
import time
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta


class DID:
    """Decentralized Identifier"""
    
    def __init__(self, entity_type: str, entity_id: str, public_key: str = None):
        """
        Args:
            entity_type: 'User', 'Device', 'System'
            entity_id: Unique identifier
            public_key: Public key for verification
        """
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.did_string = f"DID:SmartHome:{entity_type}:{entity_id}"
        self.public_key = public_key or self._generate_dummy_key()
        self.created_at = time.time()
        self.metadata = {}
    
    def _generate_dummy_key(self) -> str:
        """Generate a dummy public key"""
        key_material = f"{self.entity_type}:{self.entity_id}:{time.time()}"
        return hashlib.sha256(key_material.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert DID to dictionary"""
        return {
            'did': self.did_string,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'public_key': self.public_key,
            'created_at': self.created_at,
            'metadata': self.metadata
        }


class AccessPermission:
    """Access permission for a DID"""
    
    def __init__(self, did: str, resource: str, actions: List[str],
                 valid_from: datetime, valid_until: datetime,
                 constraints: Dict[str, Any] = None):
        self.did = did
        self.resource = resource  # e.g., 'smart_lock', 'security_camera'
        self.actions = actions  # e.g., ['unlock', 'lock']
        self.valid_from = valid_from
        self.valid_until = valid_until
        self.constraints = constraints or {}  # e.g., {'time_range': '10:00-14:00'}
        self.created_at = time.time()
        self.revoked = False
    
    def is_valid(self, current_time: datetime = None) -> bool:
        """Check if permission is currently valid"""
        if self.revoked:
            return False
        
        current_time = current_time or datetime.now()
        return self.valid_from <= current_time <= self.valid_until
    
    def check_constraints(self, context: Dict[str, Any]) -> bool:
        """Check if contextual constraints are met"""
        if not self.constraints:
            return True
        
        # Time range constraint
        if 'time_range' in self.constraints:
            time_range = self.constraints['time_range']
            start_time, end_time = time_range.split('-')
            current_time = datetime.now().strftime('%H:%M')
            
            if not (start_time <= current_time <= end_time):
                return False
        
        # IP address constraint
        if 'allowed_ips' in self.constraints:
            if context.get('ip_address') not in self.constraints['allowed_ips']:
                return False
        
        # Location constraint
        if 'allowed_locations' in self.constraints:
            if context.get('location') not in self.constraints['allowed_locations']:
                return False
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert permission to dictionary"""
        return {
            'did': self.did,
            'resource': self.resource,
            'actions': self.actions,
            'valid_from': self.valid_from.isoformat(),
            'valid_until': self.valid_until.isoformat(),
            'constraints': self.constraints,
            'created_at': self.created_at,
            'revoked': self.revoked
        }


class DIDManager:
    """Manages DIDs and access permissions"""
    
    def __init__(self):
        self.dids: Dict[str, DID] = {}
        self.permissions: Dict[str, List[AccessPermission]] = {}
        self._initialize_system_dids()
    
    def _initialize_system_dids(self):
        """Create system DIDs"""
        system_did = self.create_did('System', 'Core')
        miner_did = self.create_did('System', 'Miner')
    
    def create_did(self, entity_type: str, entity_id: str, 
                   public_key: str = None) -> DID:
        """Create a new DID"""
        did = DID(entity_type, entity_id, public_key)
        self.dids[did.did_string] = did
        self.permissions[did.did_string] = []
        return did
    
    def get_did(self, did_string: str) -> Optional[DID]:
        """Retrieve a DID"""
        return self.dids.get(did_string)
    
    def grant_permission(self, did: str, resource: str, actions: List[str],
                        duration_hours: int = 24,
                        constraints: Dict[str, Any] = None) -> AccessPermission:
        """Grant access permission to a DID"""
        valid_from = datetime.now()
        valid_until = valid_from + timedelta(hours=duration_hours)
        
        permission = AccessPermission(
            did=did,
            resource=resource,
            actions=actions,
            valid_from=valid_from,
            valid_until=valid_until,
            constraints=constraints
        )
        
        if did not in self.permissions:
            self.permissions[did] = []
        
        self.permissions[did].append(permission)
        return permission
    
    def revoke_permission(self, did: str, resource: str):
        """Revoke access permission"""
        if did in self.permissions:
            for perm in self.permissions[did]:
                if perm.resource == resource:
                    perm.revoked = True
    
    def check_permission(self, did: str, resource: str, action: str,
                        context: Dict[str, Any] = None) -> bool:
        """Check if DID has permission for action on resource"""
        if did not in self.permissions:
            return False
        
        context = context or {}
        
        for perm in self.permissions[did]:
            if perm.resource == resource and action in perm.actions:
                if perm.is_valid() and perm.check_constraints(context):
                    return True
        
        return False
    
    def get_permissions(self, did: str) -> List[Dict[str, Any]]:
        """Get all permissions for a DID"""
        if did not in self.permissions:
            return []
        
        return [perm.to_dict() for perm in self.permissions[did]]
    
    def list_all_dids(self) -> List[Dict[str, Any]]:
        """List all registered DIDs"""
        return [did.to_dict() for did in self.dids.values()]


# Singleton instance
_did_manager_instance = None

def get_did_manager() -> DIDManager:
    """Get or create DID manager singleton instance"""
    global _did_manager_instance
    if _did_manager_instance is None:
        _did_manager_instance = DIDManager()
    return _did_manager_instance
