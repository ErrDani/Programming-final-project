# Private attributes to the difficulty, sounds and music settings
import values
import random

class Configuration:
    def __init__(self, index: int):
        self.index = index
        self.difficultyMethods = (
            self.easyMode,
            self.mediumMode,
            self.extremeMode,
            self.crazyMode,
        )

    @property
    def index(self): return self.__index
    @index.setter
    def index(self, value):
        if value < 0 or value > 3:
            raise ValueError("Index must be between 0 and 3")
        self.__index = value

    def selectDifficulty(self):
        self.difficultyMethods[self.index]()

    def easyMode(self):
        values.maxFloors = 2
        values.maxBelts = 5

        #Conveyor speed
        values.oddSpeed = 40 #x1
        values.evenSpeed = 40 #x1

    def mediumMode(self):
        values.maxFloors = 3
        values.maxBelts = 7

        # Conveyor speed
        values.oddSpeed = 30 #x1.5
        values.evenSpeed = 40 #x1

    def extremeMode(self):
        values.maxFloors = 4
        values.maxBelts = 9

        # Conveyor speed
        values.oddSpeed = 20 #x2
        values.evenSpeed = 30 #x1.5

    def crazyMode(self):
        values.maxFloors = 2
        values.maxBelts = 5

        conveyorSpeeds = (40, 20) # Random x1 or x2
        # Conveyor speed
        values.oddSpeed = conveyorSpeeds[random.randint(0, 1)]
        values.evenSpeed = conveyorSpeeds[random.randint(0, 1)]
