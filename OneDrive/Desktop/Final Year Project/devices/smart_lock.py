"""
Smart Lock Device Simulator
Simulates a smart door lock with access control
"""

from .base_device import BaseIoTDevice
from typing import Dict, Any
from datetime import datetime
import time


class SmartLock(BaseIoTDevice):
    """Smart Lock IoT Device"""
    
    def __init__(self, device_id: str = "smart_lock_001"):
        super().__init__(device_id, "smart_lock", firmware_version="1.2.0")
        self.lock_state = "locked"
        self.base_power = 3.0
        self.active_power = 12.0
        self.current_power = self.base_power
    
    def unlock(self, user_did: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Unlock the door"""
        if self.lock_state == "unlocked":
            return {
                'success': False,
                'message': 'Lock already unlocked',
                'lock_state': self.lock_state
            }
        
        self.lock_state = "unlocked"
        self.state = "active"
        self.current_power = self.active_power
        self.last_activity = time.time()
        
        activity = {
            'action': 'unlock',
            'user_did': user_did,
            'timestamp': datetime.now().isoformat(),
            'lock_state': self.lock_state,
            'context': context or {}
        }
        self.activity_log.append(activity)
        
        return {
            'success': True,
            'lock_state': self.lock_state,
            'timestamp': activity['timestamp'],
            'user_did': user_did
        }
    
    def lock(self, user_did: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Lock the door"""
        if self.lock_state == "locked":
            return {
                'success': False,
                'message': 'Lock already locked',
                'lock_state': self.lock_state
            }
        
        self.lock_state = "locked"
        self.state = "on"
        self.current_power = self.base_power
        self.last_activity = time.time()
        
        activity = {
            'action': 'lock',
            'user_did': user_did,
            'timestamp': datetime.now().isoformat(),
            'lock_state': self.lock_state,
            'context': context or {}
        }
        self.activity_log.append(activity)
        
        return {
            'success': True,
            'lock_state': self.lock_state,
            'timestamp': activity['timestamp'],
            'user_did': user_did
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get lock status"""
        status = super().get_status()
        status['lock_state'] = self.lock_state
        return status
