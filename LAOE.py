import constant
import math
#Main Light Area of Effect function
def LAOE(alt, azi, orien, userPosition, light):

    if (not light):
        return (False, constant.winHeight)

    #Corners are defined from the perspective of a person inside the room looking out
    #Using azimuth relative to the window
    if (azi < 0):
        azi += 180
    projectionCoords = getProjectionCoords(alt, azi, orien)
    windowHeight = constant.winHeight - ledgeOffsetHeight(alt)
    totalWinHeight = constant.height + windowHeight
    
    #Coords for the window
    winLeftUpper = (-constant.winWidth / 2.0, 0.0, totalWinHeight)
    winRightUpper = (constant.winWidth / 2.0, 0.0, totalWinHeight)
    winLeftLower = (-constant.winWidth / 2.0, 0.0, 0.0)
    winRightLower = (constant.winWidth / 2.0, 0.0, 0.0)
    windowCoords = (winLeftUpper, winRightUpper, winLeftLower, winRightLower)

    #Check if the person is affected by the sun, if not then open blinds fully
    inLAOE = intersect(alt, windowCoords, projectionCoords, userPosition)
    print(inLAOE)

    if (not inLAOE):
        return (False, constant.winHeight)

    #If not, find the necessary change

    return blindsChange(alt, windowCoords, projectionCoords, userPosition)

def intersect(alt, windowCoords, projectionCoords, userPosition):

    windowHeight = constant.winHeight - ledgeOffsetHeight(alt)
    totalWinHeight = constant.height + windowHeight

    (wLeftUpper, wRightUpper, wLeftLower, wRightLower) = windowCoords
    (pLeftUpper, pRightUpper, pLeftLower, pRightLower) = projectionCoords
    (wLeftUpperX, wLeftUpperY, _) = wLeftUpper
    (wRightUpperX, wRightUpperY, _) = wRightUpper
    (wLeftLowerX, wLeftLowerY, _) = wLeftLower
    (wRightLowerX, wRightLowerY,_) = wRightLower
    (pLeftUpperX, pLeftUpperY, _) = pLeftUpper
    (pRightUpperX, pRightUpperY, _) = pRightUpper
    (pLeftLowerX, pLeftLowerY, _) = pLeftLower
    (pRightLowerX, pRightLowerY, _) = pRightLower
    (x, y, z) = userPosition

    #Check for vertical intersection
    #We are doing run / rise because we are checking for vertical intersection from a side view
    #of the window
    slopeUpper = (totalWinHeight) / (wLeftUpperY - pLeftUpperY)
    constUpper = totalWinHeight - (wLeftUpperY * slopeUpper)
    slopeLower = (constant.height) / (wLeftLowerY - pLeftLowerY)
    constLower = constant.height - (wLeftLowerY * slopeLower)

    #Check for horizontal intersection
    slopeLeft = (wLeftUpperY - pLeftUpperY) / (wLeftUpperX - pLeftUpperX)
    constLeft = wLeftUpperY - (wLeftUpperX * slopeLeft)
    slopeRight = (wRightUpperY - pRightUpperY) / (wRightUpperX - pRightUpperX)
    constRight = wRightUpperY - (wRightUpperX * slopeRight)

    # Since x increases left to right but y increases up to down, we invert the y inequality
    if ((z < ((slopeUpper * y) + constUpper) + 0.01) and (z > ((slopeLower * y) + constLower) - 0.01) and
        (y < ((slopeLeft * x) + constLeft) + 0.01) and (y > ((slopeRight * x) + constRight) - 0.01)):
        return True

    return False

def lineEquation(point1, point2):
    (x1, y1) = point1
    (x2, y2) = point2
    slope = (y1 - y2) / (x1 - x2)
    c = y1 - (slope * x1)
    return (slope, c)

#Gets the coordinates of the light projected onto the floor
def getProjectionCoords(alt, azi, orien):
    #origin is set at the floor, with x value at the middle of the window 

    #offset = -0.20
    offset = 0
    windowHeight = constant.winHeight - ledgeOffsetHeight(alt)
    totalWinHeight = constant.height + windowHeight

    #left upper corner
    leftUpperX = (totalWinHeight / math.tan(math.radians(alt))) * math.sin(math.radians(orien - azi)) - (constant.winWidth / 2.0)
    leftUpperY = (totalWinHeight / math.tan(math.radians(alt)))* math.cos(math.radians(orien - azi))
    leftUpper = (leftUpperX + offset, leftUpperY + offset, 0)

    #right upper corner
    rightUpperX = (totalWinHeight / math.tan(math.radians(alt))) * math.sin(math.radians(orien - azi)) + (constant.winWidth / 2.0)
    rightUpperY = (totalWinHeight / math.tan(math.radians(alt))) * math.cos(math.radians(orien - azi))
    rightUpper = (rightUpperX + offset, rightUpperY + offset, 0)

    #left lower corner
    leftLowerX = (constant.height / math.tan(math.radians(alt))) * math.sin(math.radians(orien - azi)) - (constant.winWidth / 2.0)
    leftLowerY = (constant.height / math.tan(math.radians(alt)) )* math.cos(math.radians(orien - azi))
    leftLower = (leftLowerX + offset, leftLowerY + offset, 0)

    #right lower corner
    rightLowerX = (constant.height / math.tan(math.radians(alt))) * math.sin(math.radians(orien - azi)) + (constant.winWidth / 2.0)
    rightLowerY = (constant.height / math.tan(math.radians(alt)))* math.cos(math.radians(orien - azi))
    rightLower = (rightLowerX + offset, rightLowerY + offset, 0)

    return (leftUpper, rightUpper, leftLower, rightLower)

#Finds change to blinds necessary
def blindsChange(alt, windowCoords, projectionCoords, userPosition):

    # Find z value of top of blinds so that y value of projection of blinds is at coords of face
    windowHeight = constant.winHeight - ledgeOffsetHeight(alt)
    totalWinHeight = constant.height + windowHeight
    (x, y, z) = userPosition
    offset = 0

    (wLeftUpper, _, _, _) = windowCoords
    (pLeftUpper, _, _, _) = projectionCoords

    (_, wY, wZ) = wLeftUpper
    (_, pY, pZ) = pLeftUpper

    (slope, _) = lineEquation((wY, wZ), (pY, pZ))

    c = z - (slope * y)
    result = min(max(c, constant.height), totalWinHeight)

    return (True, result - constant.height + offset)

def ledgeOffsetHeight(alt):
    angle = 90 - alt
    return constant.ledgeLen / (math.tan(math.radians(angle)))