from typing import Optional
from models.scheduler import Scheduler
from models.process import Process

class FCFS(Scheduler):
    def __init__(self):
        super().__init__()
        self.ready_queue = []

    def next_process(self) -> Optional[Process]:
        """Select the next process to execute using FCFS algorithm"""
        # If there's a current process and it's not completed, continue executing it
        if self.current_process and not self.current_process.is_completed:
            return self.current_process

        # Add arrived processes to ready queue
        for process in self.processes:
            if (not process.is_completed and 
                process.arrival_time <= self.current_time and 
                process not in self.ready_queue):
                self.ready_queue.append(process)

        # Sort ready queue by arrival time
        self.ready_queue.sort(key=lambda x: x.arrival_time)

        # If ready queue is empty, return None
        if not self.ready_queue:
            return None

        # Get the next process from the ready queue
        next_process = self.ready_queue.pop(0)
        
        # If this is the first time the process is being executed
        if next_process.start_time is None:
            next_process.start_time = self.current_time
            self.update_gantt_chart(next_process, self.current_time, 
                                  self.current_time + next_process.remaining_time)

        return next_process

    def step(self, time_interval: float = 1.0) -> bool:
        """Execute one step of the scheduling algorithm"""
        # Update current time
        self.current_time += time_interval

        # Get next process to execute
        self.current_process = self.next_process()

        # If no process is available, return False
        if self.current_process is None:
            return False

        # Execute the current process
        completed = self.execute_process(time_interval)

        # Update Gantt chart if process is completed
        if completed:
            self.update_gantt_chart(self.current_process, 
                                  self.current_process.start_time,
                                  self.current_process.completion_time)

        return True 