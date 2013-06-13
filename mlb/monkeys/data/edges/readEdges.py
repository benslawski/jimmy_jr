import json

if __name__ == "__main__":

    f = open('baseball_matrix.csv', 'r')

    edges = {}

    raw_data = f.readlines()
    headers = raw_data[0].strip().split(',')[1:]
    headers = map(lambda k: k[1:], headers)
    nheaders = len(headers)
    for dataline0 in raw_data[1:]:
        dataline = dataline0[1:].strip().split(',')
        to_state = dataline[0]
        edges[to_state] = {}
        for i in range(1, nheaders+1):
            if dataline[i]:
                edges[to_state][headers[i-1]] = dataline[i]
    f.close()
    f = open('edges.dat', 'w')
    f.write(json.dumps(edges))
    f.close()

