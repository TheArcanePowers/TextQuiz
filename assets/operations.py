#!/usr/bin/env python3
import json
import sys
import random
from codecs import decode, encode
import uu
from .PP import PPrint  # Pretty printing


class shuffle():
    def __init__(self, filename):
        self.filename = filename
        self.newdata = {}
        self.temporarydata = {}
        with open(self.filename, "r") as f:
            enc_json = f.read()
            unenc_json = decode(enc_json, "rot_13")
            self.olddata = json.loads(unenc_json)
        self.temporarydata = self.olddata

    def questions(self):
        PPrint("Shuffling questions...", "module")
        takennumbers = []
        for i in range(1, self.temporarydata["totalQuestions"] + 1):
            oldquestiondata = self.temporarydata[f"Question{i}"]
            questionNum = random.randint(
                1, self.temporarydata["totalQuestions"])  # generate random number
            while questionNum in takennumbers:  # if its taken, regenerate
                questionNum = random.randint(
                    1, self.temporarydata["totalQuestions"])
            takennumbers.append(questionNum)
            self.newdata[f"Question{str(questionNum)}"] = oldquestiondata

    def answers(self):
        PPrint("Shuffling answers...", "module")
        for i in range(1, self.olddata["totalQuestions"] + 1):
            oldquestiondata = self.temporarydata[f"Question{i}"]
            options = oldquestiondata["options"]
            # find correct answer
            # minus one because user wants 1,2,3. computer starts list at 0.
            answer = options[oldquestiondata["answerNum"] - 1]
            random.shuffle(options)
            # find new answer location
            # again human vs computer list counting
            answerNum = options.index(answer) + 1
            # reform question
            self.newdata[f"Question{str(i)}"] = {"question": oldquestiondata["question"], "options": options, "answerNum": answerNum,
                                                 "hintAvailable": oldquestiondata["hintAvailable"], "hintMessage": oldquestiondata["hintMessage"]}

    def both(self):
        PPrint("Shuffling both questions and answers:", "module")
        shuffle.questions(self)  # temporary(old)-> new(half done)
        # new(half done) -> temporary(half done)
        self.temporarydata = self.newdata
        self.newdata = {}  # new(clear), temporary(halfdone), old(old)
        shuffle.answers(self)  # temporary(halfdone) -> new(done)
        shuffle.write(self)  # new(done) + old[totalQuestions]

    def write(self):
        self.newdata["totalQuestions"] = self.olddata["totalQuestions"]
        with open(self.filename, 'w') as f:
            enc_data = encode(json.dumps(self.newdata), "rot_13")
            f.write(enc_data)
