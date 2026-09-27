" Libraries and project scripts conexions -------- "
# Import the pyxel library
import pyxel
# Import the project scripts
import configuration
import conveyors
import values
from characters import Mario, Luigi, Boss
from conveyors import boxes
from truck import Truck
" ------------------------------------------------ "

class Board:
    def __init__(self, width: int, height: int):
        # Board dimensions
        self.width = width
        self.height = height

        " Include characters and objects in the board"
        # Characters
        self.mario = Mario(184, 160)
        self.luigi = Luigi(56, 144)
        self.boss = Boss(225, 24, values.activeFailure)
        # Truck
        self.truck = Truck(10, 96)
        # Boxes
        self.boxes = boxes

        " Pyxel functions to initialize the board"
        # Pyxel board
        pyxel.init(self.width, self.height, title="Game & Watch: Mario Bros. (1983)")
        # Pyxel load sprites
        pyxel.load("assets/resources.pyxres")
        # Pyxel run sprites
        pyxel.run(self.update, self.draw)

    " Properties and setters "
    # Validate that the width and height return the correct values.
    @property
    def width(self) -> int: return self.__width
    @width.setter
    def width(self, width: int):
        if not isinstance(width, int):
            raise TypeError("The width must be an integer " + str(type(width)) + "is provided")
        elif width < 1 or width > values.WIDTH:
            raise ValueError("The width must be in the range 1 to 256")
        else:
            self.__width = width

    @property
    def height(self) -> int: return self.__height
    @height.setter
    def height(self, height: int):
        if not isinstance(height, int):
            raise TypeError("The height must be an integer " + str(type(height)) + "is provided")
        elif height < 1 or height > values.HEIGHT:
            raise ValueError("The height must be in the adequate range")
        else:
            self.__height = height

    "Pyxel method that gets executed in every iteration of the game (every frame). UPDATES THE GAME LOGIC."
    def update(self):
        # To exit the game (escape button)
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        # MAIN GAME LOGIC
        if values.active_game:

            # GAME OVER LOGIC
            if values.fails == 3:
                # Play the game over sound
                if values.gameOverSound:
                    pyxel.play(1, 4)
                    values.gameOverSound = False

                # Method to return to the main page
                if pyxel.btn(pyxel.KEY_SPACE):
                    values.active_game = False
                    values.already_played = True

                    # Reset all the counters
                    values.last_score = values.score
                    values.fails = 0
                    values.score = 0

                    # Clean all the map objects
                    self.boxes = []

                    # Reset all the characters positions
                    self.luigi.x, self.luigi.y, self.luigi.floor = 56, 144, 0
                    self.mario.x, self.mario.y, self.mario.floor = 184, 160, 0

                    # Make the boss disappear
                    values.activeFailure = False

            # GAME RUNNING ON NORMAL CONDITIONS
            else:

                # Condition when a package breaks
                if self.boss.trigger_appearance:

                    # Timer to make the boss stay in more frames and then disappear
                    if values.changeBossSprite == 200:
                        values.activeFailure = False
                        self.boss.trigger_appearance = values.activeFailure
                        values.changeBossSprite = 0

                        # Removes all the broken boxes in the game
                        for box in self.boxes[:]:
                            box.remove_broken_box()

                    values.changeBossSprite += 1

                # MARIO CARRYING BOX
                if values.MarioCarryingBox:

                    # When Mario is in the conveyor0
                    if self.mario.get_floor() == 0:
                        if values.changeMarioSprite == 60:
                            self.mario.sprite = values.MarioPickingRight
                            values.MarioCarryingBox = False
                            values.changeMarioSprite = 0
                        elif values.changeMarioSprite > 40:
                            self.mario.sprite = values.MarioDeliveringPackageLeft
                        elif values.changeMarioSprite > 2:
                            self.mario.sprite = values.MarioDeliveringPackageLeft
                        else:
                            self.mario.sprite = values.MarioPickingRight

                    # When Mario is in the even conveyors
                    else:
                        if values.changeMarioSprite == 60:
                            self.mario.sprite = values.MarioPickingLeft
                            values.MarioCarryingBox = False
                            values.changeMarioSprite = 0
                        elif values.changeMarioSprite > 40:
                            self.mario.sprite = values.MarioDeliveringPackageLeft
                        elif values.changeMarioSprite > 2:
                            self.mario.sprite = values.MarioPickingPackageLeft
                        else:
                            self.mario.sprite = values.MarioPickingLeft

                    values.changeMarioSprite += 1

                    # Luigi movement (Mario can't move during package carrying)
                    if pyxel.btnp(pyxel.KEY_W):
                        self.luigi.move("up")
                    elif pyxel.btnp(pyxel.KEY_S):
                        self.luigi.move("down")

                # LUIGI CARRYING BOX
                if values.LuigiCarryingBox:

                    # When Luigi is in the odd conveyors
                    if self.luigi.get_floor() != values.maxFloors:
                        if values.changeLuigiSprite == 60:
                            self.luigi.sprite = values.LuigiStill
                            values.LuigiCarryingBox = False
                            values.changeLuigiSprite = 0
                        elif values.changeLuigiSprite > 40:
                            self.luigi.sprite = values.LuigiDeliveringRight
                        elif values.changeLuigiSprite > 2:
                            self.luigi.sprite = values.LuigiPickingPackageRight
                        else:
                            self.luigi.sprite = values.LuigiPickingRight

                    # When Luigi delivers packages to the truck
                    else:
                        if values.changeLuigiSprite == 60:
                            self.luigi.sprite = values.LuigiStill
                            values.LuigiCarryingBox = False
                            values.changeLuigiSprite = 0
                        elif values.changeLuigiSprite > 40:
                            self.luigi.sprite = values.LuigiDeliveringLeft
                        elif values.changeLuigiSprite > 2:
                            self.luigi.sprite = values.LuigiPickingPackageRight
                        else:
                            self.luigi.sprite = values.LuigiPickingRight

                    values.changeLuigiSprite += 1

                    # Mario movement (Luigi can't move during package carrying)
                    if pyxel.btnp(pyxel.KEY_UP):
                        self.mario.move("up")
                    elif pyxel.btnp(pyxel.KEY_DOWN):
                        self.mario.move("down")

                # GAME RUNNING ON NORMAL CONDITIONS (only when both characters are NOT carrying)
                if not values.MarioCarryingBox and not values.LuigiCarryingBox:

                    # Boxes movement through conveyors
                    if not self.truck.leaving:

                        # Conveyor0 counter
                        if values.initialSpeedCounter == values.initialSpeed:
                            for box in self.boxes[:]:
                                box.move_0_box()
                                box.pick_box()
                                box.update_carrying_state()
                                box.update_sprite_stage()

                                # Checks if the box is delivered to add it to the truck
                                if box.delivered:
                                    self.truck.add_package()
                                    self.boxes.remove(box)

                            values.initialSpeedCounter = 0
                        values.initialSpeedCounter += 1

                        # Odd conveyor counter
                        if values.oddSpeedCounter == values.oddSpeed:
                            for box in self.boxes[:]:
                                box.move_odd_box()
                                box.pick_box()
                                box.update_carrying_state()
                                box.update_sprite_stage()

                                # Checks if the box is delivered to add it to the truck
                                if box.delivered:
                                    self.truck.add_package()
                                    self.boxes.remove(box)

                            values.oddSpeedCounter = 0
                        values.oddSpeedCounter += 1

                        # Even conveyor counter
                        if values.evenSpeedCounter == values.evenSpeed:
                            for box in self.boxes[:]:
                                box.move_even_box()
                                box.pick_box()
                                box.update_carrying_state()
                                box.update_sprite_stage()

                                # Checks if the box is delivered to add it to the truck
                                if box.delivered:
                                    self.truck.add_package()
                                    self.boxes.remove(box)

                            values.evenSpeedCounter = 0
                        values.evenSpeedCounter += 1

                        # Conditions that enables a minimum number of packages during the game
                        if values.minPackages > len(self.boxes):
                            if values.spawnBoxTimer == values.spawnBoxDelay:
                                new_box = conveyors.Box(238, 168, values.package1)
                                conveyors.boxes.append(new_box)
                                print("Box spawned!")
                                values.spawnBoxTimer = 0
                            values.spawnBoxTimer += 1

                        # Characters dynamic
                        # Mario movement
                        if pyxel.btnp(pyxel.KEY_UP):
                            self.mario.move("up")
                        elif pyxel.btnp(pyxel.KEY_DOWN):
                            self.mario.move("down")
                        #Update Mario sprite according to floor (if not carrying box)
                        if self.mario.get_floor() == 0:
                            self.mario.sprite = values.MarioPickingRight
                        else:
                            self.mario.sprite = values.MarioPickingLeft

                        # Luigi movement
                        if pyxel.btnp(pyxel.KEY_W):
                            self.luigi.move("up")
                        elif pyxel.btnp(pyxel.KEY_S):
                            self.luigi.move("down")

                    # BREAK TIME CONDITION
                    else:
                        self.truck.update_state()

                    # Constant update of Mario and Luigi floor level, needed for conveyor logic
                    values.LuigiCurrentFloor = self.luigi.get_floor()
                    values.MarioCurrentFloor = self.mario.get_floor()

                    # Constant update in boss trigger condition
                    self.boss.trigger_appearance = values.activeFailure

                    # Constant update of the minimum number of packages (depends on difficulty)
                    if values.difficultIndex == 0:
                        if values.minPackagesCounter == 50:
                            values.minPackages += 1
                            values.minPackagesCounter = 0
                    elif values.difficultIndex == 1 or values.difficultIndex == 2:
                        if values.minPackagesCounter == 30:
                            values.minPackages += 1
                            values.minPackagesCounter = 0
                    else:
                        if values.minPackagesCounter == 20:
                            values.minPackages += 1
                            values.minPackagesCounter = 0

        # MAIN MENU LOGIC
        else:

            # Scroll between difficulties (keys that control Mario and Luigi)
            if (pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W)) and values.difficultIndex > 0:
                for i in range(3):
                    values.difficultList[i] = False
                values.difficultIndex -= 1
                values.difficultList[values.difficultIndex] = True

                # Sound effect
                pyxel.play(1, 1)

            elif (pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S)) and values.difficultIndex < 3:
                for i in range(3):
                    values.difficultList[i] = False
                values.difficultIndex += 1
                values.difficultList[values.difficultIndex] = True

                # Sound effect
                pyxel.play(1, 1)

            # Select difficulty (Space key)
            elif pyxel.btnp(pyxel.KEY_SPACE):
                configuration.Configuration(values.difficultIndex).selectDifficulty()
                values.active_game = True

    """Pyxel method that gets executed in every iteration of the game (every frame). 
    Draws the current state of each class involved in the game"""
    def draw(self):
        # Erasing the previous screen
        pyxel.cls(0)
        # Draw the tilemaps depending on the condition (Main menu, game, game over)
        # If the game isn't active, it will display the menu tilemap
        if values.active_game:
            # Game over condition
            if values.fails == 3:
                pyxel.bltm(0, 0, 3, 0, 0, self.width, self.height)
                pyxel.blt(95, 75, *values.gameOverLetters)

            # Main game condition
            else:
                " Drawing the main tilemap depending on the difficulty "
                # Easy and crazy difficulty (two floors)
                if values.difficultIndex == 0 or values.difficultIndex == 3:
                    pyxel.bltm(0, 0, 2, 0, 0, self.width, self.height)
                # Medium difficulty (three floors)
                elif values.difficultIndex == 1:
                    pyxel.bltm(0, 0, 1, 0, 0, self.width, self.height)
                # Crazy difficulty (Four floors)
                else:
                    pyxel.bltm(0, 0, 0, 0, 0, self.width, self.height)

                " Drawing the icons"
                # Drawing the failures icons
                if values.fails == 0:
                    for i in range(3):
                        pyxel.blt(values.failureX, 20, *values.failureSpace)
                        values.failureX -= 12
                    values.failureX = 236
                elif values.fails == 1:
                    for i in range(3):
                        if i == 0:
                            pyxel.blt(values.failureX, 20, *values.failureCount)
                            values.failureX -= 12
                        else:
                            pyxel.blt(values.failureX, 20, *values.failureSpace)
                            values.failureX -= 12
                    values.failureX = 236
                elif values.fails == 2:
                    for i in range(3):
                        if i < 2:
                            pyxel.blt(values.failureX, 20, *values.failureCount)
                            values.failureX -= 12
                        else:
                            pyxel.blt(values.failureX, 20, *values.failureSpace)
                            values.failureX -= 12
                    values.failureX = 236

                # Drawing the score counter
                scoreX = 236
                score_str = str(abs(values.score))
                for digit in reversed(score_str):
                    pyxel.blt(scoreX, 10, *values.NumberIcon[int(digit)])
                    scoreX -= 8

                # Drawing the current difficulty in the game
                pyxel.blt(10, 10, *values.difficultyLetters[values.difficultIndex])

                " Drawing the current boxes circulating"
                for i in range(len(self.boxes)):
                    if not self.boxes[i].carried and not self.boxes[i].delivered:
                        pyxel.blt(self.boxes[i].x, self.boxes[i].y, *self.boxes[i].sprite)

                " Drawing the truck PENDING condition when it's in delivery to disappear"
                # Draw the vehicle
                pyxel.blt(self.truck.x, self.truck.y, *self.truck.sprite)

                # Draw the current cargo
                deliveredBoxX = 24
                deliveredBoxY = 102
                floorPackagesCount = 0
                for i in range(self.truck.current_load):
                    # This conditions makes the truck to accumulate boxes two by two
                    if floorPackagesCount == 2:
                        floorPackagesCount = 0
                        deliveredBoxY -= 7
                        deliveredBoxX = 24
                    pyxel.blt(deliveredBoxX, deliveredBoxY, *values.package5)
                    deliveredBoxX += 8
                    floorPackagesCount += 1

                " Drawing the character, parameters of pyxel.blt are (x, y, *sprite tuple) "
                # Positions when difficulty is easy or crazy
                marioYelledY = 32
                luigiYelledY = 32
                bossY = 24
                if values.difficultIndex == 3 or values.difficultIndex == 0:
                    marioYelledY = 96
                    luigiYelledY = 96
                    bossY = 80
                # Positions when difficulty is medium
                elif values.difficultIndex == 1:
                    marioYelledY = 64
                    luigiYelledY = 64
                    bossY = 56
                # Positions when difficulty is hard
                elif values.difficultIndex == 2:
                    marioYelledY = 32
                    luigiYelledY = 32
                    bossY = 32

                # Drawing the boss appearance condition
                if self.boss.trigger_appearance:
                    # Method to wait a certain amount of time to change the sprite
                    if values.changeBossSprite > 20:
                        self.boss.sprite = values.BossAngry
                        pyxel.blt(self.boss.x, bossY, *self.boss.sprite)
                        pyxel.blt(184, marioYelledY, *values.MarioCrying)
                        pyxel.blt(200, luigiYelledY, *values.LuigiCrying)
                    else:
                        pyxel.blt(self.boss.x, bossY, *self.boss.sprite)
                        pyxel.blt(184, marioYelledY, *self.mario.sprite)
                        pyxel.blt(200, luigiYelledY, *self.luigi.sprite)

                # Drawing the break time condition
                elif self.truck.leaving:
                    pyxel.blt(self.mario.x - 2, 160, *values.MarioResting)
                    pyxel.blt(15, 168, *values.LuigiResting)

                # Drawing the game condition
                else:
                    pyxel.blt(self.mario.x, self.mario.y, *self.mario.sprite)
                    pyxel.blt(self.luigi.x, self.luigi.y, *self.luigi.sprite)

        # Introduction to game board condition (not active_game)
        else:
            # Introduction to game board
            pyxel.bltm(0,0,3,0,0, self.width, self.height)
            pyxel.blt(40,25, *values.gameTitle)
            pyxel.blt(40, 70, *values.selectDifficultyLetters)

            # Change the difficulty letters sprites depending on which one is selected
            if values.difficultList[0]:
                pyxel.blt(40, 86, *values.difficultyLettersSelected[0])
                pyxel.blt(40, 96, *values.difficultyLetters[1])
                pyxel.blt(40, 106, *values.difficultyLetters[2])
                pyxel.blt(40, 116, *values.difficultyLetters[3])
            elif values.difficultList[1]:
                pyxel.blt(40, 86, *values.difficultyLetters[0])
                pyxel.blt(40, 96, *values.difficultyLettersSelected[1])
                pyxel.blt(40, 106, *values.difficultyLetters[2])
                pyxel.blt(40, 116, *values.difficultyLetters[3])
            elif values.difficultList[2]:
                pyxel.blt(40, 86, *values.difficultyLetters[0])
                pyxel.blt(40, 96, *values.difficultyLetters[1])
                pyxel.blt(40, 106, *values.difficultyLettersSelected[2])
                pyxel.blt(40, 116, *values.difficultyLetters[3])
            else:
                pyxel.blt(40, 86, *values.difficultyLetters[0])
                pyxel.blt(40, 96, *values.difficultyLetters[1])
                pyxel.blt(40, 106, *values.difficultyLetters[2])
                pyxel.blt(40, 116, *values.difficultyLettersSelected[3])

            # Draw the last score if already played before
            if values.already_played:
                pyxel.blt(40, 155, *values.lastScoreLetters)
                scoreX = 200
                last_score_str = str(abs(values.last_score))
                for digit in reversed(last_score_str):
                    pyxel.blt(scoreX, 155, *values.NumberIcon[int(digit)])
                    scoreX -= 8