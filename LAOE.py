import constant
import math
#Main Light Area of Effect function
def LAOE(alt, azi, orien, userPosition, blindsState):

    #Corners are defined from the perspective of a person inside the room looking out
    #Using azimuth relative to the window
    projectionCoords = getProjectionCoords(alt, azi - orien)
    totalWinHeight = constant.height + constant.winHeight
    
    #Coords for the window
    winLeftUpper = (-constant.winWidth / 2.0, 0.0, totalWinHeight)
    winRightUpper = (constant.winWidth / 2.0, 0.0, totalWinHeight)
    winLeftLower = (constant.winWidth / 2.0, 0.0, 0.0)
    winRightLower = (constant.winWidth / 2.0, 0.0, 0.0)
    windowCoords = (winLeftUpper, winRightUpper, winLeftLower, winRightLower)

    #Check if the person is affected by the sun, if not then open blinds fully
    if (not intersect(windowCoords, projectionCoords, userPosition)):
        return constant.winHeight

    #If not, find the necessary change

    return blindsChange(windowCoords, projectionCoords, userPosition, blindsState)

def intersect(windowCoords, projectionCoords, userPosition):

    totalWinHeight = constant.height + constant.winHeight

    (wLeftUpper, wRightUpper, wLeftLower, wRightLower) = windowCoords
    (pLeftUpper, pRightUpper, pLeftLower, pRightLower) = projectionCoords
    (wLeftUpperX, wLeftUpperY) = wLeftUpper
    (wRightUpperX, wRightUpperY) = wRightUpper
    (wLeftLowerX, wLeftLowerY) = wLeftLower
    (wRightLowerX, wRightLowerY) = wRightLower
    (pLeftUpperX, pLeftUpperY) = pLeftUpper
    (pRightUpperX, pRightUpperY) = pRightUpper
    (pLeftLowerX, pLeftLowerY) = pLeftLower
    (pRightLowerX, pRightLowerY) = pRightLower
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
    slopeRight = (wLeftLowerY - pLeftLowerY) / (wLeftLowerX - pLeftLowerX)
    constRight = wLeftLowerY - (wLeftLowerX * slopeRight)

    # Since x increases left to right but y increases up to down, we invert the y inequality
    if ((z < ((slopeUpper * y) + constUpper)) and (z > ((slopeLower * y) + constLower)) and
        (y < ((slopeLeft * x) + constLeft)) and (y > ((slopeRight * x) + constRight) )):
        return True

    return False

def lineEquation(point1, point2):
    (x1, y1) = point1
    (x2, y2) = point2
    slope = (y1 - y2) / (x1 - x2)
    c = y1 - (slope * x1)
    return (slope, c)

#Gets the coordinates of the light projected onto the floor
def getProjectionCoords(alt, azi):
    #origin is set at the floor, with x value at the middle of the window 

    #TODO: get the new "winHeight" from the blindsState (depends on how much the blinds are closed at the moment
    totalWinHeight = constant.winHeight

    #left upper corner
    leftUpperX = ((constant.height + totalWinHeight) / math.tan(math.radians(alt))) * math.sin(math.radians(180 - azi)) - (constant.winWidth / 2.0)
    leftUpperY = ((constant.height + totalWinHeight) / math.tan(math.radians(alt)))
    leftUpper = (leftUpperX, leftUpperY)

    #right upper corner
    rightUpperX = ((constant.height + totalWinHeight) / math.tan(math.radians(alt))) * math.cos(math.radians(180 - azi)) + (constant.winWidth / 2.0)
    rightUpperY = ((constant.height + totalWinHeight) / math.tan(math.radians(alt)))
    rightUpper = (rightUpperX, rightUpperY)

    #left lower corner
    leftLowerX = (constant.height / math.tan(math.radians(alt))) * math.sin(math.radians(180 - azi)) - (constant.winWidth / 2.0)
    leftLowerY = (constant.height / math.tan(math.radians(alt)))
    leftLower = (leftLowerX, leftLowerY)

    #right lower corner
    rightLowerX = (constant.height / math.tan(math.radians(alt))) * math.cos(math.radians(180 - azi)) + (constant.winWidth / 2.0)
    rightLowerY = (constant.height / math.tan(math.radians(alt)))
    rightLower = (rightLowerX, rightLowerY)

    return (leftUpper, rightUpper, leftLower, rightLower)

#Finds change to blinds necessary
def blindsChange(windowCoords, projectionCoords, userPosition, blindsState):

    # Find z value of top of blinds so that y value of projection of blinds is at coords of face
    (x, y, z) = userPosition
    offset = 0

    (wLeftUpper, _, _, _) = windowCoords
    (pLeftUpper, _, _, _) = projectionCoords

    (_, wY, wZ) = wLeftUpper
    (_, pY, pZ) = pLeftUpper

    (slope, _) = lineEquation((wY, wZ), (pY, pZ))

    c = z - (slope * y)
    result = min(max(c, constant.height), constant.height + constant.winHeight)

    return blindsState - (result - constant.height + offset)