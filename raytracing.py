import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.widgets import Slider, Button
from matplotlib import text
import mpl_axes_aligner

# user inputs:
InitialObject = []
Lenses = []

Images = [InitialObject]
FinalImage = []
colorsList = ['red']
i = 0
fig, ax = plt.subplots()  # Create a figure containing a single axes.
plt.subplots_adjust(bottom=0.35)
plt.axis([0, 300, -30, 30])

# Pure Calculations
def CalculateThinLens(ObjectDistance, FocalLength):
    if (FocalLength - ObjectDistance == 0):
        ImageDistance = FocalLength
    else:
        ImageDistance = (1 / ((1/FocalLength) - (1/ObjectDistance)))
    return ImageDistance

def CalculateMagnification(ObjectHeight, ObjectDistance, ImageDistance):
    ImageHeight = (((-ImageDistance)/(ObjectDistance))) * ObjectHeight
    return ImageHeight


def CalculateSlopeBetweenTwoPoints(x1, y1, x2, y2):
    m = (y2-y1) / (x2-x1)
    return m

def findResultingImage(Object, lens):
    # Origin: [X, Height]
    # Lens = [X, Type, Focal Length]
    objectX = Object[0]
    ObjectHeight = Object[1]
    lensX = lens[0]
    lensType = lens[1]
    FocalLength = lens[2]
    if (lensType == "C"):
        FocalLength = FocalLength * -1
    ObjectDistance = lensX - objectX
    ImageDistance = CalculateThinLens(ObjectDistance, FocalLength)
    imageX = lensX + ImageDistance
    ImageHeight = CalculateMagnification(
        ObjectHeight, ObjectDistance, ImageDistance)
    imageY = ImageHeight
    return (imageX, imageY)

def rayTrace(object, lens, Image):
    # InitialObject = [35, 10]
    # Lenses = [[50, 'V', 10]]
    objectX = object[0]
    objectY = object[1]

    lensX = lens[0]
    lensType = lens[1]
    FocalLength = lens[2]
    RightFocalPointX = lensX + FocalLength
    LeftFocalPointX = lensX - FocalLength

    ImageX = Image[0]
    ImageY = Image[1]

    if (lensX < ImageX):  # object is real
        # draw a straight line from the top of the image to the lens
        drawHorizontalLine(objectY, objectX, lensX, color=colorsList[i-1])

        # draw a sloped line through the right focal point - Using the final image
        plt.plot((lensX, ImageX), (objectY, ImageY),
                 color=colorsList[i-1], linestyle='-')

        # draw a sloped line through the left focal point - Using the final image
        plt.plot((objectX, lensX), (objectY, ImageY),
                 color=colorsList[i-1], linestyle='-')

        # draw a straight line from the lens to the image
        drawHorizontalLine(ImageY, lensX, ImageX, color=colorsList[i-1])

        # draw a straight line from the bottom of the image straight through the lens
        drawHorizontalLine(0, objectX, ImageX, color=colorsList[i-1])
    elif (ImageX < objectX):  # object is virtual, with a convex lens
        # draw a straight line from the object to the lens
        drawHorizontalLine(objectY, objectX, lensX, color=colorsList[i-1])

        # draw a sloped line through the right focal point
        slopeA = CalculateSlopeBetweenTwoPoints(
            lensX, objectY, RightFocalPointX, 0)
        drawSlopedLine(lensX, objectY, slopeA,
                       colorsList[i-1], RightFocalPointX - lensX)

        # draw a sloped virtual ray to the virtual image
        plt.plot((lensX, ImageX), (objectY, ImageY),
                 color=colorsList[i-1], linestyle='--')
        # draw a straight line from the bottom of the image straight through the lens
        drawHorizontalLine(0, RightFocalPointX, ImageX, color=colorsList[i-1])

        # draw a sloped line through the center of the convex lens
        slopeB = CalculateSlopeBetweenTwoPoints(objectX, objectY, lensX, 0)
        drawSlopedLine(objectX, objectY, slopeB,
                       colorsList[i-1], RightFocalPointX - objectX)
        plt.plot((objectX, ImageX), (objectY, ImageY),
                 color=colorsList[i-1], linestyle='--')

    elif (lensX > ImageX):  # image is virtual

        # draw a straight line from the object to the lens
        drawHorizontalLine(objectY, objectX, lensX, color=colorsList[i-1])

        # draw a sloped line refracting outwards from the concave lens
        slopeA = CalculateSlopeBetweenTwoPoints(
            lensX, objectY, LeftFocalPointX, 0)
        drawSlopedLine(lensX, objectY, slopeA,
                       colorsList[i-1], RightFocalPointX - lensX)

        # draw a straight line from the bottom of the image straight through the lens
        drawHorizontalLine(0, objectX, RightFocalPointX, color=colorsList[i-1])

        # draw a sloped virtual ray through the left focal point - Using the final image
        plt.plot((LeftFocalPointX, lensX), (0, objectY),
                 color=colorsList[i-1], linestyle='--')

        # draw a sloped line through the center of the concave lens
        slopeB = CalculateSlopeBetweenTwoPoints(objectX, objectY, lensX, 0)
        drawSlopedLine(objectX, objectY, slopeB,
                       colorsList[i-1], RightFocalPointX - objectX)
