"""
The template of the script for playing the game in the ml mode
"""

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        pass
        self.dir = 0
        self.next = 0
        self.canTurn = False #蛇可以回頭吃食物
        self.score = -3

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] == "GAME_OVER":
            return "RESET"
        
        check_body = 0
        self.score = -3

        snake_head = scene_info["snake_head"]
        food = scene_info["food"]

        snake_body = scene_info["snake_body"] #真蛇身

        if snake_head[1] < snake_body[0][1]:
            self.dir = 1 #往上
        elif snake_head[0] < snake_body[0][0]:
            self.dir = 2 #往左
        elif snake_head[1] > snake_body[0][1]:
            self.dir = 3 #往下
        elif snake_head[0] > snake_body[0][0]:
            self.dir = 4 #往右
            
        for n in snake_body:
            if n[1] == 290:
                check_body = 1 #蛇身在下 不能迴轉
            self.score += 1

        if self.score == 895 :
            return "RIGHT" #滿分的前一刻去自殺 防止當機蒐集不了數據

        if check_body == 0 and snake_head[0] <= food[0]: #沒有蛇身在下 可以迴轉
            self.canTurn = True
            
        if snake_head[1] == 290:
            if snake_head[0] == 290:
                self.next = 5
                self.canTurn = False
                return "UP"
            elif self.canTurn:
                if snake_head[0] == food[0]:
                    if food[0] % 20 == 0:
                        return "RIGHT"
                    elif food[0] % 20 == 10:
                        self.next = 5
                        self.canTurn = False
                        return "UP"
                elif snake_head[0] == food[0] + 10:
                    self.next = 5
                    self.canTurn = False
                    return "UP"
                return "RIGHT"
            else:
                return "RIGHT"
        elif self.next == 1:
            self.next = 0
            return "UP"
        elif self.next == 2:
            self.next = 0
            return "DOWN"
        elif self.next == 3:
            self.next = 0
            return "LEFT"
        elif self.next == 4:
            self.next = 0
            return "RIGHT"
        elif snake_head[1] == 0:
            self.next = 2
            return "LEFT"
        elif snake_head[1] == 280:
            if food[0] > snake_head[0]:
                if self.canTurn:
                    return "DOWN"
            if self.next == 5:
                return "UP"
            if snake_head[0] == 0:
                return "DOWN"
            else:
                self.next = 1
                return "LEFT"
        
    def reset(self):
        """
        Reset the status if needed
        """
        pass
