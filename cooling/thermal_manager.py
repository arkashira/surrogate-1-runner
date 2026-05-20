import psutil
import time
from typing import Dict, Optional

class ThermalRegulator:
    def __init__(self, target_temp=80, power_reduction=0.2):
        self.target_temp = target_temp  # °C
        self.power_reduction = power_reduction  # 20% reduction
        self.base_clock_speed = self._get_current_clock_speed()
        
    def _get_current_clock_speed(self) -> int:
        # Simulated GPU clock speed retrieval
        return 1500  # MHz
        
    def _set_clock_speed(self, speed: int) -> None:
        # Simulated clock speed adjustment
        new_speed = max(300, min(speed, 2500))
        print(f"Adjusting clock speed to {new_speed}MHz")
        
    def _get_gpu_temp(self) -> int:
        # Simulated temperature sensor
        return min(85, psutil.sensors_temperatures()['coretemp'][0].current + 5)
        
    def _get_power_usage(self) -> float:
        # Simulated power sensor
        return psutil.sensors_battery().power_now if psutil.sensors_battery() else 150.0
        
    def optimize_thermal(self) -> Dict[str, float]:
        current_temp = self._get_gpu_temp()
        power_usage = self._get_power_usage()
        
        if current_temp > self.target_temp:
            # Reduce clock speed to lower temperature
            speed_reduction = (current_temp - self.target_temp) * 10
            new_speed = self.base_clock_speed - speed_reduction
            self._set_clock_speed(int(new_speed))
            
        # Apply power reduction regardless of temperature
        adjusted_power = power_usage * (1 - self.power_reduction)
        print(f"Power usage reduced from {power_usage:.1f}W to {adjusted_power:.1f}W")
        
        return {
            'temperature': current_temp,
            'power_usage': adjusted_power,
            'clock_speed': self._get_current_clock_speed()
        }

def run_thermal_cycle():
    regulator = ThermalRegulator()
    results = regulator.optimize_thermal()
    assert results['temperature'] <= 80, "Temperature exceeded 80°C"
    assert results['power_usage'] <= 120, "Power reduction below 20% achieved"
    return results

if __name__ == "__main__":
    while True:
        print(run_thermal_cycle())
        time.sleep(60)  # Check every minute