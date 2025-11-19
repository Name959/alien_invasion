# Alien Invasion（外星人入侵）

这是一个基于 Pygame 的 2D 飞船射击小游戏。在游戏中，你控制一艘飞船，移动并发射子弹以击落入侵的外星人，避免被外星人或其子弹击中。

**主要功能**
- 玩家飞船（含环绕式护盾机制）
- 外星人编队、自动发射子弹
- 得分与最高分保存（保存在 `high_score.txt`）
- 音效与背景音乐（位于 `sounds/`）

**运行要求**
- Python 3.8 或更高（在本机已安装 Python，并已将其添加到 PATH）
- Pygame 库

**安装依赖（Windows PowerShell）**
```powershell
python -m pip install --upgrade pip
python -m pip install pygame
```

**运行游戏**
在项目根目录（包含 `main.py` 的目录）打开终端并运行：
```powershell
python main.py
```

**游戏控制**
- 向右/向左移动：按键 `→` / `←`（方向键）
- 发射子弹：按 `Space`（当游戏处于活动状态时）
- 退出游戏：按 `Q`
- 开始游戏：用鼠标点击屏幕上的 `Play` 按钮

**项目结构（主要文件）**
- `main.py`：游戏入口与主循环
- `settings.py`：游戏配置（屏幕尺寸、速度、音效路径等）
- `ship.py`：玩家飞船及护盾逻辑
- `alien.py`：外星人逻辑
- `bullet.py` / `alien_bullet.py`：玩家与外星人子弹
- `scoreboard.py`：得分显示
- `game_stats.py`：游戏状态与统计
- `button.py`：Play 按钮
- `high_score.txt`：保存最高分（由程序读写）
- `images/`：图片资源
- `sounds/`：音效与音乐资源

**常见问题**
- 如果启动时音效或背景音乐报错，可能是系统音频驱动或 Pygame 音频初始化问题。可以在 `main.py` 中临时注释掉 `pygame.mixer` 相关初始化（见 `_load_sounds`），或确保系统音频正常。
- 如果窗口尺寸或性能问题，可在 `settings.py` 中调整 `screen_width` / `screen_height` 与速度配置。

**许可与鸣谢**
该项目为个人学习/练习项目。