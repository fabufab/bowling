import pytest

class GameFinishedError(Exception):
    def __init__(self, message="Game Finished. No more rolls allowed!"):
        super().__init__(message)

class InvalidPinsError(Exception):
    def __init__(self, message="Can only register rolls with [0..10] pins!"):
        super().__init__(message)

class Game:
    def __init__(self):
        self.rolls = []
        self.frames = []
        self.gameFinished = False

    def addRoll(self, pins):
        if pins < 0 or pins > 10:
            raise InvalidPinsError()
        if len(self.frames) == 10:
            raise GameFinishedError()

        self.rolls.append(pins)
        self.updateFrames()

    def calculateScore(self):
        score = 0
        frameIndex = 0
        for frame in range(10):
            if self.rolls[frameIndex] == 10: # strike
                score += 10 + self.rolls[frameIndex+1] + self.rolls[frameIndex+2]
                frameIndex += 1
            elif self.rolls[frameIndex] + self.rolls[frameIndex+1] == 10: # spare
                score += 10 + self.rolls[frameIndex+2]
                frameIndex += 2
            else:
                score += self.rolls[frameIndex] + self.rolls[frameIndex+1]
                frameIndex += 2
        return score

    def updateFrames(self):
        frames = []
        rollIndex = 0
        for roll in range(len(self.rolls)):
            if self.rolls[roll] == 10: # strike
                frame = Frame()
                frame.pinsRolled = [10]
                if len(self.rolls) - roll - 1 == 0:
                    frame.score = 10
                elif len(self.rolls) - roll - 1 == 1:
                    frame.score = 10 + self.rolls[roll+1]
                elif len(self.rolls) - roll - 1 > 1:
                    frame.score = 10 + self.rolls[roll+1] + self.rolls[roll+2]
                frames.append(frame)
        # TODO: Add code for spares and regular rolls
        self.frames = frames

    def __str__(self):
        text = ""
        for i in range(len(self.frames)):
            text += str(self.frames[i]) + ", "
        return text

class Frame:
    def __init__(self):
        self.pinsRolled = []
        self.score = 0

    def __str__(self):
        text = "(" + str(self.pinsRolled) + "," + str(self.score) + ")"
        return text

class TestClass:
    def testAllZeros(self):
        g = Game()
        self.rollMany(g, 20, 0)
        assert g.calculateScore() == 0

    def testAllOnes(self):
        g = Game()
        self.rollMany(g, 20, 1)
        assert g.calculateScore() == 20

    def testNumFrames(self):
        g = Game()
        self.rollMany(g, 10, 10)
        print(g)
        assert len(g.frames) == 10

    def testOneSpare(self):
        g = Game()
        g.addRoll(5)
        g.addRoll(5) # spare
        g.addRoll(3)
        self.rollMany(g, 17, 0)
        assert g.calculateScore() == 16

    def testOneStrike(self):
        g = Game()
        g.addRoll(10) # strike
        g.addRoll(3)
        g.addRoll(3)
        self.rollMany(g, 17, 0)
        assert g.calculateScore() == 22

    def testPerfectGame(self):
        g = Game()
        self.rollMany(g, 12, 10)
        assert g.calculateScore() == 300

    def testGameFinishes(self):
        with pytest.raises(GameFinishedError):
            g = Game()
            self.rollMany(g, 30, 3)

    def testMaxTenPins(self):
        with pytest.raises(InvalidPinsError):
            g = Game()
            g.addRoll(11)

    def testNoNegativePins(self):
        with pytest.raises(InvalidPinsError):
            g = Game()
            g.addRoll(-1)

    def rollMany(self, game, numberOfRolls, pins):
        for i in range(numberOfRolls):
            game.addRoll(pins)
