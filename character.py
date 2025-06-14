import random
import math
import json

class Character:
    def __init__(self, name, intelligence, mood, energy, social):
        self.name = name
        self.intelligence = int(intelligence)
        self.mood = int(mood)
        self.energy = int(energy)
        self.social = int(social)
        self.knowledge = 0.00
        self.midterm = 0     # 期中考成績
        self.final = 0       # 期末考成績
        self.week_number = 0
        self.lucky_prof = 3
        self.total_score = 0
        self.GPA = 0
        self.chosen = ['0']*17
        self.home = ""
        self.last_week_change = [0,0,0,0]  # [心情, 體力, 社交, 知識]

    def study(self, degree):
        growth = int(
            self.intelligence * 0.11 +
            self.mood * 0.05 +
            self.energy * 0.08 +
            self.social * 0.03
        )
        growth = round(growth/(1+((8 - self.week_number) * 0.1)),2) if self.week_number < 8 else round(growth/(1+((16 - self.week_number) * 0.1)),2)
        self.last_week_change = [-15, -12, 0, growth+3]
        self.last_week_change = [int(grow * degree) for grow in self.last_week_change] 
        
        self.mood , self.energy , self.social, self.knowledge = \
            max(0, self.mood + self.last_week_change[0]),\
            max(0, self.energy + self.last_week_change[1]),\
            max(0, self.social + self.last_week_change[2]),\
            min(100, self.knowledge + self.last_week_change[3]) 
    
        #print(f"{self.name} 認真學習中 📖✨ 知識增加了 {growth:.2f} 點！現在是 {self.knowledge}/100")

    def socialize(self, degree):
        growth = int(
            (self.social - 30) * 0.1 +
            (self.mood - 50) * 0.03 +
            (self.energy) * 0.01
        )
        self.last_week_change = [ 3, -5, growth, 3+int(round(growth * self.social * 0.01))]
        self.last_week_change = [int(grow * degree) for grow in self.last_week_change] 
        
        self.mood , self.energy , self.social, self.knowledge = \
            min(100, self.mood + self.last_week_change[0]),\
            max(0, self.energy + self.last_week_change[1]),\
            min(100, self.social + self.last_week_change[2]),\
            min(100, self.knowledge + self.last_week_change[3]) 

        #print(f"{self.name} 正在社交中 🤝🎉 社交能力提升了 {growth:.2f} 點！現在是 {self.social}/100")

    def play_game(self, degree):
        growth = int(
            (100 - self.mood) * 0.2 +
            (self.intelligence - 30) * 0.02 +
            (self.energy) * 0.01 -
            (self.social - 30) * 0.01
        )
        self.last_week_change = [growth, 3, 0, 3+int(round(-growth * 0.1))]
        self.last_week_change = [int(grow * degree) for grow in self.last_week_change] 
        self.mood , self.energy , self.social, self.knowledge = \
            min(100, self.mood + self.last_week_change[0]),\
            max(0, self.energy + self.last_week_change[1]),\
            min(100, self.social + self.last_week_change[2]),\
            min(100, self.knowledge + self.last_week_change[3])
        #print(f"{self.name} 正在玩遊戲 🎮😄 心情提升了 {growth:.2f} 點！現在是 {self.mood}/100")

    def rest(self, degree):
        growth = int(
            (100 - self.energy) * 0.15 +
            (100 - self.mood) * 0.02 +
            (self.intelligence - 50) * 0.2 -
            (self.social - 30) * 0.01
        )
        self.last_week_change = [int(growth*0.6), growth, 1, 3+int(round(-growth * 0.1))]
        self.last_week_change = [int(grow * degree) for grow in self.last_week_change]
        self.mood , self.energy , self.social, self.knowledge = \
            min(100, self.mood + self.last_week_change[0]),\
            min(100, self.energy + self.last_week_change[1]),\
            max(0, self.social + self.last_week_change[2]),\
            min(100, self.knowledge + self.last_week_change[3])
        #print(f"{self.name} 正在休息 💤😌 體力提升了 {growth:.2f} 點！現在是 {self.energy}/100")

    def calculate_grade(self):
        score = round(self.knowledge * 0.45 + self.mood * 0.3 + self.energy * 0.2 + self.intelligence * 0.1 , 2)
        if score >= 60:
            return random.randint(int(score - 1), int(score + 15))
        else:
            luck = random.random()
            base = round(score * 0.85, 2)
            fluctuation_range = round(5 + luck * 20, 2)
            fluctuation = round(random.uniform(luck, fluctuation_range), 2)
            grade = min(100, round(base + fluctuation, 2))
        return int(round(grade))
    

    def get_final(self):
        self.final = round(self.calculate_grade()) -20


    def calculate_GPA(self):
        total_score = self.midterm * 0.35 + self.final * 0.35 + (self.knowledge) * 0.3
        total_score = max(0, int(math.sqrt(total_score) * 20 - 100))
        self.total_score = total_score
        gpa = []
        for _ in range(25):
            if random.random() < 0.8:
                gpa.append(min(4.3,score_to_gpa(total_score) + self.lucky_prof * 0.03))
            else:
                gpa.append(score_to_gpa(total_score))
        self.GPA = round(sum(gpa) / len(gpa),2)
        #print(f"total_score: {total_score}, GPA: {self.GPA:.2f}, lucky_prof: {self.lucky_prof}")
        #print(gpa)


    def show_status(self):
        pass
        #print(f"{self.name} 在第{self.week_number - 1}週的狀態：")
        #print(f"智力：{self.intelligence} | 心情：{self.mood} | 體力：{self.energy} | 社交：{self.social} | 知識：{self.knowledge:.2f}/100")
        #print("===========================================================")


