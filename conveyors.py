import pyxel

import values
import characters

boxes = []

# The conveyor will be integers, being 0 the initial one, the odd conveyor odd numbers and so on
class Box:
    def __init__(self, x: int, y: int, sprite: tuple):
        self.x = x
        self.y = y
        self.sprite = sprite

        self.conveyor = 0
        self.position = 0
        self.floor = 0
        self.carried = False
        self.broken = False
        self.delivered = False

    " Method to move the boxes through the conveyors"
    # Move conveyor0 boxes
    def move_0_box(self):
        # Condition to only include the boxes in the initial conveyor
        if self.conveyor == 0:

            # Condition to exclude those boxes that are carried at the moment, broken or delivered
            if not self.carried or not self.broken or not self.delivered:
                # Condition added to prevent overlapping with the middle column
                if self.position == 4:
                    self.position = 8
                    if self.conveyor == 0 or self.conveyor % 2 != 0:
                        self.x -= 32
                    else:
                        self.x += 32
                else:
                    if self.conveyor == 0 or self.conveyor % 2 != 0:
                        self.x -= 8
                    else:
                        self.x += 8
                    self.position += 1
                print(f"{self} moved to {self.position}")

    # Move odd boxes
    def move_odd_box(self):
        # Condition to only include the boxes in the initial conveyor
        if self.conveyor % 2 != 0:

            # Condition to exclude those boxes that are carried at the moment, broken or delivered
            if not self.carried or not self.broken or not self.delivered:
                # Condition added to prevent overlapping with the middle column
                if self.position == 4:
                    self.position = 8
                    if self.conveyor == 0 or self.conveyor % 2 != 0:
                        self.x -= 32
                    else:
                        self.x += 32
                else:
                    if self.conveyor == 0 or self.conveyor % 2 != 0:
                        self.x -= 8
                    else:
                        self.x += 8
                    self.position += 1
                print(f"{self} moved to {self.position}")

    # Move even boxes
    def move_even_box(self):
        # Condition to only include the boxes in the initial conveyor
        if self.conveyor % 2 == 0:

            # Condition to exclude those boxes that are carried at the moment, broken or delivered
            if not self.carried or not self.broken or not self.delivered:
                # Condition added to prevent overlapping with the middle column
                if self.position == 4:
                    self.position = 8
                    if self.conveyor == 0 or self.conveyor % 2 != 0:
                        self.x -= 32
                    else:
                        self.x += 32
                else:
                    if self.conveyor == 0 or self.conveyor % 2 != 0:
                        self.x -= 8
                    else:
                        self.x += 8
                    self.position += 1
                print(f"{self} moved to {self.position}")

    """ Principal method of the conveyors logic: used to check whether the character and the box meet the requirements 
    to pass the box into the next conveyor """
    def pick_box(self):
        # Condition triggered most of the time when the box is moving through the conveyors
        if self.conveyor != values.maxBelts:
            # Conveyor0
            if self.conveyor == 0:
                # The conditions between the Mario and the box being in the same floor is met
                if self.position == 4 and values.MarioCurrentFloor == 0:
                    self.carried = True
                    values.MarioCarryingBox = True
                    self.conveyor = 1
                    self.position = 0
                    self.x = 170
                    self.y = 152
                    print(f"{self} carried!")

                    # Add one point to the score
                    values.score += 1

                    # Play box sound
                    pyxel.play(1, 1)

                # Condition when the package doesn't reach the extreme of the belt
                elif self.position != 4:
                    print(f"{self} continue moving")

                # The conditions between the Mario and the box being in the same floor aren't met
                else:
                    self.failed_box()

            # Even conveyor
            elif self.conveyor % 2 == 0:
                # The conditions between the Mario and the box being in the same floor is met
                if self.position == 12 and values.MarioCurrentFloor == self.floor:
                    self.carried = True
                    values.MarioCarryingBox = True
                    self.conveyor += 1
                    self.position = 0
                    self.y -= 16
                    print(f"{self} carried!")

                    # Add one point to the score
                    values.score += 1

                    # Play box sound
                    pyxel.play(1, 1)

                # Condition when the package doesn't reach the extreme of the belt
                elif self.position != 12:
                    print(f"{self} continue moving")

                # The conditions between the Mario and the box being in the same floor aren't met
                else:
                    self.failed_box()

            # Odd conveyor
            elif self.conveyor % 2 != 0:
                # The conditions between the Luigi and the box being in the same floor is met
                if self.position == 12 and values.LuigiCurrentFloor == self.floor:
                    self.carried = True
                    values.LuigiCarryingBox = True
                    self.floor += 1
                    self.conveyor += 1
                    self.position = 0
                    self.y -= 16
                    print(f"{self} carried!")

                    # Add one point to the score
                    values.score += 1

                    # Play box sound
                    pyxel.play(1, 1)

                # Condition when the package doesn't reach the extreme of the belt
                elif self.position != 12:
                    print(f"{self} continue moving")

                # The conditions between the Mario and the box being in the same floor aren't met
                else:
                    self.failed_box()

        # Condition when the box reaches the final floor and it's about to get delivered.
        else:
            if self.position == 12 and values.LuigiCurrentFloor == self.floor:
                self.carried = True
                self.delivered = True
                values.LuigiCarryingBox = True
                print(f"{self} delivered to the truck!")

                # Add one point to the score
                values.score += 1
                values.minPackagesCounter += 1

                # Play box sound
                pyxel.play(1, 1)

            # Condition when the package doesn't reach the extreme of the final belt
            elif self.position != 12:
                print(f"{self} continue moving")

            # The conditions between the Mario and the box being in the same floor aren't met
            elif not self.broken:
                self.failed_box()

    " Method triggered when the character and box floor is not met"
    def failed_box(self):
        self.broken = True
        self.y = 184

        # Not picked up box in the conveyor0
        if self.conveyor == 0:
            self.x = 208
        # Not picked up box in an even conveyor
        elif self.conveyor % 2 == 0:
            self.x = 176
        # Not picked up box in an odd conveyor
        elif self.conveyor % 2 != 0:
            self.x = 72

        # Call out the boss
        values.activeBrokenBox = True
        values.activeFailure = True

        # Play broken box effect
        pyxel.play(1, 2)

        # Add a fail to the counter
        values.fails += 1
        print(f"{self} failed box!")

    " Method used to remove of the game all the broken boxes "
    def remove_broken_box(self):
        if self.broken:
            boxes.remove(self)
            print(f"{self} removed!")

    " Method used to return the characters to the default sprite after moving a package"
    def update_carrying_state(self):
        if self.conveyor == 0 or self.conveyor % 2 == 0:
            if not values.MarioCarryingBox:
                self.carried = False
        else:
            if not values.LuigiCarryingBox:
                self.carried = False

    " Method used to change the stage of the box depending in which conveyor is or if it's broken "
    def update_sprite_stage(self):
        if not self.broken:
            if self.conveyor == 0:
                self.sprite = values.package1
            elif self.conveyor == 1:
                self.sprite = values.package2
            elif self.conveyor == 2:
                self.sprite = values.package3
            elif self.conveyor == 3:
                self.sprite = values.package4
            else:
                self.sprite = values.package5
        else:
            self.sprite = values.brokenBox

    " Properties and setters "
    # Validate that the x and y coordinates return the correct values inside the board dimensions.
    # Prevents objects being out of the game margins
    @property
    def x(self): return self.__x
    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError("x must be an integer")
        if x < 0:
            raise ValueError("x must be positive")
        self.__x = x

    @property
    def y(self): return self.__y
    @y.setter
    def y(self, y: int):
        if not isinstance(y, int):
            raise TypeError("y must be an integer")
        if y < 0:
            raise ValueError("y must be positive")
        self.__y = y