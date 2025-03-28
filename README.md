# Energy-Efficient CPU Scheduling Simulator

A comprehensive simulator that visualizes and analyzes different CPU scheduling algorithms with a focus on energy efficiency.

## Features

- Multiple CPU scheduling algorithms:
  - Traditional: FCFS, SJF (Preemptive & Non-Preemptive), RR, Priority
  - Energy-Efficient: DVFS, DPM, EA-SJF, GRR, EA-EDF
- Interactive GUI with real-time visualization
- Process input panel for custom process creation
- Gantt chart visualization
- Power consumption graphs
- Performance metrics dashboard
- Detailed reports generation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/energy-efficient-cpu-scheduler.git
cd energy-efficient-cpu-scheduler
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the simulator:
```bash
python main.py
```

## Project Structure

```
energy-efficient-cpu-scheduler/
├── main.py                 # Main application entry point
├── gui/                    # GUI components
│   ├── __init__.py
│   ├── main_window.py     # Main application window
│   ├── process_panel.py   # Process input panel
│   └── visualization.py   # Visualization components
├── algorithms/            # Scheduling algorithms
│   ├── __init__.py
│   ├── traditional.py    # Traditional scheduling algorithms
│   └── energy_efficient.py # Energy-efficient algorithms
├── models/               # Data models
│   ├── __init__.py
│   ├── process.py       # Process class
│   └── scheduler.py     # Scheduler class
├── utils/               # Utility functions
│   ├── __init__.py
│   ├── metrics.py      # Performance metrics
│   └── report.py       # Report generation
└── tests/              # Unit tests
    └── __init__.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 