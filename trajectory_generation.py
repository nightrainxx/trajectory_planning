# src/trajectory_generation.py
import numpy as np


def generate_trajectory(path, vehicle_model, dt):
    """生成车辆轨迹。"""
    trajectory = []
    current_state = (0, 0, 0, 0)  # 初始状态 (x, y, yaw, velocity)
    #  你应该根据你的车辆模型初始状态进行修改

    for i in range(len(path) - 1):
        current_node = path[i]
        next_node = path[i + 1]

        # 计算控制输入 (方向盘角和加速度)
        #  这里使用简单的线性插值，你应该根据你的车辆模型改进
        dx = next_node[0] - current_node[0]
        dy = next_node[1] - current_node[1]
        dist = np.sqrt(dx ** 2 + dy ** 2)
        # 计算时间
        time_to_reach = dist / vehicle_model.max_velocity

        # 计算转向角
        steering_angle = np.arctan2(dy, dx)

        # 计算加速度 (考虑时间)
        # (这里可能需要更精确的加速度计算)
        acceleration = dist / (time_to_reach * dt)

        control_inputs = (steering_angle, acceleration)

        # 更新车辆状态
        next_state = vehicle_model.update(current_state, control_inputs, dt)
        trajectory.append(next_state)
        current_state = next_state

    return trajectory