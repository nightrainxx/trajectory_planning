# src/path_planning.py
import numpy as np
import heapq

class AStarPlanner:
    def __init__(self, cost_map, resolution):
        self.cost_map = cost_map
        self.resolution = resolution
        self.rows, self.cols = cost_map.shape

    def heuristic(self, a, b):
        """启发式函数 (曼哈顿距离)."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, node):
        """获取节点的邻居节点."""
        row, col = node
        neighbors = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                neighbors.append((new_row, new_col))
        return neighbors

    def plan(self, start, goal):
        """A* 算法路径规划."""
        start_node = (start[0], start[1])
        goal_node = (goal[1], goal[0])  # 调整目标坐标

        open_set = [(self.heuristic(start_node, goal_node), 0, start_node, [])]  # (f, g, node, path)
        came_from = {}
        g_score = {start_node: 0}
        f_score = {start_node: self.heuristic(start_node, goal_node)}

        while open_set:
            _, current_g, current_node, current_path = heapq.heappop(open_set)

            if current_node == goal_node:
                return current_path + [current_node]

            for neighbor in self.get_neighbors(current_node):
                tentative_g_score = current_g + self.cost_map[neighbor[0], neighbor[1]]
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal_node)
                    heapq.heappush(open_set, (f_score[neighbor], tentative_g_score, neighbor, current_path + [current_node]))

        return None