## python modules
from copy import copy
import json
import re


FAN_MONKEY_TALK = True

class FanMonkey:

    def __init__(self):
        play_file = open('data/edges/edges.dat', 'r')
        language_file = open('data/lang/features.dat', 'r')
        self.plays = json.loads(play_file.read())
        self.features = json.loads(language_file.read())
        play_file.close()

        if FAN_MONKEY_TALK:
            print self.features

        self.newGame()


    def newGame(self):
        self.state = '0-0'
        self.inning = 1
        self.atbat = 'v'
        self.score = {'h':0, 'v':0}


    def runPlay(self, playdata):
        play_type, play = playdata
        play = play.lower()
        new_states = self.features[play_type][self.state]
        for new_state in new_states:
            isMatch = False
            for or_clause in new_states[new_state]:

                ## TODO: match with re, not in

                isMatch = isMatch or (sum(map(lambda and_clause: (and_clause in play and not and_clause[0] == '!') \
                                                              or (and_clause[0] == '!' and not and_clause[1:] in play), 
                                          or_clause)) \
                                     == len(or_clause))

            if isMatch:
                if FAN_MONKEY_TALK:
                    print '[Fan]', play, 'matched to', new_state, 'from', self.state, new_states[new_state]

                runs_scored = int(self.plays[self.state][new_state])
                self.score[self.atbat] += runs_scored

                if new_state == '0-3':
                    if FAN_MONKEY_TALK:
                        print '[Fan] switching batters'
                    self.state = '0-0'

                    if self.atbat == 'v':
                        self.atbat = 'h'
                    elif self.atbat == 'h':
                        self.atbat = 'v'
                        self.inning += 1
                        print '[Fan] inning', self.inning

                else:
                    self.state = new_state

                return new_state, runs_scored

        ## unrecognized
        if FAN_MONKEY_TALK:
            print '[Fan] play not recognized:', play_type, play, new_states
            if play_type == 'AtBat':
                exit()

        return None, None


    def getScore(self):
        return copy(self.score)

