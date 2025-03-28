from abc import ABC, abstractmethod
from typing import List, Optional
from .process import Process

class Scheduler(ABC):
    def __init__(self):
        self.processes: List[Process] = []
        self.current_process: Optional[Process] = None
        self.current_time: float = 0.0
        self.total_energy_consumption: float = 0.0
        self.completed_processes: List[Process] = []
        self.gantt_chart: List[tuple] = []  # List of (process_id, start_time, end_time)

    def add_process(self, process: Process):
        """Add a process to the scheduler"""
        self.processes.append(process)

    def add_processes(self, processes: List[Process]):
        """Add multiple processes to the scheduler"""
        self.processes.extend(processes)

    @abstractmethod
    def next_process(self) -> Optional[Process]:
        """Select the next process to execute"""
        pass

    def execute_process(self, time_interval: float) -> bool:
        """Execute the current process for the given time interval"""
        if self.current_process is None:
            return False

        completed = self.current_process.execute(time_interval)
        self.total_energy_consumption += self.current_process.energy_consumption

        if completed:
            self.current_process.completion_time = self.current_time
            self.current_process.calculate_metrics()
            self.completed_processes.append(self.current_process)
            self.current_process = None

        return completed

    def update_gantt_chart(self, process: Process, start_time: float, end_time: float):
        """Update the Gantt chart with process execution information"""
        self.gantt_chart.append((process.pid, start_time, end_time))

    def get_metrics(self) -> dict:
        """Calculate and return performance metrics"""
        if not self.completed_processes:
            return {
                "avg_waiting_time": 0,
                "avg_turnaround_time": 0,
                "avg_response_time": 0,
                "throughput": 0,
                "cpu_utilization": 0,
                "total_energy_consumption": 0
            }

        total_waiting_time = sum(p.waiting_time for p in self.completed_processes)
        total_turnaround_time = sum(p.turnaround_time for p in self.completed_processes)
        total_response_time = sum(p.response_time for p in self.completed_processes)
        n_processes = len(self.completed_processes)

        # Calculate CPU utilization
        total_execution_time = max(p.completion_time for p in self.completed_processes)
        total_burst_time = sum(p.burst_time for p in self.completed_processes)
        cpu_utilization = (total_burst_time / total_execution_time) * 100 if total_execution_time > 0 else 0

        return {
            "avg_waiting_time": total_waiting_time / n_processes,
            "avg_turnaround_time": total_turnaround_time / n_processes,
            "avg_response_time": total_response_time / n_processes,
            "throughput": n_processes / total_execution_time if total_execution_time > 0 else 0,
            "cpu_utilization": cpu_utilization,
            "total_energy_consumption": self.total_energy_consumption
        }

    def reset(self):
        """Reset the scheduler to its initial state"""
        self.processes = []
        self.current_process = None
        self.current_time = 0.0
        self.total_energy_consumption = 0.0
        self.completed_processes = []
        self.gantt_chart = []

    def is_complete(self) -> bool:
        """Check if all processes have been completed"""
        return all(p.is_completed for p in self.processes) 