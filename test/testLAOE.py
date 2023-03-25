import sys
import math

sys.path.insert(0, './')
from LAOE import getProjectionCoords, intersect

def testGetProjectionCoords():

    #Case 1 (top left and right 02/15 10:14 am)

    projectionCoords = getProjectionCoords(27.87, 140.78)
    (pLeftUpper, pRightUpper, pLeftLower, pRightLower) = projectionCoords
    print("Testing Case 1 Upper Left...\n")
    #Result: (222, 306) relative to upper left -> (203, 306) relative to camera
    caseResults = (203, 306)
    print(f"Expected {caseResults}, got {pLeftUpper}\n")
    (testX, testY) = caseResults
    (x, y) = pLeftUpper
    error = (abs((x - testX)/testX) + abs((y - testY)/testY)) / 2
    print(f"Got an error of {error}\n")
    print("\n")
    print("Testing Case 1 Upper Right...\n")
    #Result: (222, 306) relative to upper right -> (241, 306) relative to camera
    caseResults = (241, 305)
    print(f"Expected {caseResults}, got {pLeftLower}\n")
    (testX, testY) = caseResults
    (x, y) = pLeftLower
    error = (abs((x - testX)/testX) + abs((y - testY)/testY)) / 2
    print(f"Got an error of {error}\n")
    print("\n")

    #Case 2 (top left and right 02/15 10:33 am)

    projectionCoords = getProjectionCoords(30.04, 145.46)
    (pLeftUpper, pRightUpper, pLeftLower, pRightLower) = projectionCoords
    print("Testing Case 2 Upper Left...\n")
    #Result: (177, 289) relative to upper left -> (158, 289) relative to camera
    caseResults = (158, 289)
    print(f"Expected {caseResults}, got {pLeftUpper}\n")
    (testX, testY) = caseResults
    (x, y) = pLeftUpper
    error = (abs((x - testX)/testX) + abs((y - testY)/testY)) / 2
    print(f"Got an error of {error}\n")
    print("\n")
    print("Testing Case 2 Upper Right...\n")
    #Result: (177, 289) relative to upper right -> (177, 289) relative to camera
    caseResults = (196, 289)
    print(f"Expected {caseResults}, got {pLeftLower}\n")
    (testX, testY) = caseResults
    (x, y) = pLeftLower
    error = (abs((x - testX)/testX) + abs((y - testY)/testY)) / 2
    print(f"Got an error of {error}\n")
    print("\n")

    #Case 3 (top left and right 02/15 10:44 am)

    projectionCoords = getProjectionCoords(31.18, 148.28)
    (pLeftUpper, pRightUpper, pLeftLower, pRightLower) = projectionCoords
    print("Testing Case 3 Upper Left...\n")
    #Result: (176, 282) relative to upper left -> (157, 282) relative to camera
    caseResults = (157, 282)
    print(f"Expected {caseResults}, got {pLeftUpper}\n")
    (testX, testY) = caseResults
    (x, y) = pLeftUpper
    error = (abs((x - testX)/testX) + abs((y - testY)/testY)) / 2
    print(f"Got an error of {error}\n")
    print("\n")
    print("Testing Case 3 Upper Right...\n")
    #Result: (176, 282) relative to upper right -> (195, 282) relative to camera
    caseResults = (195, 282)
    print(f"Expected {caseResults}, got {pLeftLower}\n")
    (testX, testY) = caseResults
    (x, y) = pLeftLower
    error = (abs((x - testX)/testX) + abs((y - testY)/testY)) / 2
    print(f"Got an error of {error}\n")
    print("\n")

testGetProjectionCoords()
