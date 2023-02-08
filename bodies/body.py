# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人
# date            :2023-01-22
# notes           :
# python_version  :3.8
# ==============================================================================
import json
import numpy as np
import math
from common.consts import AU


class Body:
    def __init__(self, name, mass, init_position, init_velocity,
                 density=5e3, color=(125 / 255, 125 / 255, 125 / 255),
                 texture=None, size_scale=1.0, distance_scale=1.0):
        """
        天体类
        :param name: 天体名称
        :param mass: 天体质量 (kg)
        :param init_position: 初始位置 (km)
        :param init_velocity: 初始速度 (km/s)
        :param density: 平均密度 (kg/m³)
        :param color: 天体颜色（纹理图片优先）
        :param texture: 纹理图片
        :param size_scale: 尺寸缩放
        :param distance_scale: 距离缩放
        """
        self.__his_pos = []
        self.__his_vel = []
        self.__his_acc = []
        self.__his_reserved_num = 100

        self.name = name
        self.__mass = mass

        self.init_position = np.array(init_position, dtype='float32')
        self.init_velocity = np.array(init_velocity, dtype='float32')

        self.__position = self.init_position
        self.__velocity = self.init_velocity

        self.__density = density

        self.color = color
        self.texture = texture

        self.size_scale = size_scale
        self.distance_scale = distance_scale

        # 初始化后，加速度为0，只有多个天体的引力才会影响到加速度
        # m/s²
        self.__acceleration = np.array([0, 0, 0], dtype='float32')
        self.__record_history()

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value
        self.__record_history()

    @property
    def acceleration(self):
        return self.__acceleration

    @acceleration.setter
    def acceleration(self, value):
        self.__acceleration = value
        self.__record_history()

    @property
    def velocity(self):
        return self.__velocity

    @velocity.setter
    def velocity(self, value):
        self.__velocity = value
        self.__record_history()

    def __append_history(self, his_list, data):
        """

        :param his_list:
        :param data:
        :return:
        """
        # 如果历史记录为0 或者 新增数据和最后的历史数据不相同，则添加
        if len(his_list) == 0 or \
                np.sum(data == his_list[-1]) < len(data):
            his_list.append(data.copy())

    def __record_history(self):
        """
        记录历史
        :return:
        """
        # 如果历史记录数超过了保留数量，则截断，只保留 __his_reserved_num 数量的历史
        if len(self.__his_pos) > self.__his_reserved_num:
            self.__his_pos = self.__his_pos[len(self.__his_pos) - self.__his_reserved_num:]
            self.__his_vel = self.__his_vel[len(self.__his_vel) - self.__his_reserved_num:]
            self.__his_acc = self.__his_acc[len(self.__his_acc) - self.__his_reserved_num:]

        # 追加历史记录(位置、速度、加速度)
        self.__append_history(self.__his_pos, self.position)
        self.__append_history(self.__his_vel, self.velocity)
        self.__append_history(self.__his_acc, self.acceleration)
        # print(self.name, "his pos->", self.__his_pos)

    def his_position(self):
        """
        历史位置
        :return:
        """
        return self.__his_pos

    def his_velocity(self):
        """
        历史瞬时速度
        :return:
        """
        return self.__his_vel

    def his_acceleration(self):
        """
        历史瞬时加速度
        :return:
        """
        return self.__his_acc

    @property
    def mass(self):
        """
        天体质量 (kg)
        :return:
        """
        return self.__mass

    @property
    def density(self):
        """
        平均密度 (kg/m³)
        :return:
        """
        return self.__density

    @property
    def volume(self):
        """
        天体的体积
        """
        # v = m/ρ
        # 体积(m³) = 质量(kg) / 密度(kg/m³)
        v = self.mass / self.density
        return v

    @property
    def raduis(self):
        """
        天体的半径
        :return:
        """
        # V = ⁴⁄₃πr³  -> r = pow((3V)/(4π),1/3)
        return pow(3 * self.volume / (4 * math.pi), 1 / 3)

    @property
    def diameter(self):
        """
        天体的直径
        :return:
        """
        return self.raduis * 2

    def __repr__(self):
        return '<%s> m=%.3e(kg), r=%.3e(km), p=[%.3e,%.3e,%.3e](km), v=%s(km/s)' % \
               (self.name, self.mass, self.raduis,
                self.position[0], self.position[1], self.position[2], self.velocity)

    def position_au(self):
        pos = self.position
        pos_au = pos / AU
        return pos_au

    def change_velocity(self, dv):
        self.velocity += dv

    def move(self, dt):
        self.position += self.velocity * dt

    def reset(self):
        self.position = self.init_position
        self.velocity = self.init_velocity

    def kinetic_energy(self):
        """
        计算动能(千焦耳)
        表示动能，单位为焦耳j，m为质量，单位为千克，v为速度，单位为米/秒。
        ek=(1/2).m.v^2
        m(kg) v(m/s) -> j
        m(kg) v(km/s) -> kj
        """
        v = self.velocity
        return 0.5 * self.mass * (v[0] ** 2 + v[1] ** 2 + v[2] ** 2)

    @staticmethod
    def build_bodies_from_json(json_file):
        bodies = []
        with open(json_file, "r") as read_content:
            json_data = json.load(read_content)
            for body_data in json_data["bodies"]:
                # print(body_data)
                body = Body(**body_data)
                bodies.append(body)
                # print(body.position_au())
        return bodies


if __name__ == '__main__':
    # build_bodies_from_json('../data/sun.json')
    bodies = Body.build_bodies_from_json('../data/sun_earth.json')
    # 太阳半径 / 地球半径
    print(bodies[0].raduis / bodies[1].raduis)
    for body in bodies:
        print(body.kinetic_energy())
