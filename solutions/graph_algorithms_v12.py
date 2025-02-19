#!/usr/bin/env python3
"""Graph Algorithm Implementations"""

from collections import deque, defaultdict

class Graph:
    """Graph representation using adjacency list"""
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        """Add edge to graph"""
        self.graph[u].append(v)

    def bfs(self, start):
        """Breadth-First Search"""
        visited = set()
        queue = deque([start])
        visited.add(start)
        result = []

        while queue:
            vertex = queue.popleft()
            result.append(vertex)

            for neighbor in self.graph[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return result

    def dfs(self, start, visited=None):
        """Depth-First Search"""
        if visited is None:
            visited = set()

        visited.add(start)
        result = [start]

        for neighbor in self.graph[start]:
            if neighbor not in visited:
                result.extend(self.dfs(neighbor, visited))

        return result

    def dijkstra(self, start):
        """Dijkstra's shortest path algorithm"""
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0
        visited = set()

        while len(visited) < len(self.graph):
            unvisited = {node: dist for node, dist in distances.items() if node not in visited}
            if not unvisited:
                break

            current = min(unvisited, key=unvisited.get)
            visited.add(current)

            for neighbor in self.graph[current]:
                distances[neighbor] = min(distances[neighbor], distances[current] + 1)

        return distances

if __name__ == "__main__":
    g = Graph()
    edges = [(0, 1), (0, 2), (1, 2), (2, 0), (2, 3), (3, 3)]

    for u, v in edges:
        g.add_edge(u, v)

    print(f"BFS: {g.bfs(2)}")
    print(f"DFS: {g.dfs(2)}")
    print(f"Dijkstra: {g.dijkstra(0)}")
