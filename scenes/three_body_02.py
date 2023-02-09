# -*- coding:utf-8 -*-
# title           :太阳系场景
# description     :
# author          :Python超人
# date            :2023-01-22
# notes           :
# python_version  :3.8
# ==============================================================================
from mayavi import mlab
from bodies import Sun, Earth
from common.consts import SECONDS_PER_WEEK
from scenes.func import mayavi_run

if __name__ == '__main__':
    """
    3个太阳、1个地球（效果2）
    可以修改影响效果的参数为： 
    1、三个方向的初始位置 init_position[x, y, z]
    2、三个方向的初始速度 init_velocity[x, y, z]
    3、天体质量 mass    
    """
    bodies = [
        Sun(mass=1.5e30, init_position=[849597870.700, 0, 0], init_velocity=[0, 7.0, 0],
            size_scale=1e2, texture="sun1.jpg"),  # 太阳放大 100 倍
        Sun(mass=2e30, init_position=[0, 0, 249597870.700], init_velocity=[0, -8.0, 0],
            size_scale=1e2, texture="sun2.jpg"),  # 太阳放大 100 倍
        Sun(mass=2.5e30, init_position=[0, -849597870.700, 0], init_velocity=[8.0, 0, 0],
            size_scale=1e2, texture="sun2.jpg"),  # 太阳放大 100 倍

        Earth(init_position=[0, -349597870.700, 0], init_velocity=[15.50, 0, 0],
              size_scale=4e3, distance_scale=1),  # 地球放大 4000 倍，距离保持不变
    ]
    mayavi_run(bodies, SECONDS_PER_WEEK, view_azimuth=0)
