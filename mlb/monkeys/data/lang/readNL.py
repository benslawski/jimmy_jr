## python modules
import re
import json



if __name__ == "__main__":

    transitions = {'AtBat':{}, 'Action':{}}

    atbat_file = open('natural_language_baseball_matrix.csv').readlines()

    headers = map(lambda k: k.strip()[1:], atbat_file[0].split('#')[1:])
    nheaders = len(headers)

    for dataline in atbat_file[1:]:
        splitline = dataline.split('#')
        from_state = splitline[0].strip()[1:]
        transitions['AtBat'][from_state] = {}

        for i in range(0, nheaders):
            features = splitline[i+1].strip().strip('[').strip(']').lower()
            clean_features = []
            for or_clause in features.split(','):
                and_clauses = or_clause.strip().split('&')
                if and_clauses and and_clauses[0]:
                    clean_features.append(and_clauses)

            if clean_features:
                transitions['AtBat'][from_state][headers[i]] = clean_features

    action_file = open('natural_language_baseball_matrix_actions.csv').readlines()

    headers = map(lambda k: k.strip()[1:], action_file[0].split('#')[1:])
    nheaders = len(headers)

    for dataline in action_file[1:]:
        splitline = dataline.split('#')
        from_state = splitline[0].strip()[1:]
        transitions['Action'][from_state] = {}
        
        for i in range(0, nheaders):
            features = splitline[i+1].strip('[').strip(']')
            clean_features = []
            for or_clause in features.split(','):
                and_clauses = or_clause.strip().split('&')
                if and_clauses and and_clauses[0]:
                    clean_features.append(and_clauses)

            if clean_features:
                transitions['Action'][from_state][headers[i]] = clean_features

    f = open('features.dat', 'w')
    f.write(json.dumps(transitions))
    f.close()

