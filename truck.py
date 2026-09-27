import pyxel
import values

class Truck:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite = values.TruckSprite

        self.capacity = 8
        self.current_load = 0
        self.deliveries = 0

        self.leaving = False
        self.leave_timer = 0
        self.leave_duration = 600

    " Method triggered to add a package to the truck "
    def add_package(self):
        self.current_load += 1
        if self.current_load >= self.capacity:
            self.start_delivery()
        print("Added package!")
        print(f"Truck current capacity: {self.current_load}")

    " Method triggered when the load is full "
    def start_delivery(self):
        self.leaving = True
        self.leave_timer = 0

        # Add 10 points to the score for delivery
        values.score += 10
        values.minPackagesCounter += 10
        # Eliminates failures if the amount of deliveries is met
        self.__eliminate_failures()

    " Method triggered when the truck is in delivery"
    def update_state(self):
        if self.leaving:
            self.current_load = 0
            self.leave_timer += 1
            self.x = -50
            if self.leave_timer == self.leave_duration:
                self.return_truck()

    " Method triggered when the delivery time is out "
    def return_truck(self):
        self.leaving = False
        self.leave_timer = 0
        self.x = 10
        # Call out the boss to put the characters back to work
        values.activeFailure = True
        print("Truck returned!")

    " Method that removes a failure when a certain amount of deliveries are met (depending on the difficulty)"
    def __eliminate_failures(self):
        if values.difficultIndex == 0:
            if self.deliveries % 3 == 0:
                values.fails -= 1
        elif values.difficultIndex == 1 or values.difficultIndex == 2:
            if self.deliveries % 5 == 0:
                values.fails -= 1

    " Properties and setters "
    # Validate that the x and y coordinates return the spected values.
    @property
    def x(self):
        return self.__x
    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError("x must be an integer")
        if x < -50:
            raise ValueError("x goes out of margins")
        self.__x = x
    @property
    def y(self):
        return self.__y
    @y.setter
    def y(self, y: int):
        if not isinstance(y, int):
            raise TypeError("y must be an integer")
        if y < 0:
            raise ValueError("y must be positive")
        self.__y = y