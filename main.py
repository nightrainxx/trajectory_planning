# src/main.py
import numpy as np
import rasterio
import geopandas as gpd
import yaml
import matplotlib.pyplot as plt

from data_io import load_data
from costmap import calculate_cost_map
from path_planning import AStarPlanner
from vehicle_model import BicycleModel
from trajectory_generation import generate_trajectory
from visualization import visualize_cost_map, visualize_path, visualize_trajectory

def get_pixel_coords(lat, lon, transform, shape):  # 辅助函数
    """将经纬度转换为像素坐标。"""
    row, col = rasterio.transform.rowcol(transform, lon, lat)
    if row < 0 or row >= shape[0] or col < 0 or col >= shape[1]:
      print(f"Warning: Goal location {lon}, {lat} outside image bounds. Using closest point.")
      row = max(0, min(row, shape[0]-1))
      col = max(0, min(col, shape[1]-1))

    return int(row), int(col)

def main():
    with open("config.yaml", 'r') as f:
        config = yaml.safe_load(f)
    try:
        dem_utm, transform_utm, crs_utm, roads_raster, resolution, bounds_utm, shape = load_data(config["dem_file"], config["road_file"], config["target_epsg"])

        # 计算代价地图
        cost_map = calculate_cost_map(dem_utm, roads_raster, resolution, config)

        # 路径规划
        planner = AStarPlanner(cost_map, resolution)
        start_row, start_col = 0, 0  # 确保 (x, y) 形式
        # 自动获取目标坐标 (重要改进)
        goal_row, goal_col = 0, 0  # 默认值为0,0，你需要根据实际情况修改
        if config.get("goal_latlon"): #尝试从配置文件中读取目标经纬度
          goal_lat, goal_lon = config["goal_latlon"]
          goal_row, goal_col = get_pixel_coords(goal_lat, goal_lon, transform_utm, shape)

        path = planner.plan((start_row, start_col), (goal_row, goal_col))

        if path is None:
            print("No path found.")
            return

        # 车辆模型初始化
        vehicle = BicycleModel(config["wheelbase"], config["max_steer_angle"], config["max_velocity"])

        # 生成轨迹
        dt = config['dt']
        trajectory = generate_trajectory(path, vehicle, dt)

        # 可视化结果
        extent = bounds_utm #将extent替换为实际的范围
        visualize_cost_map(cost_map, resolution, extent)
        visualize_path(path, cost_map, resolution, extent)
        visualize_trajectory(trajectory, resolution, extent)

    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()