"""
Security Camera Device Simulator
Simulates a security camera with recording capabilities
"""

from .base_device import BaseIoTDevice
from typing import Dict, Any
from datetime import datetime
import time


class SecurityCamera(BaseIoTDevice):
    """Security Camera IoT Device"""
    
    def __init__(self, device_id: str = "security_camera_001"):
        super().__init__(device_id, "security_camera", firmware_version="3.0.1")
        self.recording = False
        self.motion_detected = False
        self.resolution = "1080p"
        self.base_power = 8.0
        self.active_power = 12.0
        self.recording_power = 15.0
        self.current_power = self.base_power
    
    def start_recording(self) -> Dict[str, Any]:
        """Start recording"""
        if self.recording:
            return {'success': False, 'message': 'Already recording'}
        
        self.recording = True
        self.state = "active"
        self.current_power = self.recording_power
        self.last_activity = time.time()
        
        activity = {
            'action': 'start_recording',
            'timestamp': datetime.now().isoformat(),
            'resolution': self.resolution
        }
        self.activity_log.append(activity)
        
        return {
            'success': True,
            'recording': self.recording,
            'resolution': self.resolution
        }
    
    def stop_recording(self) -> Dict[str, Any]:
        """Stop recording"""
        if not self.recording:
            return {'success': False, 'message': 'Not recording'}
        
        self.recording = False
        self.state = "on"
        self.current_power = self.active_power
        self.last_activity = time.time()
        
        activity = {
            'action': 'stop_recording',
            'timestamp': datetime.now().isoformat()
        }
        self.activity_log.append(activity)
        
        return {'success': True, 'recording': self.recording}
    
    def detect_motion(self) -> Dict[str, Any]:
        """Simulate motion detection"""
        self.motion_detected = True
        self.last_activity = time.time()
        
        activity = {
            'action': 'motion_detected',
            'timestamp': datetime.now().isoformat()
        }
        self.activity_log.append(activity)
        
        # Auto-start recording on motion
        if not self.recording:
            self.start_recording()
        
        return {
            'motion_detected': True,
            'timestamp': activity['timestamp'],
            'recording': self.recording
        }
    
    def set_resolution(self, resolution: str) -> Dict[str, Any]:
        """Set video resolution"""
        valid_resolutions = ["720p", "1080p", "4K"]
        if resolution not in valid_resolutions:
            return {'success': False, 'message': f'Invalid resolution. Use: {valid_resolutions}'}
        
        self.resolution = resolution
        
        # Higher resolution = more power
        power_multiplier = {"720p": 1.0, "1080p": 1.2, "4K": 1.5}
        self.recording_power = 15.0 * power_multiplier[resolution]
        
        if self.recording:
            self.current_power = self.recording_power
        
        return {'success': True, 'resolution': self.resolution}
    
    def get_status(self) -> Dict[str, Any]:
        """Get camera status"""
        status = super().get_status()
        status['recording'] = self.recording
        status['motion_detected'] = self.motion_detected
        status['resolution'] = self.resolution
        return status