# draw
def drawSlopedLine(interceptX, interceptY, slope, color, xmax):
    x = np.linspace(0, xmax, 100)
    y = slope*x
    plt.plot(x + interceptX, y + interceptY, color=color)


def drawDottedSlopedLine(interceptX, interceptY, slope, color, xmax):
    x = np.linspace(0, xmax, 100)
    y = slope*x
    plt.plot(x + interceptX, y + interceptY, color=color, linestyle="--")


def drawHorizontalLine(y, xmin, xmax, color):
    plt.plot((xmin, xmax), (y, y), color=colorsList[i-1], linestyle='-')


def renderSurface():
    plt.axhline(y=0, color='black', linewidth=.75, zorder=0, linestyle='-')


def drawVerticalLine(x, ymin, ymax):
    plt.vlines(x=x, ymin=ymin, ymax=ymax, colors='black')


def drawLens(Lens):
    YTop = ax.get_ylim()[1]
    YBottom = ax.get_ylim()[0]
    Yadjust = YTop / (20)

    if (Lens[1] == "C"):
        color = "green"
        label = "Concave Lens"
        plt.plot(Lens[0], YTop, marker=11, markersize=8,
                 markeredgecolor=color, markerfacecolor=color, zorder=10)
        plt.plot(Lens[0], YBottom, marker=10, markersize=8,
                 markeredgecolor=color, markerfacecolor=color, zorder=10)
    elif (Lens[1] == "V"):
        color = "blue"
        label = "Convex Lens"
        plt.plot(Lens[0], YTop - Yadjust, marker=10, markersize=8,
                 markeredgecolor=color, markerfacecolor=color, zorder=10)
        plt.plot(Lens[0], YBottom + Yadjust, marker=11, markersize=8,
                 markeredgecolor=color, markerfacecolor=color, zorder=10)
    plt.vlines(Lens[0], YBottom, YTop, colors=color, label=label, zorder=10)
    plt.plot(Lens[0] - Lens[2], 0, marker="o", markersize=2.5,
             markeredgecolor=color, markerfacecolor=color, zorder=10)
    plt.plot(Lens[0] + Lens[2], 0, marker="o", markersize=2.5,
             markeredgecolor=color, markerfacecolor=color, zorder=10)


def drawFig(fig):
    drawImage(fig[0], 0, fig[1], "Object", "magenta")


def drawImage(x, y1, y2, label, color):
    plt.vlines(x, y1, y2, color=color, linewidth=2, label=label, zorder=10)
    plt.plot(x, y2, marker='o', markersize=3, color=color, zorder=9)

# Configuration:
def update(val):
    plt.sca(ax)
    plt.cla()
    objdist = objDist.val
    lenspos = lensPos.val
    objheight = objHeight.val
    type = Type.val
    focallength = FL.val

    objDist.valmax = lenspos
    objDist.ax.set_xlim(objDist.valmin, objDist.valmax)
    if (type == 0):
        t = "C"
    else:
        t = "V"
    InitialObject = [(lenspos - objdist), objheight]
    obj = InitialObject
    Lenses = [[lenspos, t, focallength]]

    i = 0
    for l in Lenses:
        resultingImage = findResultingImage(obj, l)
        if (len(Lenses) == (i + 1)):  # final image
            FinalImage.append(resultingImage)
            drawImage(resultingImage[0], 0, resultingImage[1],
                      color='#AF4BCE', label="Image")
            rayTrace(obj, l, resultingImage)
        else:
            Images.append(resultingImage)
            drawImage(resultingImage[0], 0, resultingImage[1], color=colorsList[i], label=(
                'Image #' + str(i + 1)))
            rayTrace(obj, l, resultingImage)
        plt.autoscale()
        mpl_axes_aligner.align.yaxes(ax, 0, ax, 0, 0.5)
        drawLens(l)
        drawFig(InitialObject)
        renderSurface()
        plt.legend(loc='upper right', bbox_to_anchor=(1, 1), frameon=False)
    i = i + 1


axobjDist = plt.axes([0.18, 0.25, 0.65, 0.03])
axFL = plt.axes([0.18, 0.1, 0.65, 0.03])
axType = plt.axes([0.18, 0.05, 0.65, 0.03])
axobjHeight = plt.axes([0.18, 0.2, 0.65, 0.03])
axlensPos = plt.axes([0.18, 0.15, 0.65, 0.03])

lensPos = Slider(axlensPos, 'Lens X Pos', 50, 250, 100, valstep=0.1)
objHeight = Slider(axobjHeight, 'Obj Y Pos', -25, 25, 10, valstep=0.1)
objDist = Slider(axobjDist, 'Obj Distance', 0.1, lensPos.val, 50, valstep=0.1)
FL = Slider(axFL, 'Focal Length', 1, 150, 30, valstep=0.1)
Type = Slider(axType, 'Concave', 0, 1, 1, valstep=1, dragging=True)
axType.text(1.039, plt.gca().get_ylim()[1] - 0.1, "— Convex")

objDist.on_changed(update)
objHeight.on_changed(update)
lensPos.on_changed(update)
Type.on_changed(update)
FL.on_changed(update)

update(0)
plt.show()
