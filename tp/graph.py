from tkinter import *
from cmu_112_graphics import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib
import math
matplotlib.use('TkAgg')


class StackedTimeGraph():

    def __init__(self, timeData, yDataLists, xDims, yDims):
        self.graphs = {}
        yIncrement = abs(yDims[0] - yDims[1])/len(yDataLists)
        graphYOrigin = yDims[0]
        for yData in yDataLists:
            graphYDims = (graphYOrigin, graphYOrigin + yIncrement)
            graphYOrigin += yIncrement
            self.graphs[yData.label] = Graph(timeData, yData, xDims, graphYDims)



class Graph():

    def __init__(self, xData, yData, xDims, yDims, title=""):
        self.cXOrigin, self.cYOrigin = xDims[0], yDims[0]
        self.width = abs(xDims[1] - xDims[0])
        self.height = abs(yDims[0] - yDims[1])
        self.title = title
        self.xAxis = Axis(xData)
        self.yAxis = Axis(yData)
        self.backgroundColor = "white"
        self.border = 0.05*self.height

    def draw(self, canvas):
        self.xAxis.checkScale()
        self.yAxis.checkScale()
        canvas.create_rectangle(self.cXOrigin, self.cYOrigin,
                                self.cXOrigin+self.width, self.cYOrigin-self.height,
                                fill=self.backgroundColor)
        self.createLine(canvas, self.xAxis.scaleMin, self.yAxis.scaleMin,
                        self.xAxis.scaleMin+self.xAxis.scaleRange, self.yAxis.scaleMin,
                        fill="blue")
        for xScale in self.xAxis.scale:
            x, y = self.graphToCanvasCoords(xScale, self.yAxis.scaleMin)
            canvas.create_text(x, y, text=str(round(xScale,2)), anchor="n")
        self.createLine(canvas, self.xAxis.scaleMin, self.yAxis.scaleMin,
                        self.xAxis.scaleMin, self.yAxis.scaleMin+self.yAxis.scaleRange,
                        fill="blue")
        for yScale in self.yAxis.scale:
            x, y = self.graphToCanvasCoords(self.xAxis.scaleMin, yScale)
            canvas.create_text(x, y, text=str(round(yScale, 2)), anchor="e")

        dataPoints = min(len(self.xAxis.data.data), len(self.yAxis.data.data))
        for i in range(dataPoints-1):
            x1, y1 = self.xAxis.data.data[i], self.yAxis.data.data[i]
            x2, y2 = self.xAxis.data.data[i+1], self.yAxis.data.data[i+1]
            if x1 is None or y1 is None or x2 is None or y2 is None:
                continue
            self.createLine(canvas, x1, y1, x2, y2, fill="red")

    def graphToCanvasCoords(self, x, y):
        xScaled = (x-self.xAxis.scaleMin) / self.xAxis.scaleRange
        cX = xScaled * (self.width-(2*self.border)) + self.cXOrigin + self.border
        yScaled = -(y-self.yAxis.scaleMin) / self.yAxis.scaleRange
        cY = yScaled * (self.height-(2*self.border)) + self.cYOrigin - self.border
        return cX, cY

    def createLine(self, canvas, x1, y1, x2, y2, **kwargs):
        cX1, cY1 = self.graphToCanvasCoords(x1, y1)
        cX2, cY2 = self.graphToCanvasCoords(x2, y2)
        # print(cX1, cY1)
        canvas.create_line(cX1, cY1, cX2, cY2, **kwargs)


class Axis():

    def __init__(self, data, increments=2):
        self.data = data
        self.label = self.data.label
        self.increments = increments
        self.setScale()

    def setScale(self):
        minRange = self.data.max - self.data.min
        minRange = 1 if minRange == 0 else minRange
        average = (self.data.max + self.data.min)/2
        average = 1 if average == 0 else average
        increment = self.roundToSigFigs(
            minRange, 2, math.ceil)/self.increments
        middle = self.roundToSigFigs(average, 2, round)
        rangeHalf = int(self.increments/2)
        self.scale = []
        for i in range(-rangeHalf, rangeHalf+1):
            rounded = self.roundToSigFigs(middle + (increment*i), 2, round)
            self.scale.append(rounded)
        self.scaleMin = self.scale[0]
        self.scaleRange = self.scale[-1] - self.scaleMin

    def roundToSigFigs(self, x, sigs, roundFunc):
        if x == 0:
            return 0
        power = math.floor(math.log10(abs(x)))
        floatifiedX = x/10**(power-sigs+1)
        rounded = roundFunc(floatifiedX) * 10**(power-sigs+1)
        return math.copysign(rounded, x)

    def checkScale(self):
        if self.scale[-1] < self.data.max \
                or self.scale[0] > self.data.min:
            self.setScale()


if __name__ == "__main__":
    data = [-2.0, 0.1, 0.2, 360]
    axis = Axis(data, 10)