"""
Smart Light Device Simulator
Simulates a smart light bulb with brightness control
"""

from .base_device import BaseIoTDevice
from typing import Dict, Any
from datetime import datetime
import time


class SmartLight(BaseIoTDevice):
    """Smart Light IoT Device"""
    
    def __init__(self, device_id: str = "smart_light_001"):
        super().__init__(device_id, "smart_light", firmware_version="2.1.0")
        self.brightness = 0  # 0-100
        self.color_temp = 3000  # Kelvin
        self.base_power = 0.5
        self.max_power = 60.0
        self.current_power = self.base_power
    
    def turn_on(self, brightness: int = 100) -> Dict[str, Any]:
        """Turn on the light"""
        result = self.power_on()
        if result['success']:
            self.set_brightness(brightness)
        return result
    
    def turn_off(self) -> Dict[str, Any]:
        """Turn off the light"""
        self.brightness = 0
        self.current_power = self.base_power
        return self.power_off()
    
    def set_brightness(self, brightness: int) -> Dict[str, Any]:
        """Set light brightness (0-100)"""
        if not 0 <= brightness <= 100:
            return {'success': False, 'message': 'Brightness must be 0-100'}
        
        self.brightness = brightness
        # Power consumption scales with brightness
        self.current_power = self.base_power + (self.max_power - self.base_power) * (brightness / 100.0)
        self.last_activity = time.time()
        
        activity = {
            'action': 'set_brightness',
            'brightness': brightness,
            'timestamp': datetime.now().isoformat(),
            'power': self.current_power
        }
        self.activity_log.append(activity)
        
        return {
            'success': True,
            'brightness': self.brightness,
            'power': self.current_power
        }
    
    def set_color_temp(self, kelvin: int) -> Dict[str, Any]:
        """Set color temperature (2700-6500K)"""
        if not 2700 <= kelvin <= 6500:
            return {'success': False, 'message': 'Color temp must be 2700-6500K'}
        
        self.color_temp = kelvin
        self.last_activity = time.time()
        
        activity = {
            'action': 'set_color_temp',
            'color_temp': kelvin,
            'timestamp': datetime.now().isoformat()
        }
        self.activity_log.append(activity)
        
        return {'success': True, 'color_temp': self.color_temp}
    
    def get_status(self) -> Dict[str, Any]:
        """Get light status"""
        status = super().get_status()
        status['brightness'] = self.brightness
        status['color_temp'] = self.color_temp
        return status
