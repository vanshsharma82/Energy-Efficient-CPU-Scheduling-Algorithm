import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from typing import List, Dict
import numpy as np
from models.process import Process
from algorithms.traditional import FCFS

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Energy-Efficient CPU Scheduling Simulator")
        self.root.geometry("1200x800")
        
        # Configure root window to be resizable
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        
        # Initialize scheduler
        self.scheduler = FCFS()
        self.processes: List[Process] = []
        self.current_pid = 1
        
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the main GUI components"""
        # Create main container with scrollbar
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky='nsew')
        
        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical")
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Create canvas for scrolling
        self.scroll_canvas = tk.Canvas(self.main_frame, yscrollcommand=self.scrollbar.set)
        self.scroll_canvas.grid(row=0, column=0, sticky='nsew')
        
        # Configure scrollbar
        self.scrollbar.configure(command=self.scroll_canvas.yview)
        
        # Create main container frame inside canvas
        self.main_container = ttk.Frame(self.scroll_canvas, padding="10")
        
        # Create window in canvas
        self.canvas_frame = self.scroll_canvas.create_window((0, 0), window=self.main_container, anchor='nw')
        
        # Configure main_frame grid
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        
        # Process Input Panel
        self.setup_process_panel()
        
        # Visualization Panel
        self.setup_visualization_panel()
        
        # Control Panel
        self.setup_control_panel()
        
        # Metrics Panel
        self.setup_metrics_panel()
        
        # Bind resize event
        self.scroll_canvas.bind('<Configure>', self.on_canvas_configure)
        self.main_container.bind('<Configure>', self.on_frame_configure)
        
        # Bind mouse wheel
        self.scroll_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.scroll_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def on_canvas_configure(self, event):
        """Handle canvas resize"""
        self.scroll_canvas.itemconfig(self.canvas_frame, width=event.width)
        
    def on_frame_configure(self, event=None):
        """Reset the scroll region to encompass the inner frame"""
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
        
    def setup_process_panel(self):
        """Setup the process input panel"""
        process_frame = ttk.LabelFrame(self.main_container, text="Process Input", padding="5")
        process_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Process input fields
        ttk.Label(process_frame, text="Arrival Time:").grid(row=0, column=0, padx=5)
        self.arrival_time = ttk.Entry(process_frame, width=10)
        self.arrival_time.grid(row=0, column=1, padx=5)
        
        ttk.Label(process_frame, text="Burst Time:").grid(row=0, column=2, padx=5)
        self.burst_time = ttk.Entry(process_frame, width=10)
        self.burst_time.grid(row=0, column=3, padx=5)
        
        ttk.Label(process_frame, text="Priority:").grid(row=0, column=4, padx=5)
        self.priority = ttk.Entry(process_frame, width=10)
        self.priority.grid(row=0, column=5, padx=5)
        
        # Add process button
        ttk.Button(process_frame, text="Add Process", 
                  command=self.add_process).grid(row=0, column=6, padx=5)
        
        # Process list with scrollbar
        process_list_frame = ttk.Frame(process_frame)
        process_list_frame.grid(row=1, column=0, columnspan=7, sticky=(tk.W, tk.E), pady=5)
        
        # Add scrollbar to process list
        process_scroll = ttk.Scrollbar(process_list_frame)
        process_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.process_list = ttk.Treeview(process_list_frame, columns=("PID", "AT", "BT", "Priority"), 
                                       show="headings", height=5,
                                       yscrollcommand=process_scroll.set)
        self.process_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        process_scroll.config(command=self.process_list.yview)
        
        # Configure columns
        self.process_list.heading("PID", text="PID")
        self.process_list.heading("AT", text="Arrival Time")
        self.process_list.heading("BT", text="Burst Time")
        self.process_list.heading("Priority", text="Priority")
        
    def setup_visualization_panel(self):
        """Setup the visualization panel with Gantt chart and energy consumption graph"""
        viz_frame = ttk.LabelFrame(self.main_container, text="Visualization", padding="5")
        viz_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(10, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Create subplots
        self.gantt_ax = self.fig.add_subplot(211)
        self.energy_ax = self.fig.add_subplot(212)
        
    def setup_control_panel(self):
        """Setup the control panel with simulation controls"""
        control_frame = ttk.LabelFrame(self.main_container, text="Controls", padding="5")
        control_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Algorithm selection
        ttk.Label(control_frame, text="Algorithm:").grid(row=0, column=0, padx=5)
        self.algorithm_var = tk.StringVar(value="FCFS")
        algorithms = ["FCFS", "SJF", "Priority", "Round Robin", "DVFS"]
        self.algorithm_combo = ttk.Combobox(control_frame, textvariable=self.algorithm_var, 
                                          values=algorithms)
        self.algorithm_combo.grid(row=0, column=1, padx=5)
        
        # Simulation controls
        ttk.Button(control_frame, text="Start", 
                  command=self.start_simulation).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="Step", 
                  command=self.step_simulation).grid(row=0, column=3, padx=5)
        ttk.Button(control_frame, text="Reset", 
                  command=self.reset_simulation).grid(row=0, column=4, padx=5)
        
    def setup_metrics_panel(self):
        """Setup the metrics panel to display performance metrics"""
        metrics_frame = ttk.LabelFrame(self.main_container, text="Performance Metrics", padding="5")
        metrics_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Create labels for metrics
        self.metrics_labels = {}
        metrics = ["Average Waiting Time", "Average Turnaround Time", 
                  "CPU Utilization", "Total Energy Consumption"]
        
        for i, metric in enumerate(metrics):
            ttk.Label(metrics_frame, text=f"{metric}:").grid(row=i, column=0, padx=5)
            self.metrics_labels[metric] = ttk.Label(metrics_frame, text="0.0")
            self.metrics_labels[metric].grid(row=i, column=1, padx=5)
            
    def add_process(self):
        """Add a new process to the scheduler"""
        try:
            at = float(self.arrival_time.get())
            bt = float(self.burst_time.get())
            priority = int(self.priority.get())
            
            process = Process(self.current_pid, at, bt, priority)
            self.processes.append(process)
            self.scheduler.add_process(process)
            
            # Add to process list
            self.process_list.insert("", "end", values=(self.current_pid, at, bt, priority))
            
            # Clear input fields
            self.arrival_time.delete(0, tk.END)
            self.burst_time.delete(0, tk.END)
            self.priority.delete(0, tk.END)
            
            self.current_pid += 1
            messagebox.showinfo("Success", "Process added successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values!")
            
    def update_visualization(self):
        """Update the Gantt chart and energy consumption graph"""
        # Clear previous plots
        self.gantt_ax.clear()
        self.energy_ax.clear()
        
        # Plot Gantt chart
        if self.scheduler.gantt_chart:
            for pid, start, end in self.scheduler.gantt_chart:
                self.gantt_ax.broken_barh([(start, end-start)], (0, 1), 
                                        facecolors=f'C{pid % 10}')
                self.gantt_ax.text((start + end) / 2, 0.5, f'P{pid}', 
                                 ha='center', va='center')
        
        self.gantt_ax.set_title("Gantt Chart")
        self.gantt_ax.set_xlabel("Time")
        self.gantt_ax.set_ylim(0, 1)
        
        # Plot energy consumption
        if self.processes:
            energy_data = [p.energy_consumption for p in self.processes]
            self.energy_ax.bar(range(len(energy_data)), energy_data)
            self.energy_ax.set_title("Energy Consumption per Process")
            self.energy_ax.set_xlabel("Process ID")
            self.energy_ax.set_ylabel("Energy Consumption")
            
        self.canvas.draw()
        
    def update_metrics(self):
        """Update the performance metrics display"""
        metrics = self.scheduler.get_metrics()
        
        self.metrics_labels["Average Waiting Time"].config(
            text=f"{metrics['avg_waiting_time']:.2f}")
        self.metrics_labels["Average Turnaround Time"].config(
            text=f"{metrics['avg_turnaround_time']:.2f}")
        self.metrics_labels["CPU Utilization"].config(
            text=f"{metrics['cpu_utilization']:.2f}%")
        self.metrics_labels["Total Energy Consumption"].config(
            text=f"{metrics['total_energy_consumption']:.2f}")
        
    def start_simulation(self):
        """Start the simulation"""
        if not self.processes:
            messagebox.showerror("Error", "No processes to simulate!")
            return
            
        self.scheduler.reset()
        self.scheduler.add_processes(self.processes)
        self.step_simulation()
        
    def step_simulation(self):
        """Execute one step of the simulation"""
        if self.scheduler.is_complete():
            messagebox.showinfo("Complete", "Simulation completed!")
            return
            
        self.scheduler.step()
        self.update_visualization()
        self.update_metrics()
        
    def reset_simulation(self):
        """Reset the simulation"""
        self.scheduler.reset()
        self.update_visualization()
        self.update_metrics()
        messagebox.showinfo("Reset", "Simulation reset successfully!") 