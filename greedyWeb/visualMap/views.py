from django.http import request
from django.http.response import JsonResponse
from django.shortcuts import render


# Algorithm functions
import os
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


def greedyAFn(initialNode):
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
                connections.append({'from': headers[j].replace('\n', ''),
                                    'to': headers[i].replace('\n', ''),
                                    'distance': distanceMatrix[i][j]})

    sortedConnections = sorted(connections, key=lambda k: k['distance'])

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
    pass
# Routing functions


def home(req):
    headers = ['ACAPULCO', 'CHETUMAL', 'CHIHUAHUA', 'CD.JUAREZ', 'DURANGO', 'GUADALAJARA', 'GUANAJUATO', 'HERMOSILLO', 'LA PAZ', 'MANZANILLO',
               'MATAMOROS', 'MERIDA', 'MEXICO DF', 'NOGALES', 'NVO.LAREDO', 'OAXACA', 'PIEDRAS NEGRAS', 'PUEBLA', 'QUERETARO', 'SAN LUIS POTOSI', 'TAMPICO', 'TAPACHULA', 'TIJUANA', 'VERACRUZ', 'VILLAHERMOSA']
    return render(req, 'header.html', context={'places': headers})


def greedyA(request):
    initialNode = request.GET['initialNode']
    route, distance = greedyAFn(initialNode)
    return JsonResponse({"route": route, 'distance': distance})
