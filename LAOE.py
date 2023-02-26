import constant
import math
#Main Light Area of Effect function
def LAOE(alt, azi, orien, userPosition, blindsState):
    
    #Check if it is possible for the sun to hit anyone in the room

    #If blinds are fully closed, return how much/if they should be opened

    #Corners are defined from the perspective of a person inside the room looking out
    #Using azimuth relative to the window
    projectionCoords = getProjectionCoords(alt, azi + orien, blindsState)
    totalWinHeight = constant.height + constant.winHeight - blindsState
    
    #Coords for the window
    winLeftUpper = (-constant.winWidth / 2.0, totalWinHeight)
    winRightUpper = (constant.winWidth / 2.0, totalWinHeight)
    winLeftLower = (constant.winWidth / 2.0, 0.0)
    winRightLower = (constant.winWidth / 2.0, 0.0)
    windowCoords = (winLeftUpper, winRightUpper, winLeftLower, winRightLower)

    #Check if the person is affected by the sun, if so adjust the blinds
    if (intersect(windowCoords, projectionCoords, userPosition, blindsState)):
        return

    #If not, try to maximize sunlight in the room
    return 

def intersect(windowCoords, projectionCoords, userPosition, blindsState):

    totalWinHeight = constant.height + constant.winHeight - blindsState

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
    constUpper = wLeftUpperY - (wLeftUpperX * slopeUpper)
    slopeLower = (constant.height) / (wLeftLowerY - pLeftLowerY)
    constLower = wLeftLowerY - (wLeftLowerX * slopeLower)

    #Check for horizontal intersection
    slopeLeft = (wLeftUpperY - pLeftUpperY) / (wLeftUpperX - pLeftUpperX)
    slopeRight = (wLeftLowerY - pLeftLowerY) / (wLeftLowerX - pLeftLowerX)


    return False

#Gets the coordinates of the light projected onto the floor
def getProjectionCoords(alt, azi, blindsState):
    #origin is set at the floor, with x value at the middle of the window 

    #TODO: get the new "winHeight" from the blindsState (depends on how much the blinds are closed at the moment
    totalWinHeight = constant.winHeight - blindsState

    #left upper corner
    leftUpperX = ((constant.height + totalWinHeight) / math.tan(math.radians(alt))) * math.sin(math.radians(azi)) - (constant.winWidth / 2.0)
    leftUpperY = ((constant.height + totalWinHeight) / math.tan(math.radians(alt))) * math.cos(math.radians(azi))
    leftUpper = (leftUpperX, leftUpperY)

    #right upper corner
    rightUpperX = ((constant.height + totalWinHeight) / math.tan(math.radians(alt))) * math.sin(math.radians(azi)) + (constant.winWidth / 2.0)
    rightUpperY = ((constant.height + totalWinHeight) / math.tan(math.radians(alt))) * math.cos(math.radians(azi))
    rightUpper = (rightUpperX, rightUpperY)

    #left lower corner
    leftLowerX = (constant.height / math.tan(math.radians(alt))) * math.sin(math.radians(azi)) - (constant.winWidth / 2.0)
    leftLowerY = (constant.height / math.tan(math.radians(alt))) * math.cos(math.radians(azi))
    leftLower = (leftLowerX, leftLowerY)

    #right lower corner
    rightLowerX = (constant.height / math.tan(math.radians(alt))) * math.sin(math.radians(azi)) + (constant.winWidth / 2.0)
    rightLowerY = (constant.height / math.tan(math.radians(alt))) * math.cos(math.radians(azi))
    rightLower = (rightLowerX, rightLowerY)

    return (leftUpper, rightUpper, leftLower, rightLower)

#Finds change to blinds necessary
def blindsChange():
    return