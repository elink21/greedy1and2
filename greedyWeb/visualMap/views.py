from django.http import request
from django.http.response import JsonResponse
from django.shortcuts import render
import tsp

# Algorithm functions
from typing import List


def isComplete(grades: dict):
    total = len(grades)
    actual = 0
    for x in grades:
        if x == 2:
            actual += 1
    return [actual == total, total-actual]


def searchForBestOption(actualIndex: int, row: List, alreadyVisited: List, distanceMatrix) -> int:
    # Searching lineally for a shorter distance with no inner loops
    nextToVisit = -1
    actualBestDistance = 999999
    for x in range(len(row)):
        # So distance is shorter
        if row[x] < actualBestDistance:
            # Now lets look if the node wasnt visited yet, so no inner loop is created:
            if not x in alreadyVisited and row[x] != 0:
                nextToVisit = x
                actualBestDistance = row[x]

    return nextToVisit


def routeAdded(a, b, route):
    for r in route:
        if r['from'] == a and r['to'] == b or r['from'] == b and r['to'] == a:
            return True


def notALoop(route, newF, newT):
    newRoutes = list(route)
    newRoutes.append({'from': newF, 'to': newT})

    for i in range(len(newRoutes)):
        startFrom = newRoutes[i]['from']
        startTo = newRoutes[i]['to']
        for j in range(len(newRoutes)):
            if i != j:
                if startFrom == newRoutes[j]['to']:
                    return False

    print("-"*7)

    for x in route:
        print(x)

    return True


def validCandidates(a, b):
    if a+1 > 2:
        return False
    if b+1 > 2:
        return False
    if a+b >= 2:
        return False
    return True


def greedyBFn():
    route = []

    distanceMatrix, sortedConn, headers = getDatafromFile()
    grades = []
    route = []

    for i in range(len(headers)):
        grades.append(0)

    i = 0
    alreadyVisited = []

    while i < len(sortedConn):
        actualCandidate = sortedConn[i]
        i += 1

        # checking if from,two are valid
        f = actualCandidate['from']
        t = actualCandidate['to']
        if validCandidates(grades[f], grades[t]) and not routeAdded(f, t, route) and notALoop(route, f, t,):
            grades[f] += 1
            grades[t] += 1

            route.append({'from': f, 'to': t,
                          'distance': distanceMatrix[f][t]})
    for r in route:
        print(
            f'({r["from"]}, {grades[r["from"]]})  \t ({r["to"]}, {grades[r["to"]]})\t-{r["distance"]}')
    return [route, sum([r['distance'] for r in route])]


def getDatafromFile():
    fileLines = List[str]

    with open(f'visualMap/distances.csv') as fileOfDistances:
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
                connections.append({'from': i,
                                    'to': j,
                                    'distance': distanceMatrix[i][j]})

    sortedConnections = sorted(connections, key=lambda k: k['distance'])
    cleanedSorted = [sortedConnections[i]
                     for i in range(len(sortedConnections)) if i % 2 == 0]

    return [distanceMatrix, cleanedSorted, headers]


def greedyAFn(initialNode):

    distanceMatrix, _, headers = getDatafromFile()

    # Requesting initial node, for testing its gonna be 'CHETUMAL'

    actualIndex = int(initialNode)

    # creating lvl matrix

    grades = []
    route = []
    alreadyVisited = []

    for i in range(len(headers)):
        grades.append(0)

    while(isComplete(grades)[1] != 1):
        alreadyVisited.append(actualIndex)
        nextIndex = searchForBestOption(
            actualIndex, distanceMatrix[actualIndex], alreadyVisited, distanceMatrix)

        if(nextIndex == -1):
            break
        # Updating nodes connections
        grades[actualIndex] += 1
        grades[nextIndex] += 1

        print(
            f"{actualIndex}--{nextIndex} =>({distanceMatrix[actualIndex][nextIndex]})=>{distanceMatrix[actualIndex]}")

        route.append({'from': actualIndex, 'to': nextIndex,
                      'distance': distanceMatrix[actualIndex][nextIndex]})

        # new actualIndex= nextIndex
        actualIndex = nextIndex

    route.append({'from': actualIndex, 'to': int(initialNode),
                  'distance': distanceMatrix[actualIndex][int(initialNode)]})
    for r in route:
        print(r)

    print(f"Grades: {grades}")
    print(f"total distance: {sum([r['distance'] for r in route])}")

    return [route, sum([r['distance'] for r in route])]

# Routing functions


def home(req):
    headers = ['ACAPULCO', 'CHETUMAL', 'CHIHUAHUA', 'CD.JUAREZ', 'DURANGO', 'GUADALAJARA', 'GUANAJUATO', 'HERMOSILLO', 'LA PAZ', 'MANZANILLO',
               'MATAMOROS', 'MERIDA', 'MEXICO DF', 'NOGALES', 'NVO.LAREDO', 'OAXACA', 'PIEDRAS NEGRAS', 'PUEBLA', 'QUERETARO', 'SAN LUIS POTOSI', 'TAMPICO', 'TAPACHULA', 'TIJUANA', 'VERACRUZ', 'VILLAHERMOSA']
    return render(req, 'header.html', context={'places': headers})


def greedyA(request):
    initialNode = request.GET['initialNode']
    route, distance = greedyAFn(initialNode)
    return JsonResponse({"route": route, 'distance': distance})


def greedyB(request):
    print("Activado")
    route, distance = greedyBFn()
    return JsonResponse({"route": route, 'distance': distance})
