# Scripts backlinks
import values
import pyxel

class Character:
    def __init__(self, x: int, y: int, identity: str, sprite: tuple):
        # Attributes to locate the character in the board
        self.x = x
        self.y = y
        self.identity = identity
        self.sprite = sprite
        # Private attributes, to locate and move the character between floors
        self.floor = 0
        self.floor_height = 32

    " Methods "
    # Method used to move the character between floors
    def move(self, direction: str):
        if direction == "up":
            if self.floor < values.maxFloors:
                self.floor += 1
                self.y -= self.floor_height
                # Sound effect
                pyxel.play(1, 3)
        elif direction == "down":
            if self.floor > 0:
                self.floor -= 1
                self.y += self.floor_height
                # Sound effect
                pyxel.play(1, 3)

    # Method used to get the current floor of the character (useful for the conveyor logic)
    def get_floor(self):
        return self.floor

    " Properties and setters "
    # Validate that the x and y coordinates return the appropiate values.
    @property
    def x(self):
        return self.__x
    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError("x must be an integer")
        if x < 0:
            raise ValueError("x must be positive")
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

" Subclasses for each character, inheriting the attributes and methods that correspond to each one "
# In attributes, they inherit the x and y coordinates in the board, the identifier and the sprite.
# The boss has it's unique attribute "failure" that triggers the boss appearance.
# In methods they inherit move() except the boss.
class Mario(Character):
    def __init__(self, x, y):
        super().__init__(x, y, "Mario", values.MarioStill)

    def move(self, direction: str):
        super().move(direction)

class Luigi(Character):
    def __init__(self, x, y):
        super().__init__(x, y, "Luigi", values.LuigiStill)

    def move(self, direction: str):
        super().move(direction)

class Boss(Character):
    def __init__(self, x, y, trigger_appearance: bool):
        super().__init__(x, y, "Boss", values.Boss)
        self.trigger_appearance = trigger_appearance


