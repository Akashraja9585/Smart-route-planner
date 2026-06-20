# Smart Route Planner 🗺️

An interactive route-planning visualizer that finds the shortest path between cities using Dijkstra's algorithm. Built this to get hands-on practice with graph algorithms and visualize how shortest-path finding actually works step by step.

## What it does

- Click any city to set it as the start point
- Click another city to set it as the destination
- Instantly visualizes the shortest path using Dijkstra's algorithm
- Shows total distance and the exact route taken
- Press R to reset and try different routes

## Tech used

- Python
- Pygame (for visualization)
- heapq (priority queue for Dijkstra's algorithm)

## Getting started

Clone the repo and install dependencies:

    git clone https://github.com/Akashraja9585/smart-route-planner.git
    cd smart-route-planner
    pip install pygame

Run it:

    python main.py

## How it works

The cities and roads are represented as a graph (adjacency list), where each city is a node and each road is a weighted edge (distance in km). Dijkstra's algorithm uses a priority queue (min-heap) to always explore the closest unvisited city first, guaranteeing the shortest path is found.

    Graph = { city: [(neighbor, distance), ...] }

## What I learned

This was my first time implementing a graph algorithm from scratch instead of just using a library. Understanding how a priority queue (heap) helps Dijkstra's algorithm always pick the next closest node was the most important concept I learned.

Visualizing the algorithm helped me understand why Dijkstra's algorithm explores nodes in increasing order of distance, and why it doesn't work correctly with negative edge weights.

## Future improvements

- Add A* algorithm for comparison with Dijkstra
- Allow users to add their own custom cities and roads
- Show real-time algorithm steps (which node is being processed)
- Add real-world map coordinates using an API

## License

MIT
