import pygame
from pygame.sprite import Sprite

class AlienBullet(Sprite):
    """管理外星人发射的子弹的类"""
    def __init__(self, ai_game, alien):
        """在外星人位置创建外星子弹对象"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.alien_bullet_color

        # 创建子弹矩形（向下发射）
        self.rect = pygame.Rect(
            0, 0, self.settings.alien_bullet_width, self.settings.alien_bullet_height
        )
        # 子弹位置对齐外星人底部中央
        self.rect.midbottom = alien.rect.midbottom

        # 存储小数位置
        self.y = float(self.rect.y)

    def update(self):
        """向下移动子弹"""
        self.y += self.settings.alien_bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """绘制外星子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)