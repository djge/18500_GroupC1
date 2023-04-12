import sys
import math

sys.path.insert(0, './')
from LAOE import getProjectionCoords, intersect

def testGetProjectionCoords():

    #Case 1 (top left and right 02/15 10:14 am)

    projectionCoords = getProjectionCoords(27.87, 140.78, 180)
    (pLeftUpper, pRightUpper, pLeftLower, pRightLower) = projectionCoords
    print("Testing Case 1 Upper Left...\n")
    #Result: (222, 306) relative to upper left -> (203, 306) relative to camera
    caseResults = (203, 306)
    print(f"Expected {caseResults}, got {pLeftUpper}\n")
    (testX, testY) = caseResults
    (x, y, _) = pLeftUpper
    error = (abs((x - testX)/testX) + abs((y - testY)/testY)) / 2
    print(f"Got an error of {error}\n")
    print("\n")
    print("Testing Case 1 Upper Right...\n")
    #Result: (222, 306) relative to upper right -> (241, 306) relative to camera
    caseResults = (241, 305)
    print(f"Expected {caseResults}, got {pRightUpper}\n")
    (testX, testY) = caseResults
    (x, y, _) = pRightUpper
    error = (abs((x - testX)/testX) + abs((y - testY)/testY)) / 2
    print(f"Got an error of {error}\n")
    print("\n")

    #Case 2 (top left and right 02/15 10:33 am)

    projectionCoords = getProjectionCoords(30.04, 145.46, 180)
    (pLeftUpper, pRightUpper, pLeftLower, pRightLower) = projectionCoords
    print("Testing Case 2 Upper Left...\n")
    #Result: (177, 289) relative to upper left -> (158, 289) relative to camera
    caseResults = (158, 289)
    print(f"Expected {caseResults}, got {pLeftUpper}\n")
    (testX, testY) = caseResults
    (x, y, _) = pLeftUpper
    error = (abs((x - testX)/testX) + abs((y - testY)/testY)) / 2
    print(f"Got an error of {error}\n")
    print("\n")
    print("Testing Case 2 Upper Right...\n")
    #Result: (177, 289) relative to upper right -> (177, 289) relative to camera
    caseResults = (196, 289)
    print(f"Expected {caseResults}, got {pRightUpper}\n")
    (testX, testY) = caseResults
    (x, y, _) = pRightUpper
    error = (abs((x - testX)/testX) + abs((y - testY)/testY)) / 2
    print(f"Got an error of {error}\n")
    print("\n")

    #Case 3 (top left and right 02/15 10:44 am)

    projectionCoords = getProjectionCoords(31.18, 148.28, 180)
    (pLeftUpper, pRightUpper, pLeftLower, pRightLower) = projectionCoords
    print("Testing Case 3 Upper Left...\n")
    #Result: (176, 282) relative to upper left -> (157, 282) relative to camera
    caseResults = (157, 282)
    print(f"Expected {caseResults}, got {pLeftUpper}\n")
    (testX, testY) = caseResults
    (x, y, _) = pLeftUpper
    error = (abs((x - testX)/testX) + abs((y - testY)/testY)) / 2
    print(f"Got an error of {error}\n")
    print("\n")
    print("Testing Case 3 Upper Right...\n")
    #Result: (176, 282) relative to upper right -> (195, 282) relative to camera
    caseResults = (195, 282)
    print(f"Expected {caseResults}, got {pRightUpper}\n")
    (testX, testY) = caseResults
    (x, y, _) = pRightUpper
    error = (abs((x - testX)/testX) + abs((y - testY)/testY)) / 2
    print(f"Got an error of {error}\n")
    print("\n")

    #Case 4 (top left and right 02/15 10:44 am)

    projectionCoords = getProjectionCoords(53.03, 169.93, 170)
    (pLeftUpper, pRightUpper, pLeftLower, pRightLower) = projectionCoords
    print("Testing Case 4 Upper Left...\n")
    #Result: (176, 282) relative to upper left -> (157, 282) relative to camera
    caseResults = (-0.2921, 1.30302)
    print(f"Expected {caseResults}, got {pLeftUpper}\n")
    (testX, testY) = caseResults
    (x, y, _) = pLeftUpper
    error = (abs((x - testX)/testX) + abs((y - testY)/testY)) / 2
    print(f"Got an error of {error}\n")
    print("\n")
    print("Testing Case 4 Upper Right...\n")
    #Result: (176, 282) relative to upper right -> (195, 282) relative to camera
    caseResults = (0.2921, 1.30302)
    print(f"Expected {caseResults}, got {pRightUpper}\n")
    (testX, testY) = caseResults
    (x, y, _) = pRightUpper
    error = (abs((x - testX)/testX) + abs((y - testY)/testY)) / 2
    print(f"Got an error of {error}\n")
    print("\n")

    #Case 5 (top left and right 03/29 12:37 am)

    projectionCoords = getProjectionCoords(51.52, 160.73, 170)
    (pLeftUpper, pRightUpper, pLeftLower, pRightLower) = projectionCoords
    print("Testing Case 5 Upper Left...\n")
    #Result: (176, 282) relative to upper left -> (157, 282) relative to camera
    caseResults = (-0.04572,1.40208)
    print(f"Expected {caseResults}, got {pLeftUpper}\n")
    (testX, testY) = caseResults
    (x, y, _) = pLeftUpper
    error = (abs((x - testX)/testX) + abs((y - testY)/testY)) / 2
    print(f"Got an error of {error}\n")
    print("\n")
    print("Testing Case 5 Upper Right...\n")
    #Result: (176, 282) relative to upper right -> (195, 282) relative to camera
    caseResults = (0.40894, 1.397)
    print(f"Expected {caseResults}, got {pRightUpper}\n")
    (testX, testY) = caseResults
    (x, y, _) = pRightUpper
    error = (abs((x - testX)/testX) + abs((y - testY)/testY)) / 2
    print(f"Got an error of {error}\n")
    print("\n")

    #Case 6 (top left and right 03/29 12:51 am)

    projectionCoords = getProjectionCoords(52.28, 166.26, 170)
    (pLeftUpper, pRightUpper, pLeftLower, pRightLower) = projectionCoords
    print("Testing Case 6 Upper Left...\n")
    #Result: (176, 282) relative to upper left -> (157, 282) relative to camera
    caseResults = (-0.1397, 1.36398)
    print(f"Expected {caseResults}, got {pLeftUpper}\n")
    (testX, testY) = caseResults
    (x, y, _) = pLeftUpper
    error = (abs((x - testX)/testX) + abs((y - testY)/testY)) / 2
    print(f"Got an error of {error}\n")
    print("\n")
    print("Testing Case 6 Upper Right...\n")
    #Result: (176, 282) relative to upper right -> (195, 282) relative to camera
    caseResults = (0.3683, 1.36398)
    print(f"Expected {caseResults}, got {pRightUpper}\n")
    (testX, testY) = caseResults
    (x, y, _) = pRightUpper
    error = (abs((x - testX)/testX) + abs((y - testY)/testY)) / 2
    print(f"Got an error of {error}\n")
    print("\n")

    #Case 7 (top left and right 03/29 1:01 am)

    projectionCoords = getProjectionCoords(52.67, 170.30, 170)
    (pLeftUpper, pRightUpper, pLeftLower, pRightLower) = projectionCoords
    print("Testing Case 7 Upper Left...\n")
    #Result: (176, 282) relative to upper left -> (157, 282) relative to camera
    caseResults = (-0.2921, 1.3462)
    print(f"Expected {caseResults}, got {pLeftUpper}\n")
    (testX, testY) = caseResults
    (x, y, _) = pLeftUpper
    error = (abs((x - testX)/testX) + abs((y - testY)/testY)) / 2
    print(f"Got an error of {error}\n")
    print("\n")
    print("Testing Case 7 Upper Right...\n")
    #Result: (176, 282) relative to upper right -> (195, 282) relative to camera
    caseResults = (0.1778, 1.3462)
    print(f"Expected {caseResults}, got {pRightUpper}\n")
    (testX, testY) = caseResults
    (x, y, _) = pRightUpper
    error = (abs((x - testX)/testX) + abs((y - testY)/testY)) / 2
    print(f"Got an error of {error}\n")
    print("\n")

    #Case 8 (top left and right 03/29 1:01 am)

    projectionCoords = getProjectionCoords(	26.43, 256.96, 260)
    (pLeftUpper, pRightUpper, pLeftLower, pRightLower) = projectionCoords
    print("Testing Case 8 Lower Left...\n")
    #Result: (176, 282) relative to upper left -> (157, 282) relative to camera
    caseResults = (-0.2159, 1.4478)
    print(f"Expected {caseResults}, got {pLeftLower}\n")
    (testX, testY) = caseResults
    (x, y, _) = pLeftLower
    error = (abs((x - testX)/testX) + abs((y - testY)/testY)) / 2
    print(f"Got an error of {error}\n")
    print("\n")
    print("Testing Case 8 Lower Right...\n")
    #Result: (176, 282) relative to upper right -> (195, 282) relative to camera
    caseResults = (0.3937, 1.4478)
    print(f"Expected {caseResults}, got {pRightLower}\n")
    (testX, testY) = caseResults
    (x, y, _) = pRightLower
    error = (abs((x - testX)/testX) + abs((y - testY)/testY)) / 2
    print(f"Got an error of {error}\n")
    print("\n")

testGetProjectionCoords()
