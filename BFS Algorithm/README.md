# Autonomous Mop Robot Simulation using BFS Algorithm
## 🚀 Features
Uses level-by-level approach which prevents the robot from being trapped in a long path.

## 🧠 How it Works
The algorithm explores the environment level by level using a queue to store all free (uncleaned) cells. BFS enters a cell, dequeues it, marks it as entered (cleaned) and enqueues all the neighboring free (uncleaned) cells. It repeats the process until the queue is empty (the floor is completely cleaned). The goal is to find the shortest path to the first neighboring cell.
