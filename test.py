import sys, math, pygame
import numpy as np
pygame.init()
pygame.font.init()

#constants
oneSide = math.sqrt(2)/2
black = 0, 0, 0
white = 255, 255, 255
blue = 137, 207, 240
red = 220, 20, 60
green = 0,255,0

lostColor = red
wonColor = green


radius = 200
mouseCircleRadius = 6
catCircleRadius = 9

size = width, height = radius*5, radius*5
center = (width/2, height/2)

#variables
won = None

ratio = 4
mouseSpeed = 0
maxMouseSpeed = 0.25
catAngle = 0
catSpeed = 0
catPos = np.array([center[0], center[1]]) - np.array([0, radius])
maxCatSpeed = ratio * maxMouseSpeed
maxAngleChange = math.degrees(maxCatSpeed / radius) #in radians
mousePos = np.array([center[0], center[1]])

movingLeft = False
movingUp = False
movingRight = False
movingDown = False

#key variables
mouse = False

screen = pygame.display.set_mode(size)

def getCatDirection(center, minDistancePoint, catPos):
    #returns 0 for clockwise, 1 for counterclockwise
    if center[0] == minDistancePoint[0]:
        if catPos[0] > center[0]:
            if minDistancePoint[1] > center[1]:
                return 0
            else:
                return 1
        else:
            if minDistancePoint[1] > center[1]:
                return 1
            else:
                return 0
    slope = (center[1] - minDistancePoint[1])/(center[0]-minDistancePoint[0])
    #equation is y = slope * (x - center[0]) + center[1]
    if slope >= 0:
        if catPos[1] > slope * (catPos[0] - center[0]) + center[1]:
            if minDistancePoint[0] < center[0]:
                return 0
            else:
                return 1
        elif catPos[1] < slope * (catPos[0] - center[0]) + center[1]:
            if minDistancePoint[0] < center[0]:
                return 1
            else:
                return 0
        else: 
            return 0
    else:
        if catPos[1] > slope * (catPos[0] - center[0]) + center[1]:
            if minDistancePoint[0] < center[0]:
                return 0
            else:
                return 1
        elif catPos[1] < slope * (catPos[0] - center[0]) + center[1]:
            if minDistancePoint[0] < center[0]:
                return 1
            else:
                return 0
        else:
            return 0
    

def getMinDistancePoint(center, radius, point):

    if center[0] == point[0]:
        if center[1] >= point[1]:
            return (center[0], center[1] - radius)
        else:
            return (center[0], center[1] + radius)
    
    slope = (point[1] - center[1])/(point[0] - center[0])

    point1x = math.sqrt(radius**2/(slope**2 + 1)) + center[0]
    point1y = slope * (point1x - center[0]) + center[1]

    point2x = -1 * math.sqrt(radius**2/(slope**2 + 1)) + center[0]
    point2y = slope * (point2x - center[0]) + center[1]

    dPoint1 = math.sqrt((point1y-point[1])**2+(point1x-point[0])**2)
    dPoint2 = math.sqrt((point2y-point[1])**2+(point2x-point[0])**2)
    if dPoint1 < dPoint2:
        return (point1x, point1y)
    else: 
        return (point2x, point2y)
    

