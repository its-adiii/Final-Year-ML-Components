"""
Base IoT Device Class
Provides common functionality for all IoT devices
"""

import hashlib
import time
import random
from typing import Dict, Any, Optional
from datetime import datetime
import json


class BaseIoTDevice:
    """Base class for all IoT devices"""
    
    def __init__(self, device_id: str, device_type: str, firmware_version: str = "1.0.0"):
        self.device_id = device_id
        self.device_type = device_type
        self.firmware_version = firmware_version
        self.state = "off"
        self.did = f"DID:SmartHome:Device:{device_id}"
        
        # Power consumption parameters
        self.base_power = 5.0  # Watts
        self.active_power = 20.0  # Watts
        self.current_power = self.base_power
        
        # Device metadata
        self.created_at = time.time()
        self.last_activity = time.time()
        self.activity_log = []
        
        # Firmware hash for integrity verification
        self.firmware_hash = self._calculate_firmware_hash()
    
    def _calculate_firmware_hash(self) -> str:
        """Calculate SHA-256 hash of firmware"""
        firmware_data = f"{self.device_type}:{self.firmware_version}:{self.device_id}"
        return hashlib.sha256(firmware_data.encode()).hexdigest()
    
    def verify_firmware(self, expected_hash: str) -> bool:
        """Verify firmware integrity"""
        return self.firmware_hash == expected_hash
    
    def power_on(self) -> Dict[str, Any]:
        """Power on the device"""
        if self.state == "on":
            return {'success': False, 'message': 'Device already on'}
        
        self.state = "on"
        self.current_power = self.active_power
        self.last_activity = time.time()
        
        activity = {
            'action': 'power_on',
            'timestamp': datetime.now().isoformat(),
            'state': self.state
        }
        self.activity_log.append(activity)
        
        return {'success': True, 'state': self.state, 'power': self.current_power}
    
    def power_off(self) -> Dict[str, Any]:
        """Power off the device"""
        if self.state == "off":
            return {'success': False, 'message': 'Device already off'}
        
        self.state = "off"
        self.current_power = self.base_power
        self.last_activity = time.time()
        
        activity = {
            'action': 'power_off',
            'timestamp': datetime.now().isoformat(),
            'state': self.state
        }
        self.activity_log.append(activity)
        
        return {'success': True, 'state': self.state, 'power': self.current_power}
    
    def get_power_consumption(self) -> Dict[str, Any]:
        """Get current power consumption metrics"""
        # Add some realistic variance
        variance = random.uniform(-0.1, 0.1) * self.current_power
        actual_power = max(0, self.current_power + variance)
        
        voltage = 120 + random.uniform(-2, 2)
        current_amps = actual_power / voltage
        
        return {
            'device_id': self.device_id,
            'timestamp': datetime.now().isoformat(),
            'power_watts': actual_power,
            'voltage': voltage,
            'current_amps': current_amps,
            'power_factor': 0.95 + random.uniform(-0.05, 0.05),
            'avg_power': self.current_power,
            'power_variance': abs(variance),
            'peak_power': self.active_power,
            'device_state': self.state,
            'cpu_usage': random.randint(10, 40) if self.state == "on" else random.randint(0, 10),
            'network_activity': random.randint(50, 200) if self.state == "on" else random.randint(0, 20),
            'temperature': 25 + random.uniform(-5, 5)
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get device status"""
        return {
            'device_id': self.device_id,
            'device_type': self.device_type,
            'did': self.did,
            'state': self.state,
            'firmware_version': self.firmware_version,
            'firmware_hash': self.firmware_hash,
            'current_power': self.current_power,
            'last_activity': self.last_activity,
            'uptime': time.time() - self.created_at
        }
    
    def get_activity_log(self, limit: int = 10) -> list:
        """Get recent activity log"""
        return self.activity_log[-limit:]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert device to dictionary"""
        return self.get_status()
