import pygame
from pygame.sprite import Sprite

class Shield(Sprite):
    """可破坏的护盾类（由多个小方块组成）"""
    def __init__(self, ai_game, x_position):
        """在指定x位置创建护盾"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.shield_color
        self.block_size = self.settings.shield_block_size

        # 护盾整体位置（屏幕下方，飞船上方）
        self.screen_rect = self.screen.get_rect()
        self.rect = pygame.Rect(
            x_position,
            self.screen_rect.bottom - 120,  # 距离屏幕底部120像素
            self.settings.shield_width,
            self.settings.shield_height
        )

        # 用二维列表存储护盾块（True表示块存在，False表示被破坏）
        self.blocks = []
        for y in range(0, self.settings.shield_height, self.block_size):
            row = []
            for x in range(0, self.settings.shield_width, self.block_size):
                row.append(True)
            self.blocks.append(row)

    def draw_shield(self):
        """绘制护盾（仅绘制存在的块）"""
        for row_idx, row in enumerate(self.blocks):
            for col_idx, exists in enumerate(row):
                if exists:
                    block_rect = pygame.Rect(
                        self.rect.x + col_idx * self.block_size,
                        self.rect.y + row_idx * self.block_size,
                        self.block_size - 1,  # 留1像素间隙
                        self.block_size - 1
                    )
                    pygame.draw.rect(self.screen, self.color, block_rect)

    def damage(self, bullet_rect):
        """根据子弹位置损坏护盾"""
        # 计算子弹在护盾内的相对位置
        rel_x = bullet_rect.x - self.rect.x
        rel_y = bullet_rect.y - self.rect.y

        # 找到对应的护盾块
        col_idx = rel_x // self.block_size
        row_idx = rel_y // self.block_size

        # 标记块为损坏（防止越界）
        if 0 <= row_idx < len(self.blocks) and 0 <= col_idx < len(self.blocks[0]):
            self.blocks[row_idx][col_idx] = False

        # 检查护盾是否完全损坏（所有块都不存在）
        if all(not any(row) for row in self.blocks):
            self.kill()  # 从精灵组移除