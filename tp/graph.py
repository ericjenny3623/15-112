from tkinter import *
from cmu_112_graphics import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib
import math
matplotlib.use('TkAgg')


class Graph():

    def __init__(self):

        self.width = None
        self.height = None
        self.label = ""
        self.xAxis = self.Axis(xData)
        self.yAxis = self.Axis(yData)

    def draw(self, canvas):
        None


class Axis():

    def __init__(self, data, increments=1):
        self.data = data
        self.min = min(data)
        self.max = max(data)
        self.increments = increments
        self.setScale()

    def setScale(self):
        minRange = self.max - self.min
        increment = self.roundToSigFigs(
            minRange, 2, math.ceil)/self.increments
        middle = self.roundToSigFigs(minRange, 2, round)/2
        rangeHalf = int(self.increments/2)
        self.scale = []
        for i in range(-rangeHalf, rangeHalf+1):
            self.scale.append(middle + (increment*i))

    def roundToSigFigs(self, x, sigs, roundFunc):
        power = math.floor(math.log10(abs(x)))
        floatifiedX = x/10**(power-sigs+1)
        rounded = roundFunc(floatifiedX) * 10**(power-sigs+1)
        return rounded

    def udpate(self, newData):
        if newData < self.min:
            self.min = newData
            self.setScale()
        elif newData > self.max:
            self.max = self.max
            self.setScale()


if __name__ == "__main__":
    data = [-2.0, 0.1, 0.2, 360]
    axis = Axis(data, 10)


# class GraphApp(App):
#     def appStarted(self):
#         self.x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
#         self.v = np.array ([16,16.31925,17.6394,16.003,17.2861,17.3131,19.1259,18.9694,22.0003,22.81226])
#         self.p = np.array ([16.23697,     17.31653,     17.22094,     17.68631,     17.73641 ,    18.6368,
#             19.32125,     19.31756 ,    21.20247  ,   22.41444   ,  22.11718  ,   22.12453])

#     def redrawAll(self, canvas):
#         fig = Figure(figsize=(6,6))
#         a = fig.add_subplot(111)
#         a.scatter(v,x,color='red')
#         a.plot(p, range(2 +max(x)),color='blue')
#         a.invert_yaxis()

#         a.set_title ("Estimation Grid", fontsize=16)
#         a.set_ylabel("Y", fontsize=14)
#         a.set_xlabel("X", fontsize=14)

#         canvas.

    # canvas = FigureCanvasTkAgg(fig, master=self.window)
    # canvas.get_tk_widget().pack()
    # canvas.draw()
