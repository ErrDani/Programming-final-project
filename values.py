# Board dimensions
WIDTH=256
HEIGHT=208

" CHARACTERS "
" Characters: Mario "
# Mario sprites
MarioStill = (0,0,0,16,16)
MarioPickingRight = (0, 16, 0, 16, 16)
MarioPickingLeft = (0, 32, 0, 16, 16)
MarioPickingPackageRight = (0, 0, 48, 16, 16)
MarioPickingPackageLeft = (0, 32, 48, 16, 16)
MarioDeliveringPackageLeft = (0, 0, 64, 16, 16)
MarioCrying = (0, 0, 80, 16, 16)
MarioResting = (0, 0, 96, 16, 16)

MarioCurrentFloor = 0
MarioCarryingBox = False
MarioCurrentBox = 0
changeMarioSprite = 0

" Characters: Luigi "
# Luigi sprites
LuigiStill = (0, 16, 16, 16, 16)
LuigiPickingRight = (0, 16, 16, 16, 16)
LuigiPickingPackageRight = (0, 16, 48, 16, 16)
LuigiPickingPackageLeft = (0, 48, 48, 16, 16)
LuigiDeliveringLeft = (0, 16, 64, 16, 16)
LuigiDeliveringRight = (0, 32, 64, 16, 16)
LuigiCrying = (0, 16, 80, 16, 16)
LuigiResting = (0, 16, 96, 16, 16)

# Luigi values
LuigiCurrentFloor = 0
LuigiCarryingBox = False
LuigiCurrentBox = 0
changeLuigiSprite = 0

" Characters: Boss"
# Boss sprites
Boss = (0, 0, 32, 16, 16)
BossAngry = (0, 16, 32, 16, 16)

# Boss values
activeFailure = False # Triggers the boss appearance
changeBossSprite = 0 # This is used to alternate sprites during the game depending on if the number is odd or even

" OBJECTS "
" Packages "
# Packages sprites
package1 = (1, 16, 0, 8, 8)
package2 = (1, 8, 0, 8, 8)
package3 = (1, 0, 8, 8, 8)
package4 = (1, 8, 8, 8, 8)
package5 = (1, 0, 0, 8, 8)
brokenBox = (1, 24, 8, 8, 8)

" Truck "
# Tuck sprite
TruckSprite = (2, 0, 112, 33, 24)

" Letters and numbers "
gameTitle = (1, 0, 184, 176, 36)
gameOverLetters = (1, 0, 32, 64, 32)
selectDifficultyLetters = (1, 0, 224, 50, 8)
lastScoreLetters = (1, 56, 224, 90, 8)

" Icons "
pointSymbol = (1, 24, 0, 8, 8)

failureSpace = (1, 8, 16, 8, 8)
failureCount =  (1, 0, 16, 8, 8)
failureX = 236

" Numbers "
# Each index is each number: NumberIcon[0] = 0 *sprite
NumberIcon = {
    0: (1, 24, 240, 8, 8),
    1: (1, 0, 232, 8, 8),
    2: (1, 8, 232, 8, 8),
    3: (1, 16, 232, 8, 8),
    4: (1, 24, 232, 8, 8),
    5: (1, 32, 232, 8, 8),
    6: (1, 40, 232, 8, 8),
    7: (1, 0, 240, 8, 8),
    8: (1, 8, 240, 8, 8),
    9: (1, 16, 240, 8, 8)
}

" Music playing "
gameMusic = False
bossAppearsMusic = True

" Sounds playing"
gameOverSound = False

" Counters and stats "
# Main game
fails = 0
score = 0
active_game = False # Bool that triggers whether the game is active or not

# Last game stats
last_score = 0
already_played = False

" Difficulty settings "
difficultIndex = 0
# 0: easy, 1: medium, 2: extreme, 3: crazy
difficultList = {
    0: True,
    1: False,
    2: False,
    3: False
}

# Easy[0], medium[1], difficult[2], crazy[3]
difficultyLetters = ((1, 0, 96, 36, 8), (1, 0, 104, 48, 8), (1, 0, 112, 64, 8), (1, 0, 120, 38, 8))
difficultyLettersSelected = ((1, 0, 136, 32, 8), (1, 0, 144, 48, 8), (1, 0, 152, 64, 8), (1, 0, 160, 38, 8))

" Elements that depend on difficulty "
maxFloors = 4
maxBelts = 9

minPackages = 1
minPackagesCounter = 0

# Spawn box speed (always x1)
spawnBoxDelay = 300
spawnBoxTimer = 0 # A counter used to spawn boxes with a determined frequency

# Conveyor0 speed (always x1)
initialSpeed = 40 #x1
initialSpeedCounter = 0 # A counter used to move boxes with a determined frequency

# Odd conveyor speed
oddSpeed = 40 #x1
oddSpeedCounter = 0 # A counter used to move boxes with a determined frequency

# Even conveyor speed
evenSpeed = 40 #x1
evenSpeedCounter = 0 # A counter used to move boxes with a determined frequency