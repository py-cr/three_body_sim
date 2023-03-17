# -*- coding:utf-8 -*-
# title           :ursina天体运行模拟器UI控制
# description     :ursina天体运行模拟器UI控制
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from ursina import Ursina, window, Entity, Grid, Mesh, camera, Text, application, color, mouse, Vec2, Vec3, \
    load_texture, held_keys, Button, ButtonList, destroy
from ursina.prefabs.first_person_controller import FirstPersonController

from simulators.ursina.ui_component import UiSlider, SwithButton, UiButton
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent
from ursina import WindowPanel, InputField, Button, Slider, ButtonGroup, Panel


class UrsinaUI:

    def ui_component_init(self):

        self.start_button_text = "●"  # 》●▲○◎
        self.pause_button_text = "〓"  # 〓 || ‖
        self.no_trail_button_text = "○ "
        self.trail_button_text = "○--"

        application.time_scale = 0.5
        self.slider_body_spin_factor = UiSlider(text='自转速度', min=0.01, max=30, default=1)
        self.slider_body_size_factor = UiSlider(text='天体缩放', min=0.01, max=10, default=1)
        self.slider_run_speed_factor = UiSlider(text="运行速度", min=0.01, max=800, default=1)
        self.slider_control_speed_factor = UiSlider(text="控制速度", min=0.01, max=30, default=application.time_scale)
        self.slider_trail_length = UiSlider(text="拖尾长度", min=30, max=500, default=UrsinaConfig.trail_length)

        self.slider_body_size_factor.on_value_changed = self.on_slider_body_size_changed
        self.slider_body_spin_factor.on_value_changed = self.on_slider_body_spin_changed
        self.slider_run_speed_factor.on_value_changed = self.on_slider_run_speed_changed
        self.slider_control_speed_factor.on_value_changed = self.on_slider_control_speed_changed
        self.slider_trail_length.on_value_changed = self.on_slider_trail_length_changed

        self.on_off_switch = SwithButton((self.pause_button_text,
                                          self.start_button_text),
                                         default=self.start_button_text,
                                         tooltips=('暂停', '运行'))
        self.on_off_switch.selected_color = color.red

        self.sec_per_time_switch = SwithButton(("默认", "天", "周", "月", "年", "十年", "百年"),
                                               default="默认",
                                               tooltips=("系统默认", "每秒相当于1天", "每秒相当于1周",
                                                         "每秒相当于1个月",
                                                         "每秒相当于1年", "每秒相当于十年", "每秒相当于1百年"))

        self.on_off_trail = SwithButton((self.no_trail_button_text, self.trail_button_text),
                                        default=self.no_trail_button_text,
                                        tooltips=('天体运行无轨迹', '天体运行有拖尾轨迹'))
        self.on_off_trail.on_value_changed = self.on_off_trail_changed

        self.point_button = UiButton(text='寻找', on_click=self.on_searching_bodies_click)
        self.reset_button = UiButton(text='重置', on_click=self.on_reset_button_click)

        # button1 = Button(text='Button 1', scale=(0.1, 0.1), position=(-0.1, 0))
        # button2 = Button(text='Button 2', scale=(0.1, 0.1), position=(0.1, 0))

        # btn_settings = UiButton(text='操作设置', on_click=self.on_point_button_click)
        # btn_settings.position = window.top_left
        # btn_settings.y = 0.5
        # # btn_settings.scale = (0.1,0.1)
        # # btn_settings.y = 0
        # btn_settings.scale = (.25, .025),
        # btn_settings.origin = (-.5, .5),
        # btn_settings.pressed_scale = 1,
        # if btn_settings.text_entity:
        #     btn_settings.text_entity.x = .05
        #     btn_settings.text_entity.origin = (-.5, 0)
        #     btn_settings.text_entity.scale *= .8

        self.on_off_switch.on_value_changed = self.on_off_switch_changed
        wp = WindowPanel(
            title='',
            content=(
                Text('方位控制: Q W E A S D + 鼠标右键', font='msyhl.ttc'),
                # InputField(name='name_field'),
                # Button(text='Submit', color=color.azure),
                self.point_button,
                self.reset_button,
                self.sec_per_time_switch,
                self.on_off_switch,
                self.on_off_trail,
                self.slider_trail_length,
                self.slider_body_size_factor,
                self.slider_body_spin_factor,
                self.slider_run_speed_factor,
                self.slider_control_speed_factor

            ), ignore_paused=True, color=color.rgba(0.0, 0.0, 0.0, 0.5)  # , popup=True
        )
        self.sec_per_time_switch.x = -0.5
        self.on_off_switch.x = -0.2
        self.on_off_trail.x = -0.2
        wp.y = 0.5  # wp.panel.scale_y / 2 * wp.scale_y  # center the window panel
        wp.x = 0.6  # wp.scale_x + 0.1
        # wp.x = 0#wp.panel.scale_x / 2 * wp.scale_x
        self.wp = wp
        self.wp.enabled = False

    def __init__(self):
        self.ui_component_init()

        self.settings_handler = Entity(ignore_paused=True)
        # 加载中文字体文件

        # text_time_scale = "1"
        # self.text_time_scale_info = None
        self.settings_handler.input = self.settings_handler_input
        # self.show_text_time_scale_info()
        key_info_str = "按[空格]设置"
        key_info = Text(text=key_info_str, font=UrsinaConfig.CN_FONT, position=(-0.5, 0.5), origin=(-1, 1),
                        background=True)
        # # self.show_button()
        # slider_text = Text(text='自转速度', scale=1, position=(-0.6, 0.3))
        # slider = Slider(scale=0.5, position=(-0.6, 0), min=0, max=10, step=1, text=slider_text)

    def on_off_trail_changed(self):
        if self.on_off_trail.value == self.trail_button_text:
            UrsinaConfig.show_trail = True
        else:
            UrsinaConfig.show_trail = False

    def bodies_button_list_click(self, item):
        if item is not None:
            print("select->", item)

        destroy(self.bodies_button_list)

    def on_searching_bodies_click(self):
        results = UrsinaEvent.on_searching_bodies()
        if len(results) > 0:
            sub_name, bodies = results[0]
            # print(results[0])
            button_dict = {"[关闭]": lambda: self.bodies_button_list_click(None)}

            for body in bodies:
                def callback_action(b=body):
                    self.bodies_button_list_click(b)

                button_dict[body.name] = callback_action

            self.bodies_button_list = ButtonList(button_dict, font=UrsinaConfig.CN_FONT, button_height=1.5)
            # self.bodies_button_list.input = self.bodies_button_list_input

    def on_reset_button_click(self):
        UrsinaEvent.on_reset()

    def on_off_switch_changed(self):
        if self.on_off_switch.value == self.pause_button_text:
            self.on_off_switch.selected_color = color.green
            application.paused = True
            for c in self.wp.children:
                if not c.ignore_paused:
                    # c.enabled = True
                    c.disabled = False
        else:
            self.on_off_switch.selected_color = color.red
            application.paused = False
            for c in self.wp.children:
                if not c.ignore_paused:
                    # c.enabled = True
                    c.disabled = False

    def on_slider_trail_length_changed(self):
        UrsinaConfig.trail_length = int(self.slider_trail_length.value)

    def on_slider_control_speed_changed(self):
        application.time_scale = self.slider_control_speed_factor.value

    def on_slider_body_spin_changed(self):
        UrsinaConfig.body_spin_factor = self.slider_body_spin_factor.value

    def on_slider_body_size_changed(self):
        UrsinaConfig.body_size_factor = self.slider_body_size_factor.value

    def on_slider_run_speed_changed(self):
        UrsinaConfig.run_speed_factor = self.slider_run_speed_factor.value

    def show_text_time_scale_info(self):
        if self.text_time_scale_info is not None:
            self.text_time_scale_info.disable()
        text_time_scale = "控制倍率:" + str(application.time_scale).ljust(4, " ")
        text_time_scale_info = Text(text=text_time_scale, position=(-0.8, 0.5), origin=(-1, 1), background=True)

    # def show_button(self):
    #     b = Button(scale=(0, .25), text='zzz')

    #  if key == "escape":
    #             if mouse.locked:
    #                 self.on_disable()
    #             else:
    #                 sys.exit()

    # 按空格键则暂停
    def settings_handler_input(self, key):
        import sys
        if key == "escape":
            sys.exit()
        # print(key)
        elif key == 'space':
            self.wp.enabled = not self.wp.enabled
        #     application.paused = not application.paused  # Pause/unpause the game.
        # elif key == 'tab':
        #     # application.time_scale 属性控制游戏时间流逝的速度。
        #     # 具体来说，它是一个浮点数，用于调整游戏时间流逝速度的比例，其默认值为 1.0，表示正常速度。
        #     # 当你将它设置为小于 1.0 的值时，游戏时间会变慢，而设置为大于 1.0 的值时，游戏时间则会变快。
        #     for idx, time_scale in enumerate(time_scales):
        #         if float(application.time_scale) == time_scale:
        #             if idx < len(time_scales) - 1:
        #                 application.time_scale = time_scales[idx + 1]
        #                 break
        #             else:
        #                 application.time_scale = time_scales[0]
        # elif key == '+':
        #     UrsinaConfig.run_speed_factor *= 2
        # elif key == "= up":
        #     UrsinaConfig.body_spin_factor *= 2
        #     # if application.time_scale in time_scales:
        #     #     idx = time_scales.index(application.time_scale)
        #     #     if idx < len(time_scales) - 1:
        #     #         application.time_scale = time_scales[idx + 1]
        # elif key == '-':
        #     UrsinaConfig.run_speed_factor *= 0.5
        # elif key == "- up":
        #     UrsinaConfig.body_spin_factor *= 0.5
        #     # if application.time_scale in time_scales:
        #     #     idx = time_scales.index(application.time_scale)
        #     #     if idx > 0:
        #     #         application.time_scale = time_scales[idx - 1]
        #
        # self.show_text_time_scale_info()
