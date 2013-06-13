import json
from random import *
from sys import *


class PsychicMonkey:

    def __init__(self, home, vis):
        f = open('data/matchups/' + vis + '_' + home + '.dat')
        self.transitions = json.loads(f.read())
        f.close()

        ## TODO: read pitcher info

        ## TODO: read game-level info


    def runSim(self, ngames):
        scores = []
        for i in range(0, ngames):
            hscore, vscore = self.simGame()
            scores.append(vscore - hscore)

        return scores


    def simGame(self):
        score = {'h':0, 'v':0}
        atbat = 'v'
        inning = 1
        state = (0,0)
        while inning <=9 and (atbat == 'v' or not score['h'] == score['v']):
            state, new_score = self.weighted_choice(self.transitions[state])
            score[atbat] += new_score

            if state == (0,3):
                if atbat == 'v':
                    atbat = 'h'
                elif atbat == 'h':
                    atbat = 'v'
                    inning += 1
                state = (0,0)

        return score['h'], score['v']


    def weighted_choice(self, options):
        n = random()
        count = 0.0
        for next_state in options:
            count += options[next_state]['prob']
            if count >= n:
                return next_state, options[next_state]['score']

        return None, None


if __name__ == "__main__":
    home = argv[1]
    vis = argv[2]
    ngames = int(argv[3])

    jimmy = PsychicMonkey(home, vis)
    print jimmy.runSim(ngames)






