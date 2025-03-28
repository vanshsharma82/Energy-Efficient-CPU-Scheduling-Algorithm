from dataclasses import dataclass
from typing import Optional

@dataclass
class Process:
    pid: int
    arrival_time: float
    burst_time: float
    priority: int = 0
    deadline: Optional[float] = None
    energy_consumption: float = 0.0
    remaining_time: Optional[float] = None
    start_time: Optional[float] = None
    completion_time: Optional[float] = None
    waiting_time: Optional[float] = None
    turnaround_time: Optional[float] = None
    response_time: Optional[float] = None
    is_completed: bool = False
    voltage: float = 1.0  # For DVFS
    frequency: float = 1.0  # For DVFS

    def __post_init__(self):
        self.remaining_time = self.burst_time
        self.energy_consumption = 0.0

    def update_energy_consumption(self, time_interval: float):
        """Update energy consumption based on voltage and frequency"""
        # Simplified energy consumption model: E = P * t
        # where P is power (proportional to V^2 * f) and t is time
        power = (self.voltage ** 2) * self.frequency
        self.energy_consumption += power * time_interval

    def execute(self, time_interval: float) -> bool:
        """Execute the process for the given time interval"""
        if self.remaining_time is None or self.remaining_time <= 0:
            return False

        self.remaining_time -= time_interval
        self.update_energy_consumption(time_interval)

        if self.remaining_time <= 0:
            self.remaining_time = 0
            self.is_completed = True
            return True

        return False

    def calculate_metrics(self):
        """Calculate waiting time and turnaround time"""
        if self.completion_time is not None and self.start_time is not None:
            self.turnaround_time = self.completion_time - self.arrival_time
            self.waiting_time = self.turnaround_time - self.burst_time
            if self.start_time is not None:
                self.response_time = self.start_time - self.arrival_time

    def set_dvfs_parameters(self, voltage: float, frequency: float):
        """Set voltage and frequency for DVFS"""
        self.voltage = voltage
        self.frequency = frequency

    def __str__(self):
        return f"Process(PID={self.pid}, AT={self.arrival_time}, BT={self.burst_time}, " \
               f"Priority={self.priority}, Energy={self.energy_consumption:.2f})" 