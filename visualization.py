# src/visualization.py
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from rasterio.plot import show


def visualize_cost_map(cost_map, resolution, extent, cmap='viridis'):
    """可视化代价地图。"""
    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.imshow(cost_map, cmap=cmap, aspect='auto', extent=extent)
    fig.colorbar(im, ax=ax)
    ax.set_title('代价地图')
    plt.show()


def visualize_path(path, cost_map, resolution, extent):
    """可视化路径。"""
    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.imshow(cost_map, cmap='gray', aspect='auto', extent=extent)  # 显示代价地图
    fig.colorbar(im, ax=ax)

    path_x = [point[0] for point in path]
    path_y = [point[1] for point in path]

    ax.plot(path_x, path_y, 'r-', linewidth=2)  # 绘制路径
    ax.set_title('路径')
    plt.show()


def visualize_trajectory(trajectory, resolution, extent):
    """可视化轨迹。"""
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(np.zeros_like(cost_map), cmap='gray', extent=extent, aspect='auto')  # 使用0矩阵填充

    trajectory_x = [point[0] for point in trajectory]
    trajectory_y = [point[1] for point in trajectory]
    ax.plot(trajectory_x, trajectory_y, 'g-', linewidth=2)  # 绘制轨迹
    ax.set_title('轨迹')
    plt.show()