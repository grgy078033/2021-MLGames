"""
The template of the main script of the machine learning process
"""
import random
import os.path
import pickle

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.previous_ball = (0, 0)
        filename = 'arkanoid_n3_20210309_knn_model.pickle'
        filepath = os.path.join(os.path.dirname(__file__), filename)
        self.model = pickle.load(open(filepath, 'rb'))
        self.ball_served = False

    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or
            scene_info["status"] == "GAME_PASS"):
            return "RESET"

        if not self.ball_served:
                self.ball_served = True
                if random.randint(0, 1):
                    command = "SERVE_TO_LEFT"
                else:
                    command = "SERVE_TO_RIGHT"
        else:
            nx = scene_info["ball"][0]
            ny = scene_info["ball"][1]
            Ball_speed_x = scene_info["ball"][0] - self.previous_ball[0]
            Ball_speed_y = scene_info["ball"][1] - self.previous_ball[1]
            px = scene_info["platform"][0]
            if Ball_speed_x > 0:
                if Ball_speed_y > 0:
                    Direction = 0
                else:
                    Direction = 1
            else:
                if Ball_speed_y > 0:
                    Direction = 2
                else:
                    Direction = 3

            command = self.model.predict([[nx, ny, Direction, Ball_speed_x, Ball_speed_y, px]])

            if command == 0: return "NONE"
            elif command == 1: return "MOVE_LEFT"
            else: return "MOVE_RIGHT"

        self.previous_ball = scene_info["ball"]

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
