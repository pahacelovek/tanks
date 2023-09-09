

class Tank():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 0
        self.turn_speed = 0
        self.turn_angle = 0

        self.max_front_speed = 50
        self.max_rear_speed = 20
        self.max_right_turn = 30
        self.max_left_turn = 30
        self.front_acceleration = 10
        self.rear_acceleration = 7
        self.right_acceleration = 20
        self.left_acceleration = 20

    # def move_front(self):
