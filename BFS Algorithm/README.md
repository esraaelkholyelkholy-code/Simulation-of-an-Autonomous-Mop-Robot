# Autonomous Mop Robot Simulation using BFS Algorithm
## 🚀 Features
- **Breadth-First Search:** explores layer-by-layer to ensure the shortest possible path to the next cell.
- **Systematic Coverage:** Uses an uninformed layering pattern for 100% floor coverage.
- **Output Visualization:** Visual demonstration of the output (the cleaning process).

## 🧠 How it Works
The algorithm explores the environment level by level using a queue to store all free (uncleaned) cells. BFS enters a cell, dequeues it, marks it as entered (cleaned) and enqueues all the neighboring free (uncleaned) cells. It repeats the process until the queue is empty (the floor is completely cleaned). The goal is to find the shortest path to the first neighboring cell.
