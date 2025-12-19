# Autonomous Mop Robot Simulation using A* Search Algorithm

## 🚀 Features
- **A* Algorithm:** Handles local pathfinding and obstacle avoidance.
- **Systematic Coverage:** lawnmower patterns for 100% floor coverage.
- **Output Visualization:** Visual demonstration of the output (the cleaning process).

## 🧠 How it Works
The algorithm selects the nearest free (uncleaned) cell as the target and finds the most efficient path between it and the robot’s current position ,after cleaning it the algorithm is applied to the next nearest cell until the whole floor is completely cleaned using the cost function: f(n)=g(n)+h(n) 
