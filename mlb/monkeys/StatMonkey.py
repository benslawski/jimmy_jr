## python modules
import json
from copy import *
import glob

## local modules
from FanMonkey import *


STAT_MONKEY_TALK = True

class StatMonkey:

    def __init__(self):
        self.fan = FanMonkey()

        atbats = ['h', 'v']

        edge_file = open('data/edges/edges.dat', 'r')
        possible_edges = json.loads(edge_file.read())
        edge_file.close()

        self.edges = {}
        self.inState = {}
        for batter in atbats:
            self.edges[batter] = deepcopy(possible_edges)
            self.inState[batter] = dict(map(lambda k: (k, 0), possible_edges.keys()))

            for from_state in self.edges[batter]:
                for to_state in self.edges[batter][from_state]:
                    self.edges[batter][from_state][to_state] = {'count':0, 'score':self.edges[batter][from_state][to_state]}

        if STAT_MONKEY_TALK:
            print self.edges


    def recordGame(self, game_data):
        self.fan.newGame()
        batter = 'v'
        for inning in game_data['plays']:
            current_state = '0-0'

            for play in inning:
                self.inState[batter][current_state] += 1
                new_state, score = self.fan.runPlay(play)

                if not new_state:
                    if STAT_MONKEY_TALK:
                        print '[Stat] unknown play:', play
                    continue

                if new_state == '0-3' and STAT_MONKEY_TALK:
                    print '[Stat] 3 outs'

                if STAT_MONKEY_TALK:
                    print '[Stat]', play[0], current_state, '-->', new_state, score, play[1]

                self.edges[batter][current_state][new_state]['count'] += 1
                current_state = new_state

            if STAT_MONKEY_TALK:
                print '[Stat] switch batters'

            if batter == 'v':
                batter = 'h'
            if batter == 'h':
                batter = 'v'


    def getEdges(self):
        outedges = copy(self.edges)

        for batter in atbats:
            for from_state in self.edges[batter]:
                for to_state in from_state:
                    outedges[batter][from_state][to_state]['prob'] = float(outedges[batter][from_state][to_state]['count']) / float(self.inState[batter][from_state])
                    del outedges[batter][from_state][to_state]['count']

        return outedges



if __name__ == "__main__":
    DATA_PATH = 'data/games/'
    datafiles = glob.glob(DATA_PATH + '*.dat')

    stat_monkeys = {}

    for datafile in datafiles:
        home = datafile[0:3]
        vis = datafile[4:7]

        if not (home, vis) in stat_monkeys:
            stat_monkeys[(home, vis)] = StatMonkey()

        gamedata = json.loads(open(datafile, 'r').read())
        stat_monkeys[(home, vis)].recordGame(gamedata)