# 🧸 各角色子類別
class Bubu(Character):
    def __init__(self):
        super().__init__("Bubu", intelligence=70, mood=65, energy=80, social=30)
        self.chname = "布布"
        self.animal = "熊熊"
        self.intro = "resource/gif/bubu_intro_frames"
        self.header = "resource/image/Bubu_head.png"
        self.storytyping = "resource/gif/bubu_playcomputer_frames"
        self.testing = "resource/gif/bubu_study_frames"
        self.taketest = "resource/gif/bubu_no_study_frames"
        self.ending = "resource/gif/bubu_playgame_frames"


        self.sad = "resource/gif/bubu_crying_frames"
        self.playgame = "resource/gif/bubu_playgame_frames"

    def socialize(self, degree):
        growth = round(
            (100 - self.social) * 0.1 +
            (self.mood - 30) * 0.03 +
            (self.energy) * 0.01, 2
        )

        self.last_week_change = [ 3, -15, growth, 3+int(round(growth * self.social * 0.01))]
        self.last_week_change = [int(grow * degree) for grow in self.last_week_change]
        self.mood , self.energy , self.social, self.knowledge = \
            min(100, self.mood + self.last_week_change[0]),\
            max(0, self.energy + self.last_week_change[1]),\
            max(0, self.social + self.last_week_change[2]),\
            min(100, self.knowledge + self.last_week_change[3])
        
    def get_midterm(self):
        self.midterm = self.calculate_grade() + self.knowledge * 0.4
        if self.mood > 65:
            self.midterm += 10
        if self.energy < 70:
            self.midterm -= 3
        if self.knowledge > 35:
            self.midterm += 8
        self.midterm = int(round(self.midterm))


class Yier(Character):
    def __init__(self):
        super().__init__("Yier", intelligence=75, mood=85, energy=60, social=90)
        self.animal = "熊熊"
        self.chname = "一二"
        self.intro = "resource/gif/yier_intro_frames"
        self.header = "resource/image/Yier_head.png"
        self.storytyping = "resource/gif/yier_play_game_frames"
        self.testing = "resource/gif/yier_thinking_frames"
        self.taketest = "resource/gif/yier_no_study_frames"
        self.ending = "resource/gif/yier_happyrest_frames"

        
        

    def get_midterm(self):
        self.midterm = min(100, self.calculate_grade() + self.knowledge * 0.2)
        if self.social > 80:
            self.midterm += 2
        if self.energy < 50:
            self.midterm -= 3
        if self.knowledge > 40:
            self.midterm += 4
        self.midterm = int(round(self.midterm))


class Mitao(Character):
    def __init__(self):
        super().__init__("Mitao", intelligence=95, mood=50, energy=45, social=60)
        self.animal = "貓貓"
        self.chname = "蜜桃"
        self.intro = "resource/gif/mitao_intro_frames"
        self.header = "resource/image/Mitao_head.png"
        self.storytyping = "resource/gif/mitao_rest_frames"
        self.testing = "resource/gif/mitao_testing_frames"
        self.taketest = "resource/gif/mitao_low_mood_frames"
        self.ending = "resource/gif/mitao_flower_frames"


    def get_midterm(self):
        self.midterm = min(100, self.calculate_grade() + self.knowledge * 0.2)
        self.midterm += 10
        if self.mood < 60:
            self.midterm -= 4
        if self.knowledge > 45:
            self.midterm += 5
        self.midterm = int(round(self.midterm))



class Huihui(Character):
    def __init__(self):
        super().__init__("Huihui", intelligence=80, mood=90, energy=50, social=65)
        self.animal = "貓貓"
        self.chname = "灰灰"
        self.intro = "resource/gif/huihui_intro_frames"
        self.header = "resource/image/Huihui_head.png"
        self.storytyping = "resource/gif/huihui_rest_frames"
        self.taketest = "resource/gif/huihui_sosad_frames"
        self.testing = "resource/gif/huihui_running_frames"
        self.ending = "resource/gif/huihui_flower_frames"

        self.week_number = 0

    def get_midterm(self):
        self.midterm = min(100, self.calculate_grade() + self.knowledge * 0.2)
        if self.mood > 85:
            self.midterm += 7
        if self.energy < 50:
            self.midterm -= 3
        if self.knowledge > 30:
            self.midterm += 2
        self.midterm = int(round(self.midterm))



def score_to_gpa(score):
    if score >= 95:
        return 4.3
    grading = 95/4.3 # 95分對應4.3
    return round(score / grading, 2) 
    


if __name__ == "__main__":
    player = Huihui()

    player.socialize(1)
    player.socialize(1)
    player.rest(1)
    player.play_game(1)
    player.study(1)
    player.socialize(1)
    player.rest(1)
    player.study(1)

    player.get_midterm()

    player.study(1)
    player.socialize(1)
    player.rest(1)
    player.study(1)
    player.study(1)
    player.rest(1)
    player.study(1)
    player.study(1)

    player.get_final()

    player.calculate_GPA()

    print(f"{player.name} 的期中考成績：{player.midterm}")
    print(f"{player.name} 的期末考成績：{player.final}")
    
    print(f"{player.name} 的知識：{player.knowledge}")
    print(f"{player.name} 的 GPA: {player.GPA}")
    print(f"{player.name} 的社交能力：{player.social}")
    print(f"{player.name} 的幸運教授：{player.lucky_prof}")
    print(f"{player.name} 的心情：{player.mood}")
    print(f"{player.name} 的體力：{player.energy}")
    # player.show_status()