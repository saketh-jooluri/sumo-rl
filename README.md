# SUMO RL - Traffic Signal Control with Reinforcement Learning

This project implements **Q-Learning agents** to optimize traffic signal control using the SUMO (Simulation of Urban Mobility) traffic simulator. The agents learn to make intelligent decisions about traffic light timing to reduce overall waiting times and improve traffic flow.

## 📋 Project Overview

The project explores reinforcement learning techniques for adaptive traffic signal control across two scenarios:
- **Single Intersection**: A basic intersection with one traffic light controlled by a Q-Learning agent
- **4x4 Grid**: A larger urban network with 16 intersections, each controlled by independent Q-Learning agents

## 📁 Project Structure

```
SUMO RL/
├── experiments/              # Training experiments
│   ├── ql_single-intersection.py    # Single intersection training script
│   └── ql_4x4grid.py               # 4x4 grid training script
├── outputs/                  # Results and analysis
│   ├── 4x4-plot.py          # Plotting utility for 4x4 results
│   ├── 4x4/                 # 4x4 grid experiment outputs (CSV files)
│   └── single-intersection/  # Single intersection outputs
├── sumo-rl/                 # SUMO network definitions and utilities
│   └── nets/                # Network files (.net.xml, .rou.xml)
└── README.md                # This file
```

## 🔧 Prerequisites

### Required Software
- **SUMO** (Simulation of Urban Mobility) - Version 1.8.0 or higher
- **Python** - Version 3.7 or higher
- **SUMO-RL Library** - Python package for SUMO reinforcement learning integration

### Environment Setup

1. **Install SUMO**: Download and install from https://sumo.dlr.de/docs/Downloads.php

2. **Set SUMO_HOME environment variable**:
   ```powershell
   $env:SUMO_HOME = "C:\Program Files (x86)\Eclipse\Sumo"  # Or your SUMO installation path
   ```
   Add this to your system environment variables permanently for persistent use.

3. **Install Python dependencies**:
   ```powershell
   pip install pandas sumo-rl
   ```

## 🚀 Usage

### Single Intersection Training

Train a Q-Learning agent on a single traffic intersection:

```powershell
python experiments/ql_single-intersection.py -runs 10 -s 100000 -a 0.1 -g 0.99 -e 0.05
```

**Available Arguments**:
- `-route`: Path to route definition XML file (default: `sumo_rl/nets/single-intersection/single-intersection.rou.xml`)
- `-a`: Alpha learning rate (default: 0.1)
- `-g`: Gamma discount rate (default: 0.99)
- `-e`: Initial epsilon for exploration (default: 0.05)
- `-me`: Minimum epsilon (default: 0.005)
- `-d`: Epsilon decay rate (default: 1.0)
- `-mingreen`: Minimum green light duration in seconds (default: 10)
- `-maxgreen`: Maximum green light duration in seconds (default: 50)
- `-s`: Total simulation seconds (default: 100000)
- `-runs`: Number of training runs (default: 1)
- `-gui`: Enable SUMO GUI visualization
- `-fixed`: Run with fixed timing (no learning)
- `-ns`: Fixed green time for North-South direction (default: 42)
- `-we`: Fixed green time for West-East direction (default: 42)
- `-v`: Print experience tuples during training

**Example with GUI**:
```powershell
python3 ./experiments/ql_single-intersection.py 
```

### 4x4 Grid Training

Train multiple Q-Learning agents on a 4x4 grid network:

```powershell
python3 ./experiments/ql_4x4grid.py
```

**Training Configuration** (edit in script):
- `alpha`: Learning rate (default: 0.1)
- `gamma`: Discount factor (default: 0.99)
- `decay`: Epsilon decay (default: 1)
- `runs`: Number of independent training runs (default: 30)
- `episodes`: Episodes per run (default: 4)

## 📊 Results and Analysis

### Output Format

Training results are saved as CSV files containing:
- `system_total_waiting_time`: Cumulative waiting time of all vehicles
- Per-intersection metrics and agent rewards
- Episode and run identifiers

### Plotting Results

Analyze the 4x4 grid results:

```powershell
python outputs/4x4-plot.py
```

This generates plots showing:
- Learning curves (waiting time vs. episode)
- Performance across multiple runs
- Convergence behavior of agents

## 🧠 Learning Algorithm

### Q-Learning Parameters

The agents use ε-greedy exploration with:
- **Learning Rate (α)**: Controls how quickly the agent updates its Q-values (typical: 0.1)
- **Discount Factor (γ)**: Balances immediate vs. future rewards (typical: 0.99)
- **Exploration Rate (ε)**: Probability of taking random actions (decays from 0.05 to 0.005)

### State and Action Space

- **State**: Current vehicle counts and queue lengths at the intersection
- **Actions**: Traffic signal phase transitions
- **Reward**: Negative of the waiting time (minimize wait)

## 📈 Expected Behavior

1. **Early episodes**: High exploration, suboptimal performance
2. **Mid episodes**: Gradual improvement as agents learn traffic patterns
3. **Late episodes**: Convergence to near-optimal policies with reduced waiting times

## 🐛 Troubleshooting

### "SUMO_HOME not set" Error
Ensure the SUMO_HOME environment variable is properly configured:
```powershell
$env:SUMO_HOME = "Your\SUMO\Installation\Path"
echo $env:SUMO_HOME  # Verify it's set
```


## 📚 Key Concepts

- **SUMO**: Open-source traffic simulation tool supporting agent-based modeling
- **Q-Learning**: Tabular reinforcement learning algorithm for finding optimal policies
- **ε-Greedy Exploration**: Balance between exploring random actions and exploiting learned knowledge
- **Multi-Agent RL**: Multiple independent agents operating in a shared environment


## 📝 Notes

- The agents learn independently; coordination emerges from local optimization
- Results may vary based on random initialization and traffic patterns
- For reproducible results, consider fixing random seeds
- Larger grids and longer training may require significant computation time


