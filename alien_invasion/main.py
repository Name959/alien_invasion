import sys
import pygame
import random
from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien_bullet import AlienBullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
# 1. 删除多余的 Shield 类导入（不再需要屏幕下方护盾）

class AlienInvasion:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion (Ship Shield)")

        self.stats = GameStats(self)
        self._load_high_score()
        self.ship = Ship(self)  # 飞船已集成【环绕式圆形护盾】
        self.sb = Scoreboard(self)

        # 精灵组初始化（仅保留必要组，删除 shield 相关）
        self.bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        self.play_button = Button(self, "Play")

        # 音效加载（保留原逻辑）
        self._load_sounds()
        self.last_alien_fire_time = 0

    def _load_sounds(self):
        """加载游戏音效"""
        try:
            self.shoot_sound = pygame.mixer.Sound(self.settings.shoot_sound_path)
            self.explosion_sound = pygame.mixer.Sound(self.settings.explosion_sound_path)
            pygame.mixer.music.load(self.settings.bg_music_path)
            self.shoot_sound.set_volume(self.settings.sound_volume)
            self.explosion_sound.set_volume(self.settings.sound_volume)
            pygame.mixer.music.set_volume(self.settings.sound_volume * 0.7)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"音效加载失败: {e}")
            self.shoot_sound = None
            self.explosion_sound = None

    # 2. 删除多余的 _create_shield 方法（不再需要屏幕下方3个护盾）

    def _fire_alien_bullet(self):
        """随机让一个外星人发射子弹"""
        current_time = pygame.time.get_ticks()
        if (current_time - self.last_alien_fire_time > self.settings.alien_fire_interval and
                len(self.alien_bullets) < self.settings.alien_bullet_allowed and
                self.aliens):
            random_alien = random.choice(list(self.aliens.sprites()))
            new_bullet = AlienBullet(self, random_alien)
            self.alien_bullets.add(new_bullet)
            self.last_alien_fire_time = current_time

    def _load_high_score(self):
        """从文件加载最高分"""
        try:
            with open('high_score.txt', 'r') as f:
                content = f.read().strip()
                self.stats.high_score = int(content) if content else 0
        except (FileNotFoundError, ValueError):
            self.stats.high_score = 0
            with open('high_score.txt', 'w') as f:
                f.write('0')

    def _check_play_button(self, mouse_pos):
        """在玩家单击Play按钮时开始新游戏（删除护盾相关冗余代码）"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # 清空精灵组（删除多余的 self.ship.shield.empty()）
            self.aliens.empty()
            self.bullets.empty()
            self.alien_bullets.empty()

            # 3. 删除多余的 _create_shield() 调用（环绕护盾通过 center_ship() 恢复）
            self._create_fleet()
            self.ship.center_ship()  # 重置飞船位置时，自动恢复环绕护盾
            pygame.mouse.set_visible(False)

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_alien_bullets()
                self._fire_alien_bullet()
                self._update_aliens()
                self._check_collisions()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """响应按键和鼠标事件（无修改）"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """响应按键（无修改）"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE and self.stats.game_active:
            self._fire_bullet()
            if self.shoot_sound:
                self.shoot_sound.play()

    def _check_keyup_events(self, event):
        """响应松开（无修改）"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建玩家子弹（无修改）"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新玩家子弹（无修改）"""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_alien_bullets(self):
        """更新外星子弹（无修改）"""
        self.alien_bullets.update()
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(bullet)

    def _check_collisions(self):
        """碰撞检测（仅保留环绕式护盾逻辑，无修改）"""
        # 1. 玩家子弹 ↔ 外星人
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            if self.explosion_sound:
                self.explosion_sound.play()
            if not self.aliens:
                self.bullets.empty()
                self.alien_bullets.empty()
                self._create_fleet()
                self.settings.increase_speed()
                self.stats.level += 1
                self.sb.prep_level()

        # 2. 外星子弹 ↔ 飞船（优先消耗环绕护盾）
        alien_bullet_hits = pygame.sprite.spritecollide(self.ship, self.alien_bullets, True)
        if alien_bullet_hits:
            if self.ship.has_shield:
                self.ship.lose_shield()
                if self.explosion_sound:
                    self.explosion_sound.play()
            else:
                self.alien_bullets.empty()
                self.ship_hit()
                if self.explosion_sound:
                    self.explosion_sound.play()

        # 3. 外星人 ↔ 飞船（优先消耗环绕护盾）
        alien_hits = pygame.sprite.spritecollideany(self.ship, self.aliens)
        if alien_hits:
            if self.ship.has_shield:
                self.ship.lose_shield()
                alien_hits.kill()
                if self.explosion_sound:
                    self.explosion_sound.play()
            else:
                self.ship_hit()

    def _create_fleet(self):
        """创建外星人群（无修改）"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height - 150)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """创建一个外星人（无修改）"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """检查外星人是否到达边缘（无修改）"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """改变外星人群方向（无修改）"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def ship_hit(self):
        """飞船受损逻辑（无修改，环绕护盾通过 center_ship() 恢复）"""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()
            self.alien_bullets.empty()

            self._create_fleet()
            self.ship.center_ship()  # 重置飞船时，自动恢复环绕护盾
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """检查外星人是否到达底部（无修改）"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self.ship_hit()
                break

    def _update_aliens(self):
        """更新外星人群位置（无修改）"""
        self._check_fleet_edges()
        self.aliens.update()
        self._check_aliens_bottom()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship_hit()

    def _update_screen(self):
        """更新屏幕（环绕护盾通过 ship.blitme() 绘制，无修改）"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()  # 绘制飞船 + 环绕式护盾
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for bullet in self.alien_bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()