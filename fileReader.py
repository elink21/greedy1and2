import os
from typing import List


def isComplete(grades: dict):
    for key in grades.keys():
        if grades[key] != 2:
            return False
    return True


def searchForBestOption(actualIndex: int, row: List, alreadyVisited: List, distanceMatrix) -> int:
    # Searching lineally for a shorter distance with no inner loops
    nextToVisit = -1
    actualBestDistance = 999999
    for x in range(len(row)):
        # So distance is shorter
        if row[x] < actualBestDistance:
            # Now lets look if the node wasnt visited yet, so no inner loop is created:
            if not x in alreadyVisited and row[x]!=0:
                nextToVisit = x
                actualBestDistance = row[x]
    print(actualBestDistance)
    print(row)
    return nextToVisit


fileLines = List[str]

with open(f'{os.getcwd()}/distances.csv') as fileOfDistances:
    fileLines = fileOfDistances.readlines()


headers = fileLines[0].split(',')

headers = [h.replace('\n', '') for h in headers[1:]]

distanceMatrix = []

for l in fileLines[1:]:
    line = l.split(',')

    distances = []
    for distance in line[1:]:
        if('\n' in distance):
            distance = distance[:-1]
        if distance != '':
            distances.append(int(distance))
        else:
            distances.append(0)
    distanceMatrix.append(distances)


connections = []  # str,str,d

for i in range(len(distanceMatrix)):
    for j in range(len(distanceMatrix[0])):
        if i != j:
            connections.append({'from': headers[j].replace('\n', ''),
                                'to': headers[i].replace('\n', ''),
                                'distance': distanceMatrix[i][j]})


sortedConnections = sorted(connections, key=lambda k: k['distance'])

for l in distanceMatrix:
    print(l)

# Requesting initial node, for testing its gonna be 'CHETUMAL'

actualNode = 'CHETUMAL'
actualIndex = 0
for i in range(len(headers)):
    if headers[i] == actualNode:
        actualRow = i
        break
print(headers)
print(actualIndex)

# creating lvl matrix

grades = {}
route = []
alreadyVisited = []

for place in headers:
    grades[place] = 0


alreadyVisited.append(actualIndex)
nextIndex = searchForBestOption(
    actualIndex, distanceMatrix[actualIndex], alreadyVisited, distanceMatrix)
print(nextIndex)
print(headers[nextIndex])
