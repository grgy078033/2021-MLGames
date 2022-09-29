import math
import random
import pickle
"""
The template of the main script of the machine learning process
"""

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.ball_served = False
        self.previous_ball = None
        self.first = False

    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        predict_x = 1
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or
            scene_info["status"] == "GAME_PASS"):
            self.first = False
            return "RESET"
        if not self.ball_served:
            self.ball_served = True
            if random.randint(0, 1):
                command = "SERVE_TO_LEFT"
            else:
                command = "SERVE_TO_RIGHT"
                
        else:
            if self.first == True:
                if self.previous_ball[1] - scene_info["ball"][1] != 0 :
                    n = (self.previous_ball[0] * (400 - scene_info["ball"][1]) - scene_info["ball"][0] * (400 - self.previous_ball[1])) / (self.previous_ball[1] - scene_info["ball"][1])
                    predict_x = self.adjust(n) + random.randint(-3, 3) #預測x落點 & 微調落點讓數據隨機 避免打不到或是每個紀錄都長一樣

            if abs(predict_x - (scene_info["platform"][0]+20)) < 3:
                command = "NONE"
            elif predict_x > scene_info["platform"][0]+20:
                if self.first == False:
                    self.first = True
                    command = "MOVE_RIGHT"
                else:
                    command = "MOVE_RIGHT"
                print(predict_x)
            else:
                if self.first == False:
                    self.first = True
                    command = "MOVE_LEFT"
                else:
                    command = "MOVE_LEFT"
                print(predict_x) #板子移動至預測落點
        self.previous_ball = scene_info["ball"]
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