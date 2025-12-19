# Autonomous Mop Robot Simulation using DFS Algorithm
## 🚀 Features
- **Depth-First Search:** goes deep into one path until it reaches a deadend and then backtracks to find another path.
- **Systematic Coverage:** uses a non-optimal deep clean to reach 100% floor coverage.
- **Output Visualization:** Visual demonstration of the "backtracking" logic, showing the robot moving to the furthest possible uncleaned point before returning.

## 🧠 How it Works
The algorithm stores the cells of one path in a stack and explores until the maximum depth before going back to another. Which means that the robot keeps moving in one direction cleaning the cells in the way until it reaches a dead end or an obstacle then goes back the closest free cell and repeats the process.
