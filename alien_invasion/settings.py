class Settings:
    """存储游戏《Alien Invasion》的所有设置（含扩展功能）"""
    def __init__(self):
        """初始化游戏的静态设置"""
        # 屏幕设置
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        # 飞船设置
        self.ship_speed = 1.5
        self.ship_limit = 3

        # 玩家子弹设置
        self.bullet_speed = 3.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3

        # 外星子弹设置（扩展）
        self.alien_bullet_speed = 2.0
        self.alien_bullet_width = 5
        self.alien_bullet_height = 12
        self.alien_bullet_color = (255, 165, 0)  # 橙色
        self.alien_bullet_allowed = 5  # 同时存在的最大外星子弹数
        self.alien_fire_interval = 1000  # 发射间隔（毫秒）

        # 外星人设置
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1  # 1表示向右，-1表示向左

        # 护盾设置（扩展）
        self.shield_radius = 40  # 护盾半径（比飞船略大，飞船尺寸约60x40）
        self.shield_color = (0, 255, 255)  # 青色护盾（与蓝色飞船区分）
        self.shield_width = 3  # 护盾边框宽度（0为实心圆）

        # 游戏加速设置
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.alien_points = 50

        # 音效设置（扩展）
        self.shoot_sound_path = 'sounds/shoot.wav'
        self.explosion_sound_path = 'sounds/explosion.wav'
        self.bg_music_path = 'sounds/bg_music.mp3'
        self.sound_volume = 0.5  # 音量（0-1）

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0
        self.fleet_direction = 1
        self.alien_bullet_speed = 2.0  # 动态重置外星子弹速度

    def increase_speed(self):
        """提高速度设置和外星人分数"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_bullet_speed *= self.speedup_scale  # 外星子弹同步加速
        self.alien_points = int(self.alien_points * self.score_scale)