from os import system
from pynput import keyboard

faithDict = {-3: "You have a deep conviction that the english language did not\
 adequately convey your sentiment",
             -2: "English is not suited to conveying emotion of this depth",
             -1: "English is not particularly amazing at conveying emotions",
             1: "English is sufficient to express this emotion",
             2: "English did a good job conveying my emotion.",
             3: "English was a brilliant conveyor of my purest emotion and \
             thought."}


class Question:
    netFaith = 0

    def add(self, someInt):
        # Make it so that 0 as netFaith can't occur once moved off of
        if self.netFaith + someInt == 0:
            if someInt < 0:
                self.netFaith = -1
            else:
                self.netFaith = 1
        else:
            self.netFaith += someInt

    def printWithNegatives(self, myInput):
        if myInput >= 0:
            return myInput
        else:
            return "negative {}".format(abs(myInput))

    def speak(self):
        system(
            'say {0}'.format(
                faithDict[self.netFaith]))


class QuestionMachine:
    maxFaith = 3
    runningTotalFaith = 0
    currentQuestion = 0
    numberOfQuestions = 3
    questions = []

    def __init__(self):
        # Initialize all the different question text somehow
        for i in range(self.numberOfQuestions):
            self.questions.append(Question())

    def __withinMaxFaith(self, newInt):
        if newInt > self.maxFaith or newInt < -self.maxFaith:
                return False
        else:
            return True

    def resetVars(self):
        for i in range(self.numberOfQuestions):
            self.questions[i].netFaith = 0
        self.currentQuestion = 0

    def increaseFaith(self):
        if self.__withinMaxFaith(
                self.questions[self.currentQuestion].netFaith + 1):

            self.questions[self.currentQuestion].add(1)
            self.questions[self.currentQuestion].speak()

        else:
            system("say you can\\'t feel any more positively \
            than the current level")

    def decreaseFaith(self):
        if self.__withinMaxFaith(
                self.questions[self.currentQuestion].netFaith - 1):

            self.questions[self.currentQuestion].add(-1)
            self.questions[self.currentQuestion].speak()
        else:
            system("say you can\\'t feel any more negatively\
             than the current level")

    def nextQuestion(self):
        if self.currentQuestion < (self.numberOfQuestions - 1):
            system(
                "say you entered faith level {} for question {}. Proceeding to\
                 question {}".format(
                    self.questions[self.currentQuestion].printWithNegatives(self.questions[self.currentQuestion].netFaith),
                    self.currentQuestion + 1, self.currentQuestion + 2))
            self.currentQuestion += 1
        else:
            system(
                "say you entered faith level {} for question {}. Language test \
                completed.".format(
                    self.questions[self.currentQuestion].printWithNegatives(self.questions[self.currentQuestion].netFaith),
                    self.currentQuestion + 1))

    def finish(self):
        # Clean up everything except our variable keeping track of global faith
        thisGameSum = 0
        for i in range(self.numberOfQuestions):
            thisGameSum += self.questions[i].netFaith

        self.runningTotalFaith += thisGameSum
        system(
            "say the sum of your positive and negative faith levels over all\
            questions comes out to {}. The total faith across all participants\
             this evening is now {}. Thank you for your participation.".format(
             self.questions[self.currentQuestion].printWithNegatives(thisGameSum), self.questions[self.currentQuestion].printWithNegatives(self.runningTotalFaith)
             ))
        self.resetVars()


myQMachine = QuestionMachine()


def on_press(key):
    try:
        print('string is {0}'.format(
            key.char))
        print(key.char)

    except AttributeError:
        print('special string is {0}'.format(
            key))
        if key == keyboard.Key.up:
            myQMachine.increaseFaith()
        if key == keyboard.Key.down:
            myQMachine.decreaseFaith()
        if key == keyboard.Key.left:
            myQMachine.nextQuestion()
        if key == keyboard.Key.right:
            myQMachine.finish()


def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
