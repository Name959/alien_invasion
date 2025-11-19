import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # 加载飞船图像（保留原逻辑）
        try:
            self.image = pygame.image.load('images/ship.bmp').convert_alpha()
        except pygame.error as e:
            print(f"飞船图片加载失败: {e}")
            self.image = pygame.Surface((60, 40))
            self.image.fill((0, 0, 255))  # 蓝色飞船占位

        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False

        # 护盾相关属性（新增）
        self.has_shield = True  # 初始时拥有护盾
        self.shield_radius = self.settings.shield_radius
        self.shield_color = self.settings.shield_color
        self.shield_width = self.settings.shield_width

    def update(self):
        """更新飞船位置时，同步护盾位置（无需额外操作，护盾随飞船绘制）"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def draw_shield(self):
        """绘制环绕飞船的圆形护盾（仅当护盾存在时）"""
        if self.has_shield:
            # 护盾圆心与飞船中心对齐
            shield_center = (self.rect.centerx, self.rect.centery)
            pygame.draw.circle(
                self.screen,
                self.shield_color,
                shield_center,
                self.shield_radius,
                self.shield_width  # 0为实心圆，正数为边框宽度
            )

    def blitme(self):
        """绘制飞船 + 绘制护盾（护盾在飞船之上，视觉上环绕）"""
        self.screen.blit(self.image, self.rect)
        self.draw_shield()  # 先画飞船，再画护盾，确保护盾在飞船外侧

    def center_ship(self):
        """重置飞船位置时，同步重置护盾状态（游戏重新开始时恢复护盾）"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.has_shield = True  # 重置时恢复护盾

    def lose_shield(self):
        """消耗护盾（被击中时调用）"""
        self.has_shield = False