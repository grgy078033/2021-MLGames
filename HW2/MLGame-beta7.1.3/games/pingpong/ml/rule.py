import random
import math
"""
The template of the script for the machine learning process in game pingpong
"""

class MLPlay:
    def __init__(self, side):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.ball_served = False
        self.side = side
        self.predict_x = 1
        self.count = []
        self.i = 0
        self.frame_num_to_blocker = 0
        self.temp = 0
        self.predict_b_x = -100
        self.predict_b1_x = -100
        self.predict_b2_x = -100

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"

        command = "NONE"

        if not self.ball_served:
            self.ball_served = True
            if random.randint(0, 1):
                command = "SERVE_TO_LEFT"
            else:
                command = "SERVE_TO_RIGHT"
        else:
            if self.side == "1P":
                if scene_info["ball_speed"][1] > 0 and (self.previous_ball[1] - scene_info["ball"][1]) != 0: #ball goes down
                    n = (self.previous_ball[0] * (420 - scene_info["ball"][1]) - scene_info["ball"][0] * (420 - self.previous_ball[1])) / (self.previous_ball[1] - scene_info["ball"][1])
                    self.predict_x = self.adjust(n) + random.randint(-3, 3) #預測x落點 & 微調落點讓數據隨機 避免打不到或是每個紀錄都長一樣
                    self.frame_num_to_blocker = (240 - scene_info["ball"][1]) / scene_info["ball_speed"][1]
            elif self.side == "2P":
                if scene_info["ball_speed"][1] < 0 and (self.previous_ball[1] - scene_info["ball"][1]) != 0: #ball goes up
                    n = (self.previous_ball[0] * (80 - scene_info["ball"][1]) - scene_info["ball"][0] * (80 - self.previous_ball[1])) / (self.previous_ball[1] - scene_info["ball"][1])
                    self.predict_x = self.adjust(n) + random.randint(-3, 3) #預測x落點 & 微調落點讓數據隨機 避免打不到或是每個紀錄都長一樣
                    self.frame_num_to_blocker = (260 - scene_info["ball"][1]) / scene_info["ball_speed"][1]

            z = scene_info["ball"][0] + scene_info["ball_speed"][0] * self.frame_num_to_blocker
            self.temp = self.adjust(z) # determin where ball_x is when passing several frame
            blocker_left = self.blocker_adjust(scene_info["blocker"][0] + 5 * self.frame_num_to_blocker)
            blocker_right = self.blocker_adjust(scene_info["blocker"][0] + 5 * self.frame_num_to_blocker + 30)
            print(blocker_left, ",", blocker_right)

            if self.side == "1P" and (self.previous_ball[1] - scene_info["ball"][1]) != 0:
                if scene_info["ball_speed"][1] > 0: #ball goes down
                    if self.frame_num_to_blocker > 0: #球還沒經過blocker
                        if self.temp >= blocker_left:
                            if self.temp <= blocker_right:
                                print("zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
                                p_x = self.temp
                                p_y = scene_info["ball"][1] + math.ceil(self.frame_num_to_blocker) * scene_info["ball_speed"][1]
                                n_x = self.temp + scene_info["ball_speed"][0]
                                n_y = p_y - scene_info["ball_speed"][1]
                                if p_y - n_y != 0:
                                    n = (p_x * (80 - n_y) - n_x * (80 - p_y)) / (p_y - n_y)
                                    self.predict_b2_x = self.adjust(n)
            elif self.side == "2P" and (self.previous_ball[1] - scene_info["ball"][1]) != 0:
                if scene_info["ball_speed"][1] <0: #ball goes up
                    if self.frame_num_to_blocker > 0: #球還沒經過blocker
                        if self.temp >= blocker_left:
                            if self.temp <= blocker_right:
                                print("zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
                                p_x = self.temp
                                p_y = scene_info["ball"][1] + math.ceil(self.frame_num_to_blocker) * scene_info["ball_speed"][1]
                                n_x = self.temp + scene_info["ball_speed"][0]
                                n_y = p_y - scene_info["ball_speed"][1]
                                if p_y - n_y != 0:
                                    n = (p_x * (420 - n_y) - n_x * (420 - p_y)) / (p_y - n_y)
                                    self.predict_b1_x = self.adjust(n)

            
            if self.side == "1P":
                if scene_info["ball_speed"][1] < 0:#ball goes up
                    if self.predict_b1_x != -100:
                        if abs(self.predict_b1_x - (scene_info["platform_1P"][0]+20)) < 3:
                            command = "NONE"
                        elif self.predict_b1_x > scene_info["platform_1P"][0]+20:
                            command = "MOVE_RIGHT"
                            print(self.frame_num_to_blocker)
                        else:
                            command = "MOVE_LEFT"
                            print(self.frame_num_to_blocker)
                    elif scene_info["platform_1P"][0]+20 < 100:
                        command = "MOVE_RIGHT"
                    elif scene_info["platform_1P"][0]+20 > 100:
                        command = "MOVE_LEFT"
                elif scene_info["ball_speed"][1] > 0: #ball goes down
                    if abs(self.predict_x - (scene_info["platform_1P"][0]+20)) < 3:
                        command = "NONE"
                    elif self.predict_x > scene_info["platform_1P"][0]+20:
                        command = "MOVE_RIGHT"
                        print(self.frame_num_to_blocker)
                    else:
                        command = "MOVE_LEFT"
                        print(self.frame_num_to_blocker)
                
            elif self.side == "2P":
                if scene_info["ball_speed"][1] > 0: #ball goes down
                    if self.predict_b2_x != -100:
                        if abs(self.predict_b2_x - (scene_info["platform_2P"][0]+20)) < 3:
                            command = "NONE"
                        elif self.predict_b2_x > scene_info["platform_2P"][0]+20:
                            command = "MOVE_RIGHT"
                            print(self.frame_num_to_blocker)
                        else:
                            command = "MOVE_LEFT"
                            print(self.frame_num_to_blocker)
                    elif scene_info["platform_2P"][0]+20 < 100:
                        command = "MOVE_RIGHT"
                    elif scene_info["platform_2P"][0]+20 > 100:
                        command = "MOVE_LEFT"
                elif scene_info["ball_speed"][1] < 0: #ball goes up
                    if abs(self.predict_x - (scene_info["platform_2P"][0]+20)) < 3:
                        command = "NONE"
                    elif self.predict_x > scene_info["platform_2P"][0]+20:
                        command = "MOVE_RIGHT"
                        print(self.frame_num_to_blocker)
                    else:
                        command = "MOVE_LEFT"
                        print(self.frame_num_to_blocker) #板子移動至預測落點

        self.previous_ball = scene_info["ball"]
        self.predict_b_x = -100
        self.predict_b1_x = -100
        self.predict_b2_x = -100
        return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False

    def adjust(self, n):
        while n < 0 or n > 195:
            if n < 0:
                n *= -1
            else :
                n = 390 - n
        return n
    def blocker_adjust(self, n):
        while n < 0 or n > 170:
            if n < 0:
                n *= -1
            else :
                n = 340 - n
        return n