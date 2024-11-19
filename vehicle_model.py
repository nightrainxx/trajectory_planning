# src/vehicle_model.py
import numpy as np

class BicycleModel:
    def __init__(self, wheelbase, max_steer_angle, max_velocity):
        self.wheelbase = wheelbase
        self.max_steer_angle = max_steer_angle
        self.max_velocity = max_velocity

    def update(self, current_state, control_inputs, dt):
        """更新车辆状态。"""
        x, y, yaw, velocity = current_state
        steering_angle, acceleration = control_inputs

        # 限制转向角度
        steering_angle = np.clip(steering_angle, -self.max_steer_angle, self.max_steer_angle)

        # 限制速度
        velocity = np.clip(velocity + acceleration * dt, 0, self.max_velocity)


        # 使用自行车模型的运动学方程来更新状态
        #  (这是一个简化的自行车模型，实际应用中可能有更复杂的模型)
        delta_yaw = (velocity / self.wheelbase) * np.tan(steering_angle) * dt
        delta_x = velocity * np.cos(yaw) * dt
        delta_y = velocity * np.sin(yaw) * dt
        yaw += delta_yaw
        x += delta_x
        y += delta_y

        return (x, y, yaw, velocity)