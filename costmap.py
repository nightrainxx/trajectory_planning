# src/costmap.py
import numpy as np
from rasterio.terrain import slope, aspect
from scipy.ndimage import gaussian_filter

def calculate_cost_map(dem, roads_raster, resolution, config):
    """计算代价地图。"""

    # 坡度和坡向计算
    slope_rad = slope(dem, resolution, resolution)  # 坡度（弧度）
    slope_deg = np.rad2deg(slope_rad)
    aspect_rad = aspect(dem, resolution, resolution)  # 坡向（弧度）


    # 初始化代价地图
    cost_map = np.zeros_like(dem, dtype=float)

    # 道路代价
    cost_map[roads_raster > 0] = config["road_cost"]

    # 坡度代价
    slope_cost = slope_deg * config["slope_cost_factor"]
    cost_map[slope_deg > config["max_slope"]] = config["unpassable_cost"]  # 不可通行区域代价
    cost_map[slope_deg <= config["max_slope"]] = slope_cost[slope_deg <= config["max_slope"]]


    # 高斯平滑 (可选)
    if config["smooth_costmap"]:
        cost_map = gaussian_filter(cost_map, sigma=config["smooth_sigma"])

    return cost_map