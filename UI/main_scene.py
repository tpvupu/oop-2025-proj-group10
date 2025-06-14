import pygame
import os
import json
from UI.components.character_animator import CharacterAnimator
from UI.components.button import Button
from UI.components.audio_manager import AudioManager
from UI.components.base_scene import BaseScene


class MainScene(BaseScene):
    def __init__(self, screen, player):
        super().__init__(screen)
        self.background = pygame.image.load("resource/image/background_intro.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, self.screen.get_size())
        self.animator = CharacterAnimator(player.intro, (400, 400), (300, 300))
        font = pygame.font.Font("resource/font/JasonHandwriting3-SemiBold.ttf", 36)
        self.next_week_button = Button(
            self.SCREEN_WIDTH - 200, self.SCREEN_HEIGHT - 100,

            180, 60," 下一週", font, (200, 200, 250),(50, 50, 50) ,(180, 180, 180))

        

        excl_img = pygame.image.load("resource/image/event_icon.PNG").convert_alpha()
        self.excl_img = pygame.transform.smoothscale(excl_img, (175, 175))
        self.excl_rect = self.excl_img.get_rect(center=(430, 400))
        self.excl_mask = pygame.mask.from_surface(self.excl_img)
        self.player = player
        self.is_hover = False
        self.hover_scale = 1.1
        if player.name == "Bubu":
            self.animator.frame_delay = 10  # 控制動畫速度


        self.stats_font = pygame.font.Font("resource/font/JasonHandwriting3-Regular.ttf", 28)
        self.bar_width = 150
        self.bar_height = 20
        self.bar_gap = 10
        self.bar_colors = {
            "intelligence": (135, 206, 250),  # 淺藍
            "mood":         (255, 182, 193),  # 粉紅
            "energy":       (144, 238, 144),  # 淺綠
            "social":       (255, 165, 0),    # 橘色
            "knowledge":    (221, 160, 221)    # 紫色
        }


        self.set_icon = pygame.image.load("resource/image/set.png").convert_alpha()
        self.set_icon = pygame.transform.smoothscale(self.set_icon, (80, 80))
        self.set_rect = self.set_icon.get_rect(topleft=(20, 700))
        self.set_hover = False


    def update(self):
        self.animator.update()

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # 設定按鈕 hover 與點擊
        if self.set_rect.collidepoint(mouse_pos):
            self.set_hover = True
            if not self.audio.is_sound_playing("resource/music/sound_effect/menu_hover.MP3"):
                self.audio.play_sound("resource/music/sound_effect/menu_hover.MP3")
            if mouse_pressed[0]:
                return "SETTING"
        else:
            self.set_hover = False

        # 事件泡泡 hover 與點擊邏輯
        relative_pos = (mouse_pos[0] - self.excl_rect.left, mouse_pos[1] - self.excl_rect.top)
        if (0 <= relative_pos[0] < self.excl_rect.width and
            0 <= relative_pos[1] < self.excl_rect.height and
            self.excl_mask.get_at(relative_pos)):

            if not self.is_hover:
                self.audio.play_sound("resource/music/sound_effect/menu_hover.MP3")
                self.is_hover = True

            if mouse_pressed[0]:
                if self.player.chosen[self.player.week_number] == '0':
                    return "Open Event"
                else:
                    print("this week's event has been done !")
        else:
            self.is_hover = False



    def draw_player_stats(self):

        stats_bg = pygame.Surface((480, 250), pygame.SRCALPHA)
        stats_bg.fill((255, 255, 255, 180))  # 180 可調整透明度，0~255

        # 貼到主畫面
        self.screen.blit(stats_bg, (20, 50))

        # 畫邊框
        pygame.draw.rect(self.screen, (100, 100, 100), (20, 50, 480, 250), 2)

        stats = {
            "intelligence": self.player.intelligence,
            "mood": self.player.mood,
            "energy": self.player.energy,
            "social": self.player.social,
            "knowledge": self.player.knowledge
        }

        font = self.stats_font
        x_left = 30
        x_right = x_left + self.bar_width + 80
        y_start = 180
        bar_height = self.bar_height
        bar_width = self.bar_width
        gap_y = self.bar_gap
        label_offset = -5  # 調整文字與條的對齊

        # 印出玩家的頭像
        player_imaage = pygame.image.load(self.player.header).convert_alpha()
        player_image = pygame.transform.smoothscale(player_imaage, (100, 100))
        player_rect = player_image.get_rect(topleft=(40, 60))
        self.screen.blit(player_image, player_rect)
        # 印出玩家的名字
        name_label = font.render(self.player.chname + " " + self.player.name, True, (0, 0, 0))
        name_rect = name_label.get_rect(topleft=(160, 80))
        self.screen.blit(name_label, name_rect)
        # 印出玩家的週數
        week_label = font.render(f"第 {self.player.week_number} 週", True, (0, 0, 0))
        week_rect = week_label.get_rect(topleft=(160, 120))
        self.screen.blit(week_label, week_rect)

        # 第一排：intelligence / mood
        for i, key in enumerate(["intelligence", "mood"]):
            x = x_left if i == 0 else x_right
            y = y_start
            fill = max(0, min(1, stats[key] / 100))
            pygame.draw.rect(self.screen, (200, 200, 200), (x + 65, y, bar_width, bar_height), 2)
            pygame.draw.rect(self.screen, self.bar_colors[key], (x + 65, y, int(bar_width * fill), bar_height))
            label = font.render(f"智力 {self.player.intelligence}" if key == "intelligence" else f"心情 {self.player.mood}", True, (0, 0, 0))
            self.screen.blit(label, (x, y + label_offset))

        # 第二排：energy / social
        for i, key in enumerate(["energy", "social"]):
            x = x_left if i == 0 else x_right
            y = y_start + bar_height + gap_y +10
            fill = max(0, min(1, stats[key] / 100))
            pygame.draw.rect(self.screen, (200, 200, 200), (x + 65, y, bar_width, bar_height), 2)
            pygame.draw.rect(self.screen, self.bar_colors[key], (x + 65, y, int(bar_width * fill), bar_height))
            label = font.render(f"體力 {self.player.energy}" if key == "energy" else f"社交 {self.player.social}", True, (0, 0, 0))
            self.screen.blit(label, (x, y + label_offset))
        
        # 第三排：knowledge（橫跨兩個 bar）
        y = y_start + 2 * (bar_height + gap_y) + 20
        x = x_left
        total_width = (x_right - x_left) + 130 + bar_width  # 橫跨兩欄
        fill = max(0, min(1, stats["knowledge"] / 100))
        pygame.draw.rect(self.screen, (200, 200, 200), (x + 65, y, total_width - 130, bar_height), 2)
        pygame.draw.rect(self.screen, self.bar_colors["knowledge"], (x + 65, y, int((total_width - 130) * fill), bar_height))
        label = font.render(f"知識 {self.player.knowledge:.0f}/100", True, (0, 0, 0))
        self.screen.blit(label, (x, y + label_offset))

        if self.player.week_number > 0:
            # 印出玩家選擇改變
            last_week_change = stats_change(self.player.last_week_change)
            font2 = pygame.font.Font("resource/font/JasonHandwriting3-Light.ttf", 22)
            text0 = font2.render("本週選擇改變：", True, (0, 0, 0))
            text0_rect = text0.get_rect(topleft=(x_right + 60, 90))
            self.screen.blit(text0, text0_rect)
            # 心情，知識
            text1 = font2.render(f"心情 {last_week_change[0]} 知識 {last_week_change[3]}", True, (0, 0, 0))
            text1_rect = text1.get_rect(topleft=(x_right + 60, 115))
            self.screen.blit(text1, text1_rect)
            # 體力，社交
            text2 = font2.render(f"體力 {last_week_change[1]} 社交 {last_week_change[2]}", True, (0, 0, 0))
            text2_rect = text2.get_rect(topleft=(x_right + 60, 140))
            self.screen.blit(text2, text2_rect)


        
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.animator.draw(self.screen)
        self.next_week_button.draw(self.screen)
        self.draw_player_stats()

        # 畫設定按鈕
        if self.set_hover:
            scaled = pygame.transform.scale(self.set_icon, (96, 96))
            rect = scaled.get_rect(center=self.set_rect.center)
            self.screen.blit(scaled, rect.topleft)
        else:
            self.screen.blit(self.set_icon, self.set_rect.topleft)

        if self.player.chosen[self.player.week_number] == '0':
            if self.is_hover:
                scaled_img = pygame.transform.smoothscale(
                    self.excl_img,
                    (int(self.excl_img.get_width() * self.hover_scale),
                     int(self.excl_img.get_height() * self.hover_scale))
                )
                scaled_rect = scaled_img.get_rect(center=self.excl_rect.center)
                self.screen.blit(scaled_img, scaled_rect)

        if self.player.chosen[self.player.week_number] == '0':
            # ====== 閃爍動畫（基礎 scale）======
            ticks = pygame.time.get_ticks()
            import math
            base_scale = 1 + 0.12 * math.sin(ticks * 0.01)  # 在 0.95 到 1.05 之間震盪

            # ====== hover 放大疊加效果 ======
            if self.is_hover:
                scale = base_scale * self.hover_scale

            else:
                scale = base_scale

            # ====== 計算縮放後的位置並繪製 ======
            new_width = int(self.excl_img.get_width() * scale)
            new_height = int(self.excl_img.get_height() * scale)
            scaled_img = pygame.transform.smoothscale(self.excl_img, (new_width, new_height))
            scaled_rect = scaled_img.get_rect(center=self.excl_rect.center)
            
            self.screen.blit(scaled_img, scaled_rect)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Quit"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.set_rect.collidepoint(event.pos):
                        from UI.set_scene import SetScene
                        from UI.components.blur import fast_blur
                        blurred_bg = fast_blur(self.screen.copy())
                        while True:
                            set_scene = SetScene(self.screen, blurred_bg)
                            setting_result = set_scene.run()
                            print(f"設定場景回傳：{setting_result}")

                            if setting_result == "BACK":
                                break
                            elif setting_result == "QUIT":
                                return "Quit"
                            elif setting_result in ("OPTION_1", "OPTION_2"):
                                print(f"你選擇了 {setting_result}，但仍停留在設定頁～")
                                
                if self.next_week_button.handle_event(event):
                    return "Next Story"

            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.FPS)

        return None
    



def stats_change(list):
    # 將數字轉換為帶符號的字串
    # 正數前加 "+"，負數前加 "-"，零則顯示 "-"
    result = []
    for change in list:
        change = int(change)
        if change > 0:
            result.append( "+" + str(change))
        if change == 0:
            result.append("-")
        elif change < 0:
            result.append(str(change))
    return result