while 1:
    if won == None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    mouse = not mouse
                
        """
        if not mouse:
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        movingLeft = True
                    if event.key == pygame.K_RIGHT:
                        movingRight = True
                    if event.key == pygame.K_UP:
                        movingUp = True
                    if event.key == pygame.K_DOWN:
                        movingDown = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        movingLeft = False
                    if event.key == pygame.K_RIGHT:
                        movingRight = False
                    if event.key == pygame.K_UP:
                        movingUp = False
                    if event.key == pygame.K_DOWN:
                        movingDown = False

            if movingLeft and movingUp and not movingRight and not movingDown:
                mousePos[0] -=  oneSide * maxMouseSpeed
                mousePos[1] -= oneSide * maxMouseSpeed
            elif movingLeft and movingDown and not movingRight and not movingUp:
                mousePos[0] -=  oneSide * maxMouseSpeed
                mousePos[1] += oneSide * maxMouseSpeed
            elif movingRight and movingUp and not movingLeft and not movingDown:
                mousePos[0] +=  oneSide * maxMouseSpeed
                mousePos[1] -= oneSide * maxMouseSpeed
            elif movingRight and movingDown and not movingLeft and not movingLeft:
                mousePos[0] +=  oneSide * maxMouseSpeed
                mousePos[1] += oneSide * maxMouseSpeed
            elif movingRight and not movingLeft and not movingDown and not movingUp:
                mousePos[0] += maxMouseSpeed
            elif not movingRight and movingLeft and not movingDown and not movingUp:
                mousePos[0] -= maxMouseSpeed
            elif not movingRight and not movingLeft and movingDown and not movingUp:
                mousePos[1] += maxMouseSpeed
            elif not movingRight and not movingLeft and not movingDown and movingUp:
                mousePos[1] -= maxMouseSpeed
        else:"""
        positionOfMouse = pygame.mouse.get_pos()
        #print(positionOfMouse)
        if positionOfMouse[0] > mousePos[0] and positionOfMouse[1] > mousePos[1]:

            diffx = positionOfMouse[0]-mousePos[0]
            diffy = positionOfMouse[1]-mousePos[1]
            vectorSlope = diffy/diffx
            mousePos[0] += maxMouseSpeed / math.sqrt(vectorSlope**2 + 1)
            mousePos[1] += maxMouseSpeed * vectorSlope/ math.sqrt(vectorSlope**2 + 1)
        elif positionOfMouse[0] > mousePos[0] and positionOfMouse[1] < mousePos[1]:
            diffx = positionOfMouse[0]-mousePos[0]
            diffy = abs(positionOfMouse[1]-mousePos[1])
            vectorSlope = diffy/diffx
            mousePos[0] += maxMouseSpeed / math.sqrt(vectorSlope**2 + 1)
            mousePos[1] -= maxMouseSpeed * vectorSlope/ math.sqrt(vectorSlope**2 + 1)
        elif positionOfMouse[0] < mousePos[0] and positionOfMouse[1] > mousePos[1]:
            diffx = abs(positionOfMouse[0]-mousePos[0])
            diffy = abs(positionOfMouse[1]-mousePos[1])
            vectorSlope = diffy/diffx
            mousePos[0] -= maxMouseSpeed / math.sqrt(vectorSlope**2 + 1)
            mousePos[1] += maxMouseSpeed * vectorSlope/ math.sqrt(vectorSlope**2 + 1)
        elif positionOfMouse[0] < mousePos[0] and positionOfMouse[1] < mousePos[1]:
            diffx = abs(positionOfMouse[0]-mousePos[0])
            diffy = abs(positionOfMouse[1]-mousePos[1])
            vectorSlope = diffy/diffx
            mousePos[0] -= maxMouseSpeed / math.sqrt(vectorSlope**2 + 1)
            mousePos[1] -= maxMouseSpeed * vectorSlope/ math.sqrt(vectorSlope**2 + 1)
        else:
            pass
        screen.fill(black)
        pygame.draw.circle(screen, white, (width/2, height/2), radius)
        pygame.draw.circle(screen, blue, mousePos, mouseCircleRadius)
        minDistancePoint = getMinDistancePoint(center, radius, mousePos)
        pygame.draw.circle(screen, blue, minDistancePoint, mouseCircleRadius)

        returns 0 for clockwise, 1 for counterclockwise
        catDirection = getCatDirection(center, minDistancePoint, catPos)

        if catDirection:
            catAngle = catAngle - maxAngleChange
        else:
            catAngle = catAngle + maxAngleChange

        #if negative or bigger than 360, converts it to within 0 to 360 
        if catAngle < 0:
            catAngle = 360 - (-1 * catAngle)
        if catAngle > 360:
            catAngle -= 360
        
        
        if catAngle >= 0 and catAngle < 90:
            catPos = (center[0] + radius * math.sin(math.radians(catAngle)), center[1] - radius* math.cos(math.radians(catAngle)))
        elif catAngle >= 90 and catAngle < 180:
            temp = catAngle - 90
            catPos = (center[0] + radius * math.cos(math.radians(temp)), center[1] + radius* math.sin(math.radians(temp)))
        elif catAngle >= 180 and catAngle < 270:
            temp = catAngle - 180
            catPos = (center[0] - radius * math.sin(math.radians(temp)), center[1] + radius* math.cos(math.radians(temp)))
        else:
            temp = catAngle - 270
            catPos = (center[0] - radius * math.cos(math.radians(temp)), center[1] - radius* math.sin(math.radians(temp)))
        pygame.draw.circle(screen, red, catPos, catCircleRadius)

        #calculate mouse angle -> check quadrants
        if mousePos[0] == center[0]:
            if mousePos[1] <= center[1]:
                theta = 0
            else:
                theta = 180
        elif mousePos[1] == center[1]:
            if mousePos[0] <= center[0]:
                theta = 270
            else:
                theta = 90
        #quadrant 1
        elif mousePos[0] > center[0] and mousePos[1] < center[1]:
            diffy = abs(mousePos[1] - center[1])
            diffx = abs(mousePos[0] - center[0])
            theta = math.degrees(math.atan(diffx/diffy))
        #quadrant 2
        elif mousePos[0] > center[0] and mousePos[1] > center[1]:
            diffy = abs(mousePos[1] - center[1])
            diffx = abs(mousePos[0] - center[0])
            theta = math.degrees(math.atan(diffy/diffx)) + 90
        #quadrant 3
        elif mousePos[0] < center[0] and mousePos[1] > center[1]:
            diffy = abs(mousePos[1] - center[1])
            diffx = abs(mousePos[0] - center[0])
            theta = math.degrees(math.atan(diffx/diffy)) + 180
        #quadrant 4
        elif mousePos[0] < center[0] and mousePos[1] < center[1]:
            diffy = abs(mousePos[1] - center[1])
            diffx = abs(mousePos[0] - center[0])
            theta = math.degrees(math.atan(diffy/diffx)) + 270
        else:
            raise Exception('Mouse position outside acceptable range')
        
        #check if game won/lost
        distanceToCenter = math.sqrt((mousePos[0]-center[0])**2+(mousePos[1]-center[1])**2)

        if distanceToCenter >= radius:
            if theta < catAngle + 1 and theta > catAngle - 1:
                won = False
                
            else:
                won = True

        pygame.display.flip()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            if event.type == pygame.KEYUP:
                mousePos = np.array([center[0], center[1]])
                catPos = np.array([center[0], center[1]]) - np.array([0, radius])
                won = None
        if won:
            myfont = pygame.font.SysFont('Comic Sans MS', 60)
            textsurface = myfont.render('You won!', True, wonColor)
            textSize = textsurface.get_size()


            screen.blit(textsurface, center - np.array([textSize[0]/2, textSize[1]/2]))
            pygame.display.flip()
        else:
            myfont = pygame.font.SysFont('Comic Sans MS', 60)
            textsurface = myfont.render('You lost!', True, lostColor)
            textSize = textsurface.get_size()

            
            screen.blit(textsurface, center - np.array([textSize[0]/2, textSize[1]/2]))
            pygame.display.flip()
