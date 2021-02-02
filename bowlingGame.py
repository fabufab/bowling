class Game:
    def __init__(self):
        self.frames = []
        self.gameFinished = False

    def addRoll(self, pins):
        if len(self.frames) == 0 or self.frames[-1].frameFinished:
            f = Frame()
            f.addRoll(pins)
            self.frames.append(f)
        else:
            f = self.frames[-1]
            f.addRoll(pins)
        self.updatePreviousFrame(f, pins)

    def updatePreviousFrame(self, currentFrame, pins):
        if len(self.frames) > 1:
            previousFrame = self.frames[-2]
            if previousFrame.isSpare() and (len(currentFrame.pinsRolled) == 1):
                previousFrame.score += pins
            elif previousFrame.isStrike():
                print("in isStrike")
                previousFrame.score += pins

    def calculateScore(self):
        score = 0
        for i in range(len(self.frames)):
            score = score + self.frames[i].score
        return score

    def __str__(self):
        text = ""
        for i in range(len(self.frames)):
            text += str(self.frames[i]) + ", "
        return text

class Frame:
    def __init__(self):
        self.pinsRolled = []
        self.score = 0
        self.frameFinished = False

    def addRoll(self, pins):
        self.pinsRolled.append(pins)
        self.score += pins
        if self.isSpare() or self.isStrike() or len(self.pinsRolled) == 2:
            self.frameFinished = True

    def isSpare(self):
        return (len(self.pinsRolled) == 2) and (self.score >= 10)

    def isStrike(self):
        return (len(self.pinsRolled) == 1) and (self.score >= 10)

    def __str__(self):
        text = "(" + str(self.pinsRolled) + "," + str(self.score) + ", Spare: " + str(self.isSpare()) + ", Strike: " + str(self.isStrike()) + ")"
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
        self.rollMany(g, 10, 3)
        assert len(g.frames) == 5

    def testOneSpare(self):
        g = Game()
        g.addRoll(5)
        g.addRoll(5) # spare
        g.addRoll(3)
        self.rollMany(g, 17, 0)
        print(g)
        assert g.calculateScore() == 16

    def testOneStrike(self):
        g = Game()
        g.addRoll(10) # strike
        g.addRoll(3)
        g.addRoll(3)
        self.rollMany(g, 18, 0)
        print(g)
        assert g.calculateScore() == 22

    def rollMany(self, game, numberOfRolls, pins):
        for i in range(numberOfRolls):
            game.addRoll(pins)